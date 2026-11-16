"""Gera os notebooks do projeto a partir deste script (fonte única, fácil de revisar).

Uso (na raiz do projeto)::

    python notebooks/_gerar_notebooks.py

Os notebooks são finos: toda a lógica fica em ``src/alerta_ia``. Os que usam GPU
reaproveitam resultados gravados em ``avaliacao/`` quando ``REEXECUTAR = False``.
"""

from __future__ import annotations

from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

PASTA = Path(__file__).parent

SETUP = """import json
import subprocess
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import Markdown, display

from alerta_ia import config, dados

pd.set_option("display.max_colwidth", 160)
REEXECUTAR = False  # True = refaz as etapas pesadas (GPU) em vez de ler os resultados gravados


def rodar(*args):
    \"\"\"Executa um módulo do projeto (python -m ...) na raiz do repositório e mostra a saída.\"\"\"
    r = subprocess.run([sys.executable, "-m", *args], cwd=config.RAIZ, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    print(r.stdout[-4000:])
    if r.returncode != 0:
        print(r.stderr[-4000:])
        raise RuntimeError(f"falha ao executar {args}")


def ler_json(caminho):
    return json.loads(Path(caminho).read_text(encoding="utf-8"))"""

PREREQ = (
    "> Pré-requisitos: ambiente instalado (`pip install -e .` na raiz) e dados em `base/`, "
    "`avaliacao/` e `treino/`. Rode as células em ordem. `REEXECUTAR = False` reaproveita os "
    "resultados já gravados para a reexecução ser rápida."
)


def nb(celulas):
    caderno = new_notebook()
    caderno.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    caderno.metadata["language_info"] = {"name": "python"}
    caderno.cells = [new_markdown_cell(c[1]) if c[0] == "md" else new_code_cell(c[1]) for c in celulas]
    return caderno


md = lambda t: ("md", t)  # noqa: E731
code = lambda t: ("code", t)  # noqa: E731

# ----------------------------------------------------------------------------- 01
NB01 = [
    md("""# 01 · Tarefa da IA, base de conhecimento e conjuntos de teste

**Produto:** Alerta Córrego avisa moradores da beira de córregos da Zona Leste de São Paulo sobre enchentes.

**Tarefa da IA:** responder dúvidas do morador **somente** com base em documentos oficiais (Defesa Civil e
órgãos públicos), **citando a fonte**, e **recusar** ("não consta na base") quando os documentos não cobrem
a pergunta. Em perigo, a orientação é sempre ligar **199** (Defesa Civil) ou **193** (Bombeiros).

**Objetivo declarado:** provar que a IA acerta mais e alucina menos que o mesmo modelo sem contexto, e que
roda integrada ao produto de forma segura, explicável e de acordo com a LGPD.

""" + PREREQ),
    code(SETUP),
    md("""## Contrato de saída

O modelo responde sempre um JSON estrito com 3 campos. A recusa tem formato fixo."""),
    code("""from alerta_ia import prompts

print(prompts.json_resposta("Desligue a energia no quadro de luz e vá para um local alto.", ["<id do trecho>"], True))
print(prompts.recusa_json())"""),
    md("## Base de conhecimento: fontes e trechos"),
    code("""fontes = pd.DataFrame(dados.carregar_fontes())
trechos = pd.DataFrame(dados.carregar_trechos())
trechos["palavras"] = trechos["texto"].str.split().str.len()
print(f"{len(fontes)} fontes, {len(trechos)} trechos")
fontes[["fonte_id", "titulo", "orgao", "formato", "licenca", "data_acesso", "n_trechos"]]"""),
    code("""por_fonte = trechos.groupby("fonte_id").agg(trechos=("id", "count"), palavras_medias=("palavras", "mean"))
display(por_fonte.round(1))
trechos["palavras"].describe().round(1)"""),
    code("""ax = trechos["palavras"].plot.hist(bins=20, title="Tamanho dos trechos (palavras)")
ax.set_xlabel("palavras por trecho");"""),
    md("""## Os três conjuntos: treino, dev e teste

Cada conjunto tem uma finalidade diferente e eles **não compartilham perguntas** (a checagem de vazamento
está no notebook 04). O teste só é usado para reportar números; o limiar é escolhido no dev."""),
    code("""finalidade = {
    "treino": "ajustar o adaptador LoRA (formato JSON, citação e recusa)",
    "dev": "calibrar o limiar de similaridade da busca",
    "teste": "medir e reportar o placar final (nunca usado para escolher nada)",
}
arquivos = {"treino": config.PERGUNTAS_TREINO, "dev": config.DEV, "teste": config.TESTE}
linhas = []
for nome, arq in arquivos.items():
    if not arq.exists():
        linhas.append({"conjunto": nome, "exemplos": None, "% não consta": None, "finalidade": finalidade[nome]})
        continue
    regs = dados.ler_jsonl(arq)
    nc = sum(r["tipo"] == "nao_consta" for r in regs)
    linhas.append({"conjunto": nome, "exemplos": len(regs), "% não consta": round(100 * nc / len(regs), 1),
                   "finalidade": finalidade[nome]})
pd.DataFrame(linhas).set_index("conjunto")"""),
    md("## Conjunto de teste: composição"),
    code("""teste = pd.DataFrame(dados.carregar_casos(config.TESTE))
display(pd.crosstab(teste["categoria"], teste["tipo"], margins=True, margins_name="total"))
quebradas = dados.referencias_quebradas(teste.to_dict("records"), set(trechos["id"]))
print("referências a trechos inexistentes:", quebradas or "nenhuma")"""),
    md("""## Exemplos

Um caso `responde` traz os **fatos-chave** (cada grupo aceita alternativas; acerto = todos os grupos presentes
na resposta, comparando sem acento) e os **trechos relevantes**. Um caso `nao_consta` está no domínio mas
fora da base: a resposta certa é recusar."""),
    code("""for tipo in ["responde", "nao_consta"]:
    ex = teste[teste["tipo"] == tipo].iloc[0]
    display(Markdown(f"**{tipo}** · `{ex['id']}` · categoria `{ex['categoria']}`\\n\\n"
                     f"- Pergunta: {ex['pergunta']}\\n- Resposta esperada: {ex['resposta_esperada']}\\n"
                     f"- Fatos-chave: `{ex['fatos_chave']}`\\n- Trechos relevantes: `{ex['trechos_relevantes']}`"))
    for tid in ex["trechos_relevantes"]:
        t = trechos.set_index("id").loc[tid]
        display(Markdown(f"> **{tid}** ({t['titulo']} — {t['secao']}): {t['texto']}"))"""),
]

# ----------------------------------------------------------------------------- 02
NB02 = [
    md("""# 02 · Busca: recall@1, recall@3 e limiar

A busca usa `intfloat/multilingual-e5-base` (prefixos `query:`/`passage:`, vetores normalizados,
similaridade de cosseno) sobre todos os trechos. O índice fica em cache em `base/indice/` e é refeito
automaticamente se qualquer trecho mudar (hash do conteúdo).

- **recall@k**: fração das perguntas `responde` com ao menos um trecho relevante entre os k primeiros.
- **MRR**: média de 1/posição do primeiro trecho relevante.

""" + PREREQ),
    code(SETUP),
    code("""from alerta_ia import busca

buscador = busca.Buscador()
print(f"{len(buscador.ids)} trechos indexados, dimensão {buscador.matriz.shape[1]}")"""),
    md("## Recall no conjunto de teste"),
    code("""res = busca.avaliar_busca(buscador, dados.carregar_casos(config.TESTE))
display(pd.DataFrame([{k: res[k] for k in ["n", "recall@1", "recall@3", "mrr"]}]).round(3))
pd.DataFrame(res["por_categoria"]).T.round(3)"""),
    md("Perguntas em que o trecho relevante **não** apareceu no top-3 (candidatas a erro de busca):"),
    code("""det = pd.DataFrame(res["detalhes"])
det[(det["posicao_primeiro_relevante"].isna()) | (det["posicao_primeiro_relevante"] > 3)]"""),
    md("""## Calibração do limiar (dev + treino, nunca o teste)

Se a similaridade do top-1 ficar abaixo do limiar, o sistema recusa sem chamar a LLM. A troca é explícita:

- limiar **baixo** → mais perguntas sem resposta chegam à LLM (risco de alucinação);
- limiar **alto** → mais perguntas com resposta são recusadas (recusa indevida).

**Primeira tentativa (v1):** índice de Youden só nas 30 perguntas de dev → limiar 0,8475. No teste ele
barrou 7 das 42 perguntas que tinham resposta: amostra pequena demais (`avaliacao/limiar_v1_dev30.json`).

**Versão final:** calibração em 530 perguntas rotuladas (dev + perguntas de treino) com o critério
`recusa_max`: o maior limiar que barra no máximo 2% das perguntas com resposta. Recusar uma dúvida real de
segurança custa mais do que deixar passar uma pergunta sem resposta, porque a LLM ainda pode recusá-la.
O comando é `python -m alerta_ia.busca calibrar`; aqui lemos o resultado gravado."""),
    code("""pacote = json.loads(config.LIMIAR_JSON.read_text(encoding="utf-8"))
v1 = json.loads((config.DIR_AVALIACAO / "limiar_v1_dev30.json").read_text(encoding="utf-8"))
display(Markdown(f"**Limiar escolhido: {pacote['limiar']:.4f}** (conjunto: {pacote['arquivo']})\\n\\n{pacote['justificativa']}"))
pd.DataFrame([
    {"versão": "v1 (Youden, 30 de dev)", "limiar": v1["limiar"], **{k: v1["no_limiar"][k] for k in ["sensibilidade", "especificidade", "youden"]}},
    {"versão": "final (recusa_max, 530)", "limiar": pacote["limiar"], **{k: pacote["no_limiar"][k] for k in ["sensibilidade", "especificidade", "youden"]}},
]).round(3)"""),
    code("""v = pd.DataFrame(pacote["varredura"])
fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4))
a1.plot(v["limiar"], v["recusa_indevida_pelo_limiar"], label="recusa indevida (responde barradas)")
a1.plot(v["limiar"], v["nao_consta_que_passam"], label="não consta que passam (risco de alucinação)")
a1.plot(v["limiar"], v["youden"], "--", label="Youden")
a1.axvline(pacote["limiar"], color="k", lw=1)
a1.set_xlabel("limiar"); a1.legend(fontsize=8); a1.set_title("Troca do limiar (calibração)")
s = pd.DataFrame(pacote["scores_top1"])
for tipo, g in s.groupby("tipo"):
    a2.hist(g["similaridade_top1"], bins=20, alpha=0.6, label=tipo)
a2.axvline(pacote["limiar"], color="k", lw=1); a2.legend(); a2.set_title("Similaridade do top-1 (calibração)")
plt.tight_layout()"""),
    code("""cols = ["limiar", "sensibilidade", "especificidade", "f1", "youden", "recusa_indevida_pelo_limiar",
        "nao_consta_que_passam"]
perto = v.iloc[(v["limiar"] - pacote["limiar"]).abs().argsort()[:9]].sort_values("limiar")
perto[cols].round(3)"""),
]

# ----------------------------------------------------------------------------- 03
NB03 = [
    md("""# 03 · Geração fundamentada: sem contexto × RAG

Mesmo modelo (`Qwen2.5-3B-Instruct` em 4 bits), mesma instrução de formato JSON e decodificação gulosa.
A diferença é só o contexto:

- **sem_contexto**: só a pergunta (linha de base);
- **rag**: top-3 trechos recuperados, cada um com seu id, delimitados e marcados como DADOS (defesa contra
  injeção de prompt), mais o portão por limiar.

Medimos: JSON válido (estrito: `json.loads` do texto bruto e exatamente os 3 campos), citação (ids citados
precisam estar no contexto) e recusa.

""" + PREREQ),
    code(SETUP),
    code("""from alerta_ia import prompts

msgs = prompts.montar_mensagens("Como me cadastro para receber alertas?", dados.carregar_trechos()[:3])
print(msgs[0]["content"])
print("-" * 80)
print(msgs[1]["content"][:1500])"""),
    md("""## Resultados por configuração

Com `REEXECUTAR = False`, lemos `avaliacao/resultados/<config>.jsonl`. Com `True`, roda a avaliação
(GPU, alguns minutos por configuração)."""),
    code("""for cfg in ["sem_contexto", "rag"]:
    if REEXECUTAR or not (config.DIR_RESULTADOS / f"{cfg}.jsonl").exists():
        rodar("alerta_ia.avaliacao", "--config", cfg)
res = {cfg: pd.DataFrame(dados.ler_jsonl(config.DIR_RESULTADOS / f"{cfg}.jsonl")) for cfg in ["sem_contexto", "rag"]}
from alerta_ia.avaliacao import consolidar

pd.DataFrame({cfg: consolidar(list(df["metricas"])) for cfg, df in res.items()}).T[
    ["acuracia_global", "acerto_responde", "taxa_alucinacao", "recusa_indevida", "json_valido_estrito",
     "citacao_correta", "latencia_media_ms"]]"""),
    md("## Exemplos lado a lado"),
    code("""def lado_a_lado(id_caso):
    a = res["sem_contexto"].set_index("id").loc[id_caso]
    b = res["rag"].set_index("id").loc[id_caso]
    display(Markdown(
        f"**{id_caso}** ({a['tipo']}) · {a['pergunta']}\\n\\n*Esperado:* {a['resposta_esperada']}\\n\\n"
        f"| | sem_contexto | rag |\\n|---|---|---|\\n"
        f"| resposta | {a['resposta']} | {b['resposta']} |\\n"
        f"| fontes | {a['fontes']} | {b['fontes']} |\\n"
        f"| recusou | {a['recusa']} | {b['recusa']} (limiar: {b['recusa_por_limiar']}) |\\n"
        f"| JSON estrito | {a['json_valido_estrito']} | {b['json_valido_estrito']} |\\n"
        f"| acerto | {a['metricas']['acerto']} | {b['metricas']['acerto']} |"))


df = res["rag"]
exemplos = list(df[df["tipo"] == "responde"]["id"][:2]) + list(df[df["tipo"] == "nao_consta"]["id"][:2])
for i in exemplos:
    lado_a_lado(i)"""),
    md("""## JSON inválido e citações inválidas

O parser **estrito** é a métrica. A API usa um parser **tolerante** (remove cercas de código e extrai o
primeiro objeto) como degradação elegante; ids citados fora do contexto são marcados como inválidos e não
aparecem para o morador."""),
    code("""for cfg, df in res.items():
    inval = df[~df["json_valido_estrito"] & ~df["recusa_por_limiar"]]
    cit = df[df["citacoes_invalidas"].str.len() > 0]
    print(f"{cfg}: {len(inval)} saídas com JSON inválido; {len(cit)} com citação de id fora do contexto")
    for _, r in inval.head(3).iterrows():
        print("   ", r["id"], "|", r["erro_json"], "|", r["saida_bruta"][:160].replace("\\n", " "))"""),
]

# ----------------------------------------------------------------------------- 04
NB04 = [
    md("""# 04 · Especialização com QLoRA

Treinamos um adaptador LoRA sobre o modelo base em 4 bits (NF4, dupla quantização) para reforçar o
**formato JSON**, a **citação** e a **recusa**. O dataset é montado com o **mesmo buscador e o mesmo prompt**
da configuração `rag` (top-3 reais): para `responde`, ao menos um trecho relevante é garantido no contexto
(inserido se a busca não trouxe) e a ordem é embaralhada com semente; para `nao_consta`, os top-3 reais são
distratores. O alvo é o JSON estrito; a perda é calculada só nos tokens da resposta.

Hiperparâmetros: r=16, alpha=32, dropout 0,05, alvos `q_proj,k_proj,v_proj,o_proj`, lr 2e-4 cosine com
warmup, 2 épocas, batch efetivo 8 (com recuo automático para batch 1 em falta de memória), padding dinâmico,
agrupamento por comprimento, validação ao fim de cada época.

""" + PREREQ),
    code(SETUP),
    code("""if REEXECUTAR or not config.ESTATISTICAS_TREINO.exists():
    rodar("alerta_ia.treino_lora", "--somente-dataset")
stats = ler_json(config.ESTATISTICAS_TREINO)
linhas = pd.DataFrame(dados.ler_jsonl(config.DATASET_MONTADO))
print(f"{stats['n_exemplos']} exemplos montados; sem vazamento com teste/dev: {stats['sem_vazamento']}")"""),
    md("## Estatísticas do dataset montado"),
    code("""display(pd.DataFrame(stats["por_split_e_tipo"]).fillna(0).astype(int).T.assign(total=lambda d: d.sum(axis=1)))
display(pd.DataFrame({"prompt": stats["tokens_prompt"], "alvo": stats["tokens_alvo"]}).T.rename_axis("tokens"))
display(pd.Series(stats["cobertura"], name="cobertura").to_frame())
display(pd.DataFrame(stats["vazamento"]).T[["n_perguntas_conjunto", "perguntas_em_comum"]]
        .rename_axis("checagem de vazamento"))
print("exemplos com trecho relevante inserido:", stats["exemplos_com_relevante_inserido"],
      "| com contexto truncado:", stats["exemplos_com_contexto_truncado"])
if stats.get("por_categoria"):
    display(pd.Series(stats["por_categoria"], name="exemplos").sort_values(ascending=False).to_frame())"""),
    md("## Distribuição de tamanhos (tokens)"),
    code("""fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 3.5))
a1.hist(linhas["n_tokens_prompt"], bins=30); a1.set_title("tokens do prompt"); a1.set_xlabel("tokens")
a2.hist(linhas["n_tokens_alvo"], bins=30, color="tab:orange"); a2.set_title("tokens do alvo (JSON)")
a2.set_xlabel("tokens"); plt.tight_layout()"""),
    md("""## Três exemplos completos

Um `responde`, um `nao_consta` do domínio e um **ataque** (tentativa de injeção de prompt: a resposta
correta é seguir as regras e não obedecer à instrução embutida)."""),
    code("""import re

padrao_ataque = re.compile(r"ignor|instru|regra|prompt|finja|esque[cç]a|sistema|system|jailbreak", re.I)
eh_ataque = linhas["categoria"].fillna("").str.contains("ataque|inje", case=False) | (
    linhas["pergunta"].str.contains(padrao_ataque))
escolhas = {
    "responde": linhas[(linhas["tipo"] == "responde") & ~eh_ataque].head(1),
    "nao_consta (domínio)": linhas[(linhas["tipo"] == "nao_consta") & ~eh_ataque].head(1),
    "ataque": linhas[eh_ataque].head(1),
}
for rotulo, sub in escolhas.items():
    if sub.empty:
        display(Markdown(f"### {rotulo}\\n(nenhum exemplo encontrado no dataset)"))
        continue
    r = sub.iloc[0]
    display(Markdown(f"### {rotulo} · `{r['id']}` ({r['split']})\\n**Pergunta:** {r['pergunta']}\\n\\n"
                     f"**Trechos no contexto:** `{r['ids_contexto']}`"))
    print("=== MENSAGEM DO USUÁRIO (prompt) ===")
    print(r["mensagens"][-1]["content"])
    print("=== ALVO (resposta do assistente) ===")
    print(r["alvo"])"""),
    md("""## Treino e curva de perda

O treino completo leva alguns minutos na RTX 4060 Ti 8 GB. Com `REEXECUTAR = False`, lemos
`avaliacao/treino_log.json`."""),
    code("""if REEXECUTAR or not config.TREINO_LOG.exists():
    rodar("alerta_ia.treino_lora")
log_treino = ler_json(config.TREINO_LOG)
print(f"tempo total de treino: {log_treino['tempo_total_treino_min']} min | VRAM pico: {log_treino['vram_pico_gb']} GB"
      f" | adaptador: {log_treino['tamanho_adaptador_mb']} MB | parâmetros treináveis: "
      f"{log_treino['parametros_treinaveis']:,} de {log_treino['parametros_totais']:,}")
pd.Series(log_treino["hiperparametros"]).to_frame("valor")"""),
    code("""fig, ax = plt.subplots(figsize=(8, 4))
if log_treino["perda_treino"]:
    ax.plot(*zip(*log_treino["perda_treino"]), label="treino")
if log_treino["perda_validacao"]:
    ax.plot(*zip(*log_treino["perda_validacao"]), "o-", label="validação (fim de cada época)")
ax.set_xlabel("passo de otimização"); ax.set_ylabel("perda"); ax.set_title("Curva de perda do QLoRA"); ax.legend();"""),
    md("## Comparação com o RAG simples (mesmo prompt, sem adaptador)"),
    code("""for cfg in ["rag", "rag_lora"]:
    if REEXECUTAR or not (config.DIR_RESULTADOS / f"{cfg}.jsonl").exists():
        rodar("alerta_ia.avaliacao", "--config", cfg)
from alerta_ia.avaliacao import consolidar

comp = {cfg: consolidar([l["metricas"] for l in dados.ler_jsonl(config.DIR_RESULTADOS / f"{cfg}.jsonl")])
        for cfg in ["rag", "rag_lora"]}
tab = pd.DataFrame(comp)[["rag", "rag_lora"]]
tab["diferença"] = tab["rag_lora"] - tab["rag"]
tab.loc[["acuracia_global", "acerto_responde", "recusa_correta", "taxa_alucinacao", "erro_factual",
         "recusa_indevida", "json_valido_estrito", "citacao_correta", "latencia_media_ms"]]"""),
]

# ----------------------------------------------------------------------------- 05
NB05 = [
    md("""# 05 · Placar das três configurações e erros reais

Configurações: `sem_contexto` (linha de base), `rag` (top-3 + limiar) e `rag_lora` (mesmo prompt +
adaptador). As linhas `*_sem_limiar` mostram o efeito isolado do portão por similaridade.

Métricas: acerto nas `responde` (todos os fatos-chave e sem recusa), recusa correta nas `nao_consta`,
alucinação (respondeu uma `nao_consta`), erro factual (respondeu uma `responde` faltando fatos), recusa
indevida, JSON válido estrito, citação correta, acurácia global, latência média e p95.

""" + PREREQ),
    code(SETUP),
    code("""from alerta_ia import avaliacao

if REEXECUTAR:
    rodar("alerta_ia.avaliacao", "--config", "todas")
    rodar("alerta_ia.avaliacao", "--config", "todas", "--sem-limiar")
placar = avaliacao.consolidar_placar()
display(Markdown(config.PLACAR_MD.read_text(encoding="utf-8")))"""),
    code("""m = pd.DataFrame({n: p["metricas"] for n, p in placar["configuracoes"].items()}).T
ordem = [n for n in avaliacao.ORDEM if n in m.index] + [n for n in m.index if n not in avaliacao.ORDEM]
m = m.loc[ordem]
principais = ["acuracia_global", "acerto_responde", "taxa_alucinacao", "recusa_indevida", "citacao_correta",
              "json_valido_estrito"]
ax = (m[principais].astype(float) * 100).plot.bar(figsize=(11, 4), rot=0)
ax.set_ylabel("%"); ax.set_title("Placar por configuração (teste)"); ax.legend(fontsize=8, ncol=3);"""),
    code("""ax = m[["latencia_media_ms", "latencia_p95_ms"]].astype(float).plot.bar(figsize=(8, 3.5), rot=0)
ax.set_ylabel("ms"); ax.set_title("Latência por pergunta");"""),
    md("## Efeito isolado do limiar"),
    code("""pares = [(c, f"{c}_sem_limiar") for c in ["rag", "rag_lora"] if c in m.index and f"{c}_sem_limiar" in m.index]
if not pares:
    print("Rode `python -m alerta_ia.avaliacao --config todas --sem-limiar` para ver o efeito do limiar.")
for com, sem in pares:
    t = m.loc[[sem, com], ["acerto_responde", "taxa_alucinacao", "recusa_indevida", "recusas_por_limiar",
                           "chamadas_llm", "latencia_media_ms"]]
    display(t)"""),
    md("""## Leitura do placar

Compare `rag` e `rag_lora` com `sem_contexto`: a hipótese do projeto é **mais acerto** e **menos
alucinação** com contexto, mantendo JSON válido e citação verificável. A interpretação final, com os números
reais, está no relatório."""),
    code("""base = m.loc["sem_contexto"] if "sem_contexto" in m.index else None
if base is not None:
    for cfg in [c for c in ["rag", "rag_lora"] if c in m.index]:
        print(f"{cfg} vs sem_contexto: acurácia {100 * (m.loc[cfg, 'acuracia_global'] - base['acuracia_global']):+.1f} p.p.,"
              f" alucinação {100 * (m.loc[cfg, 'taxa_alucinacao'] - base['taxa_alucinacao']):+.1f} p.p.")"""),
    md("""## Candidatos a erros reais

Todos os casos com falha, por tipo: busca não trouxe o trecho, recusa indevida, alucinação, JSON inválido,
citação errada, fato faltando. A lista completa está em `avaliacao/erros_candidatos.md`; os 5 erros
analisados no relatório saem daqui."""),
    code("""resultados = avaliacao.carregar_resultados()
linhas = []
for nome, regs in resultados.items():
    for r in regs:
        for f in r["metricas"]["falhas"][:1]:
            linhas.append({"configuracao": nome, "falha_principal": avaliacao.FALHAS[f], "id": r["id"]})
falhas = pd.DataFrame(linhas)
if falhas.empty:
    print("nenhuma falha registrada")
else:
    display(pd.crosstab(falhas["falha_principal"], falhas["configuracao"], margins=True, margins_name="total"))"""),
    code("""alvo = "rag_lora" if "rag_lora" in resultados else next(iter(resultados), None)
if alvo:
    df = pd.DataFrame(resultados[alvo])
    df["falha"] = df["metricas"].apply(lambda x: ", ".join(avaliacao.FALHAS[f] for f in x["falhas"]))
    display(df[df["falha"] != ""][["id", "tipo", "pergunta", "resposta", "fontes", "trechos_relevantes", "falha"]]
            .head(15))"""),
]

NOTEBOOKS = {
    "01_tarefa_base_e_testes.ipynb": NB01,
    "02_busca_recall_e_limiar.ipynb": NB02,
    "03_geracao_fundamentada.ipynb": NB03,
    "04_especializacao_lora.ipynb": NB04,
    "05_placar_e_erros.ipynb": NB05,
}

if __name__ == "__main__":
    for nome, celulas in NOTEBOOKS.items():
        caderno = nb(celulas)
        nbformat.validate(caderno)
        nbformat.write(caderno, PASTA / nome)
        print("gerado", nome)
