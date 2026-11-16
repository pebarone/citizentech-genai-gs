"""Leitura e validação dos arquivos de dados (JSONL e CSV)."""

from __future__ import annotations

import csv
import json
import re
import unicodedata
from pathlib import Path

from alerta_ia import config

CAMPOS_TRECHO = {"id": str, "fonte_id": str, "titulo": str, "secao": str, "texto": str, "url": str}
CAMPOS_CASO = {
    "id": str,
    "pergunta": str,
    "tipo": str,
    "categoria": str,
    "resposta_esperada": str,
    "fatos_chave": list,
    "trechos_relevantes": list,
}
CAMPOS_TREINO = {"id": str, "pergunta": str, "tipo": str, "resposta": str, "trechos_relevantes": list}
CAMPOS_FONTES = ["fonte_id", "titulo", "orgao", "url", "formato", "licenca", "data_acesso", "n_trechos"]
TIPOS = {"responde", "nao_consta"}


class ErroDados(ValueError):
    """Arquivo de dados fora do esquema combinado."""


def normalizar_texto(texto: str) -> str:
    """Minúsculas, sem acentos e com espaços colapsados (comparação de fatos e recusas)."""
    decomposto = unicodedata.normalize("NFKD", texto)
    sem_acento = "".join(c for c in decomposto if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", sem_acento.lower()).strip()


def ler_jsonl(caminho: str | Path) -> list[dict]:
    """Lê um JSONL ignorando linhas vazias; erro indica arquivo e linha."""
    caminho = Path(caminho)
    registros = []
    with caminho.open(encoding="utf-8") as f:
        for n, linha in enumerate(f, start=1):
            linha = linha.strip()
            if not linha:
                continue
            try:
                registros.append(json.loads(linha))
            except json.JSONDecodeError as e:
                raise ErroDados(f"{caminho.name}:{n}: JSON inválido ({e.msg})") from e
    return registros


def gravar_jsonl(caminho: str | Path, registros) -> None:
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with caminho.open("w", encoding="utf-8", newline="\n") as f:
        for r in registros:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def _validar_campos(registro: dict, campos: dict, origem: str) -> None:
    if not isinstance(registro, dict):
        raise ErroDados(f"{origem}: registro não é um objeto")
    for campo, tipo in campos.items():
        if campo not in registro:
            raise ErroDados(f"{origem}: campo obrigatório ausente '{campo}'")
        if not isinstance(registro[campo], tipo):
            raise ErroDados(f"{origem}: campo '{campo}' deveria ser {tipo.__name__}")


def _validar_ids_unicos(registros: list[dict], nome: str) -> None:
    vistos = set()
    for r in registros:
        if r["id"] in vistos:
            raise ErroDados(f"{nome}: id duplicado '{r['id']}'")
        vistos.add(r["id"])


def validar_caso(caso: dict, origem: str = "caso") -> None:
    _validar_campos(caso, CAMPOS_CASO, origem)
    if caso["tipo"] not in TIPOS:
        raise ErroDados(f"{origem}: tipo inválido '{caso['tipo']}'")
    for grupo in caso["fatos_chave"]:
        if not isinstance(grupo, list) or not grupo or not all(isinstance(a, str) for a in grupo):
            raise ErroDados(f"{origem}: cada item de fatos_chave deve ser lista não vazia de textos")
    if caso["tipo"] == "responde" and not caso["trechos_relevantes"]:
        raise ErroDados(f"{origem}: caso 'responde' sem trechos_relevantes")


def carregar_trechos(caminho: str | Path | None = None) -> list[dict]:
    caminho = Path(caminho or config.TRECHOS)
    trechos = ler_jsonl(caminho)
    for i, t in enumerate(trechos, start=1):
        _validar_campos(t, CAMPOS_TRECHO, f"{caminho.name}:{i}")
        if not t["texto"].strip():
            raise ErroDados(f"{caminho.name}:{i}: texto vazio")
    _validar_ids_unicos(trechos, caminho.name)
    return trechos


def carregar_casos(caminho: str | Path | None = None) -> list[dict]:
    """Carrega casos de avaliação (teste.jsonl ou dev.jsonl)."""
    caminho = Path(caminho or config.TESTE)
    casos = ler_jsonl(caminho)
    for i, c in enumerate(casos, start=1):
        validar_caso(c, f"{caminho.name}:{i}")
    _validar_ids_unicos(casos, caminho.name)
    return casos


def carregar_treino(caminho: str | Path | None = None) -> list[dict]:
    caminho = Path(caminho or config.PERGUNTAS_TREINO)
    exemplos = ler_jsonl(caminho)
    for i, e in enumerate(exemplos, start=1):
        _validar_campos(e, CAMPOS_TREINO, f"{caminho.name}:{i}")
        if e["tipo"] not in TIPOS:
            raise ErroDados(f"{caminho.name}:{i}: tipo inválido '{e['tipo']}'")
    _validar_ids_unicos(exemplos, caminho.name)
    return exemplos


def carregar_fontes(caminho: str | Path | None = None) -> list[dict]:
    caminho = Path(caminho or config.FONTES)
    with caminho.open(encoding="utf-8-sig", newline="") as f:
        leitor = csv.DictReader(f)
        faltando = [c for c in CAMPOS_FONTES if c not in (leitor.fieldnames or [])]
        if faltando:
            raise ErroDados(f"{caminho.name}: colunas ausentes {faltando}")
        return [dict(linha) for linha in leitor]


def referencias_quebradas(registros: list[dict], ids_trechos: set[str]) -> list[tuple[str, str]]:
    """Lista pares (id do registro, id de trecho) cujo trecho relevante não existe na base."""
    return [
        (r["id"], t)
        for r in registros
        for t in r.get("trechos_relevantes", [])
        if t not in ids_trechos
    ]
