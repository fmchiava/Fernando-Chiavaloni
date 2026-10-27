# 6. Padrão de evidências auditáveis

## Pacote por execução

`events.jsonl` contém um evento JSON por linha; `summary.json` consolida contagens e decisões; `report.md` fornece leitura humana; `manifest.json` guarda SHA-256 dos artefatos, das duas massas sintéticas e dos dois scripts que executam o fluxo. Todos compartilham `run_id`. Os exemplos estão em `examples/` e são **sintéticos**.

Execute `python analyze_logs.py examples/go` para verificar os hashes, conferir o `run_id`, contar retries/decisões/erros e detectar itens iniciados sem evento final. Uma alteração posterior em qualquer artefato assinado pelo manifesto faz o analisador falhar com código 2.

Exemplo de esquema de evento (valores ilustrativos):

```json
{"ts_utc":"2026-10-26T12:00:00+00:00","run_id":"...","claim_id":"SIN-001","correlation_id":"...","component":"qa_demo","event":"api_retry","outcome":"RETRY","attempt":1,"http_status":503}
```

Campos mínimos: horário UTC, versão/ambiente, `run_id`, `claim_id`, `correlation_id`, componente, evento, resultado, código técnico ou de negócio e tentativa quando aplicável. Capturar duração da chamada de API permite comparar falhas com timeouts e variações de latência. O exemplo local registra duração em chamadas bem-sucedidas.

Após o envio da decisão, `decision_submitted` registra a chave idempotente. `decision_verified` só aparece depois de leitura consistente; falha persistente de confirmação produz `decision_unverified`, `UNVERIFIED` no resumo e gate `NO_GO`. Esse estado é uma classificação do **conhecimento da automação**, não um estado confirmado do banco.

## Evidência de falha na plataforma

Em execução A360, incluir no pacote: screenshot da UI no momento da falha, estado da fila, resposta HTTP **sanitizada**, identificador da atividade no Control Room, trecho de log do Bot Agent quando necessário, versão do bot e hashes dos arquivos. A screenshot deve ser capturada **após mascarar** nome, CPF, apólice real, tokens e outras informações restritas. Se a política proibir captura, registrar o motivo e usar evidência alternativa aprovada. O demonstrador Python não fabrica screenshots.

## Cadeia de custódia e retenção

1. Salvar os arquivos em repositório de evidências com acesso controlado, não em pasta pública de execução real.
2. Gerar manifesto SHA-256 depois de finalizar o pacote; qualquer alteração posterior exige novo pacote/versão.
3. Vincular `run_id` ao caso de teste, defeito, mudança e parecer.
4. Aplicar retenção e descarte conforme política organizacional; este case não define prazo legal.
5. Validar a integridade recalculando o hash: `python -c "import hashlib,pathlib; print(hashlib.sha256(pathlib.Path('runs/execucao-transitoria/events.jsonl').read_bytes()).hexdigest())"`.

O manifesto protege contra alteração não percebida; por si só, **não autentica autoria**. Em uso real, acrescente armazenamento imutável, controle de acesso e assinatura/ateste conforme a política local.
