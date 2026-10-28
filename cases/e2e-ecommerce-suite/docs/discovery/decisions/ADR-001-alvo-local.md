# ADR-001 — Alvo local sintético

**Status:** solução implementada; justificativa registrada retrospectivamente. **Escopo:** ambiente do case.

**Contexto.** O portfólio precisa permitir execução repetível de UI, API, segurança e carga, inclusive uma falha controlada para investigação. Uma API pública introduziria dados/limites mutáveis; uma plataforma comercial completa ampliaria muito o trabalho de produto antes de demonstrar QA.

**Opções.** (A) API pública: início rápido, pouco controle de dados e defeitos. (B) plataforma completa: maior realismo, maior custo e dependência. (C) servidor local Node.js com dados sintéticos: controle e reprodução, menor realismo operacional.

**Decisão observada.** Opção C, com UI HTML e REST no mesmo [servidor](../../../src/utils/mock-server.ts), bind em `127.0.0.1` e contas `.test`. A escolha mantém o avaliador autossuficiente e permite comparar camadas sob as mesmas regras.

**Consequências.** O case prova desenho de teste e detecção de regressões específicas; não mede integração comercial, pagamentos, TLS, escalabilidade distribuída nem ambiente corporativo. O significado de `APROVADO` fica restrito ao mock.

**Verificação.** [Pré-requisitos e execução](../../qa/pre-requisitos.md), [teste E2E](../../../src/tests/e2e-purchase.spec.ts) e [relatório](../../qa/evidence/execution.md).

**Reconsiderar quando** a meta for validar integrações externas, políticas reais de negócio ou capacidade de produção.
