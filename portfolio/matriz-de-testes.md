# Exemplo de estratégia de testes: importação de chamados

**Estado:** premissas e casos do exercício documentados; subconjunto automatizado no [laboratório de importação](../laboratorio/importacao_chamados/README.md).

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
| CT-03 | Mesmo ID `T-100` em `2026-10-22`. | No exercício, a chave composta define outra ocorrência; em produto real, confirmar a regra antes de implementá-la. |
| CT-04 | Descrição vazia. | Linha rejeitada com erro específico; nenhum chamado inválido. |
| CT-05 | Categoria `financeiro`. | Linha rejeitada como categoria desconhecida. |
| CT-06 | Arquivo com uma linha válida e outra inválida. | No exercício, rejeitar o lote inteiro; em produto real, decidir atomicidade com o negócio. |

## Evidência executável e limites

Os testes do [laboratório](../laboratorio/importacao_chamados/README.md) exercitam os casos desta matriz, mais cabeçalho incompleto ou duplicado, linha truncada, coluna extra, data inválida, status inicial incorreto e conflito de atualização. Rodam em memória, com CSV sintético no próprio teste e sem dependências externas. O comando e as versões de Python verificadas estão no README do laboratório.

Ainda faltam contrato validado com um produto real, integração com API ou banco de dados, observabilidade e avaliação de dados pessoais em ambiente real. Este exercício foi estruturado com assistência de IA. **Os testes são de um sistema fictício e não representam entregas de um cliente.**
