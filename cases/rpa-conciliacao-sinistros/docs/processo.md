# 1. Contexto do negócio e contrato do processo

## Objetivo

Conciliar sinistros de até R$ 1.000,00 quando cobertura e pagamento forem consistentes. O resultado `CONCILIATED` só pode ser salvo quando todas as verificações passarem. Qualquer dúvida de negócio gera `REVIEW`; falha técnica antes da escrita preserva `PENDING`. Falha após uma escrita possivelmente aceita exige `UNVERIFIED` no relatório até reconciliação.

## Fontes e fronteiras

| Fonte | Contrato demonstrado | Proprietário lógico |
|---|---|---|
| UI `/claims` | `claim_id`, `policy_id`, `amount_cents`, status | Operação de sinistros |
| API `GET /api/coverage/{policy_id}` | `active`, `limit_cents`; 404 para apólice ausente; 503 injetável | Serviço de cobertura |
| `fixtures/pagamentos.csv` | Cabeçalho exato `claim_id,paid_cents`; IDs únicos e valores inteiros não negativos em centavos | Conciliação financeira |
| UI `POST /claims/{id}/decision` | `outcome`, `reason_code`, `request_id` | Aplicação de sinistros |
| SQLite | `claims` e `decisions`, com chave única por sinistro e request ID | Demonstrador |

Valores monetários são **inteiros em centavos** para evitar arredondamento binário. Dados de exemplo: `SIN-001` concilia R$ 800,00; `SIN-002` tem divergência de R$ 200,00; `SIN-003` tem apólice inativa. Nenhum dado pessoal é necessário.

## Regras de decisão, em ordem

1. Apólice não localizada → `REVIEW / POLICY_NOT_FOUND`.
2. Apólice inativa → `REVIEW / INACTIVE_POLICY`.
3. Valor do sinistro acima do limite de cobertura → `REVIEW / OVER_LIMIT`.
4. Pagamento ausente no arquivo → `REVIEW / MISSING_LEDGER`.
5. Valor pago diferente do sinistro → `REVIEW / AMOUNT_MISMATCH`.
6. Todos os controles aprovados → `CONCILIATED / MATCHED`.

Uma resposta 503, timeout, UI indisponível ou falha de escrita é **exceção de sistema**. Nenhuma dessas condições autoriza decisão de negócio. Antes do envio da decisão, o item permanece `PENDING`. Após o envio, se a resposta ou leitura de confirmação se perder, o estado real é desconhecido para o cliente: registrar `UNVERIFIED`, bloquear reenvio automático e consultar a persistência.
Cabeçalho duplicado, coluna inesperada e linha truncada no arquivo de pagamentos também bloqueiam o lote antes de qualquer decisão.

## Invariantes

- Um sinistro admite no máximo uma decisão persistida; a mesma requisição é idempotente e uma decisão divergente retorna 409.
- Após salvar pela UI, a automação lê `GET /api/claims/{id}` para confirmar resultado e motivo.
- A leitura de confirmação usa retry limitado, sem repetir o POST. Se continuar indisponível, o parecer registra `UNVERIFIED`, mesmo que a escrita tenha ocorrido.
- Reprocessamento não pode criar decisão duplicada nem trocar `CONCILIATED` por `REVIEW` silenciosamente.
- Dados de teste ficam isolados; artefatos publicados são marcados `SYNTHETIC`.

## Critérios de aceite do processo

`AC-01` conciliar somente a combinação ativa + dentro do limite + pagamento igual. `AC-02` encaminhar divergências para humano com motivo específico. `AC-03` não gravar decisão durante indisponibilidade técnica. `AC-04` recuperar HTTP transitório dentro do orçamento de tentativas. `AC-05` garantir rastreabilidade por sinistro, execução e correlação. `AC-06` verificar a decisão persistida e preservar idempotência.
