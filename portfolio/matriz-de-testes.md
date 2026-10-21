# Exemplo de estratégia de testes: importação de chamados

**Estado:** modelo de análise; ainda não executado nem automatizado.

**Data:** 21/10/2026.

**Contexto:** sistema fictício para importar chamados de suporte a partir de CSV. Todos os dados abaixo são sintéticos.

## Problema e contrato assumido

O sistema recebe linhas com `id_externo`, `data`, `categoria`, `descricao` e `status`. Cada linha válida cria um chamado. A mesma combinação de `id_externo` e `data` representa a mesma ocorrência e não deve gerar duplicata ao importar o arquivo novamente. `categoria` aceita `acesso`, `erro` ou `duvida`; `status` inicial deve ser `aberto`.

Antes de codificar os testes, eu confirmaria essas regras com a pessoa responsável pelo produto. Elas são **premissas deste exercício**, não regras de um cliente real.

## Riscos priorizados

| Risco | Impacto | Verificação proposta |
| --- | --- | --- |
| Importação duplicada | Contagem e indicadores incorretos | Importar o mesmo arquivo duas vezes e comparar IDs e totais. |
| Campo obrigatório ausente | Chamado inutilizável | Rejeitar a linha e retornar erro que identifique campo e linha. |
| Categoria inesperada | Classificação e roteamento errados | Rejeitar valor fora da lista sem converter silenciosamente. |
| Falha em lote | Perda parcial não percebida | Definir se a importação é atômica ou parcial e testar o comportamento acordado. |
| Dados pessoais acidentais | Exposição indevida | Usar somente dados sintéticos e verificar logs e mensagens de erro. |

## Casos mínimos

| ID | Entrada | Resultado esperado |
| --- | --- | --- |
| CT-01 | Uma linha válida com ID `T-100`, data `2026-10-21`, categoria `erro` e descrição preenchida. | Um chamado `aberto`; campos preservados. |
| CT-02 | Reimportar a linha de CT-01. | Nenhum novo chamado; retorno informa duplicidade ou operação idempotente conforme contrato. |
| CT-03 | Mesmo ID `T-100` em `2026-10-22`. | Novo chamado apenas se o produto confirmar que ID e data identificam ocorrências distintas. |
| CT-04 | Descrição vazia. | Linha rejeitada com erro específico; nenhum chamado inválido. |
| CT-05 | Categoria `financeiro`. | Linha rejeitada como categoria desconhecida. |
| CT-06 | Arquivo com uma linha válida e outra inválida. | Resultado depende da decisão de negócio sobre atomicidade; registrar essa decisão antes da execução. |

## O que falta para virar evidência técnica

- Definir contrato de erro e regra de atomicidade com critérios de aceite fechados.
- Criar CSV sintético versionado e uma API ou implementação de referência.
- Automatizar os casos e publicar comando de execução, ambiente e resultado.
- Registrar ao menos um defeito ou limite encontrado e a decisão correspondente.

Este exercício foi estruturado com assistência de IA como ponto de partida para minha revisão. **A tabela não representa testes executados nem resultados de um projeto profissional.**
