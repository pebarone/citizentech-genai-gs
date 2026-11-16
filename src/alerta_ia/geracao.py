"""Geração fundamentada: carga da LLM em 4 bits, adaptador LoRA opcional e pipeline completo.

O ``Pipeline`` junta busca, portão por limiar, prompt e geração, e devolve um dicionário
com tudo o que a avaliação e a API precisam (saída bruta, JSON interpretado, trechos,
similaridades, latência e flags).
"""

from __future__ import annotations

import gc
import json
import logging
import re
import time
from pathlib import Path

from alerta_ia import config, prompts
from alerta_ia.dados import normalizar_texto

log = logging.getLogger(__name__)

CHAVES_SAIDA = ("resposta", "fontes", "consta_na_base")


# ======================================================================
# Interpretação da saída (funções puras)
# ======================================================================
def validar_esquema(obj) -> str | None:
    """Devolve a descrição do problema ou ``None`` se ``obj`` segue o esquema exato."""
    if not isinstance(obj, dict):
        return "a saída não é um objeto JSON"
    if set(obj) != set(CHAVES_SAIDA):
        return f"campos esperados {list(CHAVES_SAIDA)}, recebidos {sorted(obj)}"
    if not isinstance(obj["resposta"], str) or not obj["resposta"].strip():
        return "'resposta' deve ser texto não vazio"
    if not isinstance(obj["fontes"], list) or not all(isinstance(f, str) for f in obj["fontes"]):
        return "'fontes' deve ser lista de textos"
    if not isinstance(obj["consta_na_base"], bool):
        return "'consta_na_base' deve ser booleano"
    return None


def interpretar_estrito(texto: str) -> tuple[dict | None, str | None]:
    """Métrica ESTRITA: ``json.loads`` do texto bruto (após strip) + esquema exato."""
    try:
        obj = json.loads(texto.strip())
    except (json.JSONDecodeError, TypeError) as e:
        return None, f"JSON inválido: {e}"
    erro = validar_esquema(obj)
    return (obj, None) if erro is None else (None, erro)


_CERCA = re.compile(r"```(?:json)?", re.IGNORECASE)


def extrair_primeiro_objeto(texto: str) -> str | None:
    """Primeiro trecho ``{...}`` balanceado, respeitando chaves dentro de strings."""
    inicio = texto.find("{")
    while inicio != -1:
        profundidade, em_string, escape = 0, False, False
        for i in range(inicio, len(texto)):
            c = texto[i]
            if em_string:
                if escape:
                    escape = False
                elif c == "\\":
                    escape = True
                elif c == '"':
                    em_string = False
            elif c == '"':
                em_string = True
            elif c == "{":
                profundidade += 1
            elif c == "}":
                profundidade -= 1
                if profundidade == 0:
                    return texto[inicio : i + 1]
        inicio = texto.find("{", inicio + 1)
    return None


def _para_bool(valor):
    if isinstance(valor, bool):
        return valor
    if isinstance(valor, str) and valor.strip().lower() in {"true", "false"}:
        return valor.strip().lower() == "true"
    return None


def interpretar_tolerante(texto: str) -> dict | None:
    """Degradação elegante: remove cercas, pega o primeiro objeto e normaliza os tipos.

    Devolve ``None`` se não houver objeto com o campo ``resposta``.
    """
    candidato = extrair_primeiro_objeto(_CERCA.sub("", texto or ""))
    if candidato is None:
        return None
    try:
        obj = json.loads(candidato)
    except json.JSONDecodeError:
        return None
    if not isinstance(obj, dict) or not isinstance(obj.get("resposta"), str):
        return None
    fontes = obj.get("fontes", [])
    if isinstance(fontes, str):
        fontes = [fontes]
    if not isinstance(fontes, list):
        fontes = []
    consta = _para_bool(obj.get("consta_na_base"))
    resposta = obj["resposta"].strip()
    if consta is None:
        consta = not normalizar_texto(resposta).startswith("nao consta")
    return {"resposta": resposta, "fontes": [str(f) for f in fontes], "consta_na_base": consta}


def verificar_citacoes(fontes: list[str], ids_contexto: list[str]) -> tuple[list[str], list[str]]:
    """Separa ids citados em válidos (estavam no contexto) e inválidos (inventados/fora)."""
    contexto = set(ids_contexto)
    validas, invalidas = [], []
    for f in fontes:
        (validas if f in contexto else invalidas).append(f)
    return validas, invalidas


def eh_recusa(obj: dict | None, texto_bruto: str = "") -> bool:
    """Recusa = o TEXTO da resposta diz "não consta" (no início) ou "não consta na base".

    Decide-se pelo texto, e não pela flag ``consta_na_base``: sem contexto, o modelo às vezes
    responde com conteúdo e marca ``consta_na_base: false``; contar isso como recusa
    esconderia alucinações da linha de base.
    """
    texto = normalizar_texto(obj.get("resposta", "") if obj is not None else (texto_bruto or ""))
    if obj is None:
        return "nao consta" in texto
    return texto.startswith("nao consta") or "nao consta na base" in texto


# ======================================================================
# LLM (exige transformers/torch; GPU recomendada)
# ======================================================================
def resolver_dtype():
    import torch

    if config.DTYPE_COMPUTACAO == "float16":
        return torch.float16
    if config.DTYPE_COMPUTACAO == "bfloat16":
        return torch.bfloat16
    if torch.cuda.is_available() and torch.cuda.is_bf16_supported():
        return torch.bfloat16
    return torch.float16 if torch.cuda.is_available() else torch.float32


def usar_4bit() -> bool:
    import torch

    if config.QUANTIZAR_4BIT == "auto":
        return torch.cuda.is_available()
    return config.QUANTIZAR_4BIT.lower() in {"1", "true", "sim"}


def carregar_llm(modelo_id: str | None = None):
    """Carrega tokenizer e modelo; em GPU usa NF4 4 bits com dupla quantização."""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

    modelo_id = modelo_id or config.MODELO_LLM
    dtype = resolver_dtype()
    tokenizer = AutoTokenizer.from_pretrained(modelo_id)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    kwargs = {"dtype": dtype}
    if usar_4bit():
        kwargs["quantization_config"] = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=dtype,
        )
        kwargs["device_map"] = {"": 0}
    elif torch.cuda.is_available():
        kwargs["device_map"] = {"": 0}
    modelo = AutoModelForCausalLM.from_pretrained(modelo_id, **kwargs)
    return modelo, tokenizer


def liberar_memoria() -> None:
    gc.collect()
    try:
        import torch

        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    except ImportError:  # pragma: no cover
        pass


class Gerador:
    """LLM base (opcionalmente com adaptador LoRA) com decodificação gulosa."""

    def __init__(self, modelo_id: str | None = None, adaptador: str | Path | None = None):
        self.modelo_id = modelo_id or config.MODELO_LLM
        self.adaptador = str(adaptador) if adaptador else None
        config.fixar_sementes()
        self.modelo, self.tokenizer = carregar_llm(self.modelo_id)
        if self.adaptador:
            from peft import PeftModel

            self.modelo = PeftModel.from_pretrained(self.modelo, self.adaptador)
        self.modelo.eval()

    def gerar(self, mensagens: list[dict], max_new_tokens: int | None = None) -> tuple[str, int]:
        import torch

        texto = self.tokenizer.apply_chat_template(mensagens, tokenize=False, add_generation_prompt=True)
        entrada = self.tokenizer(texto, return_tensors="pt").to(self.modelo.device)
        with torch.inference_mode():
            saida = self.modelo.generate(
                **entrada,
                max_new_tokens=max_new_tokens or config.MAX_NEW_TOKENS,
                do_sample=False,
                temperature=None,
                top_p=None,
                top_k=None,
                repetition_penalty=1.0,
                pad_token_id=self.tokenizer.pad_token_id,
            )
        novos = saida[0, entrada["input_ids"].shape[1] :]
        return self.tokenizer.decode(novos, skip_special_tokens=True), int(novos.shape[0])

    def liberar(self) -> None:
        self.modelo = None
        self.tokenizer = None
        liberar_memoria()


# ======================================================================
# Pipeline completo
# ======================================================================
class Pipeline:
    """Busca + portão por limiar + prompt + geração, para uma das três configurações."""

    def __init__(
        self,
        configuracao: str,
        gerador,
        buscador=None,
        limiar: float | None = None,
        usar_limiar: bool = True,
        top_k: int | None = None,
    ):
        if configuracao not in config.CONFIGURACOES:
            raise ValueError(f"configuração desconhecida: {configuracao}")
        if configuracao != "sem_contexto" and buscador is None:
            raise ValueError("configurações com RAG exigem um buscador")
        self.configuracao = configuracao
        self.gerador = gerador
        self.buscador = buscador
        self.limiar = limiar
        self.usar_limiar = usar_limiar and configuracao != "sem_contexto" and limiar is not None
        self.top_k = top_k or config.TOP_K

    def info(self) -> dict:
        return {
            "configuracao": self.configuracao,
            "modelo": getattr(self.gerador, "modelo_id", None),
            "adaptador": Path(self.gerador.adaptador).name if getattr(self.gerador, "adaptador", None) else None,
            "modelo_embeddings": getattr(self.buscador, "modelo_id", None),
            "n_trechos": len(self.buscador.ids) if self.buscador is not None else 0,
            "top_k": self.top_k if self.configuracao != "sem_contexto" else 0,
            "limiar": self.limiar if self.usar_limiar else None,
        }

    def responder(self, pergunta: str) -> dict:
        t0 = time.perf_counter()
        trechos: list[dict] = []
        top1 = None
        recusa_por_limiar = False
        if self.configuracao != "sem_contexto":
            trechos = self.buscador.buscar(pergunta, self.top_k)
            top1 = trechos[0]["similaridade"] if trechos else 0.0
            recusa_por_limiar = self.usar_limiar and top1 < self.limiar

        if recusa_por_limiar:
            bruto, n_tokens = prompts.recusa_json(), 0
        else:
            contexto = None if self.configuracao == "sem_contexto" else trechos
            bruto, n_tokens = self.gerador.gerar(prompts.montar_mensagens(pergunta, contexto, config.MAX_CHARS_TRECHO))

        estrito, erro_json = interpretar_estrito(bruto)
        obj = estrito if estrito is not None else interpretar_tolerante(bruto)
        fontes = obj["fontes"] if obj else []
        validas, invalidas = verificar_citacoes(fontes, [t["id"] for t in trechos])
        recusa = eh_recusa(obj, bruto)
        return {
            "pergunta": pergunta,
            "configuracao": self.configuracao,
            "modelo": getattr(self.gerador, "modelo_id", None),
            "adaptador": Path(self.gerador.adaptador).name if getattr(self.gerador, "adaptador", None) else None,
            "saida_bruta": bruto,
            "json_valido_estrito": estrito is not None,
            "erro_json": erro_json,
            "json": obj,
            "resposta": obj["resposta"] if obj else bruto.strip(),
            "fontes": fontes,
            "fontes_validas": validas,
            "citacoes_invalidas": invalidas,
            "consta_na_base": bool(obj["consta_na_base"]) if obj else False,
            "recusa": recusa,
            "recusa_por_limiar": recusa_por_limiar,
            "chamou_llm": not recusa_por_limiar,
            "trechos": [
                {k: t[k] for k in ("id", "fonte_id", "titulo", "secao", "url", "texto", "similaridade")}
                for t in trechos
            ],
            "similaridade_top1": top1,
            "limiar": self.limiar if self.usar_limiar else None,
            "usou_limiar": self.usar_limiar,
            "tokens_gerados": n_tokens,
            "latencia_ms": round((time.perf_counter() - t0) * 1000, 1),
        }

    def liberar(self) -> None:
        if hasattr(self.gerador, "liberar"):
            self.gerador.liberar()


def adaptador_disponivel(caminho: str | Path | None = None) -> bool:
    return (Path(caminho or config.ADAPTADOR) / "adapter_config.json").exists()


def criar_pipeline(configuracao: str, usar_limiar: bool = True, buscador=None) -> Pipeline:
    """Monta o pipeline real (carrega modelos). ``rag_lora`` exige o adaptador treinado."""
    from alerta_ia import busca

    adaptador = None
    if configuracao == "rag_lora":
        if not adaptador_disponivel():
            raise FileNotFoundError(f"adaptador LoRA não encontrado em {config.ADAPTADOR}")
        adaptador = config.ADAPTADOR
    if configuracao != "sem_contexto" and buscador is None:
        buscador = busca.Buscador()
    limiar = busca.carregar_limiar() if configuracao != "sem_contexto" else None
    gerador = Gerador(adaptador=adaptador)
    return Pipeline(configuracao, gerador, buscador if configuracao != "sem_contexto" else None,
                    limiar=limiar, usar_limiar=usar_limiar)
