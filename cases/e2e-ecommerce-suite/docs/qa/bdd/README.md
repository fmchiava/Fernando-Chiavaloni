# Especificações BDD

BDD descreve **o comportamento que importa ao cliente e ao negócio** antes de discutir seletores, SQL ou bibliotecas. Os exemplos abaixo usam Gherkin em português para tornar as regras revisáveis por QA, desenvolvimento e pessoas não técnicas. Cada cenário possui um ID e um vínculo na [matriz de rastreabilidade](../traceability.md).

| Arquivo | Conversa que o cenário sustenta | Automação correspondente |
| --- | --- | --- |
| [compra.feature](compra.feature) | O que prova que uma compra foi concluída? | `e2e-purchase.spec.ts`, três navegadores |
| [contratos.feature](contratos.feature) | Qual dado pode ser aceito e quem define o preço? | `api-contracts.spec.ts` |
| [seguranca.feature](seguranca.feature) | Quem pode criar e consultar um pedido? | `auth-security.spec.ts` |

**Estado de execução:** os `.feature` são especificações versionadas, não uma segunda suíte. Não há step definitions nem runner Cucumber; `npm test` executa os testes Playwright. A escolha evita duplicar automação apenas para criar uma aparência de BDD. A rastreabilidade deixa explícita a correspondência e as regras ainda parcialmente cobertas.

Ao revisar uma mudança, primeiro discuta o exemplo no vocabulário de negócio. Em seguida, atualize o `.feature`, o assert Playwright e a matriz. Um cenário não deve ser declarado “passou” apenas porque o texto Gherkin existe. A sintaxe segue a [referência oficial de Gherkin](https://cucumber.io/docs/gherkin/reference/).
