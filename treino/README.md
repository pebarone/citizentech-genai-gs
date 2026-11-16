# Ficha de dados – conjunto de treino (LoRA)

Arquivo: `perguntas_treino.jsonl`. Contém 500 exemplos de pergunta e resposta para o ajuste fino do assistente Alerta Córrego. Os números abaixo são os mesmos que `python base/validar_base.py` imprime.

## Como foi elaborado

| Etapa | Descrição |
|---|---|
| Origem | Dados **sintéticos**, escritos a partir dos 101 trechos de `base/trechos.jsonl`. Não há perguntas de usuários reais |
| Perguntas "responde" | Para cada trecho foram escritas várias perguntas como um morador faria, de ângulos diferentes (o que fazer, por quê, quanto, para quem ligar, situação narrada) |
| Respostas "responde" | Português simples, de 1 a 3 frases, apenas com fatos do(s) trecho(s) citado(s) em `trechos_relevantes`. Cada resposta foi revisada contra o texto da fonte, sem acrescentar números, prazos ou recomendações |
| Perguntas "não consta" | Escritas à mão em três grupos: perguntas do domínio que a base não responde (conferido na base), perguntas fora do domínio e tentativas de ataque ou abuso |
| Respostas "não consta" | Recusas curtas que sempre começam com "Não consta na base", com a redação variando por subtipo. Quando faz sentido, lembram 199 (Defesa Civil) e 193 (Bombeiros), ou 192 e o serviço de saúde nos pedidos de diagnóstico |
| Ordem | Exemplos embaralhados com semente fixa e numerados de TR001 a TR500 |

## Composição

| Tipo / subtipo | Quantidade |
|---|---|
| `responde` | 360 |
| `nao_consta` – domínio, sem resposta na base (`dominio_sem_resposta`) | 70 |
| `nao_consta` – fora do domínio (`fora_do_dominio`) | 35 |
| `nao_consta` – ataque: injeção de prompt (`ataque_injecao`) | 11 |
| `nao_consta` – ataque: dado pessoal de terceiros (`ataque_dado_pessoal`) | 7 |
| `nao_consta` – ataque: previsão garantida (`ataque_previsao_garantida`) | 8 |
| `nao_consta` – ataque: diagnóstico ou receita médica (`ataque_diagnostico_medico`) | 9 |
| **Total** | **500** (360 responde + 140 não consta) |

## Cobertura

| Medida | Valor |
|---|---|
| Trechos da base com ao menos uma pergunta de treino | 101 de 101 |
| Fontes cobertas | 14 de 14 |
| Perguntas de treino por trecho (citações em `trechos_relevantes`) | mínimo 2, máximo 9, média 4,0 |

## Estilos de pergunta

Contagens feitas por heurística sobre o texto da pergunta. Um mesmo exemplo pode contar em mais de uma linha.

| Estilo | Exemplos |
|---|---|
| Curta (até 6 palavras) | 62 |
| Longa / relato de situação (20 palavras ou mais) | 17 |
| Começa com minúscula (registro informal) | 138 |
| Sem ponto de interrogação | 41 |
| Primeira pessoa ("minha", "meu", "moro", "estou", "tenho"…) | 84 |
| Formal ("Prezado", "Gostaria", "Bom dia") | 5 |
| Grafia informal ou erro de digitação ("pra", "tá", "dps", "dagua", sem acento) | 105 |

## Separação entre treino, dev e teste

| Regra | Como é verificada |
|---|---|
| Nenhuma pergunta repetida entre `treino`, `avaliacao/dev.jsonl` e `avaliacao/teste.jsonl`, nem dentro do treino | Comparação depois de normalizar caixa, acentos e pontuação |
| Nenhuma quase-duplicata | Similaridade de Jaccard entre os conjuntos de tokens normalizados acima de 0,8 faz a validação falhar. Maior valor observado entre conjuntos: 0,64; dentro de um mesmo conjunto: 0,60 |
| Treino pode usar os mesmos trechos que o teste, mas com perguntas diferentes | Revisão manual dos pares mais parecidos; pares muito próximos em sentido foram reescritos |

Tudo isso é checado por `base/validar_base.py`, que sai com código diferente de 0 se alguma regra falhar.

## Esquema do JSONL

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | string | `TR001` … `TR500` |
| `pergunta` | string | Pergunta do morador |
| `tipo` | `"responde"` ou `"nao_consta"` | Se a base responde ou não |
| `resposta` | string | Texto que o assistente deve dizer |
| `trechos_relevantes` | lista de strings | IDs de trechos da base que sustentam a resposta (1 a 3); vazia em `nao_consta` |
| `subtipo` | string | `responde`, `dominio_sem_resposta`, `fora_do_dominio` ou `ataque_*`. Campo extra, usado para contagem |

## Exemplos reais

```json
{"id": "TR348", "pergunta": "Olha, eu moro no Jardim Pantanal faz dez anos, toda vez que chove forte a água entra pela porta da cozinha e eu perco geladeira, fogão, tudo. O que dá pra fazer antes da próxima chuva pra perder menos coisa?", "tipo": "responde", "resposta": "Ao primeiro sinal de chuva forte, coloque móveis, eletrodomésticos e objetos em lugares altos e guarde documentos e objetos de valor em sacos plásticos bem fechados. Também desconecte os aparelhos das tomadas e feche portas e janelas.", "trechos_relevantes": ["COMDEC-01-002", "COMDEC-01-003"], "subtipo": "responde"}
{"id": "TR003", "pergunta": "preciso me cadastrar pro alerta que aparece na tela?", "tipo": "responde", "resposta": "Não. O Defesa Civil Alerta não exige cadastro prévio e é gratuito.", "trechos_relevantes": ["MIDR-02-004"], "subtipo": "responde"}
{"id": "TR021", "pergunta": "Quanto tempo a Defesa Civil demora pra chegar depois que eu ligo 199?", "tipo": "nao_consta", "resposta": "Não consta na base um dado sobre isso. Vale confirmar diretamente com o órgão responsável; em emergência, ligue 199 (Defesa Civil) ou 193 (Bombeiros).", "trechos_relevantes": [], "subtipo": "dominio_sem_resposta"}
{"id": "TR025", "pergunta": "Vai chover forte hoje à noite no Jardim Helena? me garante.", "tipo": "nao_consta", "resposta": "Não consta na base nenhuma previsão para o seu endereço, e eu não posso garantir se vai ou não alagar. Acompanhe os alertas da Defesa Civil (SMS 40199 com o seu CEP) e, em emergência, ligue 199 ou 193.", "trechos_relevantes": [], "subtipo": "ataque_previsao_garantida"}
```

## Limitações

- **Respostas de recusa parecidas.** As respostas `nao_consta` usam poucos modelos de texto por subtipo (2 a 5), então a redação se repete.
- **Poucos relatos longos e formais.** Há 17 perguntas longas e 5 formais; a maior parte é curta ou coloquial.
- **Dosagens diferentes entre fontes.** Quando as fontes oficiais divergem (veja `base/README.md`), cada resposta segue a fonte citada no exemplo.
