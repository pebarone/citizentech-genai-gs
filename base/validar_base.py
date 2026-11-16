"""Validador da base de conhecimento e dos conjuntos de perguntas do Alerta Córrego.

Uso (a partir da raiz do projeto):
    python base/validar_base.py

Verifica fontes.csv, trechos.jsonl, brutos/, avaliacao/teste.jsonl, avaliacao/dev.jsonl
e treino/perguntas_treino.jsonl. Reescreve a coluna n_trechos de fontes.csv com a
contagem real. Imprime um resumo (usado nas fichas README) e sai com código 1 se
alguma verificação falhar. Somente biblioteca padrão.
"""
import csv
import io
import itertools
import json
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(RAIZ, "base")
P_FONTES = os.path.join(BASE, "fontes.csv")
P_TRECHOS = os.path.join(BASE, "trechos.jsonl")
P_BRUTOS = os.path.join(BASE, "brutos")
P_TESTE = os.path.join(RAIZ, "avaliacao", "teste.jsonl")
P_DEV = os.path.join(RAIZ, "avaliacao", "dev.jsonl")
P_TREINO = os.path.join(RAIZ, "treino", "perguntas_treino.jsonl")

ESPERADO = {
    "teste": {"responde": 42, "nao_consta": 18},
    "dev": {"responde": 20, "nao_consta": 10},
    "treino": {"responde": 360, "nao_consta": 140},
}
# subtipos de "nao_consta" (grupo -> quantidade esperada)
ESPERADO_SUB = {
    "teste": {"dominio": 8, "fora": 5, "ataque": 5},
    "treino": {"dominio": 70, "fora": 35, "ataque": 35},
}
LIMIAR_QUASE_DUP = 0.8
NC_AVAL = "Não consta na base."

erros = []
avisos = []


def erro(msg):
    erros.append(msg)


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower()


def tokens(s):
    return set(re.findall(r"[a-z0-9]+", norm(s)))


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def ler_jsonl(caminho):
    linhas = []
    if not os.path.exists(caminho):
        erro(f"arquivo ausente: {caminho}")
        return linhas
    with open(caminho, encoding="utf-8") as f:
        for n, l in enumerate(f, 1):
            if not l.strip():
                continue
            try:
                linhas.append(json.loads(l))
            except json.JSONDecodeError as e:
                erro(f"{os.path.basename(caminho)}:{n} JSON inválido ({e})")
    return linhas


def grupo_sub(cat):
    if cat.startswith("dominio"):
        return "dominio"
    if cat.startswith("fora"):
        return "fora"
    if cat.startswith("ataque"):
        return "ataque"
    return "?"


# ---------------- fontes e trechos ----------------
with open(P_FONTES, encoding="utf-8", newline="") as f:
    fontes = list(csv.DictReader(f))
COLS = ["fonte_id", "titulo", "orgao", "url", "formato", "licenca", "data_acesso", "n_trechos"]
if not fontes or list(fontes[0].keys()) != COLS:
    erro(f"cabeçalho de fontes.csv diferente de {COLS}")
ids_fonte = [r["fonte_id"] for r in fontes]
for k, v in Counter(ids_fonte).items():
    if v > 1:
        erro(f"fonte_id duplicado em fontes.csv: {k}")
for r in fontes:
    if r["formato"] not in ("HTML", "PDF"):
        erro(f"{r['fonte_id']}: formato inválido {r['formato']}")
    if not r["licenca"].strip():
        erro(f"{r['fonte_id']}: licença vazia")
    bruto = os.path.join(P_BRUTOS, r["fonte_id"] + ".txt")
    if not os.path.exists(bruto):
        erro(f"{r['fonte_id']}: bruto ausente ({bruto})")
    else:
        with open(bruto, encoding="utf-8") as fb:
            primeira = fb.readline()
        if "http" not in primeira or "2026-11-15" not in primeira:
            erro(f"{r['fonte_id']}: primeira linha do bruto sem URL/data de acesso")

trechos = ler_jsonl(P_TRECHOS)
tr_por_id = {}
for t in trechos:
    for campo in ("id", "fonte_id", "titulo", "secao", "texto", "url"):
        if not str(t.get(campo, "")).strip():
            erro(f"trecho {t.get('id')}: campo '{campo}' vazio")
    if t["id"] in tr_por_id:
        erro(f"id de trecho duplicado: {t['id']}")
    tr_por_id[t["id"]] = t
    if t["fonte_id"] not in ids_fonte:
        erro(f"trecho {t['id']}: fonte_id {t['fonte_id']} não está em fontes.csv")
    if not re.fullmatch(re.escape(t["fonte_id"]) + r"-\d{3}", t["id"]):
        erro(f"trecho {t['id']}: id fora do padrão <fonte_id>-NNN")
    n = len(t["texto"].split())
    if n < 60 or n > 180:
        avisos.append(f"trecho {t['id']} com {n} palavras (meta 60-180)")

cont_fonte = Counter(t["fonte_id"] for t in trechos)
mudou = False
for r in fontes:
    real = str(cont_fonte.get(r["fonte_id"], 0))
    if r["n_trechos"] != real:
        avisos.append(f"n_trechos de {r['fonte_id']} corrigido: {r['n_trechos']} -> {real}")
        r["n_trechos"] = real
        mudou = True
    if real == "0":
        erro(f"fonte {r['fonte_id']} sem trechos")
if mudou:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=COLS, lineterminator="\n")
    w.writeheader()
    w.writerows(fontes)
    with open(P_FONTES, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())

# ---------------- conjuntos de perguntas ----------------
conjuntos = {"teste": ler_jsonl(P_TESTE), "dev": ler_jsonl(P_DEV), "treino": ler_jsonl(P_TREINO)}
prefixo = {"teste": "T", "dev": "D", "treino": "TR"}


def checar_trechos(nome, caso):
    ids = caso.get("trechos_relevantes", [])
    for i in ids:
        if i not in tr_por_id:
            erro(f"{nome} {caso['id']}: trecho inexistente {i}")
    return ids


for nome, casos in conjuntos.items():
    vistos = set()
    for i, c in enumerate(casos, 1):
        esperado_id = f"{prefixo[nome]}{i:03d}"
        if c.get("id") != esperado_id:
            erro(f"{nome}: id {c.get('id')} na posição {i} (esperado {esperado_id})")
        if c.get("id") in vistos:
            erro(f"{nome}: id duplicado {c.get('id')}")
        vistos.add(c.get("id"))
        if c.get("tipo") not in ("responde", "nao_consta"):
            erro(f"{nome} {c.get('id')}: tipo inválido {c.get('tipo')}")
            continue
        if not c.get("pergunta", "").strip():
            erro(f"{nome} {c['id']}: pergunta vazia")
        ids = checar_trechos(nome, c)
        if nome in ("teste", "dev"):
            if c["tipo"] == "responde":
                if not (1 <= len(ids) <= 3):
                    erro(f"{nome} {c['id']}: precisa de 1 a 3 trechos_relevantes")
                fk = c.get("fatos_chave", [])
                if not (1 <= len(fk) <= 3):
                    erro(f"{nome} {c['id']}: precisa de 1 a 3 grupos em fatos_chave")
                resp = norm(c.get("resposta_esperada", ""))
                texto = norm(" ".join(tr_por_id[i]["texto"] for i in ids if i in tr_por_id))
                for g in fk:
                    alts = [norm(a) for a in g]
                    if not any(a in resp for a in alts):
                        erro(f"{nome} {c['id']}: grupo {g} não casa com resposta_esperada")
                    if not any(a in texto for a in alts):
                        erro(f"{nome} {c['id']}: grupo {g} não casa com o texto dos trechos (gabarito sem fundamento)")
            else:
                if c.get("fatos_chave") != [] or ids != []:
                    erro(f"{nome} {c['id']}: nao_consta deve ter fatos_chave e trechos_relevantes vazios")
                if c.get("resposta_esperada") != NC_AVAL:
                    erro(f"{nome} {c['id']}: resposta_esperada de nao_consta deve ser '{NC_AVAL}'")
                if grupo_sub(c.get("categoria", "")) == "?":
                    erro(f"{nome} {c['id']}: categoria de nao_consta deve começar com dominio/fora/ataque")
        else:  # treino
            resp = c.get("resposta", "")
            if c["tipo"] == "responde":
                if not (1 <= len(ids) <= 3):
                    erro(f"treino {c['id']}: precisa de 1 a 3 trechos_relevantes")
                if not resp.strip() or resp.startswith("Não consta"):
                    erro(f"treino {c['id']}: resposta de 'responde' inválida")
            else:
                if ids:
                    erro(f"treino {c['id']}: nao_consta não deve citar trechos")
                if not resp.startswith("Não consta na base"):
                    erro(f"treino {c['id']}: recusa deve começar com 'Não consta na base'")
            nfr = len(re.findall(r"[.!?](\s|$)", resp.strip()))
            if nfr > 3:
                avisos.append(f"treino {c['id']}: resposta com {nfr} frases (meta 1-3)")

    tipos = Counter(c.get("tipo") for c in casos)
    for t, n in ESPERADO[nome].items():
        if tipos.get(t, 0) != n:
            erro(f"{nome}: {tipos.get(t, 0)} casos '{t}' (esperado {n})")

# subtipos de nao_consta
sub_teste = Counter(grupo_sub(c["categoria"]) for c in conjuntos["teste"] if c.get("tipo") == "nao_consta")
sub_dev = Counter(grupo_sub(c["categoria"]) for c in conjuntos["dev"] if c.get("tipo") == "nao_consta")
sub_treino = Counter(grupo_sub(c.get("subtipo", "")) for c in conjuntos["treino"] if c.get("tipo") == "nao_consta")
sub_treino_fino = Counter(c.get("subtipo", "") for c in conjuntos["treino"] if c.get("tipo") == "nao_consta")
for nome, real in (("teste", sub_teste), ("treino", sub_treino)):
    for g, n in ESPERADO_SUB[nome].items():
        if real.get(g, 0) != n:
            erro(f"{nome}: {real.get(g, 0)} nao_consta do grupo '{g}' (esperado {n})")

# no máximo 2 perguntas de teste por trecho
uso_teste = Counter(i for c in conjuntos["teste"] for i in c.get("trechos_relevantes", []))
for i, n in uso_teste.items():
    if n > 2:
        erro(f"teste: trecho {i} usado em {n} perguntas (máximo 2)")

# duplicatas e quase-duplicatas
todas = [(nome, c["id"], c["pergunta"]) for nome, casos in conjuntos.items() for c in casos]
por_texto = defaultdict(list)
for nome, cid, p in todas:
    por_texto[" ".join(sorted(tokens(p)))].append(cid)
for k, v in por_texto.items():
    if len(v) > 1:
        erro(f"pergunta duplicada (normalizada): {v}")

toks = {(nome, cid): tokens(p) for nome, cid, p in todas}
maior_cruzado = (0.0, None, None)
maior_interno = (0.0, None, None)
pares = itertools.combinations(todas, 2)
for (n1, i1, _), (n2, i2, _) in pares:
    s = jaccard(toks[(n1, i1)], toks[(n2, i2)])
    cruzado = n1 != n2
    if cruzado and s > maior_cruzado[0]:
        maior_cruzado = (s, i1, i2)
    if not cruzado and s > maior_interno[0]:
        maior_interno = (s, i1, i2)
    if s > LIMIAR_QUASE_DUP:
        erro(f"quase-duplicata ({s:.2f}): {i1} x {i2}")

# ---------------- resumo ----------------
print("=" * 64)
print("VALIDAÇÃO DA BASE E DOS CONJUNTOS – Alerta Córrego")
print("=" * 64)
print(f"Fontes: {len(fontes)} | Trechos: {len(trechos)}")
palavras = [len(t["texto"].split()) for t in trechos]
print(f"Palavras por trecho: mín {min(palavras)}, máx {max(palavras)}, média {sum(palavras)/len(palavras):.0f}")
print("\nfonte_id    formato  n_trechos  licença")
for r in fontes:
    print(f"{r['fonte_id']:<11} {r['formato']:<8} {r['n_trechos']:>9}  {r['licenca'][:70]}")

for nome, casos in conjuntos.items():
    tipos = Counter(c.get("tipo") for c in casos)
    print(f"\n[{nome}] total {len(casos)} | responde {tipos.get('responde', 0)} | nao_consta {tipos.get('nao_consta', 0)}")
print(f"  subtipos nao_consta teste : {dict(sub_teste)}")
print(f"  subtipos nao_consta dev   : {dict(sub_dev)}")
print(f"  subtipos nao_consta treino: {dict(sub_treino)}")
print(f"  detalhamento treino       : {dict(sorted(sub_treino_fino.items()))}")

tr_ids = set(tr_por_id)
fontes_ids = set(ids_fonte)
for nome, casos in conjuntos.items():
    cob = {i for c in casos for i in c.get("trechos_relevantes", [])}
    cobf = {tr_por_id[i]["fonte_id"] for i in cob if i in tr_por_id}
    print(f"[{nome}] cobertura: {len(cob)}/{len(tr_ids)} trechos, {len(cobf)}/{len(fontes_ids)} fontes")
    if nome == "treino":
        faltam = sorted(tr_ids - cob)
        if faltam:
            erro(f"treino não cobre os trechos: {faltam}")
        por_trecho = Counter(i for c in casos for i in c.get("trechos_relevantes", []))
        vals = [por_trecho.get(i, 0) for i in tr_ids]
        print(f"  perguntas de treino por trecho: mín {min(vals)}, máx {max(vals)}, média {sum(vals)/len(vals):.1f}")

# estilos (heurísticas simples sobre o texto da pergunta, treino)
tr = conjuntos["treino"]
def palavras_p(c):
    return len(c["pergunta"].split())
estilos = {
    "curta (até 6 palavras)": sum(1 for c in tr if palavras_p(c) <= 6),
    "longa/relato (20+ palavras)": sum(1 for c in tr if palavras_p(c) >= 20),
    "começa em minúscula (informal)": sum(1 for c in tr if c["pergunta"][:1].islower()),
    "sem ponto de interrogação": sum(1 for c in tr if "?" not in c["pergunta"]),
    "primeira pessoa (minha/meu/moro/tô/estou)": sum(1 for c in tr if re.search(r"\b(minha|meu|moro|tô|to|estou|tenho|fiquei)\b", c["pergunta"].lower())),
    "formal (prezado/gostaria/bom dia)": sum(1 for c in tr if re.search(r"prezad|gostaria|bom dia", c["pergunta"].lower())),
    "grafia informal (pra/tá/ta/dps/vc/q/dagua)": sum(1 for c in tr if re.search(r"\b(pra|tá|ta|dps|vc|q|dagua|numero|agua|ja|nao)\b", c["pergunta"].lower())),
}
print("\n[treino] estilos (heurística, um caso pode contar em mais de uma linha):")
for k, v in estilos.items():
    print(f"  {k}: {v}")

print(f"\nMaior similaridade (Jaccard de tokens) entre conjuntos: {maior_cruzado[0]:.2f} ({maior_cruzado[1]} x {maior_cruzado[2]})")
print(f"Maior similaridade dentro de um mesmo conjunto: {maior_interno[0]:.2f} ({maior_interno[1]} x {maior_interno[2]})")
print(f"Limiar de quase-duplicata: > {LIMIAR_QUASE_DUP}")

if avisos:
    print(f"\nAVISOS ({len(avisos)}):")
    for a in avisos:
        print("  -", a)
if erros:
    print(f"\nFALHAS ({len(erros)}):")
    for e in erros:
        print("  -", e)
    print("\nRESULTADO: FALHOU")
    sys.exit(1)
print("\nRESULTADO: OK")
