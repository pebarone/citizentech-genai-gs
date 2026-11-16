/**
 * Chamadas à API do assistente Alerta Córrego.
 *
 * Base configurável por VITE_API_BASE (padrão: mesma origem).
 * Com VITE_MOCK=1, usa respostas de exemplo locais (ver ./mock.ts).
 */

export type Fonte = {
  id?: string
  titulo?: string
  secao?: string
  url?: string
  trecho?: string
  similaridade?: number
}

export type Explicacao = {
  limiar?: number
  similaridade_top1?: number
  recusa_por_limiar?: boolean
  configuracao?: string
  modelo?: string
}

export type Resposta = {
  resposta: string
  consta_na_base: boolean
  fontes: Fonte[]
  explicacao: Explicacao | null
  aviso_emergencia: string | null
  latencia_ms: number | null
}

export type InfoApi = Record<string, unknown>

export type ApiErrorKind =
  | "offline"
  | "rate_limit"
  | "validation"
  | "timeout"
  | "server"

export class ApiError extends Error {
  kind: ApiErrorKind
  status?: number
  detail?: string

  constructor(kind: ApiErrorKind, opts: { status?: number; detail?: string } = {}) {
    super(opts.detail ?? kind)
    this.name = "ApiError"
    this.kind = kind
    this.status = opts.status
    this.detail = opts.detail
  }
}

export const LIMITE_PERGUNTA = 500
const TEMPO_LIMITE_MS = 60_000

const API_BASE = (import.meta.env.VITE_API_BASE ?? "").replace(/\/+$/, "")
const USAR_MOCK = import.meta.env.VITE_MOCK === "1"

function texto(v: unknown): string | undefined {
  return typeof v === "string" && v.trim() !== "" ? v : undefined
}

function numero(v: unknown): number | undefined {
  return typeof v === "number" && Number.isFinite(v) ? v : undefined
}

function obj(v: unknown): Record<string, unknown> | undefined {
  return v !== null && typeof v === "object" && !Array.isArray(v)
    ? (v as Record<string, unknown>)
    : undefined
}

/** Normaliza a resposta para que campos ausentes não quebrem a interface. */
export function normalizarResposta(raw: unknown): Resposta {
  const r = obj(raw) ?? {}
  const fontes = Array.isArray(r.fontes) ? r.fontes : []
  const exp = obj(r.explicacao)
  return {
    resposta: texto(r.resposta) ?? "",
    consta_na_base: r.consta_na_base === true,
    fontes: fontes
      .map((f) => obj(f))
      .filter((f): f is Record<string, unknown> => f !== undefined)
      .map((f) => ({
        id: texto(f.id),
        titulo: texto(f.titulo),
        secao: texto(f.secao),
        url: texto(f.url),
        trecho: texto(f.trecho),
        similaridade: numero(f.similaridade),
      })),
    explicacao: exp
      ? {
          limiar: numero(exp.limiar),
          similaridade_top1: numero(exp.similaridade_top1),
          recusa_por_limiar:
            typeof exp.recusa_por_limiar === "boolean"
              ? exp.recusa_por_limiar
              : undefined,
          configuracao: texto(exp.configuracao),
          modelo: texto(exp.modelo),
        }
      : null,
    aviso_emergencia: texto(r.aviso_emergencia) ?? null,
    latencia_ms: numero(r.latencia_ms) ?? null,
  }
}

async function lerDetalhe(res: Response): Promise<string | undefined> {
  try {
    const body = obj(await res.json())
    return texto(body?.detail)
  } catch {
    return undefined
  }
}

async function requisitar(
  caminho: string,
  init: RequestInit = {},
  sinalExterno?: AbortSignal
): Promise<Response> {
  if (typeof navigator !== "undefined" && navigator.onLine === false) {
    throw new ApiError("offline")
  }
  const controle = new AbortController()
  let estourou = false
  const timer = setTimeout(() => {
    estourou = true
    controle.abort()
  }, TEMPO_LIMITE_MS)
  const repassarAbort = () => controle.abort()
  sinalExterno?.addEventListener("abort", repassarAbort)

  try {
    const res = await fetch(`${API_BASE}${caminho}`, {
      ...init,
      signal: controle.signal,
    })
    if (res.ok) return res
    const detail = await lerDetalhe(res)
    if (res.status === 429) throw new ApiError("rate_limit", { status: 429, detail })
    if (res.status === 422) throw new ApiError("validation", { status: 422, detail })
    if (res.status === 408 || res.status === 504)
      throw new ApiError("timeout", { status: res.status, detail })
    throw new ApiError("server", { status: res.status, detail })
  } catch (e) {
    if (e instanceof ApiError) throw e
    if (estourou) throw new ApiError("timeout")
    if (typeof navigator !== "undefined" && navigator.onLine === false) {
      throw new ApiError("offline")
    }
    throw new ApiError("server")
  } finally {
    clearTimeout(timer)
    sinalExterno?.removeEventListener("abort", repassarAbort)
  }
}

export async function perguntar(
  pergunta: string,
  signal?: AbortSignal
): Promise<Resposta> {
  const p = pergunta.trim()
  if (p === "" || p.length > LIMITE_PERGUNTA) {
    throw new ApiError("validation")
  }
  if (USAR_MOCK) {
    const mock = await import("./mock")
    return normalizarResposta(await mock.perguntarMock(p))
  }
  const res = await requisitar(
    "/api/v1/assistente/perguntar",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pergunta: p }),
    },
    signal
  )
  return normalizarResposta(await res.json().catch(() => ({})))
}

export async function obterInfo(signal?: AbortSignal): Promise<InfoApi> {
  if (USAR_MOCK) {
    const mock = await import("./mock")
    return mock.infoMock()
  }
  const res = await requisitar("/api/v1/info", {}, signal)
  return obj(await res.json().catch(() => ({}))) ?? {}
}
