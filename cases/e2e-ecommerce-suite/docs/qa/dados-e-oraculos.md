# Dados de teste, isolamento e oráculos

## Massa sintética conhecida

O servidor cria as tabelas e a massa inicial quando abre o SQLite. Nenhum dado vem de cliente real ou serviço externo. O e-mail identifica o titular do pedido; a senha comum às duas contas é **sintética** e está no `.env.example`, não é credencial de produção.

| ID | Registro inicial | Uso nos testes |
| --- | --- | --- |
| D-01 | `qa.alfa@example.test` | Titular do pedido e login válido |
| D-02 | `qa.beta@example.test` | Segundo titular para a tentativa IDOR |
| D-03 | `sku-1`, Fone de ouvido, 12.990 centavos | Compra feliz, contrato, preço adulterado e carga |
| D-04 | `sku-2`, Mouse sem fio, 7.990 centavos | Massa distintiva do teste sem Bearer (`quantity: 7`) |
| D-05 | Texto `' OR 1=1 --` | Entrada adversarial em login e busca |

O banco contém `users`, `products` e `orders`. O pedido gravado inclui ID autoincremental, `owner`, status `APROVADO`, `total_cents`, itens em JSON e data de criação. A aplicação consulta preços no catálogo e grava o total em centavos. O teste nunca usa um ID de pedido fixo; captura o ID devolvido e consulta o mesmo registro.

## Três oráculos independentes

1. **Interface:** o carrinho informa 1 item, o checkout mostra `Total: R$ 129.90` e a confirmação inclui o ID. Essa grafia com ponto é o comportamento atual do mock, não uma aprovação de localização `pt-BR`.
2. **API:** `GET /pedidos/{id}` para Alfa devolve o mesmo ID, status `APROVADO` e 12.990 centavos. Zod verifica os campos do contrato; Beta recebe 404.
3. **SQLite:** uma segunda conexão lê o pedido pelo ID e compara `owner`, status e `totalCents`. Isso detecta uma UI ou API que confirme sem persistir corretamente.

O teste de preço adulterado envia `totalCents: 1` e exige 12.990 tanto na resposta quanto no banco. O teste sem Bearer mede a contagem de pedidos com os itens distintivos antes e depois da requisição; assim, um 401 enviado **após** escrever no banco não passaria despercebido.

## Isolamento e limpeza

Playwright usa um contexto de navegador por teste; sessão e carrinho da UI não vazam entre os três motores. API e segurança compartilham o mock e o SQLite funcional, por isso os testes usam IDs retornados e massa de prova distintiva, sem depender da ordem. O runner k6 usa porta 4174 e `.data/performance.sqlite`, separados dos dados funcionais.

Os arquivos `.data/` são ignorados pelo Git e podem acumular pedidos entre execuções locais. Uma base vazia não é pré-condição dos asserts atuais. Caso seja preciso reiniciar a massa durante investigação, encerre os servidores antes de substituir o arquivo SQLite; registre essa ação no relato de execução para manter a comparação justa. Nunca publique um banco com dados reais como evidência.

## Lacunas de dados

Não há dataset automatizado para fronteiras 10/11 da quantidade, produtos inexistentes, IDs inexistentes, cliente sem sessão no GET ou datas inválidas. Esses exemplos estão na [matriz](traceability.md) como cobertura a ampliar. Criar mais linhas no banco sem um assert e um risco definido não melhora o poder do teste.
