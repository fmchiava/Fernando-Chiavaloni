# language: pt
Funcionalidade: Proteger pedidos e tratar entradas controladas pelo cliente
  Como cliente e operação da loja
  Quero impedir escrita anônima, leitura cruzada e consultas alteradas
  Para proteger pedidos e manter o catálogo íntegro

  @BDD-05 @REQ-03 @REQ-04
  Cenário: Requisição sem token
    Dado que não há token de autenticação na requisição
    Quando um item é enviado ao carrinho ou a um novo pedido
    Então a requisição é recusada
    E nenhum pedido com os dados de prova é gravado

  @BDD-06 @REQ-05
  Cenário: Beta tenta consultar pedido de Alfa
    Dado que Alfa criou um pedido e Beta possui outra sessão válida
    Quando Beta consulta o identificador do pedido de Alfa
    Então o pedido não é revelado a Beta
    E Alfa continua conseguindo consultar o próprio pedido

  @BDD-07 @REQ-01 @REQ-02
  Cenário: Texto com fragmento SQL
    Dado que o catálogo sintético contém dois produtos
    Quando um fragmento SQL é enviado como e-mail e como busca
    Então o login é recusado
    E a busca não devolve produtos para esse texto
    E o catálogo completo continua com dois produtos
