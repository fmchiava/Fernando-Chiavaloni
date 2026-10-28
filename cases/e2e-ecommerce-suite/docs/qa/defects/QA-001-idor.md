# QA-001 — Consulta de pedido de outro cliente por ID

| Campo | Registro |
| --- | --- |
| Tipo e estado | Defeito de autorização **demonstrado por mutação controlada**; corrigido e retestado |
| Regra e risco | REQ-05; R-01; BDD-06 |
| Severidade / prioridade | S2 alta / P1, classificações simuladas para o case |
| Ambiente | Mock local, duas contas `.test`, Node 24.19.0, Playwright 1.64.1, 27/10/2026 |
| Comando | `npx playwright test security/auth-security.spec.ts --project=api-security --grep IDOR --reporter=list` |
| Frequência | Reproduzido uma vez na mutação controlada; reteste isolado passou |

## Pré-condição e passos mínimos

1. Iniciar o mock com Alfa e Beta e autenticar as duas contas.
2. Criar um pedido com o Bearer de Alfa; guardar o ID retornado.
3. Solicitar `GET /pedidos/{id}` com o Bearer de Beta.
4. Consultar o mesmo ID com o Bearer de Alfa como controle positivo.

**Esperado:** Beta recebe 404 sem detalhes do pedido; Alfa recebe 200. **Observado durante a falha controlada:** Beta recebeu 200. O teste registrou `Expected: 404 / Received: 200` na [saída vermelha sanitizada](../evidence/QA-001-red-sanitized.txt). O caminho absoluto da máquina foi substituído por `<case>`; a saída original continha apenas dados sintéticos. Um trace foi gerado em `test-results/` nessa execução e não foi preservado no Git.

## Análise de causa e interação QA–DEV

Na demonstração, a checagem de titularidade em `GET /pedidos/{id}` foi removida temporariamente. O servidor ainda reconhecia um Bearer válido, mas devolvia o registro localizado pelo ID sem comparar `order.owner` à identidade autenticada. O risco é **acesso horizontal indevido**: autenticação, sozinha, não autoriza ler o pedido de outra pessoa.

**QA (papel simulado):** trouxe dois usuários, ID, resposta 200 indevida e critério 404. **DEV (papel simulado):** localizou a comparação ausente e restaurou a regra no servidor. A conversa descreve a triagem técnica do exercício; não representa comunicação com uma equipe externa.

## Correção, reteste e decisão

O código entregue em [`mock-server.ts`](../../../src/utils/mock-server.ts) devolve 404 quando o pedido inexiste ou o titular difere:

```ts
if (!order || order.owner !== owner) return json(response, 404, { error: 'not_found' });
```

A mutação e sua restauração foram locais; **não existe um commit separado de “correção DEV”** para a falha injetada. A versão integrada ao `master` no merge `041c4c3` contém a checagem. O [reteste isolado](../evidence/QA-001-green-sanitized.txt) registrou **1 passed (3.3s)**; o teste verifica 404 para Beta e 200 para Alfa. A [regressão completa](../evidence/execution.md) passou nas 10 execuções Playwright, inclusive na CI do `master`.

**Parecer do QA neste experimento:** defeito controlado encerrado após reteste e regressão. Isso comprova a sensibilidade do cenário a essa remoção específica de autorização; não é um incidente de produção nem uma prova de cobertura universal contra IDOR. A [política de TDD](../tdd.md) distingue a demonstração Red/Green da história de desenvolvimento.
