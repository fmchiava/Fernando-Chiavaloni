# 4. Plano, estratégia e casos de teste

## Objetivo, escopo e oráculo

Validar regras de decisão, contratos UI/API/CSV, resiliência, persistência e evidências. O **oráculo** é a tabela de regras em `processo.md` mais o estado consultado após a gravação. Não basta o bot encerrar sem erro ou exibir uma mensagem de sucesso.

Camadas: (1) validação de contrato e dados; (2) testes de integração do simulador; (3) execução assistida do bot A360 em HML; (4) smoke controlado após implantação. O demonstrador automatiza apenas as duas primeiras. Para A360, executar os mesmos casos em ambiente segregado com credenciais de teste.

## Condições de entrada e saída

**Entrada:** requisitos e critérios de aceite aprovados, massa sintética versionada, API/ambiente disponíveis, papéis e acessos segregados, versão do bot identificada, observabilidade habilitada. **Saída:** 100% dos casos P0 e P1 aprovados, nenhum defeito crítico/alto aberto, evidências completas, aprovação de negócio/segurança/QA e plano de reversão ensaiado. Casos abaixo não executados em A360 devem constar como pendentes no gate.

## Matriz de cenários

| ID | Prioridade | Situação e dados | Esperado | Tipo | Automação local |
|---|---|---|---|---|---|
| CT-01 | P0 | `SIN-001`: apólice ativa, R$ 800 pago, limite R$ 1.000 | `CONCILIATED/MATCHED` | Happy path | Sim |
| CT-02 | P0 | `SIN-002`: sinistro R$ 700, pagamento R$ 500 | `REVIEW/AMOUNT_MISMATCH` | Negócio | Sim |
| CT-03 | P1 | `SIN-003`: apólice inativa | `REVIEW/INACTIVE_POLICY` | Negócio | Sim |
| CT-04 | P1 | Valor acima do limite, apólice ativa | `REVIEW/OVER_LIMIT` | Negócio | Planejado para HML |
| CT-05 | P1 | Linha de pagamento ausente | `REVIEW/MISSING_LEDGER` | Negócio | Planejado para HML |
| CT-06 | P1 | API retorna 404 para apólice inexistente | `REVIEW/POLICY_NOT_FOUND` | Contrato/negócio | Planejado para HML |
| CT-07 | P0 | Primeira resposta API = 503, depois 200 | Retry, resultado correto, sem falsa rejeição | Sistema/resiliência | Sim |
| CT-08 | P0 | API = 503 em todas as tentativas | `PENDING`, erro técnico, `NO_GO` | Sistema | Sim |
| CT-09 | P0 | Estrutura da UI alterada | Falha detectada, item sem decisão; screenshot mascarada em A360 | UI | Detecção local; screenshot A360 pendente |
| CT-10 | P0 | Confirmação da escrita falha uma vez ou continuamente | Repetir somente a leitura; resultado correto ou `UNVERIFIED` com `NO_GO`, sem novo POST | Resiliência | Sim para falha da leitura; perda da resposta do POST pendente |
| CT-11 | P1 | CSV com ID duplicado, cabeçalho duplicado, coluna extra ou ausente, valor negativo | Bloquear lote e abrir incidente de dados | Dados | Sim para duplicidade e esquema; demais variações pendentes |
| CT-12 | P0 | Reenviar mesma decisão e tentar decisão divergente | 200 idempotente; 409 no conflito | Persistência | Sim |
| CT-13 | P0 | Inspecionar logs, Vault e screenshots de falha | Nenhum segredo/dado sensível exposto | Segurança | Inspeção manual |
| CT-14 | P1 | Conferir eventos, resumo, hashes e correlação | Manifesto íntegro e trilha reconstituível | Auditoria | Sim |
| CT-15 | P0 | API responde 200 com JSON incompleto | Contrato inválido; item `PENDING`; `NO_GO` | API/dados | Sim |

“Parcial” significa que uma regra ou mecanismo é exercitado localmente, mas não o fluxo inteiro em A360. Nenhum caso planejado deve ser declarado aprovado sem execução real.

## Massa e técnicas de desenho

- Partições: cobertura ativa/inativa/inexistente; pagamento igual/divergente/ausente; resposta API 200/404/429/503/timeout.
- Limites: R$ 0,00, R$ 1.000,00 e R$ 1.000,01; moeda representada em centavos inteiros.
- Transições confirmadas: `PENDING → CONCILIATED` ou `PENDING → REVIEW`. Falha técnica antes da escrita mantém `PENDING`; falha de confirmação pós-envio gera `UNVERIFIED` no relatório até reconciliação. Conflito não altera a decisão persistida.
- Injeção de falhas determinística (`--fault first` e `--fault always`) evita depender de incidentes aleatórios.

## Execução e registro de defeitos

Para cada caso: ID, versão, dados de entrada e hash, pré-condição, passos, resultado esperado, resultado observado, horário UTC, `run_id`, `correlation_id`, severidade, evidências e responsável. Um defeito é reaberto se o reteste passa isoladamente mas a regressão quebra outro ramo. O parecer final lista cobertura, falhas residuais e decisão recomendada.

Comandos: `python -m unittest discover -s tests -v`; execução E2E local via `README.md`. A suíte cobre um subconjunto de CTs. O gate real exige complementação em A360/HML.
