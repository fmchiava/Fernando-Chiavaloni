# language: pt
Funcionalidade: Consultar o catálogo e criar pedidos com valor correto
  Como cliente e operação da loja
  Quero conhecer os preços e aceitar somente pedidos válidos
  Para que o total gravado represente os produtos vendidos

  @BDD-02 @REQ-02
  Cenário: Catálogo inicial
    Dado que o catálogo sintético foi carregado
    Quando os produtos são consultados
    Então o fone de ouvido aparece com o preço de 12990 centavos

  @BDD-08 @REQ-04 @REQ-05
  Cenário: Pedido criado pode ser consultado pelo titular
    Dado que Alfa está autenticado e o fone custa 12990 centavos
    Quando Alfa cria um pedido de um fone
    Então o pedido é confirmado como APROVADO por 12990 centavos
    E Alfa consegue consultar o mesmo pedido

  @BDD-03 @REQ-04
  Cenário: Quantidade zero
    Dado que Alfa está autenticado
    Quando Alfa tenta criar um pedido com zero unidades
    Então o pedido é rejeitado como inválido

  @BDD-04 @REQ-04
  Cenário: Total adulterado no envio
    Dado que Alfa está autenticado e um fone custa 12990 centavos
    Quando Alfa envia um pedido de um fone indicando um total de 1 centavo
    Então a API confirma o pedido por 12990 centavos
    E o banco registra o total de 12990 centavos
