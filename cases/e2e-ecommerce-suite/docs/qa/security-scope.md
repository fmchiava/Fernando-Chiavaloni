# Segurança: ameaças, testes e limites

## Modelo de confiança

O navegador e o cliente REST podem alterar campos, URL, quantidade, total enviado e cabeçalho `Authorization`. O servidor deve decidir identidade, autorização, validade dos itens e preço antes de gravar ou devolver um pedido. O SQLite é persistência interna, não substitui a autorização por requisição. O alvo só escuta em `127.0.0.1` e utiliza dados sintéticos.

| Ameaça | Fronteira/entrada | Teste efetivo | Resultado exigido |
| --- | --- | --- | --- |
| Escrita anônima | POST `/carrinho` e `/pedidos` sem Bearer | `auth-security.spec.ts` | 401 em ambas; contagem SQL da massa de prova inalterada |
| IDOR horizontal | ID do pedido de Alfa consultado por Beta | `auth-security.spec.ts` e QA-001 | 404 para Beta; 200 para Alfa |
| Injeção no login | E-mail com `' OR 1=1 --` | `auth-security.spec.ts` | 401; sem autenticação indevida |
| Injeção na busca | `search` com o mesmo fragmento | `auth-security.spec.ts` | Busca vazia; catálogo completo ainda com dois produtos |
| Preço adulterado | `totalCents: 1` no POST | `api-contracts.spec.ts` | API e SQLite mostram 12.990 centavos |
| Item inválido | Quantidade zero | `api-contracts.spec.ts` | HTTP 400 e `invalid_order` |

O teste IDOR segue a técnica de usar dois titulares e consultar o mesmo identificador, descrita no [OWASP WSTG-ATHZ-04](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/05-Authorization/04-Insecure_Direct_Object_References/). Consultas SQL usam parâmetros `?`; a senha sintética fica como hash scrypt com salt no SQLite. Tokens são bytes aleatórios associados a e-mail em memória; não são persistidos. Esses detalhes explicam os controles implementados, mas não equivalem a uma auditoria de segurança completa.

## Cobertura residual

Não há testes de expiração/revogação de sessão, rate limiting, TLS, CSRF, enumeração extensa de IDs, payloads amplos de injeção, concorrência maliciosa ou revisão de dependências como gate separado. A UI guarda o token em `sessionStorage`, o que é aceitável apenas para este mock local; uma arquitetura real exigiria análise específica de sessão, transporte e exposição a scripts. A proteção contra SQL Injection foi exercitada com uma amostra controlada, não com uma campanha abrangente.

Uma falha de segurança com impacto em outro cliente é classificada como alta no [plano de riscos](test-strategy.md). O [QA-001](defects/QA-001-idor.md) mostra detecção e reteste; não relata incidente real. Para evoluir a cobertura, inclua caso BDD e teste antes de ampliar a afirmação de conformidade.
