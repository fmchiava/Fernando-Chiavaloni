# Matriz de rastreabilidade

| Requisito | Risco | Cenário automatizado | Evidência esperada |
| --- | --- | --- | --- |
| Compra completa com confirmação | R-02, R-07 | `e2e-purchase.spec.ts` em Chromium/Firefox/WebKit | Relatório Playwright + API GET + assert SQL |
| Produtos e preço coerentes | R-03 | `GET /produtos retorna 200` | JSON com `sku-1`, 12.990 centavos |
| Pedido válido e consulta | R-02, R-03 | `POST /pedidos retorna 201` | Schema Zod, GET 200, `APROVADO` |
| Pedido inválido recusado | R-03 | `POST /pedidos rejeita quantidade inválida` | HTTP 400, `invalid_order` |
| Escrita exige Bearer | R-04 | `rotas de carrinho e pedido recusam` | HTTP 401 em ambas |
| Titularidade do pedido | R-01 | `IDOR: outro usuário não consegue consultar` | 404 para usuário B, 200 para A |
| SQL parametrizado | R-05 | `SQL Injection em login e busca` | Login 401, busca vazia, catálogo íntegro |
| Latência e erros sob carga | R-06 | `order-load-test.js` | k6 HTML/JSON, thresholds verdes |
| Reprodutibilidade | R-08 | `e2e-pipeline.yml` | Run verde e artefato HTML |

Os nomes das linhas correspondem aos títulos dos testes no relatório Playwright. [Execução observada](evidence/execution.md) · [Defeito e reteste](defects/QA-001-idor.md).
