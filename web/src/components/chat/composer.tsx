import { useState, type FormEvent, type KeyboardEvent, type RefObject } from "react"
import { PaperPlaneRightIcon } from "@phosphor-icons/react"
import { cn } from "@/lib/utils"

import { LIMITE_PERGUNTA } from "@/lib/api"
import {
  InputGroup,
  InputGroupAddon,
  InputGroupButton,
  InputGroupText,
  InputGroupTextarea,
} from "@/components/ui/input-group"
import { Spinner } from "@/components/ui/spinner"

export function Composer({
  onSend,
  busy,
  textareaRef,
}: {
  onSend: (texto: string) => void
  busy: boolean
  textareaRef: RefObject<HTMLTextAreaElement | null>
}) {
  const [texto, setTexto] = useState("")
  const limpo = texto.trim()
  const perto = texto.length >= LIMITE_PERGUNTA - 50
  const podeEnviar = !busy && limpo.length > 0 && texto.length <= LIMITE_PERGUNTA

  function enviar() {
    if (!podeEnviar) return
    onSend(limpo)
    setTexto("")
  }

  function onSubmit(e: FormEvent) {
    e.preventDefault()
    enviar()
  }

  function onKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey && !e.nativeEvent.isComposing) {
      e.preventDefault()
      enviar()
    }
  }

  return (
    <form onSubmit={onSubmit} aria-label="Enviar pergunta">
      <label htmlFor="pergunta" className="sr-only">
        Sua pergunta
      </label>
      <InputGroup className="bg-card">
        <InputGroupTextarea
          id="pergunta"
          ref={textareaRef}
          value={texto}
          onChange={(e) => setTexto(e.target.value.slice(0, LIMITE_PERGUNTA))}
          onKeyDown={onKeyDown}
          maxLength={LIMITE_PERGUNTA}
          rows={2}
          placeholder="Escreva sua dúvida sobre enchentes..."
          aria-describedby="pergunta-ajuda pergunta-contador"
          enterKeyHint="send"
          className="max-h-40 min-h-14 px-4 pt-3"
        />
        <InputGroupAddon align="block-end" className="gap-3 px-3 pb-2">
          <InputGroupText id="pergunta-ajuda" className="hidden text-xs sm:flex">
            Enter envia · Shift+Enter pula linha
          </InputGroupText>
          <InputGroupText
            id="pergunta-contador"
            className={cn("ml-auto text-xs tabular-nums", perto && "text-warning")}
          >
            <span className="sr-only">Caracteres usados: </span>
            {texto.length}/{LIMITE_PERGUNTA}
          </InputGroupText>
          <InputGroupButton
            type="submit"
            variant="default"
            size="lg"
            disabled={!podeEnviar}
          >
            {busy ? (
              <Spinner data-icon="inline-start" />
            ) : (
              <PaperPlaneRightIcon data-icon="inline-start" />
            )}
            Enviar
          </InputGroupButton>
        </InputGroupAddon>
      </InputGroup>
    </form>
  )
}
