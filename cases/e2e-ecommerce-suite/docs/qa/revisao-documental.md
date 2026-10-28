# Registro de revisão da documentação

## Identificação e escopo

**Data da revisão:** 27/10/2026. **Base funcional:** `master` no merge `041c4c3`. **Área revisada:** README do case, pontos de entrada no README do monorepo, documentos de QA, especificações BDD, perfil de carga e workflow que valida os documentos. **Estado em 27/10:** rascunho salvo em branch local para apresentação antes de publicação remota.

A revisão toma o código como fonte para rotas, regras, dados e comandos; toma os logs sanitizados e os runs da CI como fonte para resultados. Os documentos metodológicos da pasta `docs/superpowers/` preservam o plano de trabalho e não substituem o dossiê de QA.

## Critérios da revisão

1. **Verdade factual:** nenhum número sem data, ambiente ou fonte; não confundir o mock com produção real, `.feature` com teste executado ou mutação QA-001 com histórico integral de TDD.
2. **Navegação:** todo link relativo do material revisado resolve para um arquivo existente; o índice leva de requisito a teste e evidência.
3. **Rastreabilidade:** cada ID BDD é único, aparece na matriz e é associado a um teste real ou lacuna explícita.
4. **Reprodução:** comandos e variáveis correspondem a `package.json`, `playwright.config.ts`, runner k6 e workflow.
5. **Privacidade:** apenas contas `.test`; sem token ou segredo real nos arquivos novos; saídas vermelha/verde preservadas com caminho local sanitizado.
6. **Regressão:** typecheck e suíte funcional continuam passando após a mudança do script/CI; o verificador documental é executado.

## Achados e correções nesta revisão

| Achado | Tratamento |
| --- | --- |
| O relatório anterior apontava um run anterior ao merge como “revisão atual”. | Separados resultados locais, CI da PR e gate do `master`, com commit e links explícitos. |
| BDD e TDD não estavam definidos para leitura de negócio. | Criados cenários Gherkin com IDs e explicada a prova Red/Green disponível, sem reivindicar runner Cucumber ou TDD histórico não comprovado. |
| Pré-requisitos, portas, massa e diferenças Windows/Linux estavam dispersos. | Criado guia único de reprodução e perfil de k6 detalhado. |
| O índice não mostrava cobertura parcial nem lacunas conhecidas. | Requisitos numerados, matriz com estado e riscos residuais no parecer. |
| Na primeira execução do verificador, um link relativo e a comparação de IDs BDD estavam incorretos. | Caminho e comparação corrigidos; a conferência final é registrada abaixo. |

## Resultados observados da checagem local

| Checagem | Resultado |
| --- | --- |
| `npm ci` | Exit 0; 0 vulnerabilidades reportadas pelo npm nesta instalação |
| `npm run docs:check` | Exit 0; 19 arquivos Markdown, 8 cenários BDD, IDs e links locais conferidos |
| `npm run typecheck` | Exit 0 |
| `npm test` | **10 passed (14.6s)**; API, segurança e UI nos três navegadores |
| `npm run test:performance` | **1.516 pedidos**, p95 **12,85 ms**, erro HTTP **0%**, checks **100%**, exit 0; [JSON](evidence/documentation-review-performance/summary.json) e [HTML](evidence/documentation-review-performance/summary.html) preservados |
| `git diff --cached --check` | Exit 0; nenhuma linha com erro de whitespace no conjunto preparado |
| Busca por padrões de segredo e caminho local | Nenhum token GitHub/OpenAI/AWS, Bearer longo ou caminho `C:\Users\` encontrado nos documentos novos |

O verificador automatiza estrutura e links, **não** faz interpretação semântica completa do Gherkin. A revisão manual confrontou os oito cenários com os títulos e asserts dos testes e marcou as regras parcialmente cobertas na matriz. O diff preparado altera documentos, o verificador, o script de pacote e um passo do workflow; não altera o servidor nem os asserts funcionais. O commit local registra a versão apresentada ao usuário.

## Decisão de publicação

Em 27/10/2026, a publicação estava pendente de apresentação ao proprietário do portfólio. Em 28/10/2026, ele solicitou a publicação integral da documentação no GitHub. O gate de CI da versão publicada deve ser consultado pelo commit e run correspondentes; os runs históricos acima não substituem esse gate.

## Complemento: descoberta e decisões (27/10/2026)

Após esta revisão, foi incluída uma [trilha de descoberta](../discovery/README.md) com fontes, hipóteses, levantamento, análise retrospectiva de alternativas, backlog e seis ADRs. A nova trilha classifica cada afirmação como observada, reconstruída, hipótese ou proposta. Nenhuma entrevista, workshop ou aprovação foi atribuída a stakeholders reais. Os IDs REQ/NFR permanecem definidos em [contexto e requisitos](contexto-e-requisitos.md), evitando duas fontes normativas divergentes.

O verificador documental passou a inspecionar todos os Markdown de `docs/`, inclusive os ADRs. Os números de 19 arquivos acima pertencem à revisão anterior.

| Checagem desta ampliação | Resultado local em 27/10/2026 |
| --- | --- |
| `npm run docs:check` | Exit 0; 31 arquivos Markdown, 8 cenários BDD e links locais verificados. A primeira passagem encontrou dois links inexistentes nos ADRs; ambos foram corrigidos antes da passagem verde. |
| `npm run typecheck` | Exit 0. |
| `npm test` | **10 passed (12,8s)** em API, segurança, Chromium, Firefox e WebKit. |
| Revisão factual | Rotas, valores, dados, configurações e limites confrontados com servidor, banco, schemas, testes e k6. |
| Busca de segredos nos arquivos de descoberta | Nenhum token, caminho pessoal ou senha de teste copiada para a nova trilha. |

O perfil completo de k6 não foi repetido naquela ampliação, pois a implementação e o cenário de carga não mudaram; a execução anterior continua identificada acima.

## Gate de publicação local (28/10/2026)

Após o pedido explícito de publicação, os textos que diziam “pendente” foram reescritos como **histórico datado**. O índice do monorepo passou a apontar também para descoberta e ADRs; nenhum resultado anterior foi atribuído ao novo commit.

| Checagem | Resultado |
| --- | --- |
| `npm run docs:check` | Exit 0; 31 Markdown, 8 cenários BDD e links locais verificados |
| `npm run typecheck` | Exit 0 |
| `npm test` | 10 passed (20,3s) |
| `npm run test:performance` | Exit 0; 1.504 pedidos, p95 36,53 ms, falhas 0%, checks 100%; [JSON](evidence/publication-performance/summary.json) e [HTML](evidence/publication-performance/summary.html) |
| Revisão de publicação | Saídas QA-001 sanitizadas, resumos de carga, diagramas, regras e ADRs presentes no Git; sem padrão de segredo ou caminho pessoal encontrado nos arquivos de documentação |

O gate remoto desta publicação será identificado pelo commit/run do GitHub Actions. O registro local acima não o substitui.
