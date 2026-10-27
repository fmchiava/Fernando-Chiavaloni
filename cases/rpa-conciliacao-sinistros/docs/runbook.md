# Runbook operacional de referência

## Antes da execução

Confirmar versão aprovada do bot, janela, disponibilidade da API, validade do arquivo de pagamentos, acesso mínimo ao Vault, espaço de armazenamento de evidências e canal de suporte. Registrar responsável de plantão e `run_id`.

## Durante a execução

Monitorar contagem de `CONCILIATED`, `REVIEW`, `PENDING` e `UNVERIFIED`, taxa de 429/5xx, latência e erros de UI. Alerta imediato se houver decisão sem confirmação posterior, conflito 409, falha de credencial ou aumento súbito de revisões por um mesmo motivo.

## Contenção

1. Pausar novos itens no Control Room; preservar logs, atividade e versão.
2. Separar itens `PENDING` sem envio de itens `UNVERIFIED` com escrita possivelmente concluída.
3. Consultar o estado persistido antes de qualquer reprocessamento.
4. Abrir incidente com horário UTC, `run_id`, `correlation_id`, quantidade afetada e hipótese inicial.
5. Encaminhar decisão financeira já efetuada para revisão humana; não executar estorno automático.

## Reprocessamento e retorno

Com causa corrigida e gate aprovado, reprocessar somente `PENDING` após verificar o estado no sistema de registro. Para `UNVERIFIED`, reconciliar primeiro com o banco/API e registrar o resultado; só considerar reenvio controlado com a mesma chave idempotente se não houver decisão persistida. Conflito 409 exige análise, não sobrescrita. Se a versão recém-publicada falhar, suspender execução, restaurar a versão anterior aprovada conforme procedimento de lifecycle e fazer smoke com massa controlada. Confirmar que o pacote de evidências ficou íntegro e registrar encerramento do incidente.

## Responsabilidades

QA valida testes e parecer; operação acompanha fila e exceções humanas; desenvolvimento corrige e revisa o bot; arquitetura avalia impacto de contratos; segurança/auditoria validam acesso e evidências. O dono do processo aprova a retomada de decisões automáticas.
