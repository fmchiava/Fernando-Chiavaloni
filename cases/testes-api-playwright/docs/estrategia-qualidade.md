# Estratégia de qualidade da suíte de API

## Objetivo e oráculo

Demonstrar como um QA verifica contrato, dados, autenticação e comportamento diante de falhas em APIs REST. O oráculo dos testes de posts é o comportamento documentado e observado do JSONPlaceholder; o de autenticação é a API de demonstração DummyJSON. Ambas são serviços públicos externos, sem SLA controlado por este projeto.

## Riscos e evidências

| Risco | Teste ou controle | Evidência |
| --- | --- | --- |
| Resposta 200 com estrutura incompatível | Schemas Zod para posts, comentários e resposta vazia | `tests/posts.spec.ts`, `utils/schemas.ts` |
| Filtro ou vínculo incorreto | Consulta por usuário e comentários relacionados ao post | `tests/posts.spec.ts` |
| Supor validação que a API não realiza | Casos com payloads inválidos registram o retorno real e a reprovação no schema local | `fixtures/test-data.json`, `tests/posts.spec.ts` |
| Token ausente ou aplicado ao host errado | Fixture cria contexto autenticado por teste e usa caminhos relativos; cenário sem token exige 401 | `fixtures/api-fixture.ts`, `tests/protected-routes.spec.ts` |
| Serviço externo indisponível ou lento | Mocks de 500 e timeout isolados da suíte de contrato | `tests/mocks.spec.ts` |
| Regressão sem rastreabilidade | Typecheck, 24 testes, artefato HTML e publicação do último relatório aprovado | `../../../.github/workflows/api-tests.yml` no monorepo |
| Conclusão de desempenho baseada em amostra pública | k6 separado da CI, com threshold explícito e resultado reprovado documentado | `performance/posts-load-test.js`, `README.md` |

## Execução e critério de aceite

Execute `npm ci`, `npx playwright install --only-shell chromium`, `npm run typecheck` e `npm test`. Cada teste deve terminar sem falha. O relatório HTML da execução fica em `playwright-report/`; a CI anexa o relatório mesmo quando a suíte falha. A publicação no Pages ocorre apenas após uma execução aprovada na branch `main`.

Para triagem, separe falha de contrato, regra funcional, autenticação e indisponibilidade do serviço externo. Guarde o link da execução, versão do commit, caso afetado, resposta HTTP sanitizada e resultado esperado/observado. Um teste aprovado depois de retry não demonstra ausência de instabilidade; analise as tentativas e a causa.

## Limites

- A suíte consulta serviços de demonstração. Mudanças, rate limits e indisponibilidade desses serviços podem quebrar a CI sem alteração no código deste projeto.
- `POST`, `PUT`, `PATCH` e `DELETE` do JSONPlaceholder são simulados. Não há confirmação de persistência por leitura posterior.
- O teste de k6 não mede capacidade de produção e fica fora da CI para não gerar carga recorrente em serviço público.
- Os mocks demonstram a reação do cliente a falhas específicas; eles não substituem testes de integração com o serviço real.
