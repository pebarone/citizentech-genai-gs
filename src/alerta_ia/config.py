"""Configuração central: caminhos, modelos, hiperparâmetros e semente.

Todo valor pode ser sobreposto por variável de ambiente com prefixo ``ALERTA_``
(ex.: ``ALERTA_TOP_K=5``). Os valores são lidos na importação do módulo.
"""

from __future__ import annotations

import os
import random
from pathlib import Path


def _env(nome: str, padrao, tipo=str):
    """Lê ``ALERTA_<nome>`` do ambiente convertendo para ``tipo``; usa ``padrao`` se ausente."""
    valor = os.environ.get(f"ALERTA_{nome}")
    if valor is None or valor == "":
        return padrao
    if tipo is bool:
        return valor.strip().lower() in {"1", "true", "sim", "yes", "on"}
    return tipo(valor)


def _descobrir_raiz() -> Path:
    if os.environ.get("ALERTA_RAIZ"):
        return Path(os.environ["ALERTA_RAIZ"]).resolve()
    candidata = Path(__file__).resolve().parents[2]
    if (candidata / "pyproject.toml").exists():
        return candidata
    return Path.cwd().resolve()


# ---------------------------------------------------------------- caminhos
RAIZ = _descobrir_raiz()

DIR_BASE = Path(_env("DIR_BASE", RAIZ / "base"))
TRECHOS = DIR_BASE / "trechos.jsonl"
FONTES = DIR_BASE / "fontes.csv"
DIR_INDICE = DIR_BASE / "indice"

DIR_AVALIACAO = Path(_env("DIR_AVALIACAO", RAIZ / "avaliacao"))
TESTE = DIR_AVALIACAO / "teste.jsonl"
DEV = DIR_AVALIACAO / "dev.jsonl"
LIMIAR_JSON = DIR_AVALIACAO / "limiar.json"
BUSCA_JSON = DIR_AVALIACAO / "busca_recall.json"
DIR_RESULTADOS = DIR_AVALIACAO / "resultados"
PLACAR_JSON = DIR_AVALIACAO / "placar.json"
PLACAR_MD = DIR_AVALIACAO / "placar.md"
ERROS_MD = DIR_AVALIACAO / "erros_candidatos.md"
TREINO_LOG = DIR_AVALIACAO / "treino_log.json"
DIR_GRAFICOS = DIR_AVALIACAO / "graficos"

DIR_TREINO = Path(_env("DIR_TREINO", RAIZ / "treino"))
PERGUNTAS_TREINO = DIR_TREINO / "perguntas_treino.jsonl"
DATASET_MONTADO = DIR_TREINO / "dataset_montado.jsonl"
ESTATISTICAS_TREINO = DIR_TREINO / "estatisticas.json"

DIR_MODELOS = Path(_env("DIR_MODELOS", RAIZ / "modelos"))
ADAPTADOR = Path(_env("ADAPTADOR", DIR_MODELOS / "lora-alerta-corrego"))
DIR_CHECKPOINTS = DIR_MODELOS / "_checkpoints"

DIR_WEB_DIST = Path(_env("DIR_WEB_DIST", RAIZ / "web" / "dist"))  # build estático do front (Vite)

# ---------------------------------------------------------------- modelos
MODELO_LLM = _env("MODELO_LLM", "Qwen/Qwen2.5-3B-Instruct")
MODELO_EMB = _env("MODELO_EMB", "intfloat/multilingual-e5-base")
# "auto" = cuda se disponível, senão cpu.
DISPOSITIVO_EMB = _env("DISPOSITIVO_EMB", "auto")
# "auto" = bfloat16 se a GPU suportar, senão float16.
DTYPE_COMPUTACAO = _env("DTYPE_COMPUTACAO", "auto")
# Quantização 4 bits (NF4). "auto" = só quando há CUDA (bitsandbytes exige GPU).
QUANTIZAR_4BIT = _env("QUANTIZAR_4BIT", "auto")

CONFIGURACOES = ("sem_contexto", "rag", "rag_lora")

# ---------------------------------------------------------------- busca e geração
TOP_K = _env("TOP_K", 3, int)
LIMIAR_PADRAO = _env("LIMIAR_PADRAO", 0.80, float)  # só usado se avaliacao/limiar.json não existir
CRITERIO_LIMIAR = _env("CRITERIO_LIMIAR", "recusa_max")  # "recusa_max", "youden" ou "f1"
RECUSA_INDEVIDA_MAX = _env("RECUSA_INDEVIDA_MAX", 0.02, float)  # teto de perguntas com resposta barradas
MAX_NEW_TOKENS = _env("MAX_NEW_TOKENS", 256, int)
# Limite de caracteres por trecho no prompt (os trechos têm ~60-180 palavras; o limite só
# corta casos anômalos). O mesmo valor é usado no treino e na inferência.
MAX_CHARS_TRECHO = _env("MAX_CHARS_TRECHO", 1400, int)
SEMENTE = _env("SEMENTE", 42, int)

# ---------------------------------------------------------------- QLoRA
LORA_R = _env("LORA_R", 16, int)
LORA_ALPHA = _env("LORA_ALPHA", 32, int)
LORA_DROPOUT = _env("LORA_DROPOUT", 0.05, float)
LORA_ALVOS = tuple(_env("LORA_ALVOS", "q_proj,k_proj,v_proj,o_proj").split(","))
TAXA_APRENDIZADO = _env("TAXA_APRENDIZADO", 2e-4, float)
EPOCAS = _env("EPOCAS", 2, float)
# Batch efetivo = BATCH x ACUMULO_GRADIENTE = 8. Em falta de memória (OOM) o treino
# recomeça automaticamente com batch 1 e acúmulo 8 (mesmo batch efetivo).
BATCH = _env("BATCH", 2, int)
ACUMULO_GRADIENTE = _env("ACUMULO_GRADIENTE", 4, int)
BATCH_EFETIVO = BATCH * ACUMULO_GRADIENTE
WARMUP = _env("WARMUP", 0.1, float)
MAX_LEN_TREINO = _env("MAX_LEN_TREINO", 1536, int)
FRACAO_VALIDACAO = _env("FRACAO_VALIDACAO", 0.1, float)

# ---------------------------------------------------------------- API e segurança
CONFIG_API = _env("CONFIG", "rag_lora")
CORS_ORIGENS = [o.strip() for o in _env("CORS_ORIGENS", "").split(",") if o.strip()]
MAX_CHARS_PERGUNTA = _env("MAX_CHARS_PERGUNTA", 500, int)
TAXA_MAX_REQUISICOES = _env("TAXA_MAX_REQUISICOES", 10, int)
TAXA_JANELA_S = _env("TAXA_JANELA_S", 60, float)

TELEFONE_DEFESA_CIVIL = "199"
TELEFONE_BOMBEIROS = "193"


def fixar_sementes(semente: int = SEMENTE) -> None:
    """Fixa as sementes de random, numpy e torch para reprodutibilidade."""
    random.seed(semente)
    os.environ.setdefault("PYTHONHASHSEED", str(semente))
    try:
        import numpy as np

        np.random.seed(semente)
    except ImportError:  # pragma: no cover
        pass
    try:
        import torch

        torch.manual_seed(semente)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(semente)
    except ImportError:  # pragma: no cover
        pass
