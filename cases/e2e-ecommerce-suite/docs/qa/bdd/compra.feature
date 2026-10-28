# language: pt
@BDD-01 @REQ-02 @REQ-03 @REQ-04 @NFR-01
Funcionalidade: Concluir uma compra com valor consistente
  Como cliente autenticado
  Quero selecionar um produto e receber uma confirmação
  Para saber que meu pedido foi aceito com o valor anunciado

  Cenário: Compra de um fone de ouvido
    Dado que Alfa entrou na loja e o fone de ouvido custa 12990 centavos
    Quando Alfa adiciona um fone ao carrinho e finaliza a compra
    Então a interface confirma o pedido com um identificador
    E a API mostra o pedido de Alfa como APROVADO por 12990 centavos
    E o banco registra o mesmo identificador, titular, status e valor
