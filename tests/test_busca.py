import pytest

from alerta_ia.busca import (
    escolher_limiar,
    hash_indice,
    justificativa_limiar,
    metricas_recuperacao,
    texto_consulta,
    texto_passagem,
    varrer_limiar,
)


def test_metricas_recuperacao():
    ranques = [["a", "b", "c"], ["x", "a", "c"], ["x", "y", "z", "a"]]
    relevantes = [["a"], ["a", "c"], ["a"]]
    m = metricas_recuperacao(ranques, relevantes)
    assert m["n"] == 3
    assert m["recall@1"] == pytest.approx(1 / 3)
    assert m["recall@3"] == pytest.approx(2 / 3)
    assert m["mrr"] == pytest.approx((1 + 1 / 2 + 1 / 4) / 3)


def test_metricas_vazias():
    assert metricas_recuperacao([], [])["recall@1"] is None


def test_prefixos_e5(trechos):
    assert texto_consulta(" oi ") == "query: oi"
    assert texto_passagem(trechos[0]).startswith("passage: Guia de Enchentes")


def test_hash_muda_com_conteudo(trechos):
    h1 = hash_indice(trechos, "m")
    alterado = [dict(t) for t in trechos]
    alterado[0]["texto"] += "!"
    assert h1 != hash_indice(alterado, "m")
    assert h1 != hash_indice(trechos, "outro-modelo")
    assert h1 == hash_indice([dict(t) for t in trechos], "m")


def test_varredura_separavel():
    scores = [0.90, 0.88, 0.86, 0.80, 0.78]
    rotulos = [True, True, True, False, False]
    v = varrer_limiar(scores, rotulos, limiares=[0.75, 0.79, 0.83, 0.87, 0.95])
    por_lim = {round(l["limiar"], 2): l for l in v}
    assert por_lim[0.75]["sensibilidade"] == 1 and por_lim[0.75]["especificidade"] == 0
    assert por_lim[0.83]["youden"] == 1 and por_lim[0.83]["f1"] == 1
    assert por_lim[0.87]["recusa_indevida_pelo_limiar"] == pytest.approx(1 / 3)
    assert por_lim[0.95]["recusa_indevida_pelo_limiar"] == 1
    assert por_lim[0.79]["nao_consta_que_passam"] == 0.5
    assert escolher_limiar(v)["limiar"] == 0.83


def test_empate_escolhe_mediana_do_plato():
    scores = [0.9, 0.8]
    rotulos = [True, False]
    v = varrer_limiar(scores, rotulos, limiares=[0.81, 0.83, 0.85, 0.87, 0.89])
    assert escolher_limiar(v, "youden")["limiar"] == 0.85
    assert escolher_limiar(v, "f1")["limiar"] == 0.85


def test_grade_automatica_e_justificativa():
    scores = [0.91, 0.87, 0.85, 0.84, 0.82, 0.86]
    rotulos = [True, True, True, False, False, False]
    v = varrer_limiar(scores, rotulos)
    assert v[0]["limiar"] < min(scores) and v[-1]["limiar"] > max(scores)
    esc = escolher_limiar(v)
    texto = justificativa_limiar(esc, v, "youden", 3, 3)
    assert "Youden" in texto and "Troca" in texto


def test_criterio_invalido():
    with pytest.raises(ValueError):
        escolher_limiar(varrer_limiar([0.5], [True], [0.4]), "acuracia")
