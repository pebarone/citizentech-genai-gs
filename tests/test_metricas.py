import json

import pytest

from alerta_ia import avaliacao, config
from alerta_ia.avaliacao import avaliar_caso, consolidar, fatos_presentes
from alerta_ia.geracao import Pipeline
from conftest import GeradorFalso


def _saida(resposta, fontes=(), consta=True, recusa=False, trechos=("dc-02-001",), json_ok=True, invalidas=(),
           chamou_llm=True, recusa_limiar=False):
    return {
        "resposta": resposta, "fontes": list(fontes), "consta_na_base": consta, "recusa": recusa,
        "json_valido_estrito": json_ok, "citacoes_invalidas": list(invalidas), "chamou_llm": chamou_llm,
        "recusa_por_limiar": recusa_limiar, "latencia_ms": 100.0,
        "trechos": [{"id": t, "similaridade": 0.9} for t in trechos],
    }


def test_fatos_chave_sem_acento_e_alternativas():
    ok, falta = fatos_presentes("Desligue a energia e vá para um LUGAR ALTO.",
                                [["desligue a energia", "quadro de luz"], ["local alto", "lugar alto"]])
    assert ok and falta == []
    ok, falta = fatos_presentes("Envie o CEP.", [["40199"], ["cep"]])
    assert not ok and falta == [["40199"]]
    assert fatos_presentes("qualquer", [])[0]


def test_fato_com_acento_no_gabarito():
    assert fatos_presentes("use agua sanitaria", [["água sanitária"]])[0]


def test_caso_responde_correto(casos):
    m = avaliar_caso(casos[0], _saida("Envie o CEP para 40199.", ["dc-02-001"]))
    assert m["acerto"] and m["citacao_correta"] and m["busca_trouxe_relevante"] and m["falhas"] == []


def test_caso_responde_fato_faltando_e_citacao_errada(casos):
    m = avaliar_caso(casos[0], _saida("Envie o CEP.", ["dc-01-001"], trechos=["dc-02-001", "dc-01-001"]))
    assert not m["acerto"] and m["erro_factual"] and m["citacao_correta"] is False
    assert m["falhas"] == ["fato_faltando", "citacao"]


def test_citacao_inexistente_no_contexto_invalida(casos):
    m = avaliar_caso(casos[0], _saida("Envie o CEP para 40199.", ["dc-02-001", "inventado"], invalidas=["inventado"]))
    assert m["acerto"] and m["citacao_correta"] is False


def test_recusa_indevida_com_busca_falha(casos):
    m = avaliar_caso(casos[0], _saida("Não consta na base.", consta=False, recusa=True, trechos=["dc-01-001"],
                                      chamou_llm=False, recusa_limiar=True))
    assert m["recusa_indevida"] and not m["acerto"]
    assert m["falhas"][0] == "busca" and "recusa_indevida" in m["falhas"]
    assert "json_invalido" not in m["falhas"]


def test_nao_consta_alucinacao_e_recusa(casos):
    nc = casos[4]
    assert avaliar_caso(nc, _saida("Custa R$ 50.", consta=True))["alucinacao"]
    m = avaliar_caso(nc, _saida("Não consta na base.", consta=False, recusa=True))
    assert m["acerto"] and not m["alucinacao"] and m["citacao_correta"] is None


def test_json_invalido_conta_como_falha(casos):
    m = avaliar_caso(casos[0], _saida("Envie o CEP para 40199.", ["dc-02-001"], json_ok=False))
    assert m["acerto"] and m["falhas"] == ["json_invalido"]


def test_consolidar(casos):
    ms = [
        avaliar_caso(casos[0], _saida("Envie o CEP para 40199.", ["dc-02-001"])),  # acerto
        avaliar_caso(casos[1], _saida("Não consta na base.", consta=False, recusa=True, trechos=["dc-01-002"])),
        avaliar_caso(casos[4], _saida("Custa R$ 50.", json_ok=False)),  # alucinação
        avaliar_caso(casos[5], _saida("Não consta.", consta=False, recusa=True, chamou_llm=False, recusa_limiar=True)),
    ]
    p = consolidar(ms)
    assert p["n"] == 4 and p["n_responde"] == 2 and p["n_nao_consta"] == 2
    assert p["acerto_responde"] == 0.5 and p["recusa_indevida"] == 0.5 and p["erro_factual"] == 0.0
    assert p["taxa_alucinacao"] == 0.5 and p["recusa_correta"] == 0.5
    assert p["acuracia_global"] == 0.5
    assert p["json_valido_estrito"] == pytest.approx(2 / 3, abs=1e-4)  # só chamadas à LLM
    assert p["citacao_correta"] == 0.5 and p["recusas_por_limiar"] == 1 and p["chamadas_llm"] == 3
    assert p["latencia_media_ms"] == 100.0 and p["latencia_p95_ms"] == 100.0


def test_pipeline_fim_a_fim_com_dubles(casos, buscador, tmp_path, monkeypatch):
    gerador = GeradorFalso(respostas={
        "SMS": '{"resposta": "Envie o CEP para 40199.", "fontes": ["dc-02-001"], "consta_na_base": true}',
        "mochila": '```json\n{"resposta": "Leve documentos e lanterna.", "fontes": ["dc-01-001", "xx"], '
                   '"consta_na_base": true}\n```',
    })
    pipe = Pipeline("rag", gerador, buscador, limiar=0.5)
    linhas = avaliacao.avaliar_pipeline(pipe, casos, progresso=False)
    por_id = {l["id"]: l for l in linhas}
    assert por_id["t-001"]["metricas"]["acerto"]
    mochila = por_id["t-003"]
    assert mochila["metricas"]["acerto"] and not mochila["json_valido_estrito"]
    assert mochila["citacoes_invalidas"] == ["xx"] and mochila["metricas"]["citacao_correta"] is False
    # perguntas sem palavras em comum com a base são barradas pelo limiar, sem chamar a LLM
    assert por_id["t-006"]["recusa_por_limiar"] and por_id["t-006"]["metricas"]["acerto"]
    assert len(gerador.chamadas) < len(casos)

    monkeypatch.setattr(config, "PLACAR_JSON", tmp_path / "placar.json")
    monkeypatch.setattr(config, "PLACAR_MD", tmp_path / "placar.md")
    monkeypatch.setattr(config, "ERROS_MD", tmp_path / "erros.md")
    res = tmp_path / "resultados"
    res.mkdir()
    from alerta_ia.dados import gravar_jsonl

    gravar_jsonl(res / "rag.jsonl", linhas)
    (res / "rag.meta.json").write_text(json.dumps({"arquivo": "casos.jsonl", "limite": None}), encoding="utf-8")
    placar = avaliacao.consolidar_placar(res)
    assert placar["configuracoes"]["rag"]["metricas"]["n"] == 6
    md = (tmp_path / "placar.md").read_text(encoding="utf-8")
    assert "| rag " in md and "Acurácia global" in md
    erros = (tmp_path / "erros.md").read_text(encoding="utf-8")
    assert "t-003" in erros and "JSON inválido" in erros


def test_sem_contexto_nao_busca(casos):
    gerador = GeradorFalso()
    pipe = Pipeline("sem_contexto", gerador)
    saida = pipe.responder(casos[0]["pergunta"])
    assert saida["trechos"] == [] and saida["recusa"] and not saida["recusa_por_limiar"]
    assert "<trechos>" not in gerador.chamadas[0][-1]["content"]
    m = avaliar_caso(casos[0], saida)
    assert m["busca_trouxe_relevante"] is None and "citacao" not in m["falhas"]


def test_sem_limiar_sempre_chama_llm(casos, buscador):
    gerador = GeradorFalso()
    pipe = Pipeline("rag", gerador, buscador, limiar=0.99, usar_limiar=False)
    for c in casos:
        assert not pipe.responder(c["pergunta"])["recusa_por_limiar"]
    assert len(gerador.chamadas) == len(casos)
