# E-commerce QA Documentation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Entregar um dossiê de QA completo, fiel ao código e auditável antes de publicá-lo.

**Architecture:** README como entrada; documentação temática no case; arquivos Gherkin como especificação; relatório de revisão local. Sem alterar o sistema sob teste.

**Tech Stack:** Markdown, Gherkin, Playwright, TypeScript, k6, SQLite, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-10-27-e2e-qa-documentation-design.md`

## Global Constraints

- Trabalhar em `codex/e2e-qa-documentation` sem push ou PR até a apresentação ao usuário.
- Escrever em português claro; separar fatos observados, simulação e proposta.
- Manter links relativos válidos e comandos reproduzíveis no Windows e em sistemas Unix.
- Não criar execução BDD fictícia nem inventar histórico TDD.

## Review Focus

- Cada cenário BDD deve corresponder a um teste real ou estar marcado como cobertura planejada.
- Cada número de execução deve ter fonte verificável e commit/ambiente identificados.
- Pré-requisitos devem distinguir a suíte Playwright do k6 e indicar portas/bancos.
- Parecer Go deve ser limitado ao case sintético, sem implicar prontidão de produção real.
- Evidências públicas não devem incluir tokens ou segredos reais.

---

### Task 1: Verdade técnica e navegação

- [x] Conferir código, testes, configuração, workflows e documentos atuais.
- [x] Reescrever README do case e atualizar a entrada do monorepo.
- [x] Criar índice e arquitetura com limites explícitos.

### Task 2: Requisitos e execução

- [x] Definir processo, regras, atores, contratos e critérios de aceite.
- [x] Documentar pré-requisitos, dados, instalação, comandos e solução de problemas.
- [x] Detalhar estratégia, riscos, níveis, oráculos e gates.

### Task 3: BDD, TDD e rastreabilidade

- [x] Criar especificações Gherkin legíveis e indicar que não são executadas por runner BDD.
- [x] Descrever ciclo TDD e evidência real do QA-001 sem extrapolação.
- [x] Mapear requisito → risco → BDD → teste → evidência e lacunas.

### Task 4: Governança e evidência

- [x] Reescrever segurança, ciclo de defeito, QA-001, execução e parecer.
- [x] Detalhar perfil de carga e política de evidência.
- [x] Revisar comandos, links, consistência, segredos e registrar o resultado da revisão.
- [x] Executar verificações técnicas pertinentes, salvar em commit local e apresentar antes de publicar.
