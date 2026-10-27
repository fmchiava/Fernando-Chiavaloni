# Parecer técnico de qualidade — gate do case

**Data:** 27/10/2026. **Escopo:** e-commerce local sintético de demonstração, não um serviço de produção.

| Critério | Estado | Evidência |
| --- | --- | --- |
| TypeScript sem erros | Aprovado | `npm run typecheck`, exit 0 |
| API, segurança, UI e banco | Aprovado localmente | 10/10 execuções Playwright; [relatório](evidence/execution.md) |
| QA-001 corrigido e retestado | Aprovado | [defeito e regressão](defects/QA-001-idor.md) |
| Carga k6 p95 < 500 ms, erro < 1% | Aprovado localmente | 73,77 ms; 0%; [resumo](evidence/local-performance/summary.json) |
| Mesmo gate na CI e artefato | Aprovado | [Execução da revisão atual](https://github.com/fmchiava/sdet-portfolio/actions/runs/40559468419): 10/10 Playwright; k6 p95 11,01 ms, erro 0%, checks 100%; [artefato HTML/JSON](https://github.com/fmchiava/sdet-portfolio/actions/runs/40559468419/artifacts/12759201067) |

**Decisão atual: Go para publicação deste case de portfólio.** O commit `3522a50` passou nos gates locais e remotos, com artefato auditável publicado. Sem defeitos altos abertos no escopo testado. A decisão vale para o mock e os requisitos definidos neste estudo; o desempenho de outro ambiente deve ser medido novamente.
