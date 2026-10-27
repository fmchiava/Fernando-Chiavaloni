# 8. Como apresentar o case na entrevista

## Pitch de 90 segundos

“Construí um case fictício de conciliação de sinistros de pequeno valor para mostrar como eu abordaria qualidade de uma automação RPA. O fluxo parte de uma fila web, consulta cobertura por API, confere pagamentos em CSV e persiste uma decisão idempotente. Modelei riscos de indisponibilidade, inconsistência e auditoria, converti os riscos em casos de teste e criei um simulador Python que reproduz uma falha 503 transitória e outra persistente. A primeira deve se recuperar; a segunda deve deixar o sinistro pendente. O pacote de evidências contém logs correlacionáveis e hashes. Também documentei a implementação equivalente em A360 e o gate de homologação. Como não usei um ambiente A360 neste repositório, separo claramente o que executei localmente do que ainda precisaria validar na plataforma.”

## Perguntas que o case ajuda a responder

1. **Como separar business exception de system exception?** Pela semântica do contrato, não pela ausência de dado. Apólice inativa e pagamento divergente vão para `REVIEW`; 503/timeout antes da escrita deixam `PENDING`. Se a confirmação após o envio falhar, o cliente marca `UNVERIFIED` e reconcilia o estado antes de reprocessar.
2. **Como investigar uma falha intermitente?** Correlacionar IDs e horários, comparar UI/API/arquivo, injetar falha determinística, validar hipótese e medir regressão.
3. **Como evitar dupla execução?** Chave idempotente, estado único no banco, consulta antes de repetir uma escrita e retorno 409 para conflito.
4. **O que é evidência suficiente?** Entrada versionada, esperado/observado, logs estruturados, estado final consultado, screenshot mascarada quando cabível, hash e parecer assinado.
5. **Quando você recomenda No-Go?** Falha crítica aberta, erro técnico que altera decisão de negócio, evidência insuficiente, ausência de rollback ou controles de segurança não validados.
6. **Qual o papel sênior no CoE?** Revisar requisitos e arquitetura, definir padrões e gates, orientar times, medir falhas recorrentes e proteger a rastreabilidade da decisão.

## O que demonstrar ao vivo

Abrir a fila em `/claims`, executar `--fault first` e mostrar o evento `api_retry` seguido de `decision_verified`. Repetir com `--fault always` e mostrar `PENDING` + `NO_GO`. Para o risco pós-escrita, usar `--fault verify_always` em banco novo: o relatório mostra `UNVERIFIED`, embora a decisão exista no SQLite. Apontar a matriz de riscos, os casos CT-07/08/10/12 e o parecer. Descrever quais evidências adicionais seriam exigidas numa homologação A360.

## Honestidade do portfólio

Declare como **implementado e testado**: serviço local, API, SQLite, cliente Python, testes de integração e artefatos sintéticos. Declare como **proposto**: bot A360, Credential Vault, papéis corporativos, screenshots reais, Control Room e aprovação de implantação. Não use este case para afirmar experiência de produção que ele não demonstra.
