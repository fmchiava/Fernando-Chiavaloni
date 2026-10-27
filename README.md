# SDET Portfolio — Fernando Chiavaloni

[![Python QA Tests](https://github.com/fmchiava/sdet-portfolio/actions/workflows/python-tests.yml/badge.svg)](https://github.com/fmchiava/sdet-portfolio/actions/workflows/python-tests.yml) [![API Regression Tests](https://github.com/fmchiava/sdet-portfolio/actions/workflows/api-tests.yml/badge.svg)](https://github.com/fmchiava/sdet-portfolio/actions/workflows/api-tests.yml)

Portfólio de **Quality Engineering e SDET** com casos reproduzíveis de automação de testes, qualidade de dados e governança de RPA. Cada case tem escopo, estratégia, código e evidências no próprio diretório.

## Cases

| Case | Engenharia de qualidade | Estado |
| --- | --- | --- |
| [Conciliação de sinistros com RPA](cases/rpa-conciliacao-sinistros/) | UI, API REST, CSV, SQLite, exceções, rastreabilidade e arquitetura A360 | **18 testes Python** · [CI](https://github.com/fmchiava/sdet-portfolio/actions/workflows/python-tests.yml) |
| [Testes de API com Playwright](cases/testes-api-playwright/) | Contratos Zod, autenticação, mocks, dados de teste e relatório HTML | **24 testes Playwright** · [CI](https://github.com/fmchiava/sdet-portfolio/actions/workflows/api-tests.yml) |
| [Controle de plataformas elevatórias](cases/controle-plataformas/) | Problema, regras e critérios para iniciar o desenvolvimento | **Em planejamento** |
| [Importação de chamados](laboratorio/importacao_chamados/) | Idempotência, validação e consistência de dados em lote | **15 testes Python** · [CI](https://github.com/fmchiava/sdet-portfolio/actions/workflows/python-tests.yml) |

**Stack demonstrada:** Playwright · TypeScript · Python · pytest · Zod · REST API · GitHub Actions · RPA/A360 (arquitetura proposta) · QA para dados · SQLite.

## Executar

Pré-requisitos: Python 3.11+ e Node.js 24. Os testes de API usam serviços públicos; os testes Python rodam localmente, sem contas externas.

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

Os testes Python usam `unittest.TestCase`, coletados pelo `pytest` na raiz. Os workflows em [`.github/workflows/`](.github/workflows/) executam as duas suítes e validam as evidências sintéticas do case RPA. Consulte os READMEs dos cases para demonstrar os fluxos completos.

## Documentação

- [Matriz de testes do laboratório](portfolio/matriz-de-testes.md)
- [Progresso de aprendizado](aprendizado/progresso.md)
- [Origem e migração dos cases](docs/migracao.md)

Os cases usam dados sintéticos. O case RPA inclui um simulador executável e um desenho de bot A360; o case de plataformas registra uma proposta ainda sem implementação.
