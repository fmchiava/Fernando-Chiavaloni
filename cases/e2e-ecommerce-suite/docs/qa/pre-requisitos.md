# Pré-requisitos e guia de reprodução

## Preparar a máquina

Trabalhe a partir de `cases/e2e-ecommerce-suite/`, no clone do monorepo. É preciso Node.js **24 ou superior**, npm compatível e acesso para baixar as dependências do lockfile e os navegadores Playwright. O teste de performance exige o executável **k6** no `PATH`; no Windows o runner também aceita `.tools/k6/k6.exe` dentro do case. A execução documentada usou k6 2.2.0. Python não é requisito para este case; ele só é necessário para a regressão dos outros projetos do monorepo.

Confirme o ambiente:

```text
node --version
npm --version
k6 version
```

Instale o k6 pelas [instruções oficiais](https://grafana.com/docs/k6/latest/set-up/install-k6/). Se `k6 version` não resolver no Windows, valide o caminho `.tools/k6/k6.exe` ou ajuste o `PATH`. Nenhuma conta externa ou chave de API é necessária.

## Instalar e executar o gate funcional

```text
npm ci
npx playwright install chromium firefox webkit
npm run docs:check
npm run typecheck
npm test
```

No Linux, se faltarem bibliotecas do sistema para os navegadores, use `npx playwright install --with-deps chromium firefox webkit`, como faz a CI. `npm run docs:check` confere links relativos e IDs BDD, mas não interpreta semanticamente o Gherkin. O `npm test` inicia o mock em `http://127.0.0.1:4173`, espera `/health`, executa 10 testes Playwright e encerra o servidor que iniciou. O HTML local fica em `playwright-report/`; `npm run report` o abre. Em falhas, Playwright também guarda screenshot e trace em `test-results/`.

Para executar partes da suíte:

```text
npm run test:api
npm run test:security
npx playwright test src/tests/e2e-purchase.spec.ts
```

Os comandos acima executam testes, não cenários Gherkin. Os arquivos `.feature` são especificações de negócio associadas aos testes na [matriz](traceability.md).

## Teste de carga

Depois de confirmar o k6, execute `npm run test:performance`. O runner sobe outra instância em `127.0.0.1:4174`, usa `.data/performance.sqlite`, aplica o perfil de 50 VUs e grava `performance/results/summary.html` e `summary.json`. A duração nominal das rampas é 50 segundos, acrescida do preparo e encerramento.

Para o perfil curto:

```powershell
$env:PROFILE = 'smoke'
npm run test:performance
Remove-Item Env:PROFILE
```

Em Bash: `PROFILE=smoke npm run test:performance`. O smoke verifica a instalação e a rota, mas **não** substitui o gate de carga. Os thresholds e a interpretação estão no [perfil de performance](../../performance/config/README.md).

## Ambiente e massa

O `.env` é opcional e ignorado pelo Git. Copie `.env.example` apenas se precisar alterar a configuração. `BASE_URL` determina a URL da UI e a porta do servidor Playwright; mantenha uma porta explícita. `API_URL` define o cliente REST e deve apontar para a **mesma instância** do teste E2E. `DB_PATH` seleciona o SQLite funcional; o runner k6 usa seu próprio banco. `TEST_USER` e `TEST_PASS` são dados sintéticos. A base inicial contém Alfa, Beta, Fone de ouvido e Mouse sem fio.

Não use contas reais: relatórios e traces de falha podem conter requisições e valores de entrada. Mantenha as portas 4173 e 4174 livres. Se uma execução local parecer atingir dados antigos, encerre o servidor e inspecione o arquivo em `.data/`; a suíte usa IDs devolvidos pela API e não depende de começar com uma base vazia.

## Como interpretar falhas de preparo

| Sintoma | Conferência inicial |
| --- | --- |
| `npm ci` falha | Node 24+, conexão de download e integridade de `package-lock.json` |
| Navegador não inicia | Execute a instalação dos três browsers; no Linux inclua `--with-deps` |
| `/health` não responde | Confira a porta 4173 e se outro processo está ocupando a URL |
| API e UI divergem | Compare `BASE_URL` e `API_URL`; ambas devem apontar ao mesmo mock |
| `k6` não encontrado | Verifique `k6 version` ou o executável local ignorado pelo Git |
| Threshold falha | Leia p95 e taxa de erro no JSON, confirme porta 4174 e identifique contenção da máquina antes de alterar o limite |

Uma falha por ambiente deve ser registrada como bloqueio de execução, com comando e saída, sem ser tratada automaticamente como defeito da aplicação.
