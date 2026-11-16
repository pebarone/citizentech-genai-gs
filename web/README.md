# Alerta Córrego · Assistente (frontend)

Chat de página única (Vite + React + TypeScript + Tailwind v4 + shadcn/ui, base `base`, estilo `maia`, ícones Phosphor duotone).
O build estático em `dist/` é versionado e servido pela API FastAPI em `/` (estáticos em `/assets`), então não é preciso Node para rodar o projeto.

## Requisitos (só para desenvolver)

Node 20+ e npm.

```bash
cd web
npm install
```

## Desenvolver

```bash
npm run dev        # http://localhost:5173 — encaminha /api e /healthz para http://127.0.0.1:8000
```

Para apontar para outra API, defina `VITE_API_BASE` (ex.: `VITE_API_BASE=http://127.0.0.1:8000`). Padrão: mesma origem.

## Desenvolver sem o backend (mock)

```bash
npm run dev:mock   # usa .env.mock (VITE_MOCK=1)
```

Cenários do mock (`src/lib/mock.ts`):

| Digite                                        | Resultado                               |
| --------------------------------------------- | --------------------------------------- |
| algo sobre água, casa, kit, limpar, enchente  | resposta com 2 fontes oficiais          |
| "ilhado", "socorro", "arrastado"...           | resposta com aviso de emergência        |
| outro assunto (ex.: previsão do tempo)        | recusa: "Não consta na base"            |
| "erro"                                        | API fora do ar (com "Tentar de novo")   |
| "muitas" ou "limite"                          | 429, muitas perguntas                   |

## Build

```bash
npm run build      # checa tipos e gera dist/index.html + dist/assets/
```

Depois do build, faça commit da pasta `dist/` junto com o código.

## Estrutura

- `src/lib/api.ts`: chamadas e tipos da API (`/api/v1/assistente/perguntar`, `/api/v1/info`), normalização defensiva e erros.
- `src/components/chat/`: mensagens, sugestões, campo de pergunta.
- `src/components/ui/`: componentes shadcn (gerados pelo CLI e ajustados ao tema).
- A conversa fica só em memória: nada é salvo no aparelho.
