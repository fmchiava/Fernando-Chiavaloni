# Origem dos cases

Os projetos públicos foram reunidos neste repositório para concentrar navegação, execução e CI. Os arquivos versionados foram copiados dos commits abaixo; os workflows originais foram substituídos pelos workflows da raiz.

| Pasta | Repositório de origem | Commit de origem |
| --- | --- | --- |
| `cases/rpa-conciliacao-sinistros/` | `fmchiava/qa-rpa-conciliacao-sinistros` | `1aa00a97e93604c726eb5ff9b09884efca836825` |
| `cases/testes-api-playwright/` | `fmchiava/testes-api-playwright` | `3a9cc9b052d779b656a3c8db3459c5a93d014170` |
| `cases/controle-plataformas/` | `fmchiava/controle-plataformas-elevatorias` | `4a404d8194cbd4fc81f21aa466befc4b907e906a` |
| `laboratorio/importacao_chamados/` | `fmchiava/portfolio-qa-automacao` | `b9013ff6f1b17286b42827eee5d22d41ff2957e3` |

Os repositórios de origem permanecem disponíveis até a decisão do proprietário sobre arquivamento ou privacidade. O histórico anterior pode ser consultado nos repositórios de origem; o monorepo preserva a referência ao commit de cada migração.

## Caminhos de execução

- `python -m pytest -q` na raiz: testes RPA e importação de chamados.
- `npm ci && npm run typecheck && npm test` em `cases/testes-api-playwright/`.
- Os workflows ativos ficam exclusivamente em `.github/workflows/` da raiz.
