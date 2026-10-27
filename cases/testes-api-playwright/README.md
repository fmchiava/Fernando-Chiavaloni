# 🚀 Automação de Testes de API REST — Playwright + TypeScript

[![API Regression Tests](https://github.com/fmchiava/sdet-portfolio/actions/workflows/api-tests.yml/badge.svg)](https://github.com/fmchiava/sdet-portfolio/actions/workflows/api-tests.yml)

[Relatório HTML público da última execução aprovada](https://fmchiava.github.io/sdet-portfolio/)

Suíte de testes automatizados de API REST para portfólio de QA/SDET, com validação de status HTTP, conteúdo das respostas e contrato JSON. A suíte de posts usa a [JSONPlaceholder](https://jsonplaceholder.typicode.com/); o exemplo de autenticação usa a [DummyJSON](https://dummyjson.com/docs/auth), que oferece login e rotas Bearer protegidas.

[Estratégia de qualidade e rastreabilidade dos cenários](docs/estrategia-qualidade.md) · [Portfólio principal](https://github.com/fmchiava/sdet-portfolio)

## Em 40 segundos: problema, solução e evidência

**Problema:** conferir apenas o status HTTP deixa passar mudanças no formato da resposta, dados incoerentes e falhas de autenticação. Um portfólio de QA precisa mostrar como esses riscos são testados e quais limites permanecem.

**Solução:** este projeto combina testes de API com Playwright, contratos Zod, cenários orientados a dados, uma fixture de autenticação, mocks de falhas e um módulo separado de performance. O código, as massas de teste e o workflow estão neste repositório; ele não é um fork.

**Resultado verificável:** consulte as [execuções do GitHub Actions](https://github.com/fmchiava/sdet-portfolio/actions/workflows/api-tests.yml) e o [último relatório HTML aprovado](https://fmchiava.github.io/sdet-portfolio/). No experimento local de k6 em 25/10/2026, o smoke passou; a carga rápida excedeu o limite de p95 de 200 ms, resultado registrado abaixo. São demonstrações em APIs públicas, não medições de um sistema de produção.

### Decisões técnicas e motivos

| Decisão | Motivo e limite |
| --- | --- |
| `APIRequestContext` para a suíte principal | Testa HTTP diretamente, sem depender de navegador; os exemplos de `page.route` ficam isolados porque essa interceptação atua no tráfego da página. |
| Zod além de status e valores pontuais | Detecta quebra estrutural de contrato em tempo de execução. Os casos inválidos documentam o comportamento real do JSONPlaceholder, que não rejeita aqueles payloads. |
| DummyJSON apenas para autenticação | O JSONPlaceholder não oferece login Bearer; usar outra API permite demonstrar a fixture sem inventar uma rota protegida. |
| k6 fora do CI | Evita gerar carga recorrente em uma API pública. O limite de latência é demonstrativo e deve ser calibrado em ambiente autorizado. |

O projeto foi desenvolvido com assistência de IA. As afirmações de funcionamento acima se apoiam nas execuções indicadas; o README distingue comportamento observado de capacidade não demonstrada.

## 🛠️ Tecnologias utilizadas

- [Playwright Test](https://playwright.dev/docs/api-testing): fixture `request` baseada em `APIRequestContext` para testes da API real e `page.route` para interceptar requisições nos exemplos de mocks.
- [TypeScript](https://www.typescriptlang.org/): checagem estática com `strict` e `tsc --noEmit`.
- [Zod](https://zod.dev/): validação em tempo de execução dos contratos JSON.
- [dotenv](https://github.com/motdotla/dotenv): carregamento opcional de variáveis locais de `.env`.
- [GitHub Actions](https://docs.github.com/actions): execução automática em `push` e `pull_request`, com relatório HTML como artefato.
- [Grafana k6](https://grafana.com/docs/k6/latest/): demonstração local de testes de fumaça e carga leve para GET/POST.

## 🏛️ Arquitetura e boas práticas

- **Independência:** nenhum teste depende da ordem de execução ou de alterações feitas por outro teste. Os dados de `POST`, `PUT` e `PATCH` usam títulos com UUID.
- **Contrato explícito:** `utils/schemas.ts` exige os campos e tipos de posts e comentários e rejeita propriedades extras. Respostas vazias também têm schema próprio.
- **Testes orientados a dados:** `fixtures/test-data.json` concentra casos de busca, payloads válidos e entradas de borda; cada caso gera um teste Playwright independente.
- **Autenticação reutilizável:** `fixtures/api-fixture.ts` obtém um token por worker e cria um `request` autenticado e isolado por teste. O contexto de login é descartado antes dos testes, impedindo que seus cookies substituam o header Bearer.
- **Configuração centralizada:** `playwright.config.ts` carrega `.env`, define URL base, ambiente, header `Accept`, limite de tempo e relatórios. Variáveis do processo têm prioridade sobre `.env`.
- **Mocks isolados:** `tests/mocks.spec.ts` usa um cliente `fetch` dentro de uma página local simulada para testar respostas controladas; os testes de contrato continuam consultando a API real. `APIRequestContext` não possui `request.route`, portanto esses exemplos exigem Chromium headless.
- **Sem chave na API pública:** o JSONPlaceholder dispensa chave, e `API_KEY` não é incluída nas requisições.

### Cobertura

| Cenário | Verificações principais |
| --- | --- |
| `GET /posts` | 200, lista de 100 itens, contrato de cada post |
| `GET /posts?userId=1` | 200, 10 posts pertencentes ao usuário 1 |
| `GET /posts?userId=999999` | 200 e lista vazia para filtro sem resultados |
| `GET /posts/{id}` | Casos orientados a dados: 200 para IDs existentes; 404 e JSON vazio para IDs inexistentes |
| `GET /posts/1/comments` | 200, contrato de cinco comentários vinculados ao post |
| `POST /posts` | Casos orientados a dados: 201, eco dos dados e análise do contrato Zod para payloads válidos e inválidos |
| `PUT /posts/1` | 200, contrato e substituição completa retornada |
| `PATCH /posts/1` | 200, mudança apenas no título da resposta simulada |
| `DELETE /posts/1` | 200 e corpo JSON vazio |
| `GET /auth/me` e `/auth/products` | Login prévio, Bearer automático e respostas 200 na DummyJSON |
| `GET /auth/me` sem token | 401 com um contexto HTTP sem autenticação |
| Mocks de serviço externo | Erro 500, timeout de rede e substituição por payload validado com Zod |

**Limitação do alvo:** o JSONPlaceholder simula `POST`, `PUT`, `PATCH` e `DELETE`; essas operações não persistem no servidor. Por isso, os testes validam a resposta da operação e não tentam confirmar mudanças com uma leitura posterior. Veja o [guia oficial](https://jsonplaceholder.typicode.com/).

**Validação de entrada:** o JSONPlaceholder devolve `201` inclusive para título vazio, tipos incorretos e títulos de 255 ou 256 caracteres. Os casos inválidos verificam que o contrato Zod rejeita o retorno, registrando a lacuna de validação da API. Não há limite de título documentado nem respostas `400` ou `422` para esses payloads neste serviço; esses status devem ser testados contra uma API que implemente tal regra.

## 🚀 Executar localmente

**Pré-requisito:** Node.js 22, 24 ou 26 e npm. Este projeto foi verificado com Node.js 24. Os testes com `page.route` precisam do Chromium headless; os testes diretos com `APIRequestContext` não precisam de navegador.

```bash
git clone https://github.com/fmchiava/sdet-portfolio.git
cd sdet-portfolio/cases/testes-api-playwright
npm ci
npx playwright install --only-shell chromium
npm run typecheck
npm test
```

### Variáveis de ambiente

Copie `.env.example` para `.env` se quiser configurar a execução local (`Copy-Item .env.example .env` no PowerShell). O arquivo `.env` é ignorado pelo Git.

| Variável | Valor padrão | Uso |
| --- | --- | --- |
| `BASE_URL` | `https://jsonplaceholder.typicode.com` | URL da API testada. `API_BASE_URL` continua aceito como alternativa antiga. |
| `API_KEY` | vazia | Reservada para uma futura API autenticada; a suíte atual não envia essa chave. |
| `ENVIRONMENT` | `demo` | Rótulo do ambiente nos metadados do relatório; não muda a URL por si só. |
| `AUTH_BASE_URL` | `https://dummyjson.com` | API usada pelo exemplo de login e rotas protegidas. |
| `AUTH_USERNAME` e `AUTH_PASSWORD` | conta pública de demonstração da DummyJSON | Devem ser definidos juntos ao usar credenciais próprias. |

No GitHub Actions, configure `BASE_URL`, `ENVIRONMENT` e `AUTH_BASE_URL` como **Variables**; `API_KEY`, `AUTH_USERNAME` e `AUTH_PASSWORD` são **Secrets** em *Settings → Secrets and variables → Actions*, apenas se necessários. Os segredos ficam restritos à etapa de testes. Com os alvos públicos de demonstração, nenhuma configuração no GitHub é exigida.

### Autenticação dinâmica

Os testes em `tests/protected-routes.spec.ts` importam `test` de `fixtures/api-fixture.ts`. A fixture de worker faz `POST /auth/login` uma vez por worker, valida a presença de `accessToken` e descarta o contexto de login. Cada teste que usa `request` recebe um contexto novo com `Authorization: Bearer <token>`, preservando o isolamento entre testes. O token não é salvo no repositório nem registrado pela fixture.

Sem credenciais próprias, o exemplo usa `emilys` / `emilyspass`, **credenciais públicas da [documentação da DummyJSON](https://dummyjson.com/docs/auth)**. Para outra API, configure URL e credenciais e adapte os endpoints e schemas do exemplo. Use caminhos relativos no `request` autenticado para manter o Bearer restrito ao host configurado. Se a execução puder ultrapassar a validade do token, implemente renovação controlada ou reduza a duração do worker; o exemplo não faz refresh automático.

O relatório fica em `playwright-report/index.html`. Para abri-lo pelo Playwright:

```bash
npm run report
```

Para usar outra URL base durante uma execução, defina `BASE_URL` no ambiente antes de `npm test`. A instância precisa oferecer os mesmos endpoints e contratos.

## 📈 Teste de performance com k6

Instale o [Grafana k6](https://grafana.com/docs/k6/latest/set-up/install-k6/) separadamente. No Windows, use `winget install k6 --source winget` e abra um novo terminal. O script é JavaScript nativo do k6; `npm ci` e Playwright não são necessários para executá-lo.

```powershell
# Fumaça: 1 VU, cerca de 6 segundos.
k6 run -e PROFILE=smoke performance/posts-load-test.js

# Carga rápida: rampa até 2 VUs, cerca de 25 segundos.
k6 run -e PROFILE=load performance/posts-load-test.js

# Exemplo em ambiente próprio, com limite p95 ajustado após medir a linha de base.
k6 run -e PROFILE=load -e BASE_URL=https://sua-api.example -e P95_MS=500 performance/posts-load-test.js
```

Cada iteração chama `GET /posts/1` e `POST /posts`, valida status e campos relevantes, e faz uma pausa de um segundo. As métricas de aceitação são **p95 < 200 ms por rota** (alterável com `P95_MS`), **taxa de erro HTTP < 1%** e **mais de 99% dos checks aprovados**. O k6 termina com código diferente de zero se um threshold falhar. O p95 medido pela internet inclui variações de rede e não comprova, sozinho, a capacidade do servidor; ajuste a meta com uma linha de base e execute testes maiores apenas em ambiente autorizado e controlado.

Na execução local de 25/10/2026, o smoke passou (10 requisições). O perfil load fez 56 requisições com 0% de erros e 100% dos checks aprovados, mas **reprovou p95 < 200 ms**: GET = 667 ms e POST = 525 ms. Esta é uma amostra pontual de uma API pública, não um SLA do serviço. Para explorar outro limite sem alterar o script, use `k6 run -e PROFILE=load -e P95_MS=1000 performance/posts-load-test.js`; defina a meta definitiva a partir de medições repetidas em ambiente controlado.

O JSONPlaceholder [simula o `POST` sem persistir dados](https://jsonplaceholder.typicode.com/). Esse teste demonstra a configuração e as métricas do k6, não mede a capacidade de produção do serviço. O módulo de performance não roda automaticamente no GitHub Actions para evitar carga recorrente na API pública.

## 📁 Estrutura

```text
.
├── ../../.github/workflows/api-tests.yml # Pipeline do monorepo
├── .env.example                      # Modelo público de variáveis, sem segredo
├── fixtures/api-fixture.ts           # Login por worker e request com Bearer
├── fixtures/test-data.json          # Casos positivos, negativos e de borda
├── tests/posts.spec.ts              # Dezoito cenários de posts
├── tests/protected-routes.spec.ts   # Três cenários de autenticação
├── tests/mocks.spec.ts              # Três cenários com respostas interceptadas
├── performance/posts-load-test.js    # Perfis k6 de fumaça e carga leve
├── utils/schemas.ts                  # Contratos Zod
├── playwright.config.ts              # URL base, headers e relatórios
├── tsconfig.json                     # Checagem TypeScript
├── package.json
└── package-lock.json                 # Dependências reproduzíveis
```

O pipeline executa `npm ci`, instala o Chromium headless, verifica os tipos e roda os testes em cada `push` e `pull_request`. O relatório HTML é anexado ao workflow inclusive quando os testes falham. Após uma execução aprovada por `push` na `master` do monorepo, outro job publica esse relatório no GitHub Pages. Em caso de falha, o site mantém o último relatório aprovado; o relatório da falha pode ser baixado nos artefatos da execução.

Para ativar o link público, abra **Settings → Pages → Build and deployment** no repositório e selecione **GitHub Actions** em **Source**. O relatório é público: não adicione credenciais, tokens, dados pessoais ou anexos sensíveis aos testes e seus resultados.
