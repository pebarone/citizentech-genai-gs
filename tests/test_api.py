import logging

import pytest
from fastapi.testclient import TestClient

from alerta_ia import config, seguranca
from alerta_ia.api import RESPOSTA_DEGRADADA, criar_app
from alerta_ia.geracao import Pipeline
from alerta_ia.prompts import RECUSA_PADRAO
from conftest import GeradorFalso

RESP_SMS = '{"resposta": "Envie o CEP para 40199.", "fontes": ["dc-02-001", "inventado"], "consta_na_base": true}'


@pytest.fixture
def gerador():
    return GeradorFalso(respostas={
        "quebrado": "desculpe, não sei formatar",
        "palpite": '{"resposta": "Acho que custa pouco.", "fontes": [], "consta_na_base": false}',
        "SMS": RESP_SMS,
    })


@pytest.fixture
def cliente(buscador, gerador):
    pipe = Pipeline("rag", gerador, buscador, limiar=0.3)
    app = criar_app(pipeline=pipe, limitador=seguranca.LimitadorTaxa(max_requisicoes=5, janela_s=60))
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c


def _perguntar(cliente, texto):
    return cliente.post("/api/v1/assistente/perguntar", json={"pergunta": texto})


def test_saude_e_info(cliente):
    assert cliente.get("/healthz").json() == {"status": "ok"}
    assert cliente.get("/readyz").status_code == 200
    info = cliente.get("/api/v1/info").json()
    assert info["configuracao"] == "rag" and info["telefones"] == {"defesa_civil": "199", "bombeiros": "193"}


def test_resposta_com_fontes_validas(cliente, caplog):
    caplog.set_level(logging.INFO, logger="alerta_ia.api")
    r = _perguntar(cliente, "Como recebo alerta por SMS no meu celular?")
    assert r.status_code == 200
    corpo = r.json()
    assert corpo["consta_na_base"] is True and corpo["resposta"].startswith("Envie o CEP")
    assert [f["id"] for f in corpo["fontes"]] == ["dc-02-001"]  # id inventado não aparece
    f = corpo["fontes"][0]
    assert set(f) == {"id", "titulo", "secao", "url", "trecho", "similaridade"}
    ex = corpo["explicacao"]
    assert ex["limiar"] == 0.3 and ex["recusa_por_limiar"] is False and ex["configuracao"] == "rag"
    assert ex["citacoes_invalidas"] == ["inventado"]
    assert corpo["aviso_emergencia"] is None and corpo["latencia_ms"] >= 0
    assert r.headers["x-content-type-options"] == "nosniff"
    # o log não contém o texto da pergunta
    assert "SMS no meu celular" not in caplog.text and '"hash"' in caplog.text


def test_recusa_por_limiar(cliente, gerador):
    r = _perguntar(cliente, "Qual o horário do ônibus 2002?")
    corpo = r.json()
    assert corpo["consta_na_base"] is False and corpo["fontes"] == []
    assert corpo["explicacao"]["recusa_por_limiar"] is True
    assert gerador.chamadas == []


def test_aviso_emergencia(cliente):
    corpo = _perguntar(cliente, "Socorro, a água está entrando em casa pela porta").json()
    assert corpo["aviso_emergencia"] == seguranca.AVISO_EMERGENCIA


def test_degradacao_quando_modelo_nao_gera_json(cliente):
    corpo = _perguntar(cliente, "Pergunta quebrado sobre enchente e alertas por SMS").json()
    assert corpo["resposta"] == RESPOSTA_DEGRADADA and corpo["consta_na_base"] is False


def test_resposta_sem_fundamento_vira_recusa(cliente):
    corpo = _perguntar(cliente, "Um palpite: alertas por SMS custam quanto?").json()
    assert corpo["resposta"] == RECUSA_PADRAO and corpo["consta_na_base"] is False and corpo["fontes"] == []


def test_validacao_de_tamanho(cliente):
    assert _perguntar(cliente, "a" * 600).status_code == 422
    assert _perguntar(cliente, " ").status_code == 422
    assert cliente.post("/api/v1/assistente/perguntar", json={}).status_code == 422


def test_limite_de_taxa(cliente):
    codigos = [_perguntar(cliente, "Como recebo alerta por SMS?").status_code for _ in range(6)]
    assert codigos[:5] == [200] * 5 and codigos[5] == 429


def test_erro_interno_sem_stack_trace(buscador):
    class Quebrado(GeradorFalso):
        def gerar(self, mensagens, max_new_tokens=None):
            raise RuntimeError("detalhe interno secreto")

    app = criar_app(pipeline=Pipeline("rag", Quebrado(), buscador, limiar=0.0))
    with TestClient(app, raise_server_exceptions=False) as c:
        r = _perguntar(c, "Como recebo alerta por SMS?")
    assert r.status_code == 500 and "secreto" not in r.text and "Traceback" not in r.text


def test_readyz_sem_pipeline():
    def falha():
        raise RuntimeError("sem modelo")

    app = criar_app(fabrica=falha)
    with TestClient(app) as c:
        assert c.get("/readyz").status_code == 503
        assert _perguntar(c, "Como recebo alerta por SMS?").status_code == 503
        assert c.get("/healthz").status_code == 200


def test_pagina_sem_front_buildado(buscador, tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DIR_WEB_DIST", tmp_path / "nao_existe")
    with TestClient(criar_app(pipeline=Pipeline("rag", GeradorFalso(), buscador, limiar=0.3))) as c:
        r = c.get("/")
        assert r.status_code == 200 and "/docs" in r.text and "199" in r.text
        assert c.get("/qualquer.js").status_code == 404


def test_serve_build_do_front(buscador, tmp_path, monkeypatch):
    dist = tmp_path / "dist"
    (dist / "assets").mkdir(parents=True)
    (dist / "index.html").write_text("<!doctype html><title>Front Alerta</title>", encoding="utf-8")
    (dist / "assets" / "app-123.js").write_text("console.log(1)", encoding="utf-8")
    (dist / "favicon.svg").write_text("<svg/>", encoding="utf-8")
    (tmp_path / "segredo.txt").write_text("x", encoding="utf-8")
    monkeypatch.setattr(config, "DIR_WEB_DIST", dist)
    with TestClient(criar_app(pipeline=Pipeline("rag", GeradorFalso(), buscador, limiar=0.3))) as c:
        r = c.get("/")
        assert "Front Alerta" in r.text and "default-src 'self'" in r.headers["content-security-policy"]
        assert c.get("/assets/app-123.js").text == "console.log(1)"
        assert c.get("/favicon.svg").status_code == 200
        assert c.get("/..%2Fsegredo.txt").status_code == 404
        assert c.get("/healthz").json() == {"status": "ok"}
