# Base de conhecimento – Alerta Córrego

Base usada pelo assistente (RAG) para responder dúvidas de moradores sobre enchentes, alagamentos, inundações, enxurradas e deslizamentos. Ela contém apenas conteúdo público de órgãos oficiais, em português, e cada trecho cita a sua fonte.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `fontes.csv` | Uma linha por fonte: `fonte_id,titulo,orgao,url,formato,licenca,data_acesso,n_trechos` (UTF-8) |
| `trechos.jsonl` | Um trecho por linha: `{"id","fonte_id","titulo","secao","texto","url"}` |
| `brutos/<fonte_id>.txt` | Texto bruto extraído de cada fonte. A primeira linha traz a URL e a data de acesso (2026-11-15). Quando uma fonte reúne mais de uma página, os blocos ficam separados por uma linha de `=` e cada um começa com a sua URL |
| `validar_base.py` | Validador da base e dos conjuntos de perguntas (`avaliacao/` e `treino/`) |

## Como a base foi montada

1. **Busca.** Procuramos páginas e PDFs oficiais da Prefeitura de São Paulo (Defesa Civil/COMDEC, CGE e Secretaria da Saúde), do Governo do Estado de SP (Defesa Civil Estadual e SEMIL) e do Governo Federal (Ministério da Saúde, MIDR/Defesa Civil Nacional, Ministério das Cidades, FGTS/CAIXA), além da Agência Brasil (EBC).
2. **Extração.** Baixamos o HTML e extraímos o texto da área principal da página, sem menus, rodapés e scripts. Nos PDFs usamos `pdftotext`. O resultado foi salvo sem edição em `brutos/`.
3. **Recorte em trechos.** Os trechos foram escritos a partir do texto bruto, um assunto por trecho. A limpeza se limitou a:
   - tirar marcadores de lista, numeração e quebras de linha;
   - unir itens da mesma seção (por exemplo, "antes da enchente") em prosa corrida;
   - acrescentar pequenos conectivos ou o nome do órgão para que o trecho se entenda sozinho (por exemplo, "Segundo a Defesa Civil da Prefeitura de São Paulo…");
   - repetir, quando o original dizia "nos telefones mencionados acima", o número que aparece na mesma página (199/193).

   Nenhum fato foi acrescentado. Números, dosagens, prazos e telefones são os mesmos do original.
4. **Critérios de recorte:**
   - de 60 a 180 palavras (resultado: mínimo de 61, máximo de 130, média de 90);
   - autocontido: o trecho não usa pronome que dependa do trecho anterior e nomeia o assunto;
   - um tema por trecho (por exemplo, "limpeza da caixa d'água" separada de "pisos e paredes");
   - o campo `secao` resume o assunto, e `url` aponta para a página exata (subpágina, quando houver);
   - `id` no formato `<fonte_id>-NNN`.
5. **Validação.** Rode `python base/validar_base.py`. O script confere a estrutura, a contagem por fonte (e reescreve `n_trechos`), o fundamento dos gabaritos e a separação entre treino, dev e teste.

## Tabela da base

| fonte_id | Órgão | Formato | Licença registrada | Nº de trechos |
|---|---|---|---|---|
| COMDEC-01 | Defesa Civil (COMDEC) – Prefeitura de São Paulo | HTML | Conteúdo público de órgão oficial (sem licença explícita); uso educacional com citação da fonte | 8 |
| CGE-01 | CGE – Prefeitura de São Paulo (páginas Dicas, Operação Chuvas de Verão, Quem Somos) | HTML | Conteúdo público de órgão oficial (sem licença explícita); uso educacional com citação da fonte | 8 |
| SMSSP-01 | Secretaria Municipal da Saúde de SP – folder "Cuidados básicos em relação às enchentes" (2023) | PDF | Conteúdo público de órgão oficial (sem licença explícita); uso educacional com citação da fonte | 9 |
| SEMIL-01 | SEMIL-SP – Portal de Educação Ambiental | HTML | Conteúdo público de órgão oficial (sem licença explícita); uso educacional com citação da fonte | 10 |
| DCSP-01 | Coordenadoria Estadual de Defesa Civil de SP – nota "Como evitar deslizamento" (hospedada no portal da Saúde SP) | PDF | Conteúdo público de órgão oficial (sem licença explícita); uso educacional com citação da fonte | 3 |
| MS-01 | Ministério da Saúde – "Enchentes" (Saúde de A a Z) e subpáginas de água, alimentos, leptospirose, animais peçonhentos e tétano | HTML | CC BY-ND 3.0 (rodapé do portal gov.br) | 13 |
| MS-02 | Ministério da Saúde – "Leptospirose" (Saúde de A a Z) | HTML | CC BY-ND 3.0 (rodapé do portal gov.br) | 6 |
| MS-03 | Ministério da Saúde – Cartilha de Orientação à População no Período de Alerta de Chuvas Intensas (2017) | PDF | CC BY-ND 3.0 (portal gov.br onde o PDF está hospedado); a capa indica distribuição gratuita e venda proibida | 21 |
| MIDR-01 | MIDR / Defesa Civil Nacional – serviço gov.br "Solicitar o recebimento de avisos e alertas" | HTML | CC BY-ND 3.0 (rodapé do portal gov.br) | 2 |
| MIDR-02 | MIDR – nota "kit de emergência é medida preventiva" (nov/2026) | HTML | CC BY-ND 3.0 (rodapé do portal gov.br) | 4 |
| MIDR-03 | Defesa Civil Nacional – "medidas de autoproteção em casos de alagamento" (gov.br) | HTML | CC BY-ND 3.0 (rodapé do portal gov.br) | 5 |
| MCID-01 | Ministério das Cidades – Cartilha de Prevenção (deslizamentos e inundações) | PDF | CC BY-ND 3.0 (portal gov.br onde o PDF está hospedado) | 7 |
| ABR-01 | Agência Brasil (EBC) – "Defesa Civil diz não haver motivo para pânico por kit de emergência" | HTML | Rodapé declara "Todos os direitos reservados pela EBC" (ver termos de uso da EBC); uso educacional com citação | 2 |
| FGTS-01 | CAIXA/FGTS – guia rápido "Solicitar o saque calamidade pelo app FGTS" | PDF | Conteúdo público de órgão oficial (sem licença explícita); uso educacional com citação da fonte | 3 |
| **Total** | 14 fontes | 9 HTML / 5 PDF | | **101** |

As URLs completas estão em `fontes.csv` e, por trecho, em `trechos.jsonl`.

## Assuntos cobertos

- **Antes, durante e depois** de enchentes e alagamentos: móveis no alto, documentos, tomadas, carro, ruas alagadas, evacuação.
- **Estados de criticidade do CGE:** observação, atenção, alerta e alerta máximo, com as cores do mapa.
- **Telefones e canais:** 199, 193, 190, 192, 156, 136, Disque-Intoxicação, Defesa Civil Estadual, CGE 24 h; SMS 40199, WhatsApp, Telegram, TV por assinatura e Defesa Civil Alerta (cell broadcast).
- **Deslizamentos:** sinais, prevenção na encosta, lona preta.
- **Saúde:** água de beber, alimentos, leptospirose, tétano, animais peçonhentos, doenças em abrigos, saúde mental.
- **Limpeza da casa:** caixa d'água, pisos, utensílios e cuidados com a água sanitária.
- **Kit de emergência** de 72 horas.
- **Grupos que precisam de atenção:** idosos, pessoas com deficiência, crianças e animais de estimação.
- **Saque calamidade do FGTS:** passo a passo e documentos.

## Limitações conhecidas

- **Dosagens diferentes entre fontes oficiais.** Para desinfetar pisos e objetos, as fontes não concordam:
  - Defesa Civil municipal: 1 copo para 20 L;
  - SEMIL: 200 mL para 20 L, por 30 min;
  - Secretaria Municipal da Saúde: 400 mL para 20 L, por 30 min;
  - Ministério da Saúde: 400 mL para 20 L, por 15 min.

  Também muda o tempo de espera após colocar 2 gotas de hipoclorito por litro: 30 min no Ministério da Saúde e 10 min na Secretaria Municipal da Saúde, depois de ferver. Cada trecho mantém o texto da sua fonte, e o assistente deve citar a fonte da dosagem que usar.
- **Assuntos que não estão na base:**
  - valor máximo e prazo do saque calamidade do FGTS (o guia da CAIXA não traz esses dados);
  - endereços de abrigos;
  - auxílios municipais;
  - previsões e dados de bairros específicos.

  Perguntas sobre esses temas devem receber "não consta".
- **Fontes antigas.** DCSP-01 é uma nota de imprensa de 2011 da Defesa Civil Estadual, e MS-03 é de 2017. O conteúdo ainda vale como orientação, mas não é recente.
- **Fonte de imprensa.** ABR-01 é da Agência Brasil, empresa pública de comunicação. Foi incluída porque traz a lista de itens do kit de 72 h divulgada pela Defesa Civil Nacional, que a nota do MIDR (MIDR-02) não detalha.
