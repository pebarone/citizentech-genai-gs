import { PhoneIcon } from "@phosphor-icons/react"

import { Button } from "@/components/ui/button"

export const TELEFONES = [
  { numero: "199", nome: "Defesa Civil" },
  { numero: "193", nome: "Bombeiros" },
] as const

/** Botões grandes de ligação (tel:) para Defesa Civil e Bombeiros. */
export function EmergencyPhones({ className }: { className?: string }) {
  return (
    <nav aria-label="Telefones de emergência" className={className}>
      {TELEFONES.map((t) => (
        <Button
          key={t.numero}
          variant="destructive"
          size="lg"
          nativeButton={false}
          render={
            <a
              href={`tel:${t.numero}`}
              aria-label={`Ligar para ${t.nome}, ${t.numero}`}
            />
          }
        >
          <PhoneIcon data-icon="inline-start" />
          {t.nome}
          <span className="font-semibold tabular-nums">{t.numero}</span>
        </Button>
      ))}
    </nav>
  )
}

/** Links tel: inline, para usar dentro de textos de aviso. */
export function InlinePhones() {
  return (
    <>
      ligue <a href="tel:199">199 (Defesa Civil)</a> ou{" "}
      <a href="tel:193">193 (Bombeiros)</a>
    </>
  )
}
