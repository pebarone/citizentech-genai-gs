# API do Alerta Córrego (imagem enxuta, usuário não-root).
#
# GPU (padrão, CUDA 12.4; exige NVIDIA Container Toolkit):
#   docker build -t alerta-corrego .
#   docker run --gpus all -p 8000:8000 -v %USERPROFILE%\.cache\huggingface:/home/app/.cache/huggingface alerta-corrego
# CPU (sem quantização 4 bits; bem mais lento):
#   docker build --build-arg TORCH_INDEX=https://download.pytorch.org/whl/cpu -t alerta-corrego:cpu .
#
# Os pesos dos modelos não entram na imagem: monte o cache do Hugging Face já baixado.
# O front-end entra pronto (web/dist), sem etapa Node.
FROM python:3.11-slim

ARG TORCH_INDEX=https://download.pytorch.org/whl/cu124
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HUB_OFFLINE=1 \
    ALERTA_RAIZ=/app \
    ALERTA_HOST=0.0.0.0 \
    ALERTA_PORTA=8000

RUN useradd --create-home --uid 1000 app
WORKDIR /app

RUN pip install torch==2.6.0 --index-url ${TORCH_INDEX} \
 && pip install transformers==4.57.6 peft==0.21.3 bitsandbytes==0.50.2 accelerate==1.15.0 \
        sentence-transformers==5.7.0 numpy==2.4.6 fastapi==0.163.1 uvicorn==0.54.0 pydantic==2.14.3

COPY pyproject.toml ./
COPY src/ src/
RUN pip install --no-deps .

COPY base/trechos.jsonl base/fontes.csv base/
COPY avaliacao/limiar.json avaliacao/
COPY modelos/lora-alerta-corrego/ modelos/lora-alerta-corrego/
COPY web/dist/ web/dist/

RUN mkdir -p base/indice && chown -R app:app /app
USER app

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=180s CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/readyz').status==200 else 1)"
CMD ["python", "-m", "alerta_ia.api"]
