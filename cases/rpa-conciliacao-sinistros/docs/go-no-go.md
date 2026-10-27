# 5. Checklist Ready for Production e parecer técnico

## Checklist de liberação

| Controle | Evidência exigida | Estado deste portfólio |
|---|---|---|
| Requisitos e critérios de aceite aprovados | Versão e aceite do dono do processo | Modelo documentado; aprovação real pendente |
| Riscos críticos tratados | Matriz R-01 a R-11, testes ligados e risco residual aceito | Matriz e testes locais disponíveis; HML pendente |
| P0/P1 e regressão | 100% aprovados; zero defeitos críticos/altos abertos | Subconjunto local executável; A360 pendente |
| Recuperação, idempotência e reversão | CT-07/08/10/12 e ensaio de rollback de versão | Falha da leitura pós-escrita coberta localmente; perda da resposta do POST e ensaio em HML pendentes |
| Segurança e segregação | Vault, RBAC, mascaramento, revisão de permissões | Desenho documentado; configuração real pendente |
| Observabilidade e auditoria | IDs correlacionados, logs, screenshots de falha, hashes e retenção | JSONL/manifesto local; screenshots A360 pendentes |
| Operação e suporte | Runbook, alertas, responsáveis, SLA e fila humana | Modelo documentado; validação operacional pendente |
| Implantação | Versão assinada/revisada, janela, smoke e plano de retorno | Não executada neste case |

**Regra de decisão:** `GO` somente se todos os controles obrigatórios estiverem aprovados e assinados pelos responsáveis; `NO_GO` se houver risco crítico sem mitigação, defeito P0/P1 aberto, evidência ausente, falha técnica não resolvida ou aprovação pendente. O campo `gate` de `qa_demo.py` é **somente um gate técnico da execução sintética**, não autorização de implantação.

## Modelo de parecer técnico

```text
Parecer ID: QA-REL-____
Versão do bot / dependências: ____
Ambiente e janela: ____
Requisitos e casos cobertos: ____
P0: __/__  P1: __/__  P2: __/__
Defeitos abertos e risco residual: ____
Evidências: URI controlada + hash SHA-256 + run_id ____
Segurança / auditoria: ____
Plano de reversão e smoke: ____
Recomendação QA: GO / NO_GO / GO condicionado (somente se política permitir)
Justificativa objetiva: ____
Aprovações: QA ____ | Negócio ____ | Operação ____ | Segurança ____
Data/hora UTC: ____
```

## Parecer do demonstrador

O fluxo `--fault first` deve evidenciar recuperação de 503 e decisões coerentes. O fluxo `--fault always` deve evidenciar `NO_GO`, sem decisão indevida. O fluxo `--fault verify_always` deve evidenciar `UNVERIFIED` e bloquear reprocessamento automático após a escrita. Mesmo que os testes locais estejam aprovados, o parecer de **produção real permanece NO_GO** até execução dos casos pendentes na plataforma e assinatura dos responsáveis. Isso evita confundir uma prova de conceito com homologação corporativa.
