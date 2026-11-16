/**
 * Respostas de exemplo para desenvolver a interface sem o backend.
 * Ativado com VITE_MOCK=1. Não entra no build de produção.
 *
 * Palavras-chave para testar os cenários:
 *  - "erro"                        -> falha do servidor (500)
 *  - "muitas" / "limite"           -> 429
 *  - "ilhad" / "arrast" / "socorro" / "preso" -> aviso de emergência
 *  - temas de enchente (água, casa, kit, limpar, enchente, alag...) -> resposta com fontes
 *  - qualquer outra coisa          -> recusa ("não consta na base")
 */
import { ApiError } from "./api"

const espera = (ms: number) => new Promise((r) => setTimeout(r, ms))

const EXPLICACAO_BASE = {
  limiar: 0.82,
  configuracao: "rag_lora",
  modelo: "Qwen/Qwen2.5-3B-Instruct",
}

const FONTES = [
  {
    id: "DCSP-01-003",
    titulo: "Manual de orientação à população em enchentes",
    secao: "Durante a enchente",
    url: "https://www.defesacivil.sp.gov.br/",
    trecho:
      "Desligue a energia elétrica no quadro de luz e feche o registro de gás. Leve documentos e remédios para um local alto e saia de casa se a água continuar subindo.",
    similaridade: 0.87,
  },
  {
    id: "DCSP-02-011",
    titulo: "Cartilha de prevenção de desastres",
    secao: "Plano familiar de emergência",
    url: "https://www.gov.br/mdr/pt-br/assuntos/protecao-e-defesa-civil",
    trecho:
      "Combine com a família um ponto de encontro seguro e mantenha os telefones da Defesa Civil (199) e dos Bombeiros (193) anotados.",
    similaridade: 0.84,
  },
]

export async function perguntarMock(pergunta: string): Promise<unknown> {
  const p = pergunta.toLowerCase()
  await espera(1200 + Math.random() * 1300)

  if (p.includes("erro")) {
    throw new ApiError("server", { status: 500 })
  }
  if (p.includes("muitas") || p.includes("limite")) {
    throw new ApiError("rate_limit", { status: 429 })
  }

  if (/ilhad|arrast|socorro|preso|presa/.test(p)) {
    return {
      resposta:
        "Se há pessoas ilhadas, não tente atravessar a água: 15 cm de correnteza já derrubam um adulto. Ligue agora para os Bombeiros (193) ou a Defesa Civil (199), informe o endereço e quantas pessoas estão no local. Enquanto espera, procure o ponto mais alto possível e fique longe de fios elétricos.",
      consta_na_base: true,
      fontes: [FONTES[0]],
      explicacao: { ...EXPLICACAO_BASE, similaridade_top1: 0.86, recusa_por_limiar: false },
      aviso_emergencia:
        "Parece uma situação de risco agora. Ligue imediatamente para os Bombeiros (193) ou a Defesa Civil (199).",
      latencia_ms: 3870,
    }
  }

  if (/água|agua|casa|kit|limpar|limpeza|enchente|alag|chuva|subir|córrego|corrego|voltar/.test(p)) {
    return {
      resposta:
        "Quando a água começar a subir:\n\n1. Desligue a energia no quadro de luz e feche o registro de gás.\n2. Coloque documentos, remédios e o celular em um saco plástico e leve para um lugar alto.\n3. Se a água continuar subindo, saia de casa e vá para o ponto de encontro combinado com a família.\n4. Não entre na água da enchente: ela pode estar contaminada e esconder buracos e correnteza.",
      consta_na_base: true,
      fontes: FONTES,
      explicacao: { ...EXPLICACAO_BASE, similaridade_top1: 0.87, recusa_por_limiar: false },
      aviso_emergencia: null,
      latencia_ms: 4210,
    }
  }

  return {
    resposta:
      "Não encontrei essa informação nos documentos oficiais que eu consulto, então prefiro não responder para não passar uma orientação errada. Para dúvidas fora desse tema, procure a Defesa Civil da sua cidade pelo 199.",
    consta_na_base: false,
    fontes: [],
    explicacao: { ...EXPLICACAO_BASE, similaridade_top1: 0.61, recusa_por_limiar: true },
    aviso_emergencia: null,
    latencia_ms: 980,
  }
}

export async function infoMock(): Promise<Record<string, unknown>> {
  await espera(400)
  return {
    nome: "Alerta Córrego · Assistente",
    versao: "0.1.0 (mock)",
    configuracao: "rag_lora",
    modelo: "Qwen/Qwen2.5-3B-Instruct",
    n_trechos: 412,
  }
}
