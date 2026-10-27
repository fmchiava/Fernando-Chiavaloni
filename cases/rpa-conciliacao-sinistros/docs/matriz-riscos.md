# 3. Matriz de riscos do processo robotizado

Escala: probabilidade (`P`) e impacto (`I`) de 1 a 5. `Score = P × I`; 15–25 crítico, 8–14 alto, 1–7 moderado. Valores são **hipóteses para o case**, a calibrar com incidentes, volume e controles de um ambiente real.

| ID | Risco / gatilho | P | I | Score | Controle preventivo ou detectivo | Teste |
|---|---|---:|---:|---:|---|---|
| R-01 | API de cobertura indisponível/timeout | 4 | 5 | 20 | Timeout, retry limitado, circuit breaker operacional e item `PENDING` | CT-07, CT-08 |
| R-02 | 503 classificado como falta de cobertura | 3 | 5 | 15 | Separar resposta técnica de regra de negócio; impedir decisão após erro | CT-07, CT-08 |
| R-03 | UI muda seletor, ordem ou estado assíncrono | 4 | 4 | 16 | Seletores estáveis, espera por condição, confirmação independente | CT-09, CT-10 |
| R-04 | Pagamento divergente ou ausente | 4 | 4 | 16 | Conciliação em centavos e fila de revisão humana | CT-02, CT-05 |
| R-05 | CSV duplicado, truncado ou inválido | 3 | 4 | 12 | Validação de cabeçalho, unicidade e valores antes do lote | CT-11 |
| R-06 | Sinistro processado duas vezes após retry | 3 | 5 | 15 | Chave idempotente, constraint no banco, leitura pós-gravação | CT-12 |
| R-07 | Escrita salva, confirmação perdida por rede | 3 | 5 | 15 | Repetir apenas a leitura; marcar `UNVERIFIED` e reconciliar antes de qualquer reenvio | CT-10, CT-12 |
| R-08 | Credenciais ou dados sensíveis em log/screenshot | 3 | 5 | 15 | Vault, mascaramento, acesso mínimo e inspeção de artefatos | CT-13 |
| R-09 | Apólice inativa, ausente ou limite excedido | 3 | 4 | 12 | Tabela de regras versionada; revisão humana | CT-03, CT-04, CT-06 |
| R-10 | Falta de evidência para auditoria | 3 | 4 | 12 | JSONL estruturado, manifesto SHA-256, versão e aprovação | CT-14 |
| R-11 | API retorna 200 com conteúdo incompleto | 3 | 5 | 15 | Validar esquema e tipos antes da decisão; bloquear item | CT-15 |

Os controles da matriz definem o **estado desejado**. Retry, validação de contrato, idempotência e logs são demonstrados localmente; circuit breaker, Vault, RBAC e screenshots dependem da implementação e validação em A360.

## Priorização e dono do risco

R-01, R-02, R-03 e R-06 são bloqueadores de implantação. QA e arquitetura são responsáveis por validar controles; operação aprova o tratamento das exceções de negócio; segurança e auditoria aprovam proteção e retenção de evidências. O risco residual deve constar do parecer, com proprietário e prazo de ação.

## Indicadores de acompanhamento

- Taxa de exceção técnica por 1.000 itens, separada por API, UI e persistência.
- Taxa de encaminhamento humano por `reason_code`.
- Número de reprocessamentos e conflitos 409.
- Tempo entre falha, alerta e recuperação.
- Percentual de execuções com manifesto e trilha completos.

Os indicadores são propostas de governança; o demonstrador não simula volume suficiente para estabelecer metas estatísticas reais.
