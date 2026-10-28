# Problema, fontes e hipóteses

## Enquadramento

**Problema reconstruído:** uma jornada de compra pode mostrar sucesso na interface enquanto API e banco discordam sobre valor, titular ou situação do pedido. Para um portfólio de Quality Engineering, o risco central é aceitar uma tela verde como prova suficiente de uma transação correta.

**Resultado desejado no case:** um cliente sintético autentica-se, consulta o catálogo, monta um carrinho e cria um pedido. O QA consegue demonstrar, com oráculos independentes, que o valor veio do catálogo do servidor, o pedido pertence ao cliente e o registro persistido corresponde à resposta. O significado de `APROVADO` está delimitado nos [requisitos](../qa/contexto-e-requisitos.md): aceito pelo mock, sem liquidação financeira.

**Limite:** loja local de demonstração, sem pagamento, antifraude, estoque, entrega, integrações externas ou SLO de produção. O objetivo é avaliar a disciplina de testes, não simular a complexidade operacional de uma plataforma comercial.

## Papéis e perguntas de descoberta

Os papéis abaixo são **perspectivas propostas para uma descoberta real**. Nenhuma entrevista com essas pessoas foi realizada.

| Perspectiva | Interesse a validar | Pergunta que mudaria o desenho |
| --- | --- | --- |
| Responsável pelo produto | Valor e significado do pedido aprovado | O pedido precisa reservar estoque ou apenas registrar uma intenção? |
| Operação/atendimento | Consulta e correção de pedidos | Que estados e exceções precisam ser visíveis após o checkout? |
| Segurança | Acesso entre clientes e exposição de dados | Pedido inexistente e pedido de terceiro devem ter a mesma resposta? |
| Desenvolvimento | Contrato, persistência e falhas | Há exigência de idempotência para repetição do POST após timeout? |
| QA/SDET | Oráculos e cobertura | Qual evidência é suficiente para aprovar a jornada? |
| Plataforma | Capacidade e observabilidade | Qual carga e ambiente representam o uso esperado? |

## Fontes efetivamente inspecionadas

| Fonte | O que sustenta | Limite |
| --- | --- | --- |
| [Servidor local](../../src/utils/mock-server.ts) | Rotas, autenticação Bearer, autorização por titular, preço calculado no servidor e fluxo HTML. | Mostra implementação, não aprovação de negócio. |
| [Banco](../../src/db/database.ts) e [contrato](../../src/api/OrderSchema.ts) | Massa sintética, campos, validação de quantidade e escrita do pedido. | Não prova comportamento de produção distribuída. |
| [Testes API/UI](../../src/tests/) e [segurança](../../security/auth-security.spec.ts) | Asserts executáveis e lacunas de cobertura. | Um teste verde prova somente as condições exercitadas. |
| [Configuração Playwright](../../playwright.config.ts) e [perfil k6](../../performance/scenarios/order-load-test.js) | Navegadores, relatórios, carga e thresholds locais. | Metas não foram derivadas de tráfego real. |
| [Relatório de execução](../qa/evidence/execution.md) | Resultados datados, CI e artefatos. | Resultados não equivalem a aceite de stakeholder. |

## Hipóteses e decisões pendentes

| ID | Hipótese/pergunta | Impacto se falsa | Próximo passo proposto |
| --- | --- | --- | --- |
| H-01 | `APROVADO` é estado suficiente para o exercício. | Exigiria estados, transições e testes de compensação. | Confirmar semântica com produto/operação. |
| H-02 | O preço do catálogo no servidor é a fonte de verdade. | Exigiria política de promoções, impostos e versão de preço. | Definir regra de precificação com produto. |
| H-03 | O 404 para pedido de terceiro é a resposta desejada. | Contrato e testes de autorização mudariam. | Validar política com segurança e API consumers. |
| H-04 | 50 VUs e p95 < 500 ms são metas úteis para o mock local. | O gate pode ser irrelevante para capacidade real. | Obter perfil de tráfego e SLO antes de extrapolar. |
| H-05 | Reenvio de pedido após timeout não exige idempotência neste ciclo. | Pode gerar pedidos duplicados. | Refinar chave de idempotência e teste de repetição. |

O [backlog refinado](04-refinamento-backlog.md) mantém essas dúvidas fora do conjunto considerado aceito.
