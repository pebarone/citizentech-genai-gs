"""API HTTP do assistente Alerta Córrego (FastAPI).

Subir localmente (sem log de acesso, que registraria IPs)::

    python -m alerta_ia.api
    # ou: uvicorn alerta_ia.api:app --host 127.0.0.1 --port 8000 --no-access-log

Privacidade: o texto da pergunta não é gravado em lugar nenhum. O log estruturado
contém só hash salgado, tamanho, métricas e resultado. O IP só é usado, como hash
salgado em memória, pelo limitador de taxa.
"""

from __future__ import annotations

import json
import logging
import secrets
import threading
import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from alerta_ia import config, seguranca
from alerta_ia.prompts import RECUSA_PADRAO

log = logging.getLogger("alerta_ia.api")

RESPOSTA_DEGRADADA = (
    "Não consegui formular uma resposta confiável agora. Tente reformular a pergunta. "
    "Em caso de risco, ligue 199 (Defesa Civil) ou 193 (Corpo de Bombeiros)."
)
PRIVACIDADE = (
    "Não pedimos nem guardamos dados pessoais. O texto da pergunta não é armazenado; "
    "os registros técnicos guardam apenas métricas anônimas."
)


PAGINA_SEM_FRONT = """<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Alerta Córrego - API</title></head>
<body style="font-family:system-ui,sans-serif;max-width:640px;margin:40px auto;padding:0 16px;line-height:1.5">
<h1>Alerta Córrego - API no ar</h1>
<p>O front-end ainda não foi gerado (pasta <code>web/dist</code> ausente). Rode o build do front ou use a
documentação interativa da API em <a href="/docs">/docs</a>.</p>
<p>Em perigo, ligue <strong>199</strong> (Defesa Civil) ou <strong>193</strong> (Corpo de Bombeiros).</p>
</body></html>"""


class Pergunta(BaseModel):
    pergunta: str = Field(..., max_length=5000, description="Dúvida do morador em texto livre")


def carregar_pipeline_padrao():
    """Pipeline real conforme ``ALERTA_CONFIG``; ``rag_lora`` cai para ``rag`` sem adaptador."""
    from alerta_ia.geracao import adaptador_disponivel, criar_pipeline

    cfg = config.CONFIG_API
    if cfg not in config.CONFIGURACOES:
        raise ValueError(f"ALERTA_CONFIG inválida: {cfg}")
    if cfg == "rag_lora" and not adaptador_disponivel():
        log.warning("adaptador LoRA ausente; usando configuração 'rag'")
        cfg = "rag"
    pipeline = criar_pipeline(cfg)
    if pipeline.buscador is not None:
        pipeline.buscador.buscar("aquecimento", 1)  # carrega o modelo de embeddings já no startup
    return pipeline


def _info_publica(pipeline) -> dict:
    """Info do pipeline sem caminhos locais (só o nome da pasta do adaptador)."""
    if pipeline is None:
        return {}
    info = dict(pipeline.info())
    if info.get("adaptador"):
        info["adaptador"] = Path(info["adaptador"]).name
    return info


def _registrar(evento: dict) -> None:
    log.info(json.dumps(evento, ensure_ascii=False))


def montar_resposta(saida: dict, aviso: str | None, latencia_ms: float, info: dict) -> dict:
    """Converte a saída do pipeline no contrato público da API."""
    if saida["json"] is None:
        resposta, consta = RESPOSTA_DEGRADADA, False
    else:
        resposta, consta = saida["resposta"], bool(saida["consta_na_base"]) and not saida["recusa"]
        if not consta and not saida["recusa"]:
            # o próprio modelo marcou que não está na base, mas escreveu conteúdo: não exibimos
            # resposta sem fundamento; devolvemos a recusa padrão.
            resposta = RECUSA_PADRAO
    fontes = []
    if consta:
        por_id = {t["id"]: t for t in saida["trechos"]}
        for fid in dict.fromkeys(saida["fontes_validas"]):
            t = por_id[fid]
            fontes.append({"id": t["id"], "titulo": t["titulo"], "secao": t["secao"], "url": t["url"],
                           "trecho": t["texto"], "similaridade": round(float(t["similaridade"]), 4)})
    return {
        "resposta": resposta,
        "consta_na_base": consta,
        "fontes": fontes,
        "explicacao": {
            "limiar": saida.get("limiar"),
            "similaridade_top1": None if saida.get("similaridade_top1") is None
            else round(float(saida["similaridade_top1"]), 4),
            "recusa_por_limiar": bool(saida.get("recusa_por_limiar")),
            "configuracao": info.get("configuracao"),
            "modelo": info.get("modelo"),
            "citacoes_invalidas": list(saida.get("citacoes_invalidas", [])),
        },
        "aviso_emergencia": aviso,
        "latencia_ms": round(latencia_ms, 1),
    }


def criar_app(pipeline=None, fabrica=None, limitador: seguranca.LimitadorTaxa | None = None) -> FastAPI:
    """Cria a aplicação. ``pipeline`` (pronto) ou ``fabrica`` (chamada no startup) permitem injeção nos testes."""

    @asynccontextmanager
    async def ciclo_de_vida(app: FastAPI):
        if app.state.pipeline is None:
            try:
                app.state.pipeline = (fabrica or carregar_pipeline_padrao)()
            except Exception as e:  # o processo sobe, mas /readyz indica indisponível
                log.error("falha ao carregar o pipeline: %s", type(e).__name__)
        yield
        if app.state.pipeline is not None and hasattr(app.state.pipeline, "liberar"):
            app.state.pipeline.liberar()

    app = FastAPI(title="Alerta Córrego - assistente", version="1.0.0", lifespan=ciclo_de_vida)
    app.state.pipeline = pipeline
    app.state.lock = threading.Lock()
    app.state.limitador = limitador or seguranca.LimitadorTaxa()
    app.state.sal_log = secrets.token_hex(16)

    if config.CORS_ORIGENS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=config.CORS_ORIGENS,
            allow_methods=["GET", "POST"],
            allow_headers=["Content-Type"],
        )

    @app.middleware("http")
    async def cabecalhos_seguranca(request: Request, call_next):
        resposta = await call_next(request)
        resposta.headers["X-Content-Type-Options"] = "nosniff"
        resposta.headers["Referrer-Policy"] = "no-referrer"
        resposta.headers["X-Frame-Options"] = "DENY"
        if request.url.path.startswith("/api/"):
            resposta.headers["Cache-Control"] = "no-store"
        if request.url.path == "/":
            resposta.headers["Content-Security-Policy"] = (
                "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; "
                "img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'"
            )
        return resposta

    @app.exception_handler(Exception)
    async def erro_interno(request: Request, exc: Exception):
        log.error("erro interno em %s: %s", request.url.path, type(exc).__name__)
        return JSONResponse(status_code=500, content={"detail": "Erro interno. Tente novamente em instantes."})

    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}

    @app.get("/readyz")
    def readyz():
        if app.state.pipeline is None:
            return JSONResponse(status_code=503, content={"status": "carregando ou indisponível"})
        return {"status": "pronto"}

    @app.get("/api/v1/info")
    def info():
        p = app.state.pipeline
        return {
            "servico": "Alerta Córrego",
            "pronto": p is not None,
            **_info_publica(p),
            "telefones": {"defesa_civil": config.TELEFONE_DEFESA_CIVIL, "bombeiros": config.TELEFONE_BOMBEIROS},
            "max_caracteres_pergunta": config.MAX_CHARS_PERGUNTA,
            "privacidade": PRIVACIDADE,
        }

    @app.post("/api/v1/assistente/perguntar")
    def perguntar(corpo: Pergunta, request: Request):
        inicio = time.perf_counter()
        ip = request.client.host if request.client else ""
        if not app.state.limitador.permitir(ip):
            raise HTTPException(status_code=429, detail="Muitas perguntas em pouco tempo. Aguarde um minuto.")
        try:
            pergunta = seguranca.validar_pergunta(corpo.pergunta)
        except seguranca.PerguntaInvalida as e:
            raise HTTPException(status_code=422, detail=str(e)) from None
        pipeline = app.state.pipeline
        if pipeline is None:
            raise HTTPException(status_code=503, detail="O assistente está iniciando. Tente de novo em instantes.")

        aviso = seguranca.AVISO_EMERGENCIA if seguranca.detectar_emergencia(pergunta) else None
        with app.state.lock:  # uma geração por vez na GPU
            saida = pipeline.responder(pergunta)
        latencia = (time.perf_counter() - inicio) * 1000
        corpo_resp = montar_resposta(saida, aviso, latencia, pipeline.info())
        _registrar(
            {
                "evento": "pergunta",
                "hash": seguranca.hash_texto(pergunta, app.state.sal_log),
                "tamanho": len(pergunta),
                "consta_na_base": corpo_resp["consta_na_base"],
                "recusa_por_limiar": corpo_resp["explicacao"]["recusa_por_limiar"],
                "similaridade_top1": corpo_resp["explicacao"]["similaridade_top1"],
                "n_fontes": len(corpo_resp["fontes"]),
                "json_valido": bool(saida.get("json_valido_estrito")),
                "emergencia": aviso is not None,
                "latencia_ms": corpo_resp["latencia_ms"],
            }
        )
        return corpo_resp

    dist = config.DIR_WEB_DIST
    if (dist / "assets").is_dir():
        app.mount("/assets", StaticFiles(directory=dist / "assets"), name="assets")

    @app.get("/", include_in_schema=False)
    def pagina():
        indice = dist / "index.html"
        if indice.exists():
            return FileResponse(indice, media_type="text/html; charset=utf-8")
        return HTMLResponse(PAGINA_SEM_FRONT)

    @app.get("/{nome}", include_in_schema=False)
    def arquivo_raiz(nome: str):
        """Arquivos soltos do build (favicon, manifest...). Só nomes simples dentro de web/dist."""
        alvo = (dist / nome).resolve()
        if dist.is_dir() and alvo.parent == dist.resolve() and alvo.is_file() and nome != "index.html":
            return FileResponse(alvo)
        raise HTTPException(status_code=404, detail="Não encontrado.")

    return app


app = criar_app()


def _main() -> None:
    import os

    import uvicorn

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    uvicorn.run(app, host=os.environ.get("ALERTA_HOST", "127.0.0.1"), port=int(os.environ.get("ALERTA_PORTA", "8000")),
                access_log=False)


if __name__ == "__main__":
    _main()
