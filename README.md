# SDET Portfolio — Fernando Chiavaloni

[![Python QA Tests](https://github.com/fmchiava/sdet-portfolio/actions/workflows/python-tests.yml/badge.svg)](https://github.com/fmchiava/sdet-portfolio/actions/workflows/python-tests.yml) [![API Regression Tests](https://github.com/fmchiava/sdet-portfolio/actions/workflows/api-tests.yml/badge.svg)](https://github.com/fmchiava/sdet-portfolio/actions/workflows/api-tests.yml) [![E-commerce E2E Quality Gate](https://github.com/fmchiava/sdet-portfolio/actions/workflows/e2e-pipeline.yml/badge.svg)](https://github.com/fmchiava/sdet-portfolio/actions/workflows/e2e-pipeline.yml)

Portfólio de **Quality Engineering e SDET** com casos de automação de testes, qualidade de dados e governança de RPA. Os cases executáveis reúnem estratégia, código e evidências no próprio diretório.

## Cases

| Case | Engenharia de qualidade | Estado |
| --- | --- | --- |
| [E-commerce E2E](cases/e2e-ecommerce-suite/) | Web UI, API REST, contratos Zod, SQLite, segurança, k6, BDD/TDD e [dossiê QA](cases/e2e-ecommerce-suite/docs/qa/README.md) | **10 execuções Playwright** · [CI](https://github.com/fmchiava/sdet-portfolio/actions/workflows/e2e-pipeline.yml) |
| [Conciliação de sinistros com RPA](cases/rpa-conciliacao-sinistros/) | UI, API REST, CSV, SQLite, exceções, rastreabilidade e arquitetura A360 | **18 testes Python** · [CI](https://github.com/fmchiava/sdet-portfolio/actions/workflows/python-tests.yml) |
| [Testes de API com Playwright](cases/testes-api-playwright/) | Contratos Zod, autenticação, mocks, dados de teste e relatório HTML | **24 testes Playwright** · [CI](https://github.com/fmchiava/sdet-portfolio/actions/workflows/api-tests.yml) |
| [Controle de plataformas elevatórias](cases/controle-plataformas/) | Problema, regras e critérios para iniciar o desenvolvimento | **Em planejamento** |
| [Importação de chamados](laboratorio/importacao_chamados/) | Idempotência, validação e consistência de dados em lote | **15 testes Python** · [CI](https://github.com/fmchiava/sdet-portfolio/actions/workflows/python-tests.yml) |

**Stack demonstrada:** Playwright · TypeScript · Python · pytest · Zod · REST API · GitHub Actions · k6 · RPA/A360 (arquitetura proposta) · QA para dados · SQLite.

## Executar

Pré-requisitos variam por case: Python 3.11+ para a regressão Python; Node.js 24 para Playwright; k6 para o perfil de carga do e-commerce. O case E-commerce usa somente um mock local; o case anterior de API usa serviços públicos. Cada README informa portas, massa e comandos.

```bash
git clone https://github.com/fmchiava/sdet-portfolio.git
cd sdet-portfolio
python -m pip install -r requirements-test.txt
python -m pytest -q
cd cases/testes-api-playwright
npm ci
npx playwright install --only-shell chromium
npm run typecheck
npm test
```

Os testes Python usam `unittest.TestCase`, coletados pelo `pytest` na raiz. Os [workflows](.github/workflows/) executam Python, API Playwright e E-commerce E2E, além de validar evidências sintéticas do case RPA. O [guia do E-commerce](cases/e2e-ecommerce-suite/docs/qa/pre-requisitos.md) explica a reprodução do novo case.

## Documentação

- [Matriz de testes do laboratório](portfolio/matriz-de-testes.md)
- [Dossiê de QA do E-commerce E2E](cases/e2e-ecommerce-suite/docs/qa/README.md)
- [Progresso de aprendizado](aprendizado/progresso.md)
- [Origem e migração dos cases](docs/migracao.md)

Os cases usam dados sintéticos. O case RPA inclui um simulador executável e um desenho de bot A360; o case de plataformas registra uma proposta ainda sem implementação.
