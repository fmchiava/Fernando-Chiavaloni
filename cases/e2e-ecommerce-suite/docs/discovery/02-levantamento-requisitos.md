# Levantamento e qualidade dos requisitos

## Método aplicado e método proposto

**Aplicado nesta revisão:** leitura do código, contrato, testes, pipeline e evidências; reconstrução da jornada; identificação de regras, exemplos positivos/negativos e lacunas. A [lista de requisitos vigente](../qa/contexto-e-requisitos.md) é a fonte única dos IDs REQ/NFR. Esta página explica como levantá-los e refiná-los, sem duplicar sua redação normativa.

**Proposto para um projeto com stakeholders:** entrevista curta por perspectiva, observação do fluxo atual, revisão de exemplos reais anonimizados e sessão de Example Mapping. Para cada história, discutir **regra → exemplo → dúvida** antes de automatizar. Não há registro de que essas atividades tenham ocorrido neste case.

## Inventário do que deve ser explicitado

| Tema | Regra atual / fonte | Exemplo de aceite ou dúvida | Estado |
| --- | --- | --- | --- |
| Identidade | REQ-01; `POST /login` | Credencial válida recebe token; inválida não cria sessão útil. | Implementado; casos inválidos ainda parciais. |
| Catálogo | REQ-02; `GET /produtos` | SKU e preço em centavos; busca não altera catálogo. | Implementado. |
| Carrinho | REQ-03; `POST /carrinho` | Bearer obrigatório; total calculado no servidor. | Implementado; assert dedicado parcial. |
| Pedido | REQ-04; `POST /pedidos` | Quantidade inteira de 1 a 10; HTTP 201; total e SQL concordam. | Implementado; fronteira 10/11 não testada. |
| Titularidade | REQ-05; `GET /pedidos/{id}` | Alfa lê o próprio; Beta recebe 404. | Implementado; inexistente e GET sem token sem teste dedicado. |
| Navegadores | NFR-01 | Mesma jornada em Chromium, Firefox e WebKit. | Automatizado. |
| Desempenho | NFR-02 | Perfil local tem p95 < 500 ms, falhas < 1%, checks > 99%. | Medido para mock; meta real não validada. |
| Pipeline/evidência | NFR-03 e NFR-04 | Commit gera gate e relatório investigável. | Configurado e observado na CI. |
| Reenvio após timeout | H-05 | Dois POSTs iguais devem criar um ou dois pedidos? | Pergunta de negócio aberta. |

## Critério de qualidade para cada requisito

1. **Objetivo e ator:** quem obtém valor ou é protegido pela regra.
2. **Condição inicial e gatilho:** estado de autenticação, massa, entrada e ação.
3. **Resultado observável:** resposta HTTP/UI e efeito permitido ou proibido no SQL.
4. **Fronteiras:** mínimo/máximo, ausente, inválido, concorrente e repetido, quando pertinentes.
5. **Prioridade e risco:** impacto se a regra falhar, usando a [estratégia de testes](../qa/test-strategy.md).
6. **Oráculo e evidência:** assert, teste, relatório e responsável por confirmar a regra.
7. **Lacuna explícita:** implementar, testar, ou manter como hipótese; não chamar cobertura parcial de aceite.

Exemplo de refinamento de REQ-04: **Dado** um usuário autenticado e `sku-1` a 12.990 centavos, **quando** solicita uma unidade com `totalCents: 1`, **então** a API retorna 201 e 12.990 centavos, e o SQLite registra o mesmo total. É um exemplo executável existente; a regra geral de preços promocionais continua fora do escopo.

## Controle de mudança

Uma alteração de regra deve atualizar, nesta ordem lógica: pergunta/decisão, ID REQ/NFR, exemplos BDD, teste automatizado e oráculos, [matriz de rastreabilidade](../qa/traceability.md), risco e parecer. O commit ou PR deve indicar qual hipótese foi resolvida, quem a confirmou quando houver stakeholder, e como a regressão foi verificada. Requisitos sem fonte de aprovação externa permanecem classificados como hipótese do case.
