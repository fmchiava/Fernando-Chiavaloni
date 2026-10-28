# Índice e política das evidências

Uma evidência útil permite responder **qual versão, ambiente, dado, comando, resultado e critério** foram usados. Este diretório conserva o que é pequeno e estável no Git; arquivos grandes e temporários são produzidos localmente ou pela CI.

| Evidência | Origem | Como avaliar |
| --- | --- | --- |
| [Relatório de execução](execution.md) | Comandos locais e runs do `master` em 27/10/2026 | Confrontar gate, commit, contagem e links |
| [QA-001 vermelho](QA-001-red-sanitized.txt) | Mutação controlada da checagem de titularidade | Localizar `Expected: 404 / Received: 200` |
| [QA-001 verde](QA-001-green-sanitized.txt) | Reteste isolado após restauração | Localizar `1 passed` |
| [Resumo k6 JSON](local-performance/summary.json) e [HTML](local-performance/summary.html) | Execução local de carga | Conferir p95, taxa de falha e checks |
| [Resumo k6 da revisão documental](documentation-review-performance/summary.json) e [HTML](documentation-review-performance/summary.html) | Nova execução local, preservada antes da publicação documental | Conferir 1.516 checks, p95 12,85 ms e thresholds |
| [Resumo k6 da publicação](publication-performance/summary.json) e [HTML](publication-performance/summary.html) | Gate local em 28/10/2026, antes do envio ao GitHub | Conferir 1.504 pedidos, p95 36,53 ms e thresholds |
| [Artefato da CI no master](https://github.com/fmchiava/sdet-portfolio/actions/runs/40561541646/artifacts/12760268314) | Workflow no commit `041c4c3` | Baixar Playwright HTML e k6 HTML/JSON |

O workflow configura **30 dias de retenção** para o artefato. O resumo versionado e os comandos de reprodução continuam disponíveis depois do vencimento do download. Relatórios verdes não contêm necessariamente screenshot ou trace: a configuração retém esses arquivos **somente em falhas**. O trace do experimento QA-001 foi gerado localmente, mas não foi versionado; sua evidência permanente é a saída sanitizada.

## Cadeia de custódia prática

1. Identifique commit e run antes de interpretar o número.
2. Compare o resultado ao limiar definido no [plano](../test-strategy.md), não a uma expectativa escolhida após a execução.
3. Preserve saída bruta gerada em área ignorada pelo Git; publique apenas o necessário e remova caminhos locais, tokens e dados reais.
4. Associe falha ao [ticket](../defects/QA-001-idor.md) e reteste ao mesmo requisito. Não reescreva o resultado vermelho como verde.
5. Registre lacunas e decisão no [parecer](../release-decision.md).

As contas e senhas deste case são sintéticas. Mesmo assim, traces de uma execução futura podem registrar cabeçalhos e payloads; revise o conteúdo antes de distribuir um artefato.
