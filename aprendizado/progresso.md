# Progresso em QA e IA

**Atualizado em:** 22/10/2026

**Objetivo:** transformar minha experiência em QA, APIs e dados em avaliações reproduzíveis de aplicações com IA.

## Estudos registrados

| Tema | Fonte que estudei | Aplicação que pretendo demonstrar | Evidência atual |
| --- | --- | --- | --- |
| Engenharia de prompts | [Claude Platform Docs](https://platform.claude.com/docs/pt-BR/intro) e guia de prompt engineering consultado no meu acervo | Comparar duas versões de um prompt com a mesma base de casos e uma rubrica explícita. | Leitura e síntese privadas; experimento público pendente. |
| Fluxos e agentes | [Building effective agents — Anthropic](https://www.anthropic.com/research/building-effective-agents) | Testar escolhas de ferramenta, critérios de parada, exceções e intervenção humana. | Leitura e síntese privadas; execução pendente. |
| UX de agentes | [AI Design Guide — recursos públicos](https://www.aidesign.guide/agentic-ux-patterns) | Verificar plano visível, aprovação com escopo, estados de erro e possibilidade de recuperação. | Checklist de estudo no Obsidian; testes de interface pendentes. |

O estudo dessas fontes **não equivale a experiência profissional ou domínio comprovado**. Os experimentos abaixo são o caminho para produzir evidências.

## Próximas entregas

| Ordem | Experimento | Critério para marcar como concluído | Estado |
| --- | --- | --- | --- |
| 1 | Diagnóstico e mapa de riscos de um assistente fictício | Fluxo, três riscos priorizados e critérios de aceite revisados. | Planejado |
| 2 | Avaliação de prompts | Dataset sintético, rubrica, comparação A/B e análise de falhas por caso. | Planejado |
| 3 | Contratos de API e qualidade de dados | Testes executáveis, dados de exemplo e comando de reprodução. | Em andamento: [laboratório de CSV](../laboratorio/importacao_chamados/README.md) executável; API pendente. |
| 4 | Recuperação de informação (RAG) | Separar falha de busca, contexto, resposta e citação; registrar resultados. | Planejado |
| 5 | Agente com ferramentas | Casos de permissão, falha, parada e aprovação humana, com trilha de execução. | Planejado |

## Regra de atualização

Uma entrega só muda para **concluída** quando eu puder apontar código ou artefato, versão, data, comando de reprodução e resultado observado. Quando um teste falhar ou ficar inconclusivo, registro o fato e a hipótese de causa. Dados e documentos usados em demonstrações públicas serão sintéticos.

## Registro de prática

**21/10/2026 — Qualidade de dados em importação CSV.** Publiquei uma [implementação mínima e testes automatizados](../laboratorio/importacao_chamados/README.md) derivados da matriz de riscos. O exercício cobre validação de campos, reimportação, conflito e atomicidade. Ele não comprova teste de API, integração com banco de dados ou avaliação de IA; essas etapas continuam na trilha.
