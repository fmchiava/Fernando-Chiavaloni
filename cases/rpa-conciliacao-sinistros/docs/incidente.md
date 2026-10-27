# 7. Simulador de crise: falha intermitente em produção

> História fictícia para entrevista. Números, horários e resultados abaixo descrevem uma **simulação**; não representam incidente real.

## Sintoma e impacto

Às 10h02, a operação percebe sinistros válidos encaminhados indevidamente à revisão quando o serviço de cobertura oscila. O defeito aparece em aproximadamente um a cada três lotes de pico. O comportamento incorreto da versão hipotética anterior era tratar HTTP 503 como “sem cobertura”; isso misturava **exceção técnica** com **exceção de negócio** e poderia gerar uma decisão falsa.

## Investigação conduzida pelo QA

1. **Conter:** suspender novas decisões automáticas e preservar `run_id`, IDs dos itens e versão do bot. Itens já afetados seguem revisão humana; nenhum estorno automático sem autorização.
2. **Correlacionar:** cruzar eventos do bot, Activity/Audit Log do Control Room, chamadas REST e horário UTC. Identificar que o caso falhou na validação de cobertura antes da gravação.
3. **Isolar hipóteses:** conferir se houve mudança de seletor ou carregamento lento da UI; comparar screenshot e DOM. Conferir CSV e valores em centavos. Nesses casos, UI e arquivo estavam estáveis; a anomalia era HTTP 503 intermitente, seguido de 200 em nova tentativa.
4. **Reproduzir:** executar `python app.py --db runs/crise-repro.db --fault first` e `python qa_demo.py --claim-id SIN-001 --out runs/repro`. Verificar `api_retry` na tentativa 1 e `CONCILIATED/MATCHED` após a resposta 200.
5. **Testar limite:** com `--fault always`, limitar a duas tentativas. O item deve ficar `PENDING`, o relatório deve registrar erro técnico e o gate técnico deve ser `NO_GO`.

## Causa raiz e correção

**Causa raiz simulada:** a regra anterior dependia apenas do conteúdo/ausência de dados da resposta e não separava status HTTP transitório de apólice sem cobertura. O ajuste classifica 404 como apólice não encontrada, 429/5xx/timeout como falha técnica com retry limitado, e mantém o item pendente após esgotar tentativas. A escrita usa chave idempotente; após salvar, uma leitura independente confirma o estado.

Não se aplica “retry infinito”: isso ampliaria carga no serviço degradado e esconderia incidente. O backoff do demonstrador é curto para testes; em produção, intervalos, limite e circuit breaker devem respeitar SLA e capacidade do serviço.

## Validação da correção

| Prova | Critério |
|---|---|
| CT-07 transitório | Um 503, depois 200; nenhuma falsa recusa; decisão correta e log de retry |
| CT-08 persistente | 503 em todas as tentativas; item `PENDING`; `NO_GO` |
| CT-12 reprocessamento | Mesmo request ID não duplica; decisão divergente retorna 409 |
| Regressão | Happy path, divergência financeira e apólice inativa continuam corretos |
| HML A360 | Repetir em Bot Runner e Control Room com seleção de UI, Vault, logs e captura real |

## Parecer técnico de re-liberação

**Resultado da prova local:** recomendação de avançar para homologação A360 quando CT-07, CT-08, CT-12 e regressão estiverem verdes, com evidências hashadas. **Resultado para produção real:** `NO_GO` até reproduzir a correção no bot efetivo, validar controles de UI e segurança, concluir smoke e obter aprovações do checklist. Risco residual: novas classes de erro HTTP ou mudanças de contrato podem exigir ajuste na classificação e monitoramento.

**Narrativa curta para entrevista:** “Separei o sintoma de negócio da falha técnica, preservei a trilha de execução e reproduzi o 503 de forma determinística. Impedi que indisponibilidade virasse uma decisão falsa, validei retry limitado e idempotência, rodei regressão e só então emiti um parecer condicionado às provas em homologação.”
