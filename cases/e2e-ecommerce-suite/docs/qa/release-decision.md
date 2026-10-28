# Parecer técnico de qualidade — versão integrada

**Data:** 27/10/2026. **Versão avaliada:** `master` no merge `041c4c3`. **Decisão:** **Go para apresentar este case sintético no portfólio**. Não se trata de autorização para operar uma loja real. A reescrita documental em branch local será apresentada para revisão antes de publicação.

| Critério de saída definido na estratégia | Resultado | Base da decisão |
| --- | --- | --- |
| Typecheck sem erros | Aprovado | Execução local pós-merge e [gate remoto](https://github.com/fmchiava/sdet-portfolio/actions/runs/40561541646) |
| UI, API, segurança e SQLite | Aprovado no escopo automatizado | 10/10 Playwright local e remoto; três navegadores na UI |
| Autorização do pedido e QA-001 | Aprovado para o cenário testado | [Vermelho/verde](defects/QA-001-idor.md), 404 para Beta e 200 para Alfa |
| k6 p95 < 500 ms, falha HTTP < 1%, checks > 99% | Aprovado | Local 73,77 ms/0%/100%; CI 13,81 ms/0%/100%; [métricas](evidence/execution.md) |
| Evidência recuperável | Aprovado | [Artefato remoto](https://github.com/fmchiava/sdet-portfolio/actions/runs/40561541646/artifacts/12760268314) e [resumo estável](evidence/README.md) |
| Regressão do monorepo | Aprovado | [Python](https://github.com/fmchiava/sdet-portfolio/actions/runs/40561541748) e [API anterior](https://github.com/fmchiava/sdet-portfolio/actions/runs/40561542013) verdes no merge |

## Riscos residuais e decisão de tratamento

Não há defeito S1/S2 **aberto dentro dos cenários executados**. A [matriz](traceability.md) registra cobertura parcial para limites superiores de quantidade, GET sem token/ID inexistente e carrinho válido sem escrita em `orders`. Expiração de sessão, rate limiting, TLS, pagamentos e infraestrutura distribuída estão fora do escopo. A UI usa ponto decimal em `R$ 129.90`; a apresentação `pt-BR` fica como melhoria futura. Essas lacunas não são descritas como testes aprovados e exigiriam critérios próprios antes de qualquer uso fora deste mock.

## Condição de No-Go para próxima revisão

Reabrir o parecer se uma mudança no código, massa ou workflow derrubar qualquer gate, se um retry ocultar falha intermitente relevante, se o artefato não for publicado ou se um defeito alto surgir. Uma nova versão precisa de novo run e novo registro de decisão; este documento é um **snapshot**, não uma aprovação permanente.

**Responsabilidade no case:** parecer elaborado pelo papel de QA do estudo. Não há aceite de negócio real nem equipe de aprovação externa. A [execução](evidence/execution.md) contém os dados que sustentam a decisão.
