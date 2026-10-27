# Plano de QA e estratégia de testes

## Missão e critérios

Verificar que um cliente autenticado consegue comprar um produto, recebe confirmação coerente na UI/API e encontra o pedido correto no SQLite. O gate também precisa impedir acesso cruzado a pedidos, requisições sem Bearer e consultas alteradas por entrada maliciosa. Sob a carga local definida, p95 deve ficar abaixo de 500 ms e a taxa de falhas HTTP abaixo de 1%.

**Escopo:** UI de login/catálogo/checkout, contratos HTTP e Zod, SQLite, segurança de autenticação/autorização/consulta, k6 e CI. **Fora do escopo:** pagamento real, antifraude, provedores externos, escalabilidade distribuída e testes em dispositivos móveis físicos.

## Matriz de riscos

| ID | Risco | Impacto | Probabilidade | Controle e evidência |
| --- | --- | --- | --- | --- |
| R-01 | Pedido de outro cliente acessível por ID | Alto | Média | Teste IDOR com duas contas; resposta 404 ao segundo usuário |
| R-02 | UI confirma compra sem persistência ou com valor errado | Alto | Média | Fluxo UI → GET API → consulta SQL; total literal de 12.990 centavos |
| R-03 | Alteração de contrato sem quebra de status HTTP | Médio | Média | Parse Zod do pedido criado e consultado |
| R-04 | Ausência de Bearer aceita escrita | Alto | Média | POST no carrinho e pedido sem token deve retornar 401 |
| R-05 | Campo de busca/login altera consulta SQL | Alto | Baixa | Entradas com aspas/SQL; consultas parametrizadas; catálogo íntegro |
| R-06 | Concorrência degrada ou falha na criação | Médio | Média | k6 com 50 VUs e thresholds; banco de performance separado |
| R-07 | Diferença entre navegadores quebra checkout | Médio | Média | Mesmo E2E em Chromium, Firefox e WebKit |
| R-08 | CI não reproduz ambiente local | Médio | Média | `npm ci`, Node 24, navegadores e k6 instalados no workflow |

## Desenho dos testes

| Nível | Técnica | Oráculo |
| --- | --- | --- |
| UI E2E | Page Object Model e seletores por papel/label | Navegação, carrinho, confirmação e ID do pedido |
| API/contrato | Requisição HTTP real ao mock + Zod | Status 200/201/400, JSON e campos tipados |
| Persistência | SQL em conexão separada | `owner`, `status='APROVADO'`, `totalCents=12990` |
| Segurança | Particionamento de autorização e entrada adversarial | 401/404, sem bypass de login ou busca |
| Performance | Ramping VUs e thresholds k6 | p95 < 500 ms; erro HTTP < 1%; checks > 99% |

Os testes de API/segurança rodam uma vez; o teste de UI roda em três navegadores. Pedidos são criados por teste e identificados pelo ID retornado, sem depender de uma ordem de execução. Capturas de falha e traces são produzidos pelo Playwright; relatório HTML e resumo k6 são gerados pela CI.

## Critérios de entrada e saída

**Ready para testar:** Node 24+, lockfile resolvido por `npm ci`, navegadores disponíveis, mock local saudável em `/health`, massa sintética inicializada e porta livre. **Go:** typecheck sem erros, Playwright 100% verde, thresholds k6 verdes, defeitos críticos/altos abertos = 0, artefatos publicados. **No-Go:** qualquer falha de contrato, segurança, persistência, navegador ou threshold; indisponibilidade de artefato; teste não executado sem justificativa.

Quando um teste falha, o QA registra comando, ambiente, resultado esperado/obtido, evidência e impacto. Após a correção, executa primeiro o cenário que falhou, depois a regressão completa e atualiza o [parecer](release-decision.md).
