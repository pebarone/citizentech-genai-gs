import json

import pytest

from alerta_ia import dados
from conftest import FIXTURES


def test_carrega_fixtures():
    assert len(dados.carregar_trechos(FIXTURES / "trechos.jsonl")) == 5
    assert len(dados.carregar_casos(FIXTURES / "casos.jsonl")) == 6
    assert len(dados.carregar_treino(FIXTURES / "treino.jsonl")) == 4
    fontes = dados.carregar_fontes(FIXTURES / "fontes.csv")
    assert {f["fonte_id"] for f in fontes} == {"dc-01", "dc-02"}


def test_caso_invalido_indica_linha(tmp_path):
    arq = tmp_path / "ruim.jsonl"
    caso = {"id": "x", "pergunta": "p", "tipo": "talvez", "categoria": "c", "resposta_esperada": "r",
            "fatos_chave": [], "trechos_relevantes": []}
    arq.write_text(json.dumps(caso) + "\n", encoding="utf-8")
    with pytest.raises(dados.ErroDados, match="ruim.jsonl:1: tipo inválido"):
        dados.carregar_casos(arq)


def test_id_duplicado(tmp_path):
    arq = tmp_path / "t.jsonl"
    linha = (FIXTURES / "trechos.jsonl").read_text(encoding="utf-8").splitlines()[0]
    arq.write_text(linha + "\n" + linha + "\n", encoding="utf-8")
    with pytest.raises(dados.ErroDados, match="duplicado"):
        dados.carregar_trechos(arq)


def test_referencias_quebradas(casos):
    assert dados.referencias_quebradas(casos, {"dc-02-001", "dc-01-002", "dc-01-001"}) == [("t-004", "dc-01-003")]


def test_normalizar_texto():
    assert dados.normalizar_texto("  Água   SANITÁRIA ") == "agua sanitaria"
