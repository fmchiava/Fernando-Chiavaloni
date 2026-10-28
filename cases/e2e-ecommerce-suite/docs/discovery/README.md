# Descoberta e refinamento do case

Esta trilha explica **por que** a loja sintética foi delimitada assim e **como** uma equipe de produto, desenvolvimento e QA poderia amadurecer seus requisitos. O case foi construído antes deste registro; portanto, esta é uma **análise retrospectiva do código, dos testes e das evidências**, não uma ata de entrevistas, workshops ou aprovações que não ocorreram.

## Ordem de leitura

1. [Problema, fontes e hipóteses](01-problema-e-fontes.md): objetivo, atores, fontes consultadas e perguntas abertas.
2. [Levantamento de requisitos](02-levantamento-requisitos.md): técnicas, critérios de qualidade e exemplos verificáveis.
3. [Brainstorm e alternativas](03-brainstorm-e-opcoes.md): opções consideradas agora e critérios de comparação.
4. [Refinamento do backlog](04-refinamento-backlog.md): fatias de entrega, prioridade, Definition of Ready e Definition of Done.
5. [Decisões de arquitetura](decisions/README.md): justificativas, custos e gatilhos de revisão.
6. [Requisitos normativos e cobertura](../qa/contexto-e-requisitos.md): IDs REQ/NFR vigentes e [rastreabilidade](../qa/traceability.md).

## Regra de evidência

| Marca | Significado | Uso neste dossiê |
| --- | --- | --- |
| **Observado** | Existe no código, teste, configuração ou saída versionada. | Rotas, schemas, persistência, thresholds e asserts. |
| **Reconstruído** | Interpretação técnica formulada após a implementação. | Problema, motivação e comparação de alternativas. |
| **Hipótese** | Decisão de produto sem validação externa. | Valor para usuário, prioridade e política de negócio. |
| **Proposto** | Atividade futura, ainda não executada. | Entrevistas, novos testes e refinamentos. |

Uma decisão técnica registrada aqui descreve o **estado implementado e sua justificativa atual**; não atesta que a mesma justificativa foi documentada antes da codificação. Para resultados de testes, use o [relatório de execução](../qa/evidence/execution.md). Para um release real, hipóteses de negócio e metas de serviço precisariam de confirmação de quem responde pelo produto.

## Referenciais de método

- [Cucumber: Example Mapping](https://cucumber.io/docs/bdd/example-mapping/) para discutir história, regra, exemplo e pergunta antes de escrever cenários.
- [Scrum Guide](https://scrumguides.org/scrum-guide) para refinamento contínuo do Product Backlog; as definições locais de Ready e Done abaixo são convenções do case, não regras obrigatórias do Scrum.
- [Playwright: Page Object Models](https://playwright.dev/docs/pom) e [k6: thresholds](https://grafana.com/docs/k6/latest/using-k6/thresholds/) para decisões de implementação e gate.
