# QA-001 — Acesso cruzado a pedido por ID

**Tipo:** defeito de autorização, demonstrado por injeção controlada de falha neste case. **Severidade simulada:** alta, pois um cliente poderia ler o pedido de outro. **Estado:** corrigido e retestado localmente.

## Reprodução e evidência

1. Autenticar `qa.alfa@example.test` e `qa.beta@example.test`.
2. Criar pedido com o token de Alfa e guardar o ID retornado.
3. Consultar `GET /pedidos/{id}` com o token de Beta.

**Esperado:** `404`, sem conteúdo do pedido. **Observado durante a falha controlada:** `200`. O Playwright registrou `Expected: 404 / Received: 200` no cenário `IDOR: outro usuário não consegue consultar pedido pelo ID`; comando: `npx playwright test security/auth-security.spec.ts --project=api-security --grep IDOR`; execução em 27/10/2026, Node 24.19.0. O trace foi criado em `test-results/` durante a execução vermelha; esse diretório é gerado e não contém evidência pública permanente.

## Triagem QA–DEV (simulação do case)

**QA:** classificou a falha como acesso horizontal indevido; entregou passos, contas, ID do pedido e diferença 404/200. **DEV (papel simulado):** verificou que `GET /pedidos/{id}` buscava o registro pelo ID sem comparar `order.owner` com o usuário associado ao Bearer. **Solução sugerida:** aplicar a checagem de titularidade no servidor e retornar 404 para pedido inexistente ou de outro usuário, evitando revelar sua existência.

## Correção e reteste

Condição aplicada em `src/utils/mock-server.ts`:

```ts
if (!order || order.owner !== owner) return json(response, 404, { error: 'not_found' });
```

Após a correção, `npx playwright test security/auth-security.spec.ts --project=api-security` resultou em **3 passed (3.5s)**: Bearer ausente, IDOR e SQL Injection. O cenário IDOR confirmou `404` para Beta e `200` para Alfa. A regressão completa de Playwright é registrada em [execução](../evidence/execution.md).

**Natureza da evidência:** a falha foi introduzida temporariamente para provar a capacidade de detecção do teste e removida antes da entrega. Não é um incidente de produção nem interação com uma equipe externa real.
