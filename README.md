# Alerta Córrego · Assistente (Generative AI for Engineering)

> Global Solution 2026.2, FIAP, Engenharia de Software 4º ano. Componente **Inteligência** do MVP
> [Alerta Córrego](https://github.com/pebarone/citizentech-devops-gs). Tema: **segurança**.

LLM local (Qwen2.5-3B, 4 bits) que responde dúvidas de moradores sobre enchentes **só com base em
documentos oficiais**, em JSON, citando a fonte e respondendo "não consta" quando a base não cobre.

**Relatório completo:** [docs/RELATORIO.md](docs/RELATORIO.md) · **Vídeo:** [demonstração no YouTube](https://www.youtube.com/watch?v=P-Zmz2omcuM)

| Nome completo | RM |
|---|---|
| João Pedro de Albuquerque Oliveira | 551579 |
| Pedro Augusto Carneiro Barone Bomfim | 99781 |
| Matheus Augusto Santos Rego | 551466 |

## Resultado (60 perguntas de teste, mesma decodificação nas três configurações)

| Configuração | Acerto | Fatos cobertos | Recusa indevida | Recusa correta ("não consta") | Citação correta | JSON válido |
|---|---|---|---|---|---|---|
| Sem contexto | 0,0% | 4,4% | 81,0% | 100% | 0,0% | 100% |
| RAG simples | 52,4% | 57,1% | 28,6% | 100% | 71,4% | 100% |
| RAG + LoRA | 52,4% | 67,5% | 7,1% | 100% | 85,7% | 100% |

Busca: **recall@1 83,3%**, **recall@3 92,9%**, limiar de similaridade **0,815**.
Placar completo em [avaliacao/placar.md](avaliacao/placar.md); interpretação e os 5 erros no
[relatório](docs/RELATORIO.md#5-performance-das-configurações).

## Onde está cada item da avaliação

| # | Critério | Onde |
|---|---|---|
| 01 | Tarefa e casos de teste com gabarito e "não consta" | [avaliacao/teste.jsonl](avaliacao/teste.jsonl), [notebook 01](notebooks/01_tarefa_base_e_testes.ipynb) |
| 02 | Base de conhecimento em trechos com fonte | [base/trechos.jsonl](base/trechos.jsonl), [base/fontes.csv](base/fontes.csv), [base/README.md](base/README.md) |
| 03 | recall@1, recall@3 e limiar justificado | [notebook 02](notebooks/02_busca_recall_e_limiar.ipynb), [avaliacao/limiar.json](avaliacao/limiar.json) |
| 04 | Geração fundamentada: JSON, citação e recusa | [notebook 03](notebooks/03_geracao_fundamentada.ipynb), [src/alerta_ia/prompts.py](src/alerta_ia/prompts.py), [geracao.py](src/alerta_ia/geracao.py) |
| 05 | LoRA comparado ao RAG simples | [notebook 04](notebooks/04_especializacao_lora.ipynb), [treino/README.md](treino/README.md), [avaliacao/treino_log.json](avaliacao/treino_log.json) |
| 06 | Placar das três configurações | [notebook 05](notebooks/05_placar_e_erros.ipynb), [avaliacao/placar.md](avaliacao/placar.md) |
| 07 | 5 erros reais com correção | [relatório, seção 6](docs/RELATORIO.md#6-cinco-erros-reais-causa-e-correção) |
| 08 | Reprodutibilidade | esta página |

## Estrutura

```
base/         trechos, fontes, textos brutos e validador
treino/       500 perguntas de treino, dataset montado e estatísticas
avaliacao/    teste, dev, limiar, resultados por pergunta e placar
notebooks/    5 notebooks com as saídas salvas
src/alerta_ia busca, prompts, geração, treino LoRA, avaliação, segurança e API
modelos/      adaptador LoRA treinado (28 MB)
web/          chat (React + shadcn/ui); build pronto em web/dist
docs/         relatório
```

## Como reproduzir

Requisitos: Python 3.11 e GPU NVIDIA com 8 GB (testado em RTX 4060 Ti, Windows). Os modelos são baixados
do Hugging Face sem autenticação.

```bash
python -m venv .venv
```
```bash
.venv\Scripts\pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cu124
```
```bash
.venv\Scripts\pip install -r requirements.txt -e .
```

| Etapa | Comando (`.venv\Scripts\python -m ...`) | Tempo |
|---|---|---|
| Validar base e conjuntos | `python base\validar_base.py` | segundos |
| Medir recall | `alerta_ia.busca avaliar` | < 1 min |
| Calibrar limiar | `alerta_ia.busca calibrar` | < 1 min |
| Treinar LoRA (opcional, adaptador já incluso) | `alerta_ia.treino_lora` | ~25 min |
| Avaliar | `alerta_ia.avaliacao --config sem_contexto` (e `rag`, `rag_lora`) | 4 a 8 min cada |
| Placar | `alerta_ia.avaliacao --placar` | segundos |
| Testes | `pytest -q` | segundos |
| API + chat | `alerta_ia.api` e abrir http://127.0.0.1:8000 | carga ~20 s |

Rode uma etapa de GPU por vez. Os notebooks leem os resultados gravados (`REEXECUTAR = False`).

## API

`POST /api/v1/assistente/perguntar` com `{"pergunta": "..."}` devolve a resposta, as fontes (id, título,
URL, trecho e similaridade) e a explicação da decisão (limiar, similaridade, configuração).
Também: `GET /api/v1/info`, `/healthz`, `/readyz` e documentação em `/docs`.

Segurança e LGPD: o texto da pergunta não é armazenado, o log guarda só hash e métricas, há limite de
tamanho e de taxa, e os trechos entram no prompt marcados como dados. Detalhes no
[relatório, seção 7](docs/RELATORIO.md#7-segurança-explicabilidade-e-lgpd).

## Licenças

Trechos: ver [base/fontes.csv](base/fontes.csv). Modelo base Qwen2.5-3B-Instruct sob licença de pesquisa
(não comercial); embeddings multilingual-e5-base sob MIT.
