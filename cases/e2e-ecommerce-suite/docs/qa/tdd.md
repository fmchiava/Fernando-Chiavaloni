# TDD e prova de sensibilidade dos testes

## Como aplicar TDD neste case

Test-Driven Development orienta uma alteração pequena de cada vez: listar exemplos, escrever um teste que falha pela razão esperada (**Red**), implementar o mínimo para fazê-lo passar (**Green**) e melhorar a estrutura sem perder o comportamento (**Refactor**). O próximo requisito ou defeito recomeça o ciclo. O método está descrito por [Martin Fowler](https://martinfowler.com/bliki/TestDrivenDevelopment.html).

Para uma mudança futura neste case, o registro mínimo será: ID da regra/risco, commit base, comando exato, falha inicial, alteração aplicada, reteste isolado, regressão pertinente e revisão do diff. Em segurança, o teste deve provar também o efeito lateral proibido; receber 401 não basta se o pedido já foi gravado. Em preço, a resposta e o SQLite precisam concordar com o catálogo.

## O que está demonstrado neste repositório

O experimento **QA-001** preserva uma verificação vermelho/verde: uma remoção temporária da checagem de titularidade fez o teste IDOR receber HTTP 200 quando exigia 404; a checagem foi restaurada e o reteste isolado passou. Veja [saída vermelha](evidence/QA-001-red-sanitized.txt), [saída verde](evidence/QA-001-green-sanitized.txt) e o [report do defeito](defects/QA-001-idor.md).

Essa evidência prova que o teste detecta **a regressão específica de autorização**. Como a falha foi introduzida de forma controlada sobre uma implementação existente, ela **não comprova** que a primeira versão do produto foi construída integralmente em TDD. As verificações por mutação de escrita antes do 401 e de total adulterado foram observadas durante a revisão, mas não têm log vermelho independente versionado; servem como relato de revisão, não como prova histórica adicional de TDD.

| Fase | Exemplo QA-001 | Evidência |
| --- | --- | --- |
| Lista de casos | Cliente B não deve ler pedido de A | `BDD-06`, `REQ-05`, `R-01` |
| Red controlado | Sem checagem de titular, GET responde 200 | Saída vermelha sanitizada |
| Green | Checagem `order.owner !== owner` devolve 404 | Saída verde e teste automatizado |
| Refactor | Nenhuma refatoração comportamental foi necessária nesse experimento | Não se reivindica etapa executada |
| Regressão | Suíte completa de UI, API, segurança e banco | [Relatório de execução](evidence/execution.md) |

## Executar o reteste sem modificar o produto

Na pasta do case, use:

```text
npx playwright test security/auth-security.spec.ts --project=api-security --grep IDOR --reporter=list
npm test
```

O primeiro comando verifica a regra isolada na versão corrigida; o segundo procura efeitos indiretos. Não introduza uma falha no `master` para reproduzir o log vermelho. Se uma nova correção exigir prova Red, faça o experimento em branch isolada e preserve apenas saídas sanitizadas, sem tokens nem senhas reais.
