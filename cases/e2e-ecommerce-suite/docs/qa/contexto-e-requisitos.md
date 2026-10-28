# Contexto do processo e critérios de aceite

## Problema e objetivo

Uma loja de demonstração precisa aceitar a compra de um produto por um cliente autenticado. Um pedido confirmado deve ter o mesmo identificador, titular, situação e valor quando observado pela interface, pela API e pelo banco. O processo foi reduzido ao mínimo para que a investigação de QA seja reproduzível: não há cobrança, estoque, entrega ou antifraude. **“APROVADO” significa que o mock aceitou e gravou o pedido; não significa pagamento liquidado.**

Há dois clientes sintéticos, Alfa e Beta. O catálogo inicial contém `sku-1` (Fone de ouvido, 12.990 centavos) e `sku-2` (Mouse sem fio, 7.990 centavos). O preço é mantido em centavos; o servidor é a fonte do valor cobrado.

## Jornada observável

1. O cliente entra com e-mail e senha e recebe uma sessão Bearer temporária.
2. Consulta o catálogo e adiciona um produto ao carrinho.
3. Confere o total apresentado e finaliza o pedido.
4. Recebe a confirmação com ID; um consumidor da API pode consultar o mesmo pedido.
5. O QA compara a resposta com uma consulta SQL independente, incluindo titular, status e total.

## Regras funcionais

| ID | Regra e critério verificável | Situação da cobertura |
| --- | --- | --- |
| REQ-01 | Login válido retorna HTTP 200 e token; tentativa inválida retorna HTTP 401 sem criar sessão útil. | Parcial: login válido em fluxos API/UI; entrada com SQL em e-mail retorna 401. Outros tipos de credencial inválida não têm cenário dedicado. |
| REQ-02 | `GET /produtos` retorna HTTP 200 com preço em centavos; busca textual filtra o catálogo sem alterar dados. | Coberto para catálogo inicial e busca adversarial. |
| REQ-03 | `POST /carrinho` exige Bearer; para item válido, calcula o total do catálogo e retorna HTTP 200. | Parcial: UI percorre o carrinho; teste isolado prova 401 e ausência de escrita para requisição sem token. |
| REQ-04 | `POST /pedidos` exige Bearer, aceita quantidade inteira de 1 a 10, ignora total informado pelo cliente, responde HTTP 201 e grava pedido `APROVADO` com titular e valor calculado no servidor. | Coberto para 1 unidade, quantidade 0, total adulterado e ausência de token. O limite superior 10 e concorrência de escrita não têm assert funcional específico. |
| REQ-05 | `GET /pedidos/{id}` retorna HTTP 200 ao titular; retorna 404 a outro cliente ou ID inexistente; sem Bearer retorna 401. | Parcial: titular e acesso cruzado cobertos; ID inexistente e ausência de token no GET não têm teste dedicado. |

O contrato retornado pelo pedido contém `id`, `owner`, `status`, `totalCents`, `items` e `createdAt`. O teste de contrato usa Zod para verificar formato; o E2E compara valor e titular no SQLite. Os endpoints e formatos derivam de [`OrderSchema.ts`](../../src/api/OrderSchema.ts) e [`mock-server.ts`](../../src/utils/mock-server.ts).

## Requisitos não funcionais

| ID | Critério | Como é medido |
| --- | --- | --- |
| NFR-01 | O fluxo de compra passa em Chromium, Firefox e WebKit. | Mesmo teste UI em três projetos Playwright. |
| NFR-02 | No perfil local de carga, p95 da criação de pedidos < 500 ms; falhas HTTP < 1%; checks > 99%. | Thresholds k6 sobre chamadas marcadas `endpoint:order`. |
| NFR-03 | A CI instala dependências pelo lockfile, executa typecheck, Playwright e k6 e publica relatórios. | GitHub Actions `e2e-pipeline.yml` e artefato `e2e-ecommerce-evidence`. |
| NFR-04 | Uma falha de teste gera informação suficiente para investigação. | Lista e HTML Playwright; screenshot e trace retidos em falhas; registro de defeito vinculado. |

## Escopo assumido e pontos de evolução

O alvo roda apenas em `127.0.0.1` e usa contas `.test`. Não se testa pagamento, integração externa, dispositivos físicos, TLS, expiração de sessão, rate limiting ou capacidade de produção distribuída. A UI mostra `R$ 129.90`, com ponto decimal; a formatação `pt-BR` é uma melhoria de apresentação, não um critério aprovado neste ciclo. Os itens de cobertura parcial constam da [rastreabilidade](traceability.md) e dos riscos residuais do [parecer](release-decision.md).
