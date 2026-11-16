import json

from alerta_ia.geracao import (
    eh_recusa,
    extrair_primeiro_objeto,
    interpretar_estrito,
    interpretar_tolerante,
    verificar_citacoes,
)

VALIDO = '{"resposta": "Ligue 199.", "fontes": ["dc-02-002"], "consta_na_base": true}'


def test_estrito_aceita_json_exato_com_espacos():
    obj, erro = interpretar_estrito("  \n" + VALIDO + "\n ")
    assert erro is None and obj["fontes"] == ["dc-02-002"]


def test_estrito_rejeita_cerca_de_codigo():
    obj, erro = interpretar_estrito("```json\n" + VALIDO + "\n```")
    assert obj is None and "JSON inválido" in erro


def test_estrito_rejeita_campo_extra_ou_faltando():
    extra = json.dumps({"resposta": "a", "fontes": [], "consta_na_base": False, "nota": 1})
    falta = json.dumps({"resposta": "a", "fontes": []})
    assert interpretar_estrito(extra)[0] is None
    assert interpretar_estrito(falta)[0] is None


def test_estrito_rejeita_tipos_errados():
    assert interpretar_estrito('{"resposta": "a", "fontes": "x", "consta_na_base": true}')[0] is None
    assert interpretar_estrito('{"resposta": "a", "fontes": [], "consta_na_base": "true"}')[0] is None
    assert interpretar_estrito('{"resposta": "", "fontes": [], "consta_na_base": true}')[0] is None


def test_tolerante_remove_cerca_e_texto_ao_redor():
    obj = interpretar_tolerante("Claro! Aqui está:\n```json\n" + VALIDO + "\n```\nEspero ter ajudado.")
    assert obj == {"resposta": "Ligue 199.", "fontes": ["dc-02-002"], "consta_na_base": True}


def test_tolerante_normaliza_tipos():
    obj = interpretar_tolerante('{"resposta": "Não consta na base.", "fontes": "x", "consta_na_base": "false"}')
    assert obj["fontes"] == ["x"] and obj["consta_na_base"] is False
    obj = interpretar_tolerante('{"resposta": "Não consta na base. Ligue 199."}')
    assert obj["consta_na_base"] is False and obj["fontes"] == []


def test_tolerante_falha_sem_objeto():
    assert interpretar_tolerante("não sei responder") is None
    assert interpretar_tolerante('{"outra": 1}') is None


def test_extrair_respeita_chaves_em_strings():
    texto = 'lixo {"resposta": "use {chaves} aqui }", "fontes": [], "consta_na_base": true} fim'
    assert json.loads(extrair_primeiro_objeto(texto))["resposta"] == "use {chaves} aqui }"


def test_citacoes_invalidas():
    validas, invalidas = verificar_citacoes(["a", "zzz", "b"], ["a", "b", "c"])
    assert validas == ["a", "b"] and invalidas == ["zzz"]


def test_eh_recusa():
    assert eh_recusa({"resposta": "Não consta na base.", "fontes": [], "consta_na_base": False})
    assert eh_recusa({"resposta": "NAO CONSTA na base", "fontes": [], "consta_na_base": True})
    assert not eh_recusa({"resposta": "Ligue 199.", "fontes": [], "consta_na_base": True})
    # conteúdo com flag falsa conta como resposta (não esconde alucinação)
    assert not eh_recusa({"resposta": "Lave com sabão.", "fontes": [], "consta_na_base": False})
    assert eh_recusa(None, "Infelizmente não consta.")
    assert not eh_recusa(None, "Ligue 199.")
