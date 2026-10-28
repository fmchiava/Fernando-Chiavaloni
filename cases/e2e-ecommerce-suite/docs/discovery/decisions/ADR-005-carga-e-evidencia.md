# ADR-005 — k6 com thresholds e evidências em CI

**Status:** solução implementada; justificativa registrada retrospectivamente. **Escopo:** gate de carga local e observabilidade de testes.

**Contexto.** Um número de latência isolado não demonstra critério de aceite. O case precisa de perfil versionado, falha automática ao violar limites e relatórios que um avaliador possa consultar.

**Opções.** (A) medição manual: rápida, difícil de repetir. (B) script de carga sem gate: fornece números sem decisão. (C) k6 com rampa, checks, thresholds e relatórios na CI: decisão reproduzível, embora sensível ao ambiente.

**Decisão observada.** Opção C. O [cenário k6](../../../performance/scenarios/order-load-test.js) usa 50 VUs no perfil padrão, p95 < 500 ms, erros HTTP < 1% e checks > 99%; o [workflow](../../../../../.github/workflows/e2e-pipeline.yml) publica os relatórios. [Thresholds do k6](https://grafana.com/docs/k6/latest/using-k6/thresholds/) transformam a medição em saída de aprovação/reprovação.

**Consequências.** O gate detecta degradação no mock/runner dentro do perfil; não estima SLA ou capacidade de uma aplicação real. O perfil smoke é apenas checagem rápida, não substitui a carga padrão.

**Verificação.** [Perfil e limitações](../../../performance/config/README.md), [evidência datada](../../qa/evidence/execution.md), [workflow](../../../../../.github/workflows/e2e-pipeline.yml).

**Reconsiderar quando** houver baseline de tráfego real, meta de negócio aprovada ou infraestrutura estável que justifique outro perfil.
