# Plano de performance — criação de pedidos

## Pergunta e perfil

O teste pergunta se o **mock local** continua criando pedidos corretos quando o número de usuários virtuais cresce. Ele não estima capacidade de uma arquitetura de e-commerce real. [`order-load-test.js`](../scenarios/order-load-test.js) autentica uma vez no `setup()` e envia um pedido de `sku-1` por iteração, com pausa de 1 segundo por VU.

| Etapa | Duração | VUs alvo |
| --- | --- | --- |
| Aquecimento/rampa | 30 s | 0 → 50 |
| Patamar | 10 s | 50 |
| Redução | 10 s | 50 → 0 |

O perfil `smoke` dura 6 s com 1 VU de pico e serve para confirmar que servidor e k6 iniciam. **O perfil de carga é o gate.** O runner [`run-performance.mjs`](run-performance.mjs) abre o servidor na porta 4174 com `.data/performance.sqlite`, aguarda `/health`, executa k6 e encerra o processo.

## Critérios definidos antes da execução

| Métrica | Limiar | Leitura correta |
| --- | --- | --- |
| `http_req_duration{endpoint:order}` | p(95) < 500 ms | 95% das chamadas de criação marcadas devem terminar abaixo de 500 ms |
| `http_req_failed{endpoint:order}` | rate < 0,01 | Menos de 1% das criações devem falhar no sentido HTTP do k6 |
| `checks` | rate > 0,99 | Mais de 99% das respostas devem cumprir o check de HTTP 201 |

O login de preparo não integra o subgrupo `endpoint:order`. O k6 retorna exit code não zero quando um threshold falha, interrompendo o gate da CI. Os limites são de **demonstração**, não SLO acordado com um serviço real. A sintaxe e o comportamento de falha seguem a [documentação oficial de thresholds do k6](https://grafana.com/docs/k6/latest/using-k6/thresholds/).

## Executar e investigar

Na pasta do case, com k6 instalado: `npm run test:performance`. Leia `performance/results/summary.json` para as métricas completas e `summary.html` para a visão rápida. O [relatório de execução](../../docs/qa/evidence/execution.md) preserva um exemplo local e links da CI. Se o p95 exceder 500 ms, compare taxa de erro, checks, uso da máquina, porta e banco antes de alterar o limite. O valor não deve ser ajustado depois da medição apenas para tornar o job verde.

O SQLite, o servidor e a geração de carga dividem a máquina local ou o runner; contenção de CPU/disco e variação de ambiente afetam latência. Não há aquecimento de cache controlado, rede distribuída ou múltiplas instâncias do serviço.
