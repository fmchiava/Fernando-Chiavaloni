# 2. Arquitetura de automação e tratamento de erros no A360

## Fluxo proposto

| Etapa | Ação no A360 | Saída/controle |
|---|---|---|
| Inicializar | Obter credenciais por `Credential Vault`; carregar parâmetros não secretos e ID da execução | Segredos nunca embutidos no bot nem no log |
| Ler fila | Abrir navegador, localizar linhas da fila por seletores estáveis e capturar ID/apólice/valor | Validar unicidade, formato e status `PENDING` |
| Validar cobertura | Chamar API REST com timeout explícito e cabeçalho de correlação | Aceitar somente contrato esperado; 404 vira exceção de negócio; 429/5xx/timeout são técnicos |
| Confrontar pagamento | Ler CSV controlado ou chamar script Python validado; normalizar valores em centavos | Arquivo duplicado/inválido bloqueia lote |
| Decidir | Aplicar a tabela de regras de `processo.md` | Registrar motivo explícito |
| Persistir | Preencher formulário da UI com `request_id` estável e salvar | Reler API de consulta para confirmar estado |
| Encerrar | Consolidar logs, evidências, contagens e status de execução | Falha antes do envio mantém `PENDING`; escrita sem confirmação fica `UNVERIFIED`; nenhum segredo nas evidências |

O `qa_demo.py` reproduz a lógica para estudo. Não substitui os comandos de navegador, REST, arquivo e Credential Vault da plataforma.

## Estrutura sugerida de bots

- `BOT_Main_Conciliacao`: orquestra lote, mede SLA, consolida relatório e aborta se o serviço crítico estiver indisponível.
- `BOT_Validar_Sinistro`: executa um item, aplica regras e retorna `{outcome, reason_code, correlation_id}`.
- `BOT_Registrar_Decisao`: salva na UI e confirma via leitura independente; recebe chave idempotente.
- `BOT_Emitir_Evidencia`: grava evento estruturado e screenshot de falha após mascaramento.

Evite repetir lógica de retry e classificação de erros em cada subbot. Configure retry **apenas** para falhas transitórias, com tentativas limitadas e espera crescente. Não repita uma escrita quando seu resultado for desconhecido sem antes consultar o estado ou reutilizar a mesma chave idempotente.

## `Try / Catch / Finally` e compensação

```text
Try (lote)
  obter credenciais do Vault; abrir navegador e arquivo
  para cada sinistro PENDING:
    Try (item)
      ler UI → validar API → confrontar pagamento → decidir
      salvar com request_id estável → confirmar por leitura
    Catch exceção de negócio
      registrar motivo; encaminhar REVIEW quando o contrato permitir
    Catch exceção de sistema
      antes da escrita: não salvar decisão; registrar erro técnico
      após envio sem confirmação: marcar UNVERIFIED e reconciliar estado
      registrar screenshot mascarada; não repetir POST automaticamente
    Finally (item)
      fechar contexto do item; emitir evento final
Catch falha crítica do lote
  suspender novos itens; marcar NO_GO operacional
Finally (lote)
  fechar navegador/arquivo/conexões e consolidar manifesto
```

`Finally` encerra recursos; não “desfaz” automaticamente uma escrita já confirmada. SQLite executa rollback de transação local quando a escrita falha. Em sistemas distribuídos, a compensação é consultar o estado e abrir uma tarefa controlada de correção ou estorno; nunca prometer rollback atômico entre UI, API e arquivo. A [documentação do Error handler](https://docs.automationanywhere.com/r/automation-360/cloud-error-handling-command) descreve `Try`, `Catch`, `Finally` e `Throw`.

## Governança e segurança

- **Credenciais:** locker e permissões mínimas no Credential Vault; rotação e revogação seguindo política do ambiente. Configurações e mudanças são auditáveis no Control Room. [Credential Vault](https://docs.automationanywhere.com/r/automation-360/cloud-configure-credential-vault-connection).
- **Acesso:** papéis separados para criar, revisar, implantar e executar; contas de serviço sem privilégio administrativo desnecessário.
- **Versão:** bot e dependências versionados; revisão por par, tag de release, artefato imutável e plano de rollback de versão. Promover DEV → HML → PROD somente após gate aprovado. [Bot Lifecycle Management](https://docs.automationanywhere.com/r/automation-360/cloud-bot-lifecycle-management).
- **Observabilidade:** `run_id`, `claim_id`, `correlation_id`, evento, resultado, tentativa, duração e código de motivo. Relacionar isso às atividades e ao Audit Log do Control Room. [Administração e Audit Log](https://docs.automationanywhere.com/r/automation-360/cloud-manage).
- **Proteção de dados:** capturar telas somente em falhas, mascarar campos sensíveis, limitar retenção e controlar acesso ao repositório de evidências.
