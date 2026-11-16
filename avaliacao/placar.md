# Placar

| Configuração        | Acurácia global   | Acerto (responde)   | Fatos cobertos   | Precisão quando responde   | Recusa correta (não consta)   | Alucinação   | Erro factual   | Recusa indevida   | JSON válido (estrito)   | Citação correta   |   Latência média (ms) |   Latência p95 (ms) |
|---------------------|-------------------|---------------------|------------------|----------------------------|-------------------------------|--------------|----------------|-------------------|-------------------------|-------------------|-----------------------|---------------------|
| sem_contexto        | 30.0%             | 0.0%                | 4.4%             | 0.0%                       | 100.0%                        | 0.0%         | 19.1%          | 81.0%             | 100.0%                  | 0.0%              |                  3580 |                5558 |
| rag                 | 66.7%             | 52.4%               | 57.1%            | 73.3%                      | 100.0%                        | 0.0%         | 19.1%          | 28.6%             | 100.0%                  | 71.4%             |                  5170 |               10844 |
| rag_lora            | 66.7%             | 52.4%               | 67.5%            | 56.4%                      | 100.0%                        | 0.0%         | 40.5%          | 7.1%              | 100.0%                  | 85.7%             |                  7488 |               12703 |
| rag_sem_limiar      | 66.7%             | 52.4%               | 57.1%            | 73.3%                      | 100.0%                        | 0.0%         | 19.1%          | 28.6%             | 100.0%                  | 71.4%             |                  5030 |                8586 |
| rag_lora_sem_limiar | 66.7%             | 52.4%               | 67.5%            | 56.4%                      | 100.0%                        | 0.0%         | 40.5%          | 7.1%              | 100.0%                  | 85.7%             |                  8797 |               11395 |

Gerado em 2026-11-15T20:58:10. Conjunto: teste.jsonl.

- Acerto (responde): todos os fatos-chave presentes e sem recusa.
- Fatos cobertos: média da fração de fatos-chave presentes (crédito parcial; recusa = 0).
- Precisão quando responde: das perguntas `responde` que o modelo não recusou, quantas acertou.
- Recusa correta / Alucinação: sobre as perguntas `nao_consta` (somam 100%).
- Erro factual e recusa indevida: sobre as perguntas `responde`.
- JSON válido (estrito): `json.loads` do texto bruto + exatamente os 3 campos, sobre as chamadas à LLM (recusas pelo limiar não chamam a LLM).
- Citação correta: `responde` em que `fontes` contém um trecho relevante e nenhum id fora do contexto.
- Linhas `*_sem_limiar`: mesmas configurações com o portão por similaridade desligado.
