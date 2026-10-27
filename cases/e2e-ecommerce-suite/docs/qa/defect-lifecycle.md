# Procedimento de triagem e comunicação QA–DEV

## Da observação à decisão

1. **Detectar:** vincular a falha a requisito, risco e cenário da [matriz](traceability.md); preservar comando, ambiente e saída bruta gerada.
2. **Classificar:** *defeito* quando o comportamento viola um critério; *melhoria* quando propõe um comportamento novo; *bloqueio de ambiente* quando o alvo não pode ser exercitado. Separar severidade (impacto) de prioridade (ordem de tratamento).
3. **Registrar:** título, versão/commit, pré-condições, dados sintéticos, passos mínimos, esperado/obtido, impacto, evidência e frequência. Não incluir tokens ou credenciais reais.
4. **Triar com DEV:** reproduzir, localizar fronteira e causa, acordar alteração mínima e critério de aceite. Neste case, os papéis DEV/QA são **simulados**; o [QA-001](defects/QA-001-idor.md) registra a conversa técnica proposta.
5. **Corrigir e retestar:** executar primeiro o cenário que falhou, depois regressão por risco (segurança, contrato, compra em três navegadores, carga se afetada). Anexar os resultados vermelho/verde.
6. **Encerrar:** QA emite parecer com riscos residuais e Go/No-Go. Reabertura exige nova evidência observável.

## Campos mínimos do report de bug

`ID · título · requisito/risco · severidade · prioridade · versão · ambiente · pré-condição · passos · esperado · observado · evidência · causa raiz · correção/commit · reteste · regressão · decisão`.

O [QA-001](defects/QA-001-idor.md) é o exemplo preenchido. Logs e traces completos ficam no artefato da execução correspondente; resumos estáveis e sem segredos ficam no Git.
