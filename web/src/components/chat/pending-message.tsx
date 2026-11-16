import { useEffect, useState } from "react"

import { AssistantAvatar } from "@/components/chat/assistant-message"
import { Bubble, BubbleContent } from "@/components/ui/bubble"
import {
  Message,
  MessageContent,
  MessageHeader,
} from "@/components/ui/message"
import { Skeleton } from "@/components/ui/skeleton"
import { Spinner } from "@/components/ui/spinner"

/** Indicador enquanto a API responde (3 a 20 s, sem streaming). */
export function PendingMessage() {
  const [demorando, setDemorando] = useState(false)

  useEffect(() => {
    const t = setTimeout(() => setDemorando(true), 8000)
    return () => clearTimeout(t)
  }, [])

  return (
    <Message align="start" aria-busy="true">
      <AssistantAvatar />
      <MessageContent>
        <MessageHeader>Assistente</MessageHeader>
        <Bubble variant="outline" className="w-full max-w-full">
          <BubbleContent className="flex w-full flex-col gap-3">
            <span className="flex items-center gap-2 text-primary">
              <Spinner />
              <span className="shimmer motion-reduce:shimmer-none">
                Consultando os documentos oficiais...
              </span>
            </span>
            <span className="flex flex-col gap-2" aria-hidden="true">
              <Skeleton className="h-3.5 w-11/12" />
              <Skeleton className="h-3.5 w-4/5" />
              <Skeleton className="h-3.5 w-3/5" />
            </span>
          </BubbleContent>
        </Bubble>
        {demorando && (
          <p className="px-1 text-sm text-muted-foreground">
            Ainda buscando. Isso pode levar até 20 segundos.
          </p>
        )}
      </MessageContent>
    </Message>
  )
}
