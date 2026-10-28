# ADR-004 — Gherkin como especificação, Playwright como execução

**Status:** solução implementada; justificativa registrada retrospectivamente. **Escopo:** comunicação e rastreabilidade.

**Contexto.** O case precisa mostrar regras de negócio em linguagem acessível e associá-las a testes. Executar os mesmos passos por Cucumber e Playwright adicionaria integração/duplicação sem benefício comprovado neste alvo pequeno.

**Opções.** (A) apenas títulos de testes: baixo custo, pouca leitura de negócio. (B) Cucumber executável: rastreio automático maior, runner e glue code adicionais. (C) arquivos Gherkin como especificação e matriz que aponta para Playwright: comunicação clara com manutenção manual.

**Decisão observada.** Opção C. Os [cenários](../../qa/bdd/README.md) usam IDs BDD; a [matriz](../../qa/traceability.md) liga cada ID ao assert executável ou à lacuna. O [verificador](../../../scripts/check-docs.mjs) confere IDs e links, mas não executa Gherkin. A distinção é explícita para não inflar contagens.

**Consequências.** O texto é legível em entrevista e o runner fica simples. Divergência semântica entre especificação e teste continua possível e requer revisão humana. O [Example Mapping](https://cucumber.io/docs/bdd/example-mapping/) orienta a conversa de regra, exemplo e dúvida.

**Verificação.** [Índice BDD](../../qa/bdd/README.md), [rastreabilidade](../../qa/traceability.md), `npm run docs:check`.

**Reconsiderar quando** houver muitos cenários compartilhados, stakeholders editando `.feature` continuamente ou necessidade concreta de execução Gherkin no pipeline.
