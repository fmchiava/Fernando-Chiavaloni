# E-commerce E2E Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Entregar um case de QA/SDET executável e auditável para compra em e-commerce local.

**Architecture:** Servidor Node.js com UI mínima, REST e SQLite. Playwright exercita UI, API, segurança e persistência; k6 mede criação de pedidos. Um workflow da raiz executa e publica evidências.

**Tech Stack:** Node.js 24, TypeScript, Playwright, Zod, dotenv, sqlite3, k6, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-10-27-e2e-ecommerce-suite-design.md`

## Global Constraints

- O sistema de apoio é mínimo; estratégia, testes e evidências são o foco.
- Workflows ficam em `.github/workflows/` na raiz.
- Dados e credenciais são sintéticos; tokens e senhas não entram em evidências públicas.
- Relatórios distinguem observação real de simulação do fluxo QA–DEV.

## Review Focus

- Pedido sem Bearer deve ser rejeitado sem escrita em banco.
- Pedido de outro usuário não pode ser lido pelo ID.
- Preço deve ser recalculado no servidor e persistido em centavos.
- Entrada com aspas/SQL em login e busca não pode mudar a consulta.
- Paralelismo dos três navegadores não pode reutilizar pedido ou depender da ordem dos testes.

---

### Task 1: Infraestrutura e contrato do servidor

**Files:** `cases/e2e-ecommerce-suite/package.json`, `playwright.config.ts`, `.env.example`, `src/tests/api-contracts.spec.ts`, `src/api/OrderSchema.ts`, `src/api/client.ts`, `src/db/database.ts`, `src/utils/mock-server.ts`.

**Interfaces:** `openDatabase(path)`, `getOrderById(db,id)`, `ApiClient.login/products/createOrder/getOrder`, endpoints `/login`, `/produtos`, `/carrinho`, `/pedidos`, `/health`.

- [ ] Criar configuração e teste de API com respostas esperadas 200, 201 e 400.
- [ ] Instalar dependências, executar o teste e observar falha por servidor/comportamento ausente.
- [ ] Implementar o mínimo do servidor, contratos, cliente e SQLite.
- [ ] Executar API, typecheck e conferir contrato e persistência.

### Task 2: Fluxo UI e persistência

**Files:** `src/pages/LoginPage.ts`, `CatalogPage.ts`, `CheckoutPage.ts`, `src/tests/e2e-purchase.spec.ts`, `src/utils/mock-server.ts`.

**Interfaces:** `LoginPage.signIn`, `CatalogPage.addProduct/goToCheckout`, `CheckoutPage.placeOrder`, `getOrderById`.

- [ ] Criar teste de compra que verifica UI, API e SQL com valor literal de referência.
- [ ] Executar o teste e observar falha pela UI ausente.
- [ ] Implementar as três páginas locais e Page Objects mínimos.
- [ ] Executar os três navegadores e verificar independência dos pedidos.

### Task 3: Segurança e performance

**Files:** `security/auth-security.spec.ts`, `performance/scenarios/order-load-test.js`, `performance/config/README.md`, `src/utils/mock-server.ts`.

- [ ] Criar testes de Bearer ausente, IDOR e SQL Injection; observar falhas relevantes.
- [ ] Corrigir o comportamento demonstrado pelos testes e registrar ciclo de defeito real.
- [ ] Criar script k6 com rampa/thresholds pedidos; instalar k6 quando houver script executável.
- [ ] Rodar k6 localmente e guardar métricas reais sem tokens.

### Task 4: CI e documentação profissional

**Files:** `.github/workflows/e2e-pipeline.yml`, `cases/e2e-ecommerce-suite/README.md`, `docs/qa/*`, `README.md` da raiz.

- [ ] Adicionar workflow de instalação, typecheck, Playwright, k6 e upload de evidências.
- [ ] Documentar plano, riscos, matriz, critérios, resultado e fluxo QA–DEV/defeito/reteste.
- [ ] Rodar `npm ci`, typecheck, `npx playwright test` e k6 com resultado completo.
- [ ] Verificar artefatos, revisar diff e publicar branch/PR para inspeção da CI.
