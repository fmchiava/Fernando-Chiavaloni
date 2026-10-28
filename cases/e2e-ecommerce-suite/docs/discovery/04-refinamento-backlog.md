# Refinamento do backlog

O backlog abaixo é uma **reconstrução para orientar avaliação e evolução**. Prioridades são julgamento de QA por impacto/risco, não ordem aprovada por Product Owner. A [matriz](../qa/traceability.md) continua sendo a fonte do estado de cobertura.

## Mapa da jornada e fatias verticais

| Etapa | História | Regra | Fatia verificável | Estado |
| --- | --- | --- | --- | --- |
| Entrar | US-01: cliente acessa com credenciais sintéticas | REQ-01 | UI + API retornam sessão; acesso inválido é recusado. | Implementada; negativos parciais. |
| Escolher | US-02: cliente consulta e busca produtos | REQ-02 | Catálogo mostra SKU/preço; busca segura. | Implementada. |
| Preparar | US-03: cliente adiciona item e vê total | REQ-03 | API calcula total; UI mostra carrinho. | Implementada; assert isolado parcial. |
| Comprar | US-04: cliente confirma pedido | REQ-04 | UI confirma ID; API/SQL concordam em titular, status e valor. | Implementada para 1 unidade. |
| Consultar | US-05: cliente consulta seu pedido | REQ-05 | Titular recebe 200; outro cliente recebe 404. | Implementada; negativos parciais. |
| Operar com confiança | US-06: QA emite parecer reproduzível | NFR-01 a NFR-04 | 3 browsers, k6, CI e evidência. | Implementada no alvo local. |

## Ordem proposta para fechar riscos residuais

| Prioridade | Item | Por que agora | Critério de pronto para teste |
| --- | --- | --- | --- |
| P1 | B-01: quantidade 10 e 11 | Fecha fronteira de REQ-04 já implementada mas sem assert. | 10 aceito com total correto; 11 retorna 400 sem escrita. |
| P1 | B-02: GET sem token e ID inexistente | Fecha negações de REQ-05, risco de exposição. | 401 sem token; 404 para ID ausente; nenhum dado de terceiro. |
| P1 | B-03: carrinho válido e ausência de escrita | Evita confundir prévia com pedido gravado. | POST válido retorna total; contagem de orders não muda. |
| P2 | B-04: idempotência de POST após timeout | Risco de duplicidade; depende de política de produto. | Pergunta H-05 respondida; chave/semântica definida antes do teste. |
| P2 | B-05: formato monetário pt-BR | Melhora apresentação, sem alterar valor em centavos. | Exemplo de locale aprovado e assert UI definido. |
| P2 | B-06: SLO/carga representativa | Threshold local não deve virar promessa de produção. | Volume, hardware e limite acordados; perfil k6 revisado. |

## Definition of Ready local

Uma história fica pronta para implementação quando: ator e objetivo estão claros; regra e exceções críticas têm exemplos; dúvidas que mudam o contrato foram respondidas; massa e oráculo foram definidos; dependências e risco estão identificados; e o teste pode ser escrito de forma que falhe pela razão certa. **DoR é convenção de trabalho proposta para este case.**

Para B-04, a história **não está Ready**: é preciso resolver se duas requisições equivalentes representam compras distintas ou repetição de uma tentativa. Fazer um teste antes disso codificaria uma suposição como regra.

## Definition of Done local

Para uma mudança futura: regra atualizada; ciclo Red/Green registrado quando aplicável; teste de unidade/API/E2E na camada adequada; assert de efeito lateral para falhas críticas; matriz e BDD revisados; typecheck e regressão pertinentes verdes; relatório com commit, ambiente e artefatos; riscos remanescentes explícitos no parecer. O [guia TDD](../qa/tdd.md) separa prática futura da prova histórica existente. **DoD é convenção de qualidade proposta**, não declaração de que houve cerimônia Scrum.

## Ritual de refinamento proposto

1. Selecionar a história mais arriscada e reunir perspectivas de produto, DEV e QA.
2. Mapear regra, exemplos e perguntas em até uma página; dividir história se houver mais de um resultado independente.
3. Tornar explícita a decisão de produto e seu responsável; para hipótese não respondida, registrar bloqueio.
4. Atualizar ID REQ/NFR, BDD, risco, testes e matriz no mesmo PR da implementação.
5. Reordenar backlog após a evidência; não atribuir porcentagem de cobertura por contagem de cenários.

O [Scrum Guide](https://scrumguides.org/scrum-guide) descreve refinamento contínuo; as etapas acima são uma adaptação proporcional ao case.
