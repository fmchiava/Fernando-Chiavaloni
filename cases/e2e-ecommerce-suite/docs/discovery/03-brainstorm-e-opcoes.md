# Brainstorm retrospectivo: opções e critérios

Esta análise compara caminhos **agora**, com o sistema já existente. Não representa uma reunião histórica nem consenso de stakeholders. O ponto de partida é o objetivo do portfólio: demonstrar avaliação de qualidade com UI, REST, persistência, segurança, carga e evidência reproduzível.

## Critérios usados

1. **Reprodução:** avaliador executa sem conta, serviço pago ou dados pessoais.
2. **Controle do defeito:** é possível provocar, investigar e retestar um erro específico.
3. **Oráculos independentes:** a saída não depende apenas da própria UI.
4. **Custo de manutenção:** complexidade proporcional ao valor demonstrado.
5. **Representatividade:** fluxos e riscos transferíveis para sistemas reais, sem alegar equivalência de escala.

## Alternativas comparadas

| Tema | Opções | Escolha presente no código e motivo | Custo assumido |
| --- | --- | --- | --- |
| Alvo de teste | API pública; plataforma completa de e-commerce; mock local | **Mock local**: determinismo, sem dependência externa e permite falha controlada. [ADR-001](decisions/ADR-001-alvo-local.md). | Menor realismo operacional. |
| Persistência | Dados só em memória; SQLite em arquivo; PostgreSQL | **SQLite em arquivo**: SQL verificável entre servidor e teste sem serviço adicional. [ADR-002](decisions/ADR-002-persistencia.md). | Escrita concorrente e escala diferem de um banco de produção. |
| Automação | Só UI; só API; UI+API+SQL | **UI+API+SQL**: triangula confirmação, contrato e persistência. Playwright/TypeScript oferece um runner único; POM isola navegação. [ADR-003](decisions/ADR-003-automacao.md). | Mais pontos de integração no teste E2E. |
| Especificação | Casos em texto livre; Gherkin + runner Cucumber; Gherkin como especificação + Playwright | **Gherkin como especificação**: linguagem de negócio e rastreabilidade sem duplicar execução. [ADR-004](decisions/ADR-004-bdd.md). | Mapeamento manual precisa ser revisto. |
| Carga | Sem teste; script ad hoc; k6 com gate | **k6**: perfil e thresholds versionados, saída que falha a CI. [ADR-005](decisions/ADR-005-carga-e-evidencia.md). | Métrica local não define capacidade de produção. |
| Segurança do pedido | Confiar no total/ID do cliente; recalcular e verificar titular | **Servidor recalcula e autoriza**: protege integridade de valor e acesso. [ADR-006](decisions/ADR-006-integridade-e-acesso.md). | Políticas comerciais e de autorização reais precisam ser refinadas. |

## Example Mapping reconstruído para REQ-04

| Tipo | Conteúdo |
| --- | --- |
| História | Como cliente autenticado, quero concluir a compra para obter confirmação do pedido. |
| Regra | O servidor calcula o total usando preço do catálogo e quantidade válida. |
| Exemplos | Uma unidade de `sku-1` → 12.990 centavos; quantidade zero → 400; total enviado como 1 → persistência em 12.990. |
| Perguntas | O preço congela no carrinho? Qual tratamento de promoção? Um POST repetido após timeout é idempotente? |

Os exemplos estão refletidos em [BDD](../qa/bdd/README.md) e testes. As perguntas não viraram regras por inferência; constam das [hipóteses](01-problema-e-fontes.md) e do [backlog](04-refinamento-backlog.md). Esse formato segue o [Example Mapping do Cucumber](https://cucumber.io/docs/bdd/example-mapping/).
