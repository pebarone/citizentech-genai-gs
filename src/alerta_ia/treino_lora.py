"""Especialização QLoRA do modelo base no formato e no comportamento do Alerta Córrego.

O dataset é montado com o MESMO buscador e o MESMO prompt da configuração ``rag``:
top-3 reais; para perguntas ``responde`` garante-se ao menos um trecho relevante no
contexto (inserido no lugar do 3º se a busca não trouxe) e a ordem é embaralhada com
semente; para ``nao_consta`` os top-3 reais servem de distratores. O alvo é o JSON
estrito com ``fontes`` = trechos relevantes presentes no contexto. A perda é calculada
só nos tokens da resposta do assistente.

Uso::

    python -m alerta_ia.treino_lora                    # treino completo
    python -m alerta_ia.treino_lora --somente-dataset  # só monta o dataset e as estatísticas
    python -m alerta_ia.treino_lora --limite 24 --epocas 1 --saida modelos/_fumaca  # teste rápido
"""

from __future__ import annotations

import argparse
import json
import logging
import random
import time
from pathlib import Path

from alerta_ia import config, dados, prompts

log = logging.getLogger(__name__)


# ======================================================================
# Montagem do dataset (pura, exceto a busca que é passada pronta)
# ======================================================================
def montar_exemplo(exemplo: dict, recuperados: list[dict], por_id: dict, rng: random.Random, k: int = 3) -> dict:
    """Monta contexto e alvo de um exemplo de treino a partir dos top-k recuperados."""
    contexto = [dict(t) for t in recuperados[:k]]
    inseriu = False
    fontes: list[str] = []
    if exemplo["tipo"] == "responde":
        ids = {t["id"] for t in contexto}
        if not any(r in ids for r in exemplo["trechos_relevantes"]):
            relevante = next((r for r in exemplo["trechos_relevantes"] if r in por_id), None)
            if relevante is None:
                raise dados.ErroDados(f"{exemplo['id']}: nenhum trecho relevante existe na base")
            contexto = contexto[: k - 1] + [{**por_id[relevante], "similaridade": None}]
            inseriu = True
        rng.shuffle(contexto)
        ids = {t["id"] for t in contexto}
        fontes = [r for r in exemplo["trechos_relevantes"] if r in ids]
    else:
        rng.shuffle(contexto)
    alvo = prompts.json_resposta(exemplo["resposta"], fontes, exemplo["tipo"] == "responde")
    return {
        "id": exemplo["id"],
        "tipo": exemplo["tipo"],
        "categoria": exemplo.get("categoria"),
        "pergunta": exemplo["pergunta"],
        "contexto": [
            {k2: t[k2] for k2 in ("id", "fonte_id", "titulo", "secao", "texto", "url")}
            | {"similaridade": t.get("similaridade")}
            for t in contexto
        ],
        "inseriu_relevante": inseriu,
        "alvo": alvo,
    }


def separar_validacao(montados: list[dict], fracao: float, semente: int) -> tuple[list[dict], list[dict]]:
    """Separação estratificada por tipo (determinística pela semente)."""
    rng = random.Random(semente)
    treino, val = [], []
    for tipo in sorted({m["tipo"] for m in montados}):
        grupo = [m for m in montados if m["tipo"] == tipo]
        rng.shuffle(grupo)
        n_val = max(1, round(len(grupo) * fracao)) if len(grupo) > 1 and fracao > 0 else 0
        val += grupo[:n_val]
        treino += grupo[n_val:]
    rng.shuffle(treino)
    return treino, val


def tokenizar_exemplo(tokenizer, montado: dict, max_len: int) -> dict:
    """input_ids/labels com perda só no alvo; trunca o texto dos trechos (nunca o alvo)."""
    alvo_ids = tokenizer(montado["alvo"] + tokenizer.eos_token, add_special_tokens=False)["input_ids"]
    # Começa com o mesmo limite por trecho da inferência e só reduz se não couber.
    maior = max((len(t["texto"]) for t in montado["contexto"]), default=0)
    max_chars = min(config.MAX_CHARS_TRECHO, maior) if maior else None
    truncado = False
    while True:
        msgs = prompts.montar_mensagens(montado["pergunta"], montado["contexto"], max_chars)
        prompt_ids = list(tokenizer.apply_chat_template(msgs, tokenize=True, add_generation_prompt=True))
        if len(prompt_ids) + len(alvo_ids) <= max_len:
            break
        if not max_chars or max_chars < 50:
            raise ValueError(f"{montado['id']}: não cabe em {max_len} tokens nem com os trechos truncados")
        max_chars = int(max_chars * 0.8)
        truncado = True
    return {
        "input_ids": prompt_ids + alvo_ids,
        "labels": [-100] * len(prompt_ids) + alvo_ids,
        "truncado": truncado,
        "n_prompt": len(prompt_ids),
        "n_alvo": len(alvo_ids),
        "mensagens": msgs,
    }


def colar(lote: list[dict], pad_id: int) -> dict:
    import torch

    tam = max(len(x["input_ids"]) for x in lote)
    ids, labels, mascara = [], [], []
    for x in lote:
        falta = tam - len(x["input_ids"])
        ids.append(x["input_ids"] + [pad_id] * falta)
        labels.append(x["labels"] + [-100] * falta)
        mascara.append([1] * len(x["input_ids"]) + [0] * falta)
    return {
        "input_ids": torch.tensor(ids),
        "labels": torch.tensor(labels),
        "attention_mask": torch.tensor(mascara),
    }


def linha_dataset(montado: dict, tok: dict, split: str) -> dict:
    """Registro completo do dataset montado (o que de fato entra no treino)."""
    return {
        "id": montado["id"],
        "split": split,
        "tipo": montado["tipo"],
        "categoria": montado.get("categoria"),
        "pergunta": montado["pergunta"],
        "ids_contexto": [t["id"] for t in montado["contexto"]],
        "inseriu_relevante": montado["inseriu_relevante"],
        "mensagens": tok["mensagens"],
        "alvo": montado["alvo"],
        "n_tokens_prompt": tok["n_prompt"],
        "n_tokens_alvo": tok["n_alvo"],
        "contexto_truncado": tok["truncado"],
    }


def _resumo(valores: list[int]) -> dict:
    if not valores:
        return {"media": None, "max": None, "min": None}
    return {"media": round(sum(valores) / len(valores), 1), "max": max(valores), "min": min(valores)}


def estatisticas_dataset(linhas: list[dict], fonte_do_trecho: dict, perguntas_avaliacao: dict) -> dict:
    """Contagens por tipo/split, tamanhos em tokens, cobertura da base e checagem de vazamento.

    ``fonte_do_trecho``: id do trecho -> fonte_id (base inteira). ``perguntas_avaliacao``:
    nome do conjunto (teste, dev) -> perguntas; o vazamento compara perguntas normalizadas
    (sem acento, minúsculas, espaços colapsados).
    """
    por_split_tipo: dict[str, dict[str, int]] = {}
    for l in linhas:
        por_split_tipo.setdefault(l["split"], {}).setdefault(l["tipo"], 0)
        por_split_tipo[l["split"]][l["tipo"]] += 1
    trechos_ctx = {t for l in linhas for t in l["ids_contexto"]}
    trechos_alvo = {f for l in linhas for f in json.loads(l["alvo"])["fontes"]}
    normalizadas = {dados.normalizar_texto(l["pergunta"]) for l in linhas}
    vazamento = {}
    for nome, perguntas in perguntas_avaliacao.items():
        comuns = sorted(normalizadas & {dados.normalizar_texto(p) for p in perguntas})
        vazamento[nome] = {"n_perguntas_conjunto": len(perguntas), "perguntas_em_comum": len(comuns),
                           "exemplos": comuns[:5]}
    categorias: dict[str, int] = {}
    for l in linhas:
        if l.get("categoria"):
            categorias[l["categoria"]] = categorias.get(l["categoria"], 0) + 1
    return {
        "n_exemplos": len(linhas),
        "por_tipo": {t: sum(1 for l in linhas if l["tipo"] == t) for t in sorted({l["tipo"] for l in linhas})},
        "por_split": {sp: sum(v.values()) for sp, v in sorted(por_split_tipo.items())},
        "por_split_e_tipo": por_split_tipo,
        "por_categoria": categorias or None,
        "tokens_prompt": _resumo([l["n_tokens_prompt"] for l in linhas]),
        "tokens_alvo": _resumo([l["n_tokens_alvo"] for l in linhas]),
        "exemplos_com_contexto_truncado": sum(1 for l in linhas if l["contexto_truncado"]),
        "exemplos_com_relevante_inserido": sum(1 for l in linhas if l["inseriu_relevante"]),
        "cobertura": {
            "trechos_distintos_no_contexto": len(trechos_ctx),
            "fontes_distintas_no_contexto": len({fonte_do_trecho[t] for t in trechos_ctx if t in fonte_do_trecho}),
            "trechos_distintos_citados_no_alvo": len(trechos_alvo),
            "trechos_na_base": len(fonte_do_trecho),
            "fontes_na_base": len(set(fonte_do_trecho.values())),
        },
        "vazamento": vazamento,
        "sem_vazamento": all(v["perguntas_em_comum"] == 0 for v in vazamento.values()),
    }


def montar_dataset(exemplos: list[dict], buscador, k: int, semente: int) -> list[dict]:
    rng = random.Random(semente)
    recuperados = buscador.buscar_lote([e["pergunta"] for e in exemplos], k)
    return [montar_exemplo(e, r, buscador.por_id, rng, k) for e, r in zip(exemplos, recuperados)]


# ======================================================================
# Treino (GPU)
# ======================================================================
def _grafico_perda(registro: dict, caminho: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7, 4))
    if registro["perda_treino"]:
        ax.plot(*zip(*registro["perda_treino"]), label="treino")
    if registro["perda_validacao"]:
        ax.plot(*zip(*registro["perda_validacao"]), marker="o", label="validação")
    ax.set_xlabel("passo de otimização")
    ax.set_ylabel("perda (entropia cruzada no JSON de resposta)")
    ax.set_title("Curva de perda do QLoRA")
    ax.legend()
    fig.tight_layout()
    caminho.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(caminho, dpi=120)
    plt.close(fig)


def _treinar_uma_vez(treino_tok: list[dict], val_tok: list[dict], epocas: float, batch: int, acumulo: int):
    """Carrega o modelo, aplica LoRA e treina. Devolve (modelo, trainer, contagens)."""
    import torch
    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
    from transformers import Trainer, TrainingArguments, set_seed

    from alerta_ia.geracao import carregar_llm, resolver_dtype

    set_seed(config.SEMENTE)
    modelo, tokenizer = carregar_llm()
    modelo.config.use_cache = False
    modelo = prepare_model_for_kbit_training(
        modelo, use_gradient_checkpointing=True, gradient_checkpointing_kwargs={"use_reentrant": False}
    )
    modelo = get_peft_model(
        modelo,
        LoraConfig(
            r=config.LORA_R,
            lora_alpha=config.LORA_ALPHA,
            lora_dropout=config.LORA_DROPOUT,
            target_modules=list(config.LORA_ALVOS),
            bias="none",
            task_type="CAUSAL_LM",
        ),
    )
    contagens = modelo.get_nb_trainable_parameters()
    log.info("parâmetros treináveis: %d de %d (%.2f%%)", *contagens, 100 * contagens[0] / contagens[1])

    dtype = resolver_dtype()
    args = TrainingArguments(
        output_dir=str(config.DIR_CHECKPOINTS),
        per_device_train_batch_size=batch,
        per_device_eval_batch_size=batch,
        gradient_accumulation_steps=acumulo,
        num_train_epochs=epocas,
        learning_rate=config.TAXA_APRENDIZADO,
        lr_scheduler_type="cosine",
        warmup_ratio=config.WARMUP,
        optim="paged_adamw_8bit",
        gradient_checkpointing=True,
        gradient_checkpointing_kwargs={"use_reentrant": False},
        bf16=dtype == torch.bfloat16,  # autocast em bf16 (ou fp16 abaixo)
        fp16=dtype == torch.float16,
        group_by_length=True,  # lotes de comprimento parecido: menos padding desperdiçado
        logging_steps=5,
        eval_strategy="epoch" if val_tok else "no",  # validação só ao fim de cada época
        save_strategy="no",
        report_to="none",
        seed=config.SEMENTE,
        data_seed=config.SEMENTE,
        dataloader_num_workers=0,
        remove_unused_columns=False,
    )
    pad_id = tokenizer.pad_token_id
    sem_extra = lambda xs: [{"input_ids": x["input_ids"], "labels": x["labels"]} for x in xs]  # noqa: E731
    trainer = Trainer(
        model=modelo,
        args=args,
        train_dataset=sem_extra(treino_tok),
        eval_dataset=sem_extra(val_tok) or None,
        data_collator=lambda lote: colar(lote, pad_id),  # padding dinâmico, só até o maior do lote
    )
    trainer.train()
    return modelo, trainer, contagens


def treinar(treino_tok: list[dict], val_tok: list[dict], saida: Path, epocas: float) -> dict:
    """Treina com o batch configurado; em OOM recomeça com batch 1 mantendo o batch efetivo."""
    import torch

    from alerta_ia.geracao import liberar_memoria, resolver_dtype

    tentativas = [(config.BATCH, config.ACUMULO_GRADIENTE)]
    if config.BATCH > 1:
        tentativas.append((1, config.BATCH * config.ACUMULO_GRADIENTE))
    inicio = time.time()
    for i, (batch, acumulo) in enumerate(tentativas):
        try:
            modelo, trainer, (treinaveis, total) = _treinar_uma_vez(treino_tok, val_tok, epocas, batch, acumulo)
            break
        except torch.cuda.OutOfMemoryError:
            if i == len(tentativas) - 1:
                raise
            log.warning("sem memória com batch %d; recomeçando com batch %d e acúmulo %d", batch, *tentativas[i + 1])
        # fora do except: o traceback já foi descartado e a VRAM pode ser liberada de fato
        modelo = trainer = None
        liberar_memoria()
    duracao = time.time() - inicio

    saida.mkdir(parents=True, exist_ok=True)
    modelo.save_pretrained(str(saida))
    tamanho_mb = sum(f.stat().st_size for f in saida.rglob("*") if f.is_file()) / 2**20
    historico = trainer.state.log_history
    perdas_val = [(h["step"], h["eval_loss"]) for h in historico if "eval_loss" in h]
    registro = {
        "modelo_base": config.MODELO_LLM,
        "adaptador": Path(saida).name,
        "tamanho_adaptador_mb": round(tamanho_mb, 2),
        "parametros_treinaveis": treinaveis,
        "parametros_totais": total,
        "n_treino": len(treino_tok),
        "n_validacao": len(val_tok),
        "exemplos_truncados": sum(1 for x in treino_tok + val_tok if x["truncado"]),
        "tempo_total_treino_s": round(duracao, 1),
        "tempo_total_treino_min": round(duracao / 60, 2),
        "vram_pico_gb": round(torch.cuda.max_memory_allocated() / 2**30, 2) if torch.cuda.is_available() else None,
        "hiperparametros": {
            "r": config.LORA_R,
            "alpha": config.LORA_ALPHA,
            "dropout": config.LORA_DROPOUT,
            "alvos": list(config.LORA_ALVOS),
            "lr": config.TAXA_APRENDIZADO,
            "agendador": "cosine",
            "warmup_ratio": config.WARMUP,
            "epocas": epocas,
            "batch": batch,
            "acumulo_gradiente": acumulo,
            "batch_efetivo": batch * acumulo,
            "fallback_oom_usado": batch != config.BATCH,
            "max_len": config.MAX_LEN_TREINO,
            "max_chars_trecho": config.MAX_CHARS_TRECHO,
            "quantizacao": "NF4 4 bits, dupla quantização",
            "dtype_computacao": str(resolver_dtype()).replace("torch.", ""),
            "semente": config.SEMENTE,
        },
        "perda_treino": [(h["step"], h["loss"]) for h in historico if "loss" in h],
        "perda_validacao": perdas_val,
        "perda_validacao_final": perdas_val[-1][1] if perdas_val else None,
        "historico": historico,
    }
    del trainer, modelo
    liberar_memoria()
    return registro


def _main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    ap = argparse.ArgumentParser(description="Treino QLoRA do Alerta Córrego")
    ap.add_argument("--arquivo", default=str(config.PERGUNTAS_TREINO))
    ap.add_argument("--saida", default=str(config.ADAPTADOR), help="pasta do adaptador")
    ap.add_argument("--epocas", type=float, default=config.EPOCAS)
    ap.add_argument("--max-len", type=int, default=config.MAX_LEN_TREINO)
    ap.add_argument("--limite", type=int, help="usa só os N primeiros exemplos (teste rápido)")
    ap.add_argument("--somente-dataset", action="store_true", help="só monta e grava o dataset")
    args = ap.parse_args()

    from alerta_ia.busca import Buscador
    from transformers import AutoTokenizer

    config.fixar_sementes()
    exemplos = dados.carregar_treino(args.arquivo)
    if args.limite:
        exemplos = exemplos[: args.limite]
    buscador = Buscador()
    quebradas = dados.referencias_quebradas(exemplos, set(buscador.ids))
    if quebradas:
        log.warning("%d referências a trechos inexistentes, ex.: %s", len(quebradas), quebradas[:3])
    montados = montar_dataset(exemplos, buscador, config.TOP_K, config.SEMENTE)
    fonte_do_trecho = {t["id"]: t["fonte_id"] for t in buscador.trechos}
    buscador.liberar_modelo()  # libera VRAM antes de carregar a LLM
    del buscador

    # Com --limite (teste rápido) nada sobrescreve os artefatos oficiais: tudo vai para --saida.
    oficial = not args.limite
    pasta_aux = Path(args.saida)
    arq_dataset = config.DATASET_MONTADO if oficial else pasta_aux / "dataset_montado.jsonl"
    arq_stats = config.ESTATISTICAS_TREINO if oficial else pasta_aux / "estatisticas.json"
    arq_log = config.TREINO_LOG if oficial else pasta_aux / "treino_log.json"
    arq_grafico = config.DIR_GRAFICOS / "treino_perda.png" if oficial else pasta_aux / "treino_perda.png"

    treino, val = separar_validacao(montados, config.FRACAO_VALIDACAO, config.SEMENTE)
    tokenizer = AutoTokenizer.from_pretrained(config.MODELO_LLM)
    treino_tok = [tokenizar_exemplo(tokenizer, m, args.max_len) for m in treino]
    val_tok = [tokenizar_exemplo(tokenizer, m, args.max_len) for m in val]
    linhas = [linha_dataset(m, t, "treino") for m, t in zip(treino, treino_tok)]
    linhas += [linha_dataset(m, t, "validacao") for m, t in zip(val, val_tok)]
    dados.gravar_jsonl(arq_dataset, linhas)

    perguntas_avaliacao = {}
    for nome, arq in (("teste", config.TESTE), ("dev", config.DEV)):
        if arq.exists():
            perguntas_avaliacao[nome] = [c["pergunta"] for c in dados.ler_jsonl(arq)]
        else:
            log.warning("%s não encontrado; checagem de vazamento contra '%s' não feita", arq, nome)
    stats = estatisticas_dataset(linhas, fonte_do_trecho, perguntas_avaliacao)
    stats["arquivo"] = Path(args.arquivo).name
    stats["max_len"] = args.max_len
    arq_stats.parent.mkdir(parents=True, exist_ok=True)
    arq_stats.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"dataset: {len(treino)} treino, {len(val)} validação; tokens de prompt: médio "
          f"{stats['tokens_prompt']['media']}, máx {stats['tokens_prompt']['max']}; "
          f"sem vazamento: {stats['sem_vazamento']} -> {arq_dataset}, {arq_stats}")
    if not stats["sem_vazamento"]:
        log.warning("há perguntas do treino iguais às de teste/dev: %s", stats["vazamento"])
    if args.somente_dataset:
        return

    registro = treinar(treino_tok, val_tok, Path(args.saida), args.epocas)
    registro["n_inseriu_relevante"] = stats["exemplos_com_relevante_inserido"]
    registro["arquivo"] = Path(args.arquivo).name
    arq_log.parent.mkdir(parents=True, exist_ok=True)
    arq_log.write_text(json.dumps(registro, ensure_ascii=False, indent=2), encoding="utf-8")
    _grafico_perda(registro, arq_grafico)
    print(f"adaptador salvo em {args.saida} ({registro['tamanho_adaptador_mb']} MB); log em {arq_log}")


if __name__ == "__main__":
    _main()
