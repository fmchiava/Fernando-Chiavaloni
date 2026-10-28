# Dossiê de QA — E-commerce E2E

Este índice organiza o material como uma revisão de qualidade. O sistema de apoio é uma loja local sintética; o objeto principal do case é a capacidade de definir critérios, projetar testes, reconhecer riscos, produzir evidências e sustentar uma decisão técnica.

## Percurso recomendado

| Tempo | Leia | O que deve conseguir avaliar |
| --- | --- | --- |
| 4 min | [Descoberta e refinamento](../discovery/README.md) | Problema, hipóteses, alternativas, backlog e motivos das decisões |
| 2 min | [Contexto e requisitos](contexto-e-requisitos.md) | Processo, regras observáveis, fronteiras e significado de “pedido aprovado” |
| 3 min | [Arquitetura](arquitetura.md), [dados e oráculos](dados-e-oraculos.md) e [pré-requisitos](pre-requisitos.md) | Fluxo UI/API/SQLite/k6, massa e reprodução sem contas externas |
| 4 min | [BDD](bdd/README.md), [TDD](tdd.md) e [rastreabilidade](traceability.md) | Linguagem de negócio, ciclo de teste e relação com testes reais |
| 4 min | [Estratégia e riscos](test-strategy.md) e [segurança](security-scope.md) | Priorização, oráculos, gates e limites de cobertura |
| 4 min | [QA-001](defects/QA-001-idor.md), [execução](evidence/execution.md) e [parecer](release-decision.md) | Falha controlada, reteste, resultados observados e decisão |

## Estado dos artefatos

- **Executável:** testes Playwright em `src/tests/` e `security/`, carga k6 em `performance/scenarios/`, workflow na raiz do monorepo.
- **Especificação:** arquivos `.feature` em `bdd/`. Eles descrevem comportamento em Gherkin e **não** são executados por Cucumber neste repositório; a matriz liga cada cenário à automação disponível.
- **Evidência preservada:** saídas sanitizadas do QA-001, resumo local k6 e links para as execuções do GitHub Actions. Relatórios completos da CI têm retenção configurada de 30 dias.
- **Simulação declarada:** a conversa QA–DEV do defeito é um exercício de portfólio. As saídas de teste referidas como observadas foram efetivamente produzidas.
- **Análise retrospectiva:** a trilha de [descoberta](../discovery/README.md) reconstrói motivos e opções a partir da implementação; não registra entrevistas ou aprovações históricas.

## Convenções de leitura

`REQ-*` identifica regra funcional, `NFR-*` requisito não funcional, `R-*` risco, `BDD-*` cenário e `QA-*` defeito. “Coberto” significa que existe assert automatizado correspondente; “parcial” indica que o fluxo passa pelo comportamento, mas não prova todos os aspectos da regra; “não coberto” não deve ser tratado como aprovado.

O [registro da revisão documental](revisao-documental.md) descreve as verificações desta atualização. A [página inicial do case](../../README.md) oferece os comandos de entrada.
