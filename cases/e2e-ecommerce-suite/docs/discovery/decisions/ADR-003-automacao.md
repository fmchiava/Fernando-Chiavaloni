# ADR-003 — Playwright, Page Objects e oráculos entre camadas

**Status:** solução implementada; justificativa registrada retrospectivamente. **Escopo:** automação funcional.

**Contexto.** Uma confirmação na UI não basta para provar contrato e persistência. O case também precisa exercitar três motores de navegador e capturar falhas de modo reproduzível.

**Opções.** (A) só UI: maior aderência visual, diagnóstico mais lento. (B) só API: contrato rápido, jornada não verificada. (C) Playwright/TypeScript para UI e API, com SQL independente: mais cobertura e atribuição de falhas, com maior custo de manutenção.

**Decisão observada.** Opção C. O [runner](../../../playwright.config.ts) separa projeto API/segurança e jornada UI em Chromium, Firefox e WebKit; [Page Objects](../../../src/pages/) encapsulam navegação/locators; [Zod](../../../src/api/OrderSchema.ts) verifica o contrato; o [E2E](../../../src/tests/e2e-purchase.spec.ts) compara API/UI/SQLite. [Playwright recomenda Page Objects](https://playwright.dev/docs/pom) como organização possível para suites maiores.

**Consequências.** Falhas podem ser localizadas por camada e oráculo. A jornada completa custa mais tempo e pode falhar por ambiente; por isso regras simples também têm testes de API. O teste não prova todos os estados, como mostra a [matriz](../../qa/traceability.md).

**Verificação.** [Estratégia](../../qa/test-strategy.md), [matriz](../../qa/traceability.md), [execução](../../qa/evidence/execution.md).

**Reconsiderar quando** os Page Objects virarem abstração sem redução de duplicação, ou outra stack se tornar padrão obrigatório do produto.
