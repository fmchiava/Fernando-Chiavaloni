# ADR-006 — Integridade de preço e acesso no servidor

**Status:** solução implementada; justificativa registrada retrospectivamente. **Escopo:** regras de pedido.

**Contexto.** Valor enviado pelo navegador e ID de pedido na URL são controláveis pelo cliente. Aceitá-los sem verificação poderia gravar preço incorreto ou expor pedido de outro usuário.

**Opções.** (A) confiar no total e ID da UI: implementação menor, integridade frágil. (B) recalcular total no servidor e checar titular a cada consulta: custo de validação/SQL, fronteira de confiança explícita.

**Decisão observada.** Opção B. O [servidor](../../../src/utils/mock-server.ts) valida itens com [Zod](../../../src/api/OrderSchema.ts), lê preço da tabela, ignora `totalCents` enviado e retorna 404 se o pedido não pertence ao usuário autenticado. O [banco](../../../src/db/database.ts) usa parâmetros SQL. Os testes cobrem preço adulterado, Bearer ausente, IDOR e amostras de entrada SQL.

**Consequências.** A amostra protegida reduz risco de manipulação e vazamento. Não constitui auditoria de segurança completa; políticas de promoção, sessão, rate limiting e autorização mais ampla seguem fora do escopo. O 404 para pedido alheio é uma hipótese de contrato [H-03](../01-problema-e-fontes.md), a confirmar num produto real.

**Verificação.** [Testes de segurança](../../../security/auth-security.spec.ts), [teste de preço](../../../src/tests/api-contracts.spec.ts), [QA-001](../../qa/defects/QA-001-idor.md).

**Reconsiderar quando** a política de acesso, preço ou autenticação for definida de outra forma pelo produto e por segurança.
