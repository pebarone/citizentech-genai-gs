import pytest

from alerta_ia import seguranca


def test_mascarar_pii():
    texto = ("Meu CPF é 123.456.789-09, tel (11) 98765-4321, outro 11987654321, "
             "e-mail maria.silva@exemplo.com.br; ligue 199 ou 193. CEP 08250-000.")
    m = seguranca.mascarar_pii(texto)
    for dado in ["123.456.789-09", "98765-4321", "11987654321", "maria.silva@exemplo.com.br"]:
        assert dado not in m
    assert "[CPF]" in m and "[TELEFONE]" in m and "[EMAIL]" in m
    assert "199" in m and "193" in m and "08250-000" in m


def test_cpf_sem_pontuacao():
    assert seguranca.mascarar_pii("cpf 12345678909") == "cpf [CPF]"


def test_validar_pergunta():
    assert seguranca.validar_pergunta("  como   faço?  ") == "como faço?"
    with pytest.raises(seguranca.PerguntaInvalida):
        seguranca.validar_pergunta(" ")
    with pytest.raises(seguranca.PerguntaInvalida, match="longa"):
        seguranca.validar_pergunta("a" * 501, max_chars=500)


def test_limitador_taxa_janela_e_hash():
    agora = [0.0]
    lim = seguranca.LimitadorTaxa(max_requisicoes=2, janela_s=60, sal="s", relogio=lambda: agora[0])
    assert lim.permitir("10.0.0.1") and lim.permitir("10.0.0.1")
    assert not lim.permitir("10.0.0.1")
    assert lim.permitir("10.0.0.2")  # outro cliente
    agora[0] = 61
    assert lim.permitir("10.0.0.1")  # janela passou
    assert all("10.0.0" not in k for k in lim.chaves_guardadas)  # nunca guarda IP em claro


def test_sal_aleatorio_muda_hash():
    a, b = seguranca.LimitadorTaxa(), seguranca.LimitadorTaxa()
    assert a.chave("1.2.3.4") != b.chave("1.2.3.4")


@pytest.mark.parametrize("texto", [
    "Socorro, a água está entrando em casa!",
    "Estamos presos no segundo andar",
    "Tem criança na água",
    "não consigo sair de casa",
    "fio caído na rua alagada",
])
def test_detecta_emergencia(texto):
    assert seguranca.detectar_emergencia(texto)


@pytest.mark.parametrize("texto", [
    "Como me cadastro para receber SMS?",
    "O que levar na mochila de emergência?",
    "Como limpar a casa depois da enchente?",
])
def test_sem_emergencia(texto):
    assert not seguranca.detectar_emergencia(texto)
