import {
  ArrowSquareOutIcon,
  BooksIcon,
  DropIcon,
  FileTextIcon,
  LightbulbIcon,
  QuestionIcon,
  SealCheckIcon,
  SirenIcon,
} from "@phosphor-icons/react"

import type { Explicacao, Fonte, Resposta } from "@/lib/api"
import { InlinePhones } from "@/components/emergency-phones"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Badge } from "@/components/ui/badge"
import { Bubble, BubbleContent } from "@/components/ui/bubble"
import {
  Message,
  MessageAvatar,
  MessageContent,
  MessageHeader,
} from "@/components/ui/message"
import {
  Trace,
  TraceCollapsible,
  TraceCollapsibleContent,
  TraceCollapsibleTrigger,
  TraceDescription,
  TraceIcon,
  TraceLine,
  TraceTitle,
} from "@/components/ui/trace"

function porcentagem(v: number | undefined) {
  if (v === undefined) return "—"
  return `${Math.round(Math.min(Math.max(v, 0), 1) * 100)}%`
}

function segundos(ms: number | null) {
  if (ms === null) return "—"
  return `${(ms / 1000).toLocaleString("pt-BR", { maximumFractionDigits: 1 })} s`
}

export function AssistantAvatar() {
  return (
    <MessageAvatar aria-hidden="true" className="hidden size-8 bg-secondary text-primary sm:flex">
      <DropIcon />
    </MessageAvatar>
  )
}

export function AssistantMessage({ data }: { data: Resposta }) {
  return (
    <Message align="start">
      <AssistantAvatar />
      <MessageContent>
        <MessageHeader>Assistente</MessageHeader>

        {data.aviso_emergencia && (
          <Alert variant="destructive">
            <SirenIcon />
            <AlertTitle>Atenção: possível emergência</AlertTitle>
            <AlertDescription>
              <p>{data.aviso_emergencia}</p>
              <p>
                Se houver perigo agora, <InlinePhones />.
              </p>
            </AlertDescription>
          </Alert>
        )}

        <Bubble variant="outline" className="max-w-full">
          <BubbleContent className="whitespace-pre-line">
            {data.resposta || "O assistente não enviou um texto de resposta."}
          </BubbleContent>
        </Bubble>

        <div className="flex flex-wrap gap-2">
          {data.consta_na_base ? (
            <Badge variant="success">
              <SealCheckIcon data-icon="inline-start" />
              Com base em fonte oficial
            </Badge>
          ) : (
            <Badge variant="warning">
              <QuestionIcon data-icon="inline-start" />
              Não consta na base
            </Badge>
          )}
        </div>

        <Trace className="gap-1">
          {data.fontes.length > 0 && <Fontes fontes={data.fontes} />}
          <ComoCheguei explicacao={data.explicacao} latencia={data.latencia_ms} />
        </Trace>
      </MessageContent>
    </Message>
  )
}

function Fontes({ fontes }: { fontes: Fonte[] }) {
  return (
    <TraceCollapsible>
      <TraceCollapsibleTrigger className="min-h-11">
        <TraceLine>
          <TraceIcon className="text-success">
            <BooksIcon />
          </TraceIcon>
          <TraceTitle>
            {fontes.length === 1
              ? "Ver a fonte usada"
              : `Ver as ${fontes.length} fontes usadas`}
          </TraceTitle>
        </TraceLine>
      </TraceCollapsibleTrigger>
      <TraceCollapsibleContent>
        <Trace className="gap-1">
          {fontes.map((f, i) => (
            <FonteItem key={f.id ?? i} fonte={f} />
          ))}
        </Trace>
      </TraceCollapsibleContent>
    </TraceCollapsible>
  )
}

function FonteItem({ fonte }: { fonte: Fonte }) {
  const titulo = fonte.titulo ?? fonte.id ?? "Documento oficial"
  return (
    <TraceCollapsible>
      <TraceCollapsibleTrigger className="min-h-11">
        <TraceLine>
          <TraceIcon className="text-primary">
            <FileTextIcon />
          </TraceIcon>
          <TraceTitle>{titulo}</TraceTitle>
          {fonte.similaridade !== undefined && (
            <TraceDescription>{porcentagem(fonte.similaridade)}</TraceDescription>
          )}
        </TraceLine>
      </TraceCollapsibleTrigger>
      <TraceCollapsibleContent>
        <div className="flex flex-col gap-2 text-sm">
          <p className="font-medium text-foreground">{titulo}</p>
          {fonte.secao && <p>Seção: {fonte.secao}</p>}
          {fonte.trecho && (
            <blockquote className="border-l-2 border-primary/40 pl-3 text-foreground/90 italic">
              “{fonte.trecho}”
            </blockquote>
          )}
          {fonte.similaridade !== undefined && (
            <p>
              Parecido com a sua pergunta:{" "}
              <span className="font-medium text-foreground tabular-nums">
                {porcentagem(fonte.similaridade)}
              </span>
            </p>
          )}
          {fonte.url && (
            <a
              href={fonte.url}
              target="_blank"
              rel="noreferrer noopener"
              className="inline-flex min-h-11 w-fit items-center gap-1.5 rounded-md font-medium text-primary underline underline-offset-4 outline-none focus-visible:ring-[3px] focus-visible:ring-ring/50"
            >
              Abrir o documento oficial
              <ArrowSquareOutIcon aria-hidden="true" className="size-4 shrink-0" />
              <span className="sr-only"> (abre em uma nova aba)</span>
            </a>
          )}
        </div>
      </TraceCollapsibleContent>
    </TraceCollapsible>
  )
}

function ComoCheguei({
  explicacao,
  latencia,
}: {
  explicacao: Explicacao | null
  latencia: number | null
}) {
  const e = explicacao ?? {}
  const linhas: { rotulo: string; valor: string }[] = []
  if (e.similaridade_top1 !== undefined || e.limiar !== undefined) {
    linhas.push({
      rotulo: "Trecho mais parecido",
      valor: `${porcentagem(e.similaridade_top1)} (mínimo exigido: ${porcentagem(e.limiar)})`,
    })
  }
  if (e.recusa_por_limiar !== undefined) {
    linhas.push({
      rotulo: "Recusou por falta de base?",
      valor: e.recusa_por_limiar
        ? "Sim. Nenhum trecho foi parecido o suficiente, então o assistente preferiu não responder."
        : "Não. Havia trechos oficiais parecidos com a pergunta.",
    })
  }
  if (e.configuracao) linhas.push({ rotulo: "Configuração", valor: e.configuracao })
  if (e.modelo) linhas.push({ rotulo: "Modelo", valor: e.modelo })
  linhas.push({ rotulo: "Tempo de resposta", valor: segundos(latencia) })

  return (
    <TraceCollapsible>
      <TraceCollapsibleTrigger className="min-h-11">
        <TraceLine>
          <TraceIcon className="text-warning">
            <LightbulbIcon />
          </TraceIcon>
          <TraceTitle>Como cheguei nessa resposta</TraceTitle>
        </TraceLine>
      </TraceCollapsibleTrigger>
      <TraceCollapsibleContent>
        <dl className="grid grid-cols-1 gap-x-4 gap-y-1.5 text-sm sm:grid-cols-[auto_1fr]">
          {linhas.map((l) => (
            <div key={l.rotulo} className="contents">
              <dt className="font-medium text-foreground">{l.rotulo}</dt>
              <dd className="mb-1.5 break-words sm:mb-0">{l.valor}</dd>
            </div>
          ))}
        </dl>
      </TraceCollapsibleContent>
    </TraceCollapsible>
  )
}
