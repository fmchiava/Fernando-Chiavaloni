# Registros de decisão técnica

Estes ADRs documentam **retrospectivamente** as escolhas visíveis na implementação. O status “implementada” significa que a solução está no repositório; não afirma que a decisão foi formalizada ou aprovada antes da construção. Cada registro apresenta contexto, opções, motivo, consequência, fonte verificável e quando reabrir a escolha.

| ADR | Decisão | Principal razão |
| --- | --- | --- |
| [001](ADR-001-alvo-local.md) | Loja e API locais sintéticas | Reprodução e controle de defeitos |
| [002](ADR-002-persistencia.md) | SQLite em arquivo e DB separado para carga | Oráculo SQL sem infraestrutura externa |
| [003](ADR-003-automacao.md) | Playwright/TypeScript, POM e oráculos UI/API/SQL | Rastreabilidade entre camadas |
| [004](ADR-004-bdd.md) | Gherkin como especificação, Playwright como runner | Linguagem de negócio sem runner duplicado |
| [005](ADR-005-carga-e-evidencia.md) | k6 com thresholds e CI com artefatos | Gate e investigação reproduzíveis |
| [006](ADR-006-integridade-e-acesso.md) | Valor e autorização controlados no servidor | Integridade e isolamento de pedidos |

As regras aceitas pelo case estão em [REQ/NFR](../../qa/contexto-e-requisitos.md); os ADRs explicam a solução, não substituem o contrato.
