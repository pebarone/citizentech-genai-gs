import { useCallback, useEffect, useRef, useState } from "react"
import { DropIcon, WifiSlashIcon } from "@phosphor-icons/react"

import { ApiError, perguntar, type Resposta } from "@/lib/api"
import { AboutDialog } from "@/components/about-dialog"
import { AssistantMessage } from "@/components/chat/assistant-message"
import { Composer } from "@/components/chat/composer"
import { ErrorMessage } from "@/components/chat/error-message"
import { PendingMessage } from "@/components/chat/pending-message"
import { Suggestions } from "@/components/chat/suggestions"
import { EmergencyPhones, InlinePhones } from "@/components/emergency-phones"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Bubble, BubbleContent } from "@/components/ui/bubble"
import { Message, MessageContent } from "@/components/ui/message"
import {
  MessageScroller,
  MessageScrollerButton,
  MessageScrollerContent,
  MessageScrollerItem,
  MessageScrollerProvider,
  MessageScrollerViewport,
} from "@/components/ui/message-scroller"

type ChatItem =
  | { id: string; role: "user"; texto: string }
  | { id: string; role: "assistant"; data: Resposta }
  | { id: string; role: "error"; error: ApiError; pergunta: string }

let contador = 0
const novoId = () => `m${++contador}`

function useOnline() {
  const [online, setOnline] = useState(() =>
    typeof navigator === "undefined" ? true : navigator.onLine
  )
  useEffect(() => {
    const on = () => setOnline(true)
    const off = () => setOnline(false)
    window.addEventListener("online", on)
    window.addEventListener("offline", off)
    return () => {
      window.removeEventListener("online", on)
      window.removeEventListener("offline", off)
    }
  }, [])
  return online
}

export function App() {
  // A conversa fica só em memória (nada é salvo no aparelho).
  const [itens, setItens] = useState<ChatItem[]>([])
  const [pendente, setPendente] = useState(false)
  const [anuncio, setAnuncio] = useState("")
  const online = useOnline()
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const consultar = useCallback(async (pergunta: string) => {
    setPendente(true)
    setAnuncio("Consultando os documentos oficiais...")
    try {
      const data = await perguntar(pergunta)
      setItens((xs) => [...xs, { id: novoId(), role: "assistant", data }])
      setAnuncio(`Resposta do assistente: ${data.resposta}`)
    } catch (e) {
      const error = e instanceof ApiError ? e : new ApiError("server")
      setItens((xs) => [...xs, { id: novoId(), role: "error", error, pergunta }])
      setAnuncio("")
    } finally {
      setPendente(false)
    }
  }, [])

  const enviar = useCallback(
    (texto: string) => {
      if (pendente) return
      setItens((xs) => [...xs, { id: novoId(), role: "user", texto }])
      void consultar(texto)
    },
    [pendente, consultar]
  )

  const repetir = useCallback(
    (id: string, pergunta: string) => {
      if (pendente) return
      setItens((xs) => xs.filter((x) => x.id !== id))
      void consultar(pergunta)
    },
    [pendente, consultar]
  )

  const vazio = itens.length === 0 && !pendente

  return (
    <div className="flex h-dvh flex-col overflow-hidden bg-background">
      <header className="shrink-0 border-b bg-card">
        <div className="mx-auto flex w-full max-w-3xl flex-col gap-3 px-4 py-3 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex min-w-0 items-center gap-3">
            <span
              aria-hidden="true"
              className="flex size-10 shrink-0 items-center justify-center rounded-xl bg-primary text-primary-foreground"
            >
              <DropIcon className="size-6" />
            </span>
            <div className="min-w-0">
              <h1 className="font-heading text-base leading-tight font-semibold">
                Alerta Córrego · Assistente
              </h1>
              <p className="text-sm leading-snug text-muted-foreground">
                Tire dúvidas sobre enchentes com base em orientações oficiais
              </p>
            </div>
          </div>
          <EmergencyPhones className="grid shrink-0 grid-cols-2 gap-2" />
        </div>
      </header>

      <main className="flex min-h-0 flex-1 flex-col" aria-label="Conversa">
        {!online && (
          <div className="mx-auto w-full max-w-3xl px-4 pt-3">
            <Alert variant="warning">
              <WifiSlashIcon />
              <AlertTitle>Você está sem internet</AlertTitle>
              <AlertDescription>
                Não dá para consultar o assistente agora. Em caso de perigo,{" "}
                <InlinePhones /> (a ligação funciona sem internet).
              </AlertDescription>
            </Alert>
          </div>
        )}

        {vazio ? (
          <div className="min-h-0 flex-1 overflow-y-auto">
            <div className="mx-auto flex min-h-full w-full max-w-3xl px-4 py-6">
              <Suggestions onPick={enviar} disabled={pendente} />
            </div>
          </div>
        ) : (
          <MessageScrollerProvider autoScroll>
            <MessageScroller className="flex-1">
              <MessageScrollerViewport>
                <MessageScrollerContent className="mx-auto w-full max-w-3xl px-4 py-6">
                  {itens.map((item) => (
                    <MessageScrollerItem
                      key={item.id}
                      messageId={item.id}
                      scrollAnchor={item.role === "user"}
                    >
                      {item.role === "user" && (
                        <Message align="end">
                          <MessageContent>
                            <span className="sr-only">Você perguntou:</span>
                            <Bubble variant="default" align="end">
                              <BubbleContent className="whitespace-pre-line">
                                {item.texto}
                              </BubbleContent>
                            </Bubble>
                          </MessageContent>
                        </Message>
                      )}
                      {item.role === "assistant" && (
                        <AssistantMessage data={item.data} />
                      )}
                      {item.role === "error" && (
                        <ErrorMessage
                          error={item.error}
                          disabled={pendente}
                          onRetry={() => repetir(item.id, item.pergunta)}
                        />
                      )}
                    </MessageScrollerItem>
                  ))}
                  {pendente && (
                    <MessageScrollerItem messageId="pendente">
                      <PendingMessage />
                    </MessageScrollerItem>
                  )}
                </MessageScrollerContent>
              </MessageScrollerViewport>
              <MessageScrollerButton size="icon-lg" />
            </MessageScroller>
          </MessageScrollerProvider>
        )}

        <div aria-live="polite" aria-atomic="true" className="sr-only">
          {anuncio}
        </div>
      </main>

      <footer className="shrink-0 border-t bg-card">
        <div className="mx-auto flex w-full max-w-3xl flex-col gap-1 px-4 pt-3 pb-[max(0.5rem,env(safe-area-inset-bottom))]">
          <Composer onSend={enviar} busy={pendente} textareaRef={textareaRef} />
          <div className="flex items-center justify-between gap-2">
            <p className="text-xs leading-snug text-muted-foreground">
              Não guardamos sua pergunta nem dados pessoais. Este assistente
              orienta, mas não substitui a Defesa Civil.
            </p>
            <AboutDialog />
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
