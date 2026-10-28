# Relatório de execução e proveniência

## Identificação

**Data das execuções registradas:** 27/10/2026. **Alvo:** e-commerce sintético local. **Versão integrada ao `master`:** merge `041c4c3eb721addca8032cec66110e82220a510d`. **Ambiente local observado:** Windows, Node 24.19.0, npm 11.17.0, Playwright 1.64.1, k6 2.2.0. **Dados:** Alfa/Beta `.test`; SQLite em arquivos ignorados. As interações QA–DEV são simulação; resultados de comando abaixo são observações.

## Gate funcional e regressão local

| Etapa | Comando | Resultado observado | Interpretação |
| --- | --- | --- | --- |
| Instalação inicial | `npm ci` | Exit 0; npm reportou 0 vulnerabilidades naquela instalação | Não substitui análise de segurança de dependências |
| TypeScript no `master` | `npm run typecheck` | Exit 0 após o merge | Sem erro de tipo nessa versão |
| Playwright no `master` | `npm test` | **10 passed (18.6s)** | 4 API, 3 segurança, 1 UI em 3 navegadores |
| k6 smoke local | `PROFILE=smoke npm run test:performance` | p95 33,22 ms; HTTP 0%; checks 100% | Preparo, não aceite de carga |
| k6 carga local | `npm run test:performance` | **1.500 iterações/pedidos**, 50 VUs de pico, p95 **73,77 ms**, HTTP **0%**, checks **100%**, exit 0 | Passou os limites do perfil local |
| Regressão Python do monorepo | `python -m pytest -q` | **33 passed (11.59s)** após instalar `requirements-test.txt` | Cases Python existentes |
| Regressão API anterior | `cases/testes-api-playwright/npm test` | **24 passed (7.1s)** | Case Playwright anterior |

O resumo [JSON](local-performance/summary.json) e [HTML](local-performance/summary.html) preserva a execução local de carga. São 1.501 requisições HTTP no total, pois o preparo faz um login antes das 1.500 criações. O p95 de aceite usa o subgrupo `endpoint:order`, não a média de todas as rotas. Esses números caracterizam o mock na máquina usada, sem extrapolação de capacidade.

## Gate remoto do commit integrado

| Workflow | Run e observação |
| --- | --- |
| [E-commerce E2E Quality Gate](https://github.com/fmchiava/sdet-portfolio/actions/runs/40561541646) | **Success** no `master`: typecheck, **10 passed (10.2s)**, k6 p95 **13,81 ms**, falhas HTTP **0%**, checks **100%** |
| [Artefato E2E](https://github.com/fmchiava/sdet-portfolio/actions/runs/40561541646/artifacts/12760268314) | `e2e-ecommerce-evidence`, Playwright HTML e k6 HTML/JSON, retenção configurada de 30 dias |
| [Python QA Tests](https://github.com/fmchiava/sdet-portfolio/actions/runs/40561541748) | **Success** em Python 3.11 e 3.12; no job 3.12, 33 passed |
| [API Regression Tests](https://github.com/fmchiava/sdet-portfolio/actions/runs/40561542013) | **Success**, **24 passed (4.2s)** e relatório publicado no [GitHub Pages](https://fmchiava.github.io/sdet-portfolio/) |

O p95 remoto muda conforme o runner e não precisa reproduzir o número local. O que deve se repetir é o atendimento aos thresholds definidos **antes** da medição. A documentação nesta branch local ainda não gerou uma nova execução remota; esses links identificam a versão funcional já integrada.

## Verificação local da revisão documental

Na branch local `codex/e2e-qa-documentation`, `npm ci` terminou com 0 vulnerabilidades reportadas; `npm run docs:check` verificou 19 arquivos Markdown, 8 cenários BDD e seus links; `npm run typecheck` saiu com código 0; `npm test` registrou **10 passed (14.6s)**. `npm run test:performance` executou **1.516 iterações/pedidos**, com p95 **12,85 ms**, falhas HTTP **0%**, checks **100%** e exit 0. O [JSON](documentation-review-performance/summary.json) e [HTML](documentation-review-performance/summary.html) desta carga foram preservados sem credenciais. Essa verificação é **local**; a versão documental ainda não foi enviada para uma CI remota.

## Falha controlada e reteste

O [QA-001](../defects/QA-001-idor.md) foi exercitado com uma mutação temporária. A [saída vermelha](QA-001-red-sanitized.txt) mostra **1 failed**, esperado 404 e recebido 200. Depois de restaurar a checagem, a [saída verde](QA-001-green-sanitized.txt) mostra **1 passed (3.3s)**. A suíte completa voltou a passar. Também foram feitas mutações temporárias de escrita antes do 401 e aceitação de `totalCents: 1`; os respectivos asserts detectaram as violações, mas seus logs vermelhos não foram versionados. Não se atribui a esses dois testes uma evidência pública além do código de assert e do relato.

## Reprodução e limites

Os comandos exatos e a configuração estão nos [pré-requisitos](../pre-requisitos.md). `npm run report` abre o HTML local; na CI, baixe o artefato do run indicado. `.data/`, `test-results/` e `performance/results/` são gerados e ignorados pelo Git. Screenshot e trace são retidos em falhas, não em toda execução verde. Um resultado de carga neste mock não estabelece SLO ou prontidão de uma operação comercial real.
