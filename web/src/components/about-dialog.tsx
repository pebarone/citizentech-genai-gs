import { useEffect, useState } from "react"
import {
  ChatCircleDotsIcon,
  MagnifyingGlassIcon,
  ShieldCheckIcon,
} from "@phosphor-icons/react"

import { obterInfo, type InfoApi } from "@/lib/api"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Separator } from "@/components/ui/separator"
import { Skeleton } from "@/components/ui/skeleton"

const ROTULOS: Record<string, string> = {
  nome: "Nome",
  versao: "Versão",
  version: "Versão",
  configuracao: "Configuração",
  modelo: "Modelo",
  n_trechos: "Trechos na base",
  num_trechos: "Trechos na base",
  trechos: "Trechos na base",
  limiar: "Limiar de similaridade",
}

function formatar(v: unknown): string | null {
  if (v === null || v === undefined) return null
  if (typeof v === "number") return v.toLocaleString("pt-BR")
  if (typeof v === "boolean") return v ? "sim" : "não"
  if (typeof v === "string") return v.trim() || null
  return null
}

const PASSOS = [
  {
    icone: MagnifyingGlassIcon,
    cor: "text-primary",
    texto: "Sua pergunta é comparada com trechos de documentos oficiais de Defesa Civil.",
  },
  {
    icone: ChatCircleDotsIcon,
    cor: "text-success",
    texto: "A resposta é escrita só com base nos trechos encontrados, e as fontes ficam visíveis.",
  },
  {
    icone: ShieldCheckIcon,
    cor: "text-warning",
    texto: "Se nenhum trecho for parecido o suficiente, o assistente avisa que não consta na base em vez de inventar.",
  },
]

export function AboutDialog() {
  const [aberto, setAberto] = useState(false)
  const [info, setInfo] = useState<InfoApi | null>(null)
  const [falhou, setFalhou] = useState(false)

  useEffect(() => {
    if (!aberto || info) return
    const ctrl = new AbortController()
    obterInfo(ctrl.signal)
      .then((i) => {
        setInfo(i)
        setFalhou(false)
      })
      .catch(() => {
        if (!ctrl.signal.aborted) setFalhou(true)
      })
    return () => ctrl.abort()
  }, [aberto, info])

  const linhas = info
    ? Object.entries(info)
        .map(([k, v]) => ({ k, rotulo: ROTULOS[k] ?? k.replace(/_/g, " "), valor: formatar(v) }))
        .filter((l): l is { k: string; rotulo: string; valor: string } => l.valor !== null)
    : []

  return (
    <Dialog open={aberto} onOpenChange={setAberto}>
      <DialogTrigger render={<Button variant="link" size="lg" className="px-1" />}>
        Sobre
      </DialogTrigger>
      <DialogContent className="max-h-[90dvh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Como o assistente funciona</DialogTitle>
          <DialogDescription>
            Ele orienta com base em documentos oficiais, mas não substitui a
            Defesa Civil.
          </DialogDescription>
        </DialogHeader>

        <ol className="flex flex-col gap-3 text-sm">
          {PASSOS.map(({ icone: Icone, cor, texto }) => (
            <li key={texto} className="flex gap-3">
              <Icone aria-hidden="true" className={cn("mt-0.5 size-5 shrink-0", cor)} />
              <span>{texto}</span>
            </li>
          ))}
        </ol>

        <Separator />

        <section aria-labelledby="sobre-servico" className="flex flex-col gap-2">
          <h3 id="sobre-servico" className="text-sm font-medium">
            Sobre o serviço
          </h3>
          {!info && !falhou && (
            <div className="flex flex-col gap-2" aria-label="Carregando informações">
              <Skeleton className="h-4 w-2/3" />
              <Skeleton className="h-4 w-1/2" />
              <Skeleton className="h-4 w-3/5" />
            </div>
          )}
          {falhou && (
            <p className="text-sm text-muted-foreground">
              Não foi possível carregar as informações do serviço agora.
            </p>
          )}
          {info && linhas.length === 0 && (
            <p className="text-sm text-muted-foreground">Sem informações disponíveis.</p>
          )}
          {linhas.length > 0 && (
            <dl className="grid grid-cols-[auto_1fr] gap-x-4 gap-y-1.5 text-sm">
              {linhas.map((l) => (
                <div key={l.k} className="contents">
                  <dt className="text-muted-foreground first-letter:uppercase">{l.rotulo}</dt>
                  <dd className="min-w-0 break-words">{l.valor}</dd>
                </div>
              ))}
            </dl>
          )}
        </section>
      </DialogContent>
    </Dialog>
  )
}
