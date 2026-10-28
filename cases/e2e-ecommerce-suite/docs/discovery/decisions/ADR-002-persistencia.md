# ADR-002 — SQLite em arquivo e isolamento da carga

**Status:** solução implementada; justificativa registrada retrospectivamente. **Escopo:** persistência do mock.

**Contexto.** O teste E2E deve verificar o registro por SQL, separado da resposta da API. Um banco apenas em memória dificultaria compartilhar o estado entre processo servidor e runner; PostgreSQL exigiria instalação/serviço adicional.

**Opções.** (A) memória: simples, mas oráculo entre processos mais difícil. (B) SQLite em arquivo: SQL real, baixa infraestrutura. (C) PostgreSQL: aproximação maior de alguns ambientes, custo operacional desnecessário para este case.

**Decisão observada.** Opção B. O [helper](../../../src/db/database.ts) usa arquivo configurável por `DB_PATH`; a [configuração de carga](../../../performance/config/run-performance.mjs) usa outra instância/porta para não misturar resultados de k6 com a suíte funcional.

**Consequências.** A consulta SQL comprova persistência e valor no alvo local; não prova semântica de concorrência, transação distribuída ou tuning de PostgreSQL. O teste de carga pode encontrar contenção específica de SQLite.

**Verificação.** [Teste de compra](../../../src/tests/e2e-purchase.spec.ts), [dados e oráculos](../../qa/dados-e-oraculos.md), [configuração de carga](../../../performance/config/README.md).

**Reconsiderar quando** houver requisito de múltiplos escritores, isolamento transacional específico ou banco corporativo.
