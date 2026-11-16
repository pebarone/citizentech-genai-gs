"""Fixtures compartilhadas: dados pequenos e dublês de buscador e gerador (sem GPU)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from alerta_ia import dados

FIXTURES = Path(__file__).parent / "fixtures"


class BuscadorFalso:
    """Similaridade = fração de palavras (3+ letras) da pergunta contidas no trecho (determinística)."""

    modelo_id = "buscador-falso"

    def __init__(self, trechos):
        self.trechos = trechos
        self.por_id = {t["id"]: t for t in trechos}
        self.ids = [t["id"] for t in trechos]

    def _score(self, pergunta, trecho):
        limpa = "".join(c if c.isalnum() else " " for c in dados.normalizar_texto(pergunta))
        palavras = {p for p in limpa.split() if len(p) >= 3}
        texto = dados.normalizar_texto(trecho["titulo"] + " " + trecho["secao"] + " " + trecho["texto"])
        return sum(1 for p in palavras if p in texto) / max(1, len(palavras))

    def buscar(self, pergunta, k=3):
        pontuados = sorted(self.trechos, key=lambda t: -self._score(pergunta, t))
        return [{**t, "similaridade": self._score(pergunta, t)} for t in pontuados[:k]]

    def buscar_lote(self, perguntas, k=3):
        return [self.buscar(p, k) for p in perguntas]


class GeradorFalso:
    """Devolve respostas pré-definidas por pergunta (ou uma padrão) e guarda as mensagens."""

    modelo_id = "gerador-falso"
    adaptador = None

    def __init__(self, respostas=None, padrao=None):
        self.respostas = respostas or {}
        self.padrao = padrao or json.dumps(
            {"resposta": "Não consta na base.", "fontes": [], "consta_na_base": False}, ensure_ascii=False
        )
        self.chamadas = []

    def gerar(self, mensagens, max_new_tokens=None):
        self.chamadas.append(mensagens)
        usuario = mensagens[-1]["content"]
        pergunta = usuario.split("<pergunta>")[-1].split("</pergunta>")[0]
        for chave, texto in self.respostas.items():
            if chave in pergunta:
                return texto, 10
        return self.padrao, 5

    def liberar(self):
        pass


@pytest.fixture
def trechos():
    return dados.carregar_trechos(FIXTURES / "trechos.jsonl")


@pytest.fixture
def casos():
    return dados.carregar_casos(FIXTURES / "casos.jsonl")


@pytest.fixture
def buscador(trechos):
    return BuscadorFalso(trechos)
