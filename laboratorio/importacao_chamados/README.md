# Laboratório: importação de chamados

Exercício **fictício**, com dados sintéticos, para mostrar testes de contrato de dados, validação, idempotência, conflito e importação atômica. O [plano de testes](../../portfolio/matriz-de-testes.md) registra as premissas e os riscos que motivaram os casos.

## Executar

Na raiz do repositório, com Python 3.12. A CI também verifica a versão estável 3.15:

```sh
python -m unittest discover -s laboratorio/importacao_chamados -p 'test_*.py' -v
```

Não há dependências externas. Os testes também rodam no [GitHub Actions](https://github.com/fmchiava/portfolio-qa-automacao/actions/workflows/testes.yml) a cada push e PR.

## Contrato assumido

- O CSV exige `id_externo`, `data`, `categoria`, `descricao` e `status`; colunas duplicadas no cabeçalho são rejeitadas.
- A chave de uma ocorrência é `(id_externo, data)`; reimportação idêntica é idempotente e conteúdo diferente para a mesma chave é conflito.
- A data deve ser válida e estar em `AAAA-MM-DD`; `categoria` aceita `acesso`, `erro` ou `duvida`; o `status` inicial é `aberto`.
- Uma linha inválida rejeita o lote inteiro. O dicionário de registros existente não é alterado.
- Mensagens de erro identificam a linha e o campo ou tipo de problema.

O código é uma implementação mínima em memória para exercitar a estratégia. Não é uma API, banco de dados ou sistema de produção. As regras acima são hipóteses do exercício e exigiriam validação com o produto em um caso real. Este material foi desenvolvido com assistência de IA; os resultados são os da execução automatizada, não uma alegação de experiência profissional com esse sistema.
