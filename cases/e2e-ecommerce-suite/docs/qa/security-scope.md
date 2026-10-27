# Escopo de segurança e fronteiras de confiança

| Entrada controlada pelo cliente | Fronteira | Controle exercitado |
| --- | --- | --- |
| `Authorization` ausente | POST carrinho/pedidos | 401 antes da escrita |
| ID de pedido de outro usuário | GET pedido → SQLite | Comparação de `owner` com identidade do Bearer; 404 |
| E-mail com fragmento SQL | Login → consulta de usuários | Parâmetro `?`; 401 sem bypass |
| Busca com fragmento SQL | Catálogo → consulta de produtos | Parâmetro `?`; resultado vazio e catálogo íntegro |
| Quantidade inválida | JSON → cálculo de preço | Zod + HTTP 400 |

Os riscos mapeiam acesso indevido, autenticação e injeção (OWASP A01, A07 e A05). O token de sessão é aleatório e só existe na memória do mock; a senha sintética é armazenada como hash scrypt no SQLite. O preço é recalculado no servidor em centavos, sem confiar em valor fornecido pela UI.

**Limites deliberados do alvo de teste:** não há rate limit, expiração de sessão, TLS nem integração com identidade/pagamento real. São controles que um serviço de produção precisaria especificar e testar; este servidor roda somente em `127.0.0.1` com dados sintéticos. O caso não reivindica conformidade OWASP completa. [Teste automatizado](../../security/auth-security.spec.ts) · [risco e critério](test-strategy.md).
