# Relatório de execução — 27/10/2026

## Identificação

**Alvo:** e-commerce local sintético, branch `codex/e2e-ecommerce-suite`. **Ambiente local:** Windows, Node.js 24.19.0, npm 11.17.0, Playwright 1.64.1 e k6 2.2.0. **Dados:** duas contas `.test`, SQLite local em arquivos ignorados pelo Git. **Responsável:** execução automatizada deste estudo de caso; a interação QA–DEV é uma simulação declarada.

| Gate | Comando | Resultado observado |
| --- | --- | --- |
| Instalação | `npm ci` | Concluído; auditoria npm: 0 vulnerabilidades reportadas |
| Checagem estática | `npm run typecheck` | Exit code 0 |
| API, segurança, Web UI e SQLite | `npm test` após revisão dos testes | **10 passed (15.6s)**, 0 falhas; 3 UI (Chromium/Firefox/WebKit), 4 API e 3 segurança |
| k6 smoke | `PROFILE=smoke npm run test:performance` | p95 **33,22 ms**, taxa de erro **0%**, checks **100%** |
| k6 carga | `npm run test:performance` | **1.500 pedidos** em 50 s, 50 VUs de pico; p95 **73,77 ms**, taxa de erro **0%**, checks **100%**; exit code 0 |

O k6 realizou 1.501 requisições HTTP no total, incluindo o login de preparo. O p95 informado é o subgrupo `endpoint:order`, comparado ao limite de 500 ms. O [resumo JSON completo](local-performance/summary.json) e o [HTML local](local-performance/summary.html) foram copiados diretamente da execução de carga observada.

## Evidência de defeito e reteste

Na falha controlada QA-001, o teste IDOR retornou **1 failed**, com `Expected: 404` e `Received: 200`; [saída vermelha](QA-001-red-sanitized.txt). Após restaurar a checagem de titularidade, o [reteste isolado](QA-001-green-sanitized.txt) registrou **1 passed**. Duas verificações adicionais foram submetidas a mutações temporárias: uma escrita antes do 401 foi detectada pela contagem SQL (esperado 0, recebido 1), e um preço fornecido pelo cliente foi detectado (esperado 12.990, recebido 1). Essas mutações foram removidas antes da regressão final de **10 passed**. Veja [passos, causa e correção](../defects/QA-001-idor.md).

## Regressão do monorepo

Após a inclusão do case, as suítes anteriores foram executadas sem alteração de código: `python -m pytest -q` → **33 passed (11.59s)**; `cases/testes-api-playwright/npm test` → **24 passed (7.1s)**. O primeiro comando exigiu instalar `requirements-test.txt` neste Python local antes da coleta.

## Como inspecionar e reproduzir

- O [workflow E-commerce E2E Quality Gate](https://github.com/fmchiava/sdet-portfolio/actions/workflows/e2e-pipeline.yml) publica `playwright-report/`, `test-results/` e `performance/results/` no artefato `e2e-ecommerce-evidence` por 30 dias. A [primeira execução remota](https://github.com/fmchiava/sdet-portfolio/actions/runs/40511942716) passou com a versão inicial de 9 testes; a revisão que acrescentou o décimo teste exige novo gate remoto.
- Localmente, `npm ci`, `npx playwright install chromium firefox webkit`, `npm run typecheck`, `npm test` e `npm run test:performance` reproduzem o gate. `npm run report` abre o HTML do Playwright.
- Os arquivos `.data/`, `test-results/` e `performance/results/` são gerados e ignorados pelo Git. O dossiê estável não inclui tokens. Traces temporários podem registrar credenciais **sintéticas** do mock; nunca execute esta suíte com contas reais ao publicar artefatos.

**Interpretação:** o limiar de carga passou nesta máquina. O resultado não mede um ambiente distribuído nem estabelece SLO de uma loja real; na CI, a mesma regra será avaliada no runner remoto.
