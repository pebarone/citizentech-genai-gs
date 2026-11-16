"""Proteções de privacidade (LGPD) e de uso: mascaramento, limites, taxa e emergência."""

from __future__ import annotations

import hashlib
import re
import secrets
import threading
import time
from collections import deque

from alerta_ia import config
from alerta_ia.dados import normalizar_texto

# ---------------------------------------------------------------- dados pessoais
_EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
_CPF = re.compile(r"(?<!\d)\d{3}\.?\d{3}\.?\d{3}-?\d{2}(?!\d)")
_TELEFONE = re.compile(r"(?<!\d)(?:\+?55[\s.-]?)?(?:\(?\d{2}\)?[\s.-]?)?9?\d{4}[\s.-]?\d{4}(?!\d)")


def mascarar_pii(texto: str) -> str:
    """Substitui e-mail, CPF e telefone por marcadores. Use em QUALQUER texto que vá para log."""
    texto = _EMAIL.sub("[EMAIL]", texto)
    texto = _CPF.sub("[CPF]", texto)
    return _TELEFONE.sub("[TELEFONE]", texto)


def hash_texto(texto: str, sal: str) -> str:
    """Hash curto e salgado (permite correlacionar repetições sem guardar o conteúdo)."""
    return hashlib.sha256((sal + texto).encode("utf-8")).hexdigest()[:16]


class PerguntaInvalida(ValueError):
    pass


def validar_pergunta(texto: str, max_chars: int | None = None) -> str:
    """Normaliza espaços e aplica o limite de tamanho; lança ``PerguntaInvalida``."""
    max_chars = max_chars or config.MAX_CHARS_PERGUNTA
    if not isinstance(texto, str):
        raise PerguntaInvalida("A pergunta precisa ser um texto.")
    limpo = re.sub(r"\s+", " ", texto).strip()
    if len(limpo) < 3:
        raise PerguntaInvalida("Escreva sua pergunta.")
    if len(limpo) > max_chars:
        raise PerguntaInvalida(f"A pergunta é longa demais. Use até {max_chars} caracteres.")
    return limpo


# ---------------------------------------------------------------- limitador de taxa
class LimitadorTaxa:
    """Janela deslizante em memória por cliente. Guarda só o hash salgado do IP, nunca o IP.

    O sal é aleatório por processo (não persistido), então os hashes não podem ser
    revertidos nem correlacionados entre reinícios.
    """

    def __init__(self, max_requisicoes: int | None = None, janela_s: float | None = None, sal: str | None = None,
                 relogio=time.monotonic):
        self.max = max_requisicoes or config.TAXA_MAX_REQUISICOES
        self.janela = janela_s or config.TAXA_JANELA_S
        self._sal = sal or secrets.token_hex(16)
        self._relogio = relogio
        self._registros: dict[str, deque] = {}
        self._lock = threading.Lock()

    def chave(self, ip: str) -> str:
        return hash_texto(ip or "desconhecido", self._sal)

    def permitir(self, ip: str) -> bool:
        agora = self._relogio()
        chave = self.chave(ip)
        with self._lock:
            fila = self._registros.setdefault(chave, deque())
            while fila and agora - fila[0] >= self.janela:
                fila.popleft()
            if len(fila) >= self.max:
                return False
            fila.append(agora)
            if len(self._registros) > 10_000:  # limpeza ocasional de clientes inativos
                for k in [k for k, f in self._registros.items() if not f or agora - f[-1] >= self.janela]:
                    del self._registros[k]
            return True

    @property
    def chaves_guardadas(self) -> list[str]:
        return list(self._registros)


# ---------------------------------------------------------------- emergência
_EMERGENCIA = [
    r"agua (esta )?(entrando|invadindo|subindo)",
    r"(entrando|entrou|invadiu|invadindo) agua",
    r"\bpres[oa]s?\b",
    r"\bilhad[oa]s?\b",
    r"\bsocorro\b",
    r"\barrastad[oa]s?\b",
    r"\bafogando\b",
    r"\bsoterrad[oa]s?\b",
    r"\bdesaband[oa]\b|\bdesabou\b|\bdesabamento\b",
    r"nao (consigo|conseguimos|da para|da pra) sair",
    r"\b(socorr[ae]|ajuda) urgente\b|\burgente\b",
    r"\b(fio|fiacao)( eletric[oa])? (caido|na agua)\b|choque eletrico",
    r"crianca na agua|alguem na agua|pessoa na agua",
]
_EMERGENCIA_RE = re.compile("|".join(f"(?:{p})" for p in _EMERGENCIA))

AVISO_EMERGENCIA = (
    "Se você ou alguém está em perigo agora, ligue já para 199 (Defesa Civil) ou 193 (Corpo de Bombeiros). "
    "Vá para um lugar alto e seguro, longe da água e de fios elétricos. "
    "Este assistente apenas orienta: quem decide e faz o resgate são as equipes de emergência."
)


def detectar_emergencia(texto: str) -> bool:
    """Detecção simples por palavras-chave (sem acento). Não substitui avaliação humana."""
    return bool(_EMERGENCIA_RE.search(normalizar_texto(texto or "")))
