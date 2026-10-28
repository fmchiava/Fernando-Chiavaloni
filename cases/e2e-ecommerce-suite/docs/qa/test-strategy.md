# Estratégia de testes e governança do gate

## Objetivo da qualidade

Demonstrar que a loja sintética preserva a identidade e o valor de um pedido do início ao fim. A confirmação na UI, a consulta REST e a linha no SQLite devem concordar. O QA também desafia as fronteiras de autorização, validação de entrada e comportamento sob a carga definida. A [regra de negócio](contexto-e-requisitos.md) é a referência do oráculo; um status HTTP verde isolado não é evidência suficiente.

## Abordagem por risco

Impacto e probabilidade são estimativas **qualitativas para este mock**, de 1 (baixo) a 3 (alto). A prioridade usa o produto dos dois valores para ordenar o trabalho, sem fingir precisão estatística. Um risco alto aberto bloqueia o parecer Go mesmo que a média dos testes esteja verde.

| Risco | Falha possível | Impacto × prob. | Controle executado | Lacuna ou observação |
| --- | --- | --- | --- | --- |
| R-01 | Cliente B lê pedido de A pelo ID | 3 × 2 = 6 | Duas contas, GET cruzado 404 e GET do titular 200 | Outros caminhos de acesso não existem no mock |
| R-02 | UI confirma pedido sem gravação ou com valor errado | 3 × 2 = 6 | UI → GET API → SELECT SQL no mesmo ID; 12.990 centavos | Sem pagamento ou estoque |
| R-03 | Contrato muda sem erro HTTP evidente | 2 × 2 = 4 | Zod no POST e GET; status 200/201/400 | Schema de catálogo não usa Zod |
| R-04 | Requisição anônima grava pedido | 3 × 2 = 6 | 401 no carrinho/pedido e contagem SQL de prova inalterada | GET sem token não tem assert dedicado |
| R-05 | Texto de entrada altera consulta SQL | 3 × 1 = 3 | Login com fragmento SQL → 401; busca vazia; catálogo íntegro | Amostra básica, não campanha ampla de injeção |
| R-06 | Carga causa latência ou falha | 2 × 2 = 4 | k6 até 50 VUs, p95 < 500 ms, HTTP < 1%, checks > 99% | Runner e banco locais não simulam arquitetura distribuída |
| R-07 | Checkout diverge entre navegadores | 2 × 2 = 4 | Mesmo E2E em Chromium, Firefox e WebKit | Sem dispositivos físicos ou acessibilidade completa |
| R-08 | CI não reproduz o gate local | 2 × 2 = 4 | `npm ci`, Node 24, browsers, typecheck, Playwright, k6 e upload | Diferença de desempenho entre máquinas é esperada |

## Níveis, técnicas e oráculos

| Nível | Seleção dos casos | Oráculo e evidência |
| --- | --- | --- |
| Jornada UI | Caminho feliz em três motores; Page Objects e elementos visíveis | Carrinho com 1 item, total exibido, ID de confirmação, API e SQL coerentes |
| API e contrato | Partições válida/inválida; alteração adversarial de total | HTTP 200/201/400, `OrderSchema` Zod, 12.990 centavos persistidos |
| Segurança | Ausência de token, acesso horizontal, entrada com fragmento SQL | 401 sem escrita, 404 para Beta/200 para Alfa, busca e catálogo íntegros |
| Persistência | Consulta em conexão SQLite separada da aplicação | Mesmo ID, titular, `APROVADO`, total 12990 |
| Performance | Rampa 0→50 VUs em 30 s, 10 s estáveis, 10 s de descida | Thresholds k6 marcados `endpoint:order` e check de 201 |

São **oito testes lógicos e dez execuções Playwright**: quatro API, três segurança e uma jornada UI repetida em três navegadores. O objetivo da suíte é dar sinais claros sobre regras importantes, não maximizar contagem. Os testes podem rodar em paralelo; cada pedido é localizado pelo ID retornado. Contextos de navegador são isolados, mas o arquivo SQLite é compartilhado dentro da suíte funcional. A independência é verificada por dados e IDs, não por limpeza global entre testes.

A [política de massa e oráculos](dados-e-oraculos.md) registra contas, produtos, preço, consulta SQL e isolamento da carga.

## Sequência do gate

1. Preparar Node, dependências e browsers conforme [pré-requisitos](pre-requisitos.md); verificar `/health`.
2. Rodar `npm run docs:check` e typecheck; links ou IDs BDD quebrados também impedem afirmar que o dossiê está pronto.
3. Rodar Playwright completo. Uma falha de assert, browser, contrato, autorização ou SQL exige triagem; um retry verde na CI não apaga a necessidade de investigar intermitência.
4. Rodar k6 de carga no banco e porta separados. O perfil smoke confirma preparo, mas não é aceite de performance.
5. Publicar e conferir HTML/JSON; associar run, commit, ambiente e decisão. O [workflow](../../../../.github/workflows/e2e-pipeline.yml) executa os passos automatizados e publica artefatos mesmo após uma falha, quando arquivos estiverem disponíveis.

## Critérios de entrada e saída

**Entrada:** requisito e massa definidos; Node 24+; lockfile instalável; navegadores presentes; portas 4173/4174 livres; contas `.test`; mock saudável; k6 disponível para o gate de carga. Se uma dependência faltar, registre **bloqueio de ambiente**, não um falso defeito do produto.

**Go deste case:** typecheck sem erros; 10/10 execuções Playwright verdes sem falha escondida; p95 < 500 ms, HTTP < 1% e checks > 99% no perfil de carga; nenhum defeito alto aberto no escopo; artefato da CI acessível; riscos residuais descritos. **No-Go:** falha em qualquer um desses critérios, evidência ausente ou teste obrigatório não executado. Um resultado de runner não prova capacidade de produção.

## Registro e comunicação

Uma falha deve conter commit, comando, ambiente, massa, esperado/obtido, frequência, impacto e evidência. QA e DEV acordam causa e critério de correção; QA retesta primeiro o cenário afetado, depois a regressão conforme risco. O [procedimento](defect-lifecycle.md), a [matriz](traceability.md) e o [parecer](release-decision.md) formam a trilha de decisão.

## Cobertura residual conhecida

Não há asserts específicos para quantidade 10/11, GET sem token, ID inexistente, inexistência de gravação em carrinho válido, sessão expirada ou formatação monetária `pt-BR`. A [matriz](traceability.md) marca a cobertura parcial; esses itens entram no backlog de uma próxima iteração e não são relatados como testes aprovados. A estratégia se apoia na recomendação de [isolamento e comportamento observável do Playwright](https://playwright.dev/docs/best-practices/).
