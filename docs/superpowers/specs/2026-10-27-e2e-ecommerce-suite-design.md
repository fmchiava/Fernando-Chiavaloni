# E-commerce E2E: desenho do case

## Intenção

Demonstrar trabalho de QA/SDET em um fluxo de compra verificável de ponta a ponta. A aplicação de apoio é deliberadamente pequena; o produto do case é a estratégia, a cobertura, as evidências e o ciclo de defeitos.

## Escopo aprovado

- UI local com login, catálogo e checkout, testada por Page Objects em Chromium, Firefox e WebKit.
- API REST local para login, produtos, carrinho e pedidos, com contratos Zod e respostas 200, 201, 400 e 401.
- SQLite local para confirmar persistência, status `APROVADO` e valor calculado pelo servidor.
- Segurança: ausência de Bearer, acesso a pedido de outro usuário e entradas de SQL Injection.
- Performance: k6 com rampa até 50 VUs em 30 s, p95 < 500 ms e taxa de falhas < 1%.
- Workflow na `.github/workflows/` da raiz, executando suítes e publicando relatório HTML como artefato.
- Documentação de QA, rastreabilidade, relatório de execução e ciclo de defeito com evidências reais.

## Decisões

O alvo será um servidor Node.js local e isolado, com dados sintéticos e SQLite. Não dependerá de uma API pública nem de uma loja externa. Os três navegadores exercitam somente a UI; API e segurança rodam uma vez. Os testes usam pedidos independentes para permitir paralelismo. O k6 será instalado/acionado quando o primeiro cenário estiver pronto e verificado localmente.

O servidor de apoio não será apresentado como produto comercial. Interações QA–DEV serão descritas como simulação controlada do case; execução, falhas e retestes serão registrados conforme observados. Evidências estáveis não conterão tokens; traces temporários poderão conter apenas credenciais sintéticas do mock, nunca contas reais.

## Critérios de aceite

`npm ci`, checagem de tipos, `npx playwright test` e k6 concluem sem erro na máquina local. A CI executa o mesmo fluxo em ambiente limpo e disponibiliza relatório HTML. O README permite que um entrevistador reproduza e inspecione plano, cenários, bugs, correção e reteste.
