import {
  ArrowClockwiseIcon,
  WarningCircleIcon,
  WifiSlashIcon,
} from "@phosphor-icons/react"

import type { ApiError } from "@/lib/api"
import { InlinePhones } from "@/components/emergency-phones"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Button } from "@/components/ui/button"

const MENSAGENS: Record<ApiError["kind"], { titulo: string; texto: string }> = {
  offline: {
    titulo: "Você está sem internet",
    texto: "Confira sua conexão e tente de novo.",
  },
  rate_limit: {
    titulo: "Muitas perguntas em pouco tempo",
    texto: "Espere um pouquinho (cerca de 1 minuto) e tente de novo.",
  },
  validation: {
    titulo: "Não deu para enviar essa pergunta",
    texto: "Escreva uma pergunta com até 500 caracteres.",
  },
  timeout: {
    titulo: "A resposta demorou demais",
    texto: "O serviço está lento agora. Tente de novo em instantes.",
  },
  server: {
    titulo: "O assistente está fora do ar",
    texto: "Não conseguimos falar com o serviço agora. Tente de novo em alguns minutos.",
  },
}

export function ErrorMessage({
  error,
  onRetry,
  disabled,
}: {
  error: ApiError
  onRetry?: () => void
  disabled?: boolean
}) {
  const m = MENSAGENS[error.kind] ?? MENSAGENS.server
  const Icone = error.kind === "offline" ? WifiSlashIcon : WarningCircleIcon
  const podeRepetir = error.kind !== "validation" && onRetry

  return (
    <Alert variant="destructive">
      <Icone />
      <AlertTitle>{m.titulo}</AlertTitle>
      <AlertDescription className="flex flex-col gap-3">
        <div>
          {error.kind === "validation" && error.detail ? error.detail : m.texto}
        </div>
        <div>
          Em caso de perigo, não espere: <InlinePhones />.
        </div>
        {podeRepetir && (
          <Button
            variant="outline"
            size="lg"
            className="w-fit"
            onClick={onRetry}
            disabled={disabled}
          >
            <ArrowClockwiseIcon data-icon="inline-start" />
            Tentar de novo
          </Button>
        )}
      </AlertDescription>
    </Alert>
  )
}
