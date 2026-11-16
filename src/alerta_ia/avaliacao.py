"""Avaliação das configurações sobre o conjunto de teste e consolidação do placar.

Uso::

    python -m alerta_ia.avaliacao --config sem_contexto
    python -m alerta_ia.avaliacao --config rag
    python -m alerta_ia.avaliacao --config rag_lora
    python -m alerta_ia.avaliacao --config rag --sem-limiar     # efeito isolado do portão
    python -m alerta_ia.avaliacao --config todas                # as três em sequência
    python -m alerta_ia.avaliacao --placar                      # só reconsolida placar e erros
    python -m alerta_ia.avaliacao --config rag --limite 5       # teste rápido (marcado como parcial)

Cada execução grava ``avaliacao/resultados/<nome>.jsonl`` (um caso por linha) e
``<nome>.meta.json``; em seguida regrava ``placar.json``, ``placar.md`` e
``erros_candidatos.md`` a partir de todos os resultados existentes.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import logging
import math
from pathlib import Path

from alerta_ia import config, dados
from alerta_ia.dados import normalizar_texto

log = logging.getLogger(__name__)

FALHAS = {
    "busca": "busca não trouxe o trecho relevante",
    "recusa_indevida": "recusa indevida",
    "alucinacao": "alucinação (respondeu sem a informação estar na base)",
    "json_invalido": "JSON inválido (métrica estrita)",
    "citacao": "citação errada ou ausente",
    "fato_faltando": "fato-chave faltando na resposta",
}


# ======================================================================
# Métricas (funções puras)
# ======================================================================
def fatos_presentes(resposta: str, fatos_chave: list[list[str]]) -> tuple[bool, list[list[str]]]:
    """Para CADA grupo, ao menos uma alternativa deve ser substring da resposta (sem acento, minúsculas)."""
    texto = normalizar_texto(resposta or "")
    faltando = [g for g in fatos_chave if not any(normalizar_texto(a) in texto for a in g)]
    return not faltando, faltando


def avaliar_caso(caso: dict, saida: dict) -> dict:
    """Métricas de um caso a partir do gabarito e da saída do ``Pipeline.responder``."""
    responde = caso["tipo"] == "responde"
    recusou = bool(saida["recusa"])
    todos_fatos, faltando = fatos_presentes(saida["resposta"], caso["fatos_chave"]) if responde else (True, [])
    ids_contexto = [t["id"] for t in saida.get("trechos", [])]
    relevantes = set(caso["trechos_relevantes"])
    busca_ok = bool(relevantes & set(ids_contexto)) if (responde and ids_contexto) else None
    citacao_ok = (
        bool(relevantes & set(saida["fontes"])) and not saida["citacoes_invalidas"] if responde else None
    )
    m = {
        "tipo": caso["tipo"],
        "recusou": recusou,
        "acerto": (not recusou and todos_fatos) if responde else recusou,
        "alucinacao": (not responde) and not recusou,
        "erro_factual": responde and not recusou and not todos_fatos,
        "recusa_indevida": responde and recusou,
        "fatos_faltando": faltando,
        "n_fatos": len(caso["fatos_chave"]) if responde else 0,
        "json_valido_estrito": bool(saida["json_valido_estrito"]),
        "chamou_llm": bool(saida.get("chamou_llm", True)),
        "citacao_correta": citacao_ok,
        "citacoes_invalidas": list(saida["citacoes_invalidas"]),
        "busca_trouxe_relevante": busca_ok,
        "recusa_por_limiar": bool(saida.get("recusa_por_limiar", False)),
        "latencia_ms": saida["latencia_ms"],
    }
    m["falhas"] = classificar_falhas(m)
    return m


def classificar_falhas(m: dict) -> list[str]:
    """Tipos de falha do caso, do mais ao menos determinante (a 1ª é a principal)."""
    falhas = []
    if m["tipo"] == "responde":
        if not m["acerto"] and m["busca_trouxe_relevante"] is False:
            falhas.append("busca")
        if m["recusa_indevida"]:
            falhas.append("recusa_indevida")
        if m["erro_factual"]:
            falhas.append("fato_faltando")
        if m["citacao_correta"] is False and m["busca_trouxe_relevante"] is not None:
            falhas.append("citacao")
    elif m["alucinacao"]:
        falhas.append("alucinacao")
    if m["chamou_llm"] and not m["json_valido_estrito"]:
        falhas.append("json_invalido")
    return falhas


def _pct(parte: int, total: int) -> float | None:
    return round(parte / total, 4) if total else None


def _p95(valores: list[float]) -> float | None:
    if not valores:
        return None
    ordenados = sorted(valores)
    return ordenados[min(len(ordenados) - 1, math.ceil(0.95 * len(ordenados)) - 1)]


def consolidar(metricas: list[dict]) -> dict:
    """Agrega as métricas por caso de UMA configuração."""
    resp = [m for m in metricas if m["tipo"] == "responde"]
    nc = [m for m in metricas if m["tipo"] == "nao_consta"]
    llm = [m for m in metricas if m["chamou_llm"]]
    lat = [m["latencia_ms"] for m in metricas]
    respondidas = [m for m in resp if not m["recusou"]]
    cobertura = [
        0.0 if m["recusou"] else 1 - len(m["fatos_faltando"]) / m["n_fatos"]
        for m in resp if m.get("n_fatos")
    ]
    return {
        "n": len(metricas),
        "n_responde": len(resp),
        "n_nao_consta": len(nc),
        "acerto_responde": _pct(sum(m["acerto"] for m in resp), len(resp)),
        "recusa_correta": _pct(sum(m["acerto"] for m in nc), len(nc)),
        "taxa_alucinacao": _pct(sum(m["alucinacao"] for m in nc), len(nc)),
        "erro_factual": _pct(sum(m["erro_factual"] for m in resp), len(resp)),
        "precisao_quando_responde": _pct(sum(m["acerto"] for m in respondidas), len(respondidas)),
        "cobertura_fatos": round(sum(cobertura) / len(cobertura), 4) if cobertura else None,
        "recusa_indevida": _pct(sum(m["recusa_indevida"] for m in resp), len(resp)),
        "json_valido_estrito": _pct(sum(m["json_valido_estrito"] for m in llm), len(llm)),
        "citacao_correta": _pct(sum(bool(m["citacao_correta"]) for m in resp), len(resp)),
        "acuracia_global": _pct(sum(m["acerto"] for m in metricas), len(metricas)),
        "busca_trouxe_relevante": _pct(sum(bool(m["busca_trouxe_relevante"]) for m in resp), len(resp))
        if any(m["busca_trouxe_relevante"] is not None for m in resp) else None,
        "chamadas_llm": len(llm),
        "recusas_por_limiar": sum(m["recusa_por_limiar"] for m in metricas),
        "latencia_media_ms": round(sum(lat) / len(lat), 1) if lat else None,
        "latencia_p95_ms": _p95(lat),
    }


COLUNAS_PLACAR = [
    ("acuracia_global", "Acurácia global"),
    ("acerto_responde", "Acerto (responde)"),
    ("cobertura_fatos", "Fatos cobertos"),
    ("precisao_quando_responde", "Precisão quando responde"),
    ("recusa_correta", "Recusa correta (não consta)"),
    ("taxa_alucinacao", "Alucinação"),
    ("erro_factual", "Erro factual"),
    ("recusa_indevida", "Recusa indevida"),
    ("json_valido_estrito", "JSON válido (estrito)"),
    ("citacao_correta", "Citação correta"),
    ("latencia_media_ms", "Latência média (ms)"),
    ("latencia_p95_ms", "Latência p95 (ms)"),
]

ORDEM = ["sem_contexto", "rag", "rag_lora", "rag_sem_limiar", "rag_lora_sem_limiar"]


def placar_markdown(placar: dict) -> str:
    from tabulate import tabulate

    nomes = sorted(placar["configuracoes"], key=lambda n: (ORDEM.index(n) if n in ORDEM else 99, n))
    linhas = []
    for nome in nomes:
        p = placar["configuracoes"][nome]
        linha = [nome + (" (parcial)" if p["meta"].get("limite") else "")]
        for chave, _ in COLUNAS_PLACAR:
            v = p["metricas"][chave]
            if v is None:
                linha.append("-")
            elif chave.startswith("latencia"):
                linha.append(f"{v:.0f}")
            else:
                linha.append(f"{100 * v:.1f}%")
        linhas.append(linha)
    tabela = tabulate(linhas, headers=["Configuração"] + [r for _, r in COLUNAS_PLACAR], tablefmt="github")
    notas = [
        "",
        f"Gerado em {placar['gerado_em']}. Conjunto: {placar.get('arquivo', '-')}.",
        "",
        "- Acerto (responde): todos os fatos-chave presentes e sem recusa.",
        "- Fatos cobertos: média da fração de fatos-chave presentes (crédito parcial; recusa = 0).",
        "- Precisão quando responde: das perguntas `responde` que o modelo não recusou, quantas acertou.",
        "- Recusa correta / Alucinação: sobre as perguntas `nao_consta` (somam 100%).",
        "- Erro factual e recusa indevida: sobre as perguntas `responde`.",
        "- JSON válido (estrito): `json.loads` do texto bruto + exatamente os 3 campos, sobre as chamadas à LLM"
        " (recusas pelo limiar não chamam a LLM).",
        "- Citação correta: `responde` em que `fontes` contém um trecho relevante e nenhum id fora do contexto.",
        "- Linhas `*_sem_limiar`: mesmas configurações com o portão por similaridade desligado.",
    ]
    return tabela + "\n" + "\n".join(notas) + "\n"


def erros_markdown(resultados: dict[str, list[dict]], max_por_config: int = 30) -> str:
    """Lista casos com falha (candidatos aos "5 erros reais") por configuração."""
    partes = ["# Candidatos a erros reais", "",
              "Casos com ao menos uma falha, por configuração. A primeira falha listada é a principal.", ""]
    for nome in sorted(resultados, key=lambda n: (ORDEM.index(n) if n in ORDEM else 99, n)):
        casos = [r for r in resultados[nome] if r["metricas"]["falhas"]]
        contagem = {}
        for r in casos:
            contagem[r["metricas"]["falhas"][0]] = contagem.get(r["metricas"]["falhas"][0], 0) + 1
        partes += [f"## {nome}: {len(casos)} casos com falha", ""]
        partes += [f"- {FALHAS[k]}: {v}" for k, v in sorted(contagem.items(), key=lambda kv: -kv[1])] + [""]
        for r in casos[:max_por_config]:
            m = r["metricas"]
            trechos = ", ".join(f"{t['id']} ({t['similaridade']:.3f})" for t in r.get("trechos", [])) or "-"
            partes += [
                f"### {r['id']} ({r['tipo']}, {r['categoria']}): {FALHAS[m['falhas'][0]]}",
                "",
                f"- Falhas: {', '.join(FALHAS[f] for f in m['falhas'])}",
                f"- Pergunta: {r['pergunta']}",
                f"- Esperado: {r['resposta_esperada']}",
                f"- Resposta do modelo: {r['resposta']}",
                f"- Fontes citadas: {r['fontes'] or '-'}; relevantes: {r['trechos_relevantes'] or '-'}",
                f"- Trechos recuperados (similaridade): {trechos}",
                f"- Recusa pelo limiar: {'sim' if m['recusa_por_limiar'] else 'não'}"
                + (f"; fatos faltando: {m['fatos_faltando']}" if m["fatos_faltando"] else ""),
                f"- Saída bruta: `{r['saida_bruta'][:400].replace('`', chr(39))}`",
                "",
            ]
        if len(casos) > max_por_config:
            partes += [f"(mais {len(casos) - max_por_config} casos em resultados/{nome}.jsonl)", ""]
    return "\n".join(partes)


# ======================================================================
# Execução
# ======================================================================
def nome_resultado(configuracao: str, sem_limiar: bool) -> str:
    return f"{configuracao}_sem_limiar" if sem_limiar and configuracao != "sem_contexto" else configuracao


def avaliar_pipeline(pipeline, casos: list[dict], progresso: bool = True) -> list[dict]:
    """Roda o pipeline (real ou falso) em cada caso e junta gabarito, saída e métricas."""
    linhas = []
    for i, caso in enumerate(casos, start=1):
        saida = pipeline.responder(caso["pergunta"])
        metricas = avaliar_caso(caso, saida)
        linhas.append(
            {
                "id": caso["id"],
                "tipo": caso["tipo"],
                "categoria": caso["categoria"],
                "pergunta": caso["pergunta"],
                "resposta_esperada": caso["resposta_esperada"],
                "fatos_chave": caso["fatos_chave"],
                "trechos_relevantes": caso["trechos_relevantes"],
                **{k: saida[k] for k in ("saida_bruta", "json", "resposta", "fontes", "citacoes_invalidas",
                                          "json_valido_estrito", "erro_json", "recusa", "recusa_por_limiar",
                                          "similaridade_top1", "limiar", "latencia_ms", "tokens_gerados")},
                "trechos": [{"id": t["id"], "similaridade": round(t["similaridade"], 4)} for t in saida["trechos"]],
                "metricas": metricas,
            }
        )
        if progresso:
            estado = "ok" if metricas["acerto"] else ",".join(metricas["falhas"]) or "erro"
            print(f"[{i}/{len(casos)}] {caso['id']} {caso['tipo']}: {estado} ({saida['latencia_ms']:.0f} ms)",
                  flush=True)
    return linhas


def executar(configuracao: str, arquivo: Path, sem_limiar: bool, limite: int | None, buscador=None) -> Path:
    from alerta_ia.geracao import criar_pipeline

    casos = dados.carregar_casos(arquivo)
    if limite:
        casos = casos[:limite]
    config.fixar_sementes()
    pipeline = criar_pipeline(configuracao, usar_limiar=not sem_limiar, buscador=buscador)
    try:
        linhas = avaliar_pipeline(pipeline, casos)
        info = pipeline.info()
    finally:
        pipeline.liberar()
    nome = nome_resultado(configuracao, sem_limiar)
    config.DIR_RESULTADOS.mkdir(parents=True, exist_ok=True)
    destino = config.DIR_RESULTADOS / f"{nome}.jsonl"
    dados.gravar_jsonl(destino, linhas)
    meta = {**info, "nome": nome, "arquivo": arquivo.name, "sem_limiar": sem_limiar, "limite": limite,
            "n_casos": len(linhas), "max_new_tokens": config.MAX_NEW_TOKENS, "semente": config.SEMENTE,
            "data": dt.datetime.now().isoformat(timespec="seconds")}
    (config.DIR_RESULTADOS / f"{nome}.meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"-> {destino}")
    return destino


def carregar_resultados(diretorio: Path | None = None) -> dict[str, list[dict]]:
    diretorio = Path(diretorio or config.DIR_RESULTADOS)
    return {p.stem: dados.ler_jsonl(p) for p in sorted(diretorio.glob("*.jsonl"))}


def consolidar_placar(diretorio: Path | None = None) -> dict:
    """Regrava placar.json, placar.md e erros_candidatos.md a partir dos resultados existentes."""
    diretorio = Path(diretorio or config.DIR_RESULTADOS)
    resultados = carregar_resultados(diretorio)
    placar = {"gerado_em": dt.datetime.now().isoformat(timespec="seconds"), "configuracoes": {}}
    arquivos = set()
    for nome, linhas in resultados.items():
        meta_arq = diretorio / f"{nome}.meta.json"
        meta = json.loads(meta_arq.read_text(encoding="utf-8")) if meta_arq.exists() else {}
        arquivos.add(meta.get("arquivo", "?"))
        for l in linhas:  # resultados gravados antes de existir o campo n_fatos
            l["metricas"].setdefault("n_fatos", len(l["fatos_chave"]) if l["tipo"] == "responde" else 0)
        placar["configuracoes"][nome] = {"meta": meta, "metricas": consolidar([l["metricas"] for l in linhas])}
    placar["arquivo"] = ", ".join(sorted(arquivos)) if arquivos else None
    config.PLACAR_JSON.parent.mkdir(parents=True, exist_ok=True)
    config.PLACAR_JSON.write_text(json.dumps(placar, ensure_ascii=False, indent=2), encoding="utf-8")
    config.PLACAR_MD.write_text("# Placar\n\n" + placar_markdown(placar), encoding="utf-8")
    config.ERROS_MD.write_text(erros_markdown(resultados), encoding="utf-8")
    return placar


def _main() -> None:
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(message)s")
    ap = argparse.ArgumentParser(description="Avaliação das configurações do Alerta Córrego")
    ap.add_argument("--config", choices=list(config.CONFIGURACOES) + ["todas"])
    ap.add_argument("--arquivo", default=str(config.TESTE))
    ap.add_argument("--sem-limiar", action="store_true", help="desliga o portão por similaridade")
    ap.add_argument("--limite", type=int, help="avalia só os N primeiros casos")
    ap.add_argument("--placar", action="store_true", help="só consolida o placar a partir dos resultados")
    args = ap.parse_args()
    if not args.config and not args.placar:
        ap.error("informe --config ou --placar")

    if args.config:
        alvos = list(config.CONFIGURACOES) if args.config == "todas" else [args.config]
        if args.sem_limiar and args.config == "todas":
            alvos.remove("sem_contexto")  # sem contexto não tem portão
        buscador = None
        if any(c != "sem_contexto" for c in alvos):
            from alerta_ia.busca import Buscador

            buscador = Buscador()  # reaproveitado entre configurações; a LLM é liberada a cada uma
        for c in alvos:
            print(f"== {nome_resultado(c, args.sem_limiar)} ==")
            executar(c, Path(args.arquivo), args.sem_limiar, args.limite, buscador)

    placar = consolidar_placar()
    print(placar_markdown(placar))
    print(f"-> {config.PLACAR_JSON}, {config.PLACAR_MD}, {config.ERROS_MD}")


if __name__ == "__main__":
    _main()
