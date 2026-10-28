# Matriz de rastreabilidade e estado de cobertura

A matriz conecta a conversa de negócio aos asserts executados. “Evidência” aponta para o [relatório observado](evidence/execution.md), para o [defeito](defects/QA-001-idor.md) ou para o artefato da CI indicado no relatório. Os `.feature` são especificações; a coluna “teste” é o que `npm test` realmente executa.

| Regra | Risco | BDD | Teste automatizado / assert principal | Estado |
| --- | --- | --- | --- | --- |
| REQ-01 login válido | R-05 | BDD-01, BDD-08 | `e2e-purchase.spec.ts` e `api-contracts.spec.ts`: acesso com token | Parcial: não há teste dedicado para todas as credenciais inválidas |
| REQ-02 catálogo/preço | R-03 | BDD-02 | `api-contracts.spec.ts`: GET 200 e `sku-1` a 12990 | Coberto para dados iniciais |
| REQ-02 busca segura | R-05 | BDD-07 | `auth-security.spec.ts`: fragmento SQL → lista vazia e catálogo com 2 produtos | Coberto para a amostra adversarial |
| REQ-03 carrinho | R-02, R-04 | BDD-01, BDD-05 | `e2e-purchase.spec.ts`: 1 item e total; `auth-security.spec.ts`: 401 sem Bearer e sem pedido gravado | Parcial: falta teste isolado do POST válido e de ausência de escrita no carrinho válido |
| REQ-04 pedido válido/contrato | R-02, R-03 | BDD-01, BDD-08 | `api-contracts.spec.ts`: POST 201, Zod, GET 200, `APROVADO`; UI/API/SQL no E2E | Coberto para 1 unidade |
| REQ-04 quantidade inválida | R-03 | BDD-03 | `api-contracts.spec.ts`: quantidade 0 → 400 `invalid_order` | Parcial: limite superior 10/11 não exercitado |
| REQ-04 preço de servidor | R-02 | BDD-04 | `api-contracts.spec.ts`: total 1 enviado → API e SQLite 12990 | Coberto |
| REQ-04 escrita autenticada | R-04 | BDD-05 | `auth-security.spec.ts`: POST carrinho/pedido 401; contagem SQL inalterada | Coberto para ausência de Bearer |
| REQ-05 titularidade | R-01 | BDD-06, BDD-08 | `auth-security.spec.ts`: Beta 404, Alfa 200; `api-contracts.spec.ts`: GET do titular | Parcial: GET sem token e ID inexistente sem teste dedicado |
| NFR-01 navegadores | R-07 | BDD-01 | `e2e-purchase.spec.ts` em Chromium, Firefox e WebKit | Coberto no ambiente automatizado |
| NFR-02 carga | R-06 | — | `order-load-test.js`: p95, falhas HTTP e checks com thresholds | Coberto para o perfil local de 50 VUs |
| NFR-03 CI e evidência | R-08 | — | `e2e-pipeline.yml`: instalação, typecheck, Playwright, k6 e upload | Coberto pela execução no `master` |
| NFR-04 diagnóstico | R-08 | — | Configuração Playwright: HTML, screenshot e trace somente em falha | Configurado; artefato com falha controlada não está na CI verde |

## Consultar o resultado

O [relatório de execução](evidence/execution.md) informa run, commit e contagens. O [QA-001](defects/QA-001-idor.md) preserva o ciclo vermelho/verde. O [parecer](release-decision.md) transforma as evidências em decisão. Uma linha parcial permanece parcial mesmo quando a suíte geral está verde.

## Próxima iteração proposta

Priorize (1) limites 10/11 de quantidade, (2) GET sem Bearer e ID inexistente, (3) carrinho válido sem escrita em `orders`, (4) apresentação monetária `pt-BR`. Para cada item: acrescente exemplo BDD, teste que falhe pela regra nova, correção mínima, reteste e atualização desta matriz.
