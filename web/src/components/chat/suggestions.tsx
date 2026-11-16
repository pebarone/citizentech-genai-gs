import type { Icon } from "@phosphor-icons/react"
import {
  BroomIcon,
  ChatCircleDotsIcon,
  FirstAidKitIcon,
  HouseLineIcon,
  LifebuoyIcon,
  WavesIcon,
} from "@phosphor-icons/react"

import { Button } from "@/components/ui/button"
import {
  Empty,
  EmptyContent,
  EmptyDescription,
  EmptyHeader,
  EmptyMedia,
  EmptyTitle,
} from "@/components/ui/empty"

const SUGESTOES: { texto: string; icone: Icon; cor: string }[] = [
  { texto: "O que fazer quando a água começa a subir?", icone: WavesIcon, cor: "text-primary" },
  { texto: "Posso voltar para casa depois da enchente?", icone: HouseLineIcon, cor: "text-primary" },
  { texto: "O que levar no kit de emergência?", icone: FirstAidKitIcon, cor: "text-success" },
  { texto: "Como limpar a casa depois do alagamento?", icone: BroomIcon, cor: "text-warning" },
  {
    texto: "Tem gente ilhada na minha rua. O que eu faço?",
    icone: LifebuoyIcon,
    cor: "text-destructive",
  },
]

export function Suggestions({
  onPick,
  disabled,
}: {
  onPick: (texto: string) => void
  disabled?: boolean
}) {
  return (
    <Empty className="p-4 sm:p-8">
      <EmptyHeader>
        <EmptyMedia variant="icon" className="size-12 bg-secondary text-primary">
          <ChatCircleDotsIcon />
        </EmptyMedia>
        <EmptyTitle>Como posso ajudar?</EmptyTitle>
        <EmptyDescription>
          Escreva sua dúvida ou toque em uma das perguntas abaixo. As respostas
          vêm de orientações oficiais da Defesa Civil.
        </EmptyDescription>
      </EmptyHeader>
      <EmptyContent className="max-w-xl">
        <ul className="grid w-full grid-cols-1 gap-2 sm:grid-cols-2" aria-label="Perguntas sugeridas">
          {SUGESTOES.map(({ texto, icone: Icone, cor }) => (
            <li key={texto} className="flex">
              <Button
                variant="outline"
                size="lg"
                className="h-auto min-h-12 w-full justify-start py-3 text-left whitespace-normal"
                onClick={() => onPick(texto)}
                disabled={disabled}
              >
                <Icone data-icon="inline-start" className={cor} />
                {texto}
              </Button>
            </li>
          ))}
        </ul>
      </EmptyContent>
    </Empty>
  )
}
