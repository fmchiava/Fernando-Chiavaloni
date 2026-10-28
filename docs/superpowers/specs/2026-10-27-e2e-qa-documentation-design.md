# Design da documentação de QA do case E-commerce E2E

## Intenção

Transformar o case em um dossiê que um entrevistador consiga percorrer sem assistência: entender o processo, instalar o ambiente, relacionar critérios de negócio a cenários BDD e testes, examinar um ciclo de defeito e conferir resultados reais. A documentação precisa servir também a outro QA que vá reproduzir a execução.

## Escopo e limites

- Reescrever a documentação do case `cases/e2e-ecommerce-suite/` e corrigir seus pontos de entrada no README do monorepo.
- Preservar a lógica do sistema sob teste, as dependências e as evidências brutas. Acrescentar à CI apenas a validação documental. Não apresentar `.feature` como teste executado: os cenários BDD são especificações legíveis vinculadas aos testes Playwright.
- Explicar TDD como prática de desenvolvimento e identificar com precisão a evidência existente: o experimento controlado QA-001 demonstra detecção vermelha e reteste verde; ele não comprova que toda a implementação original foi escrita em TDD.
- Separar resultados históricos de 27/10/2026, execução atual no `master`, critérios futuros e hipóteses não verificadas.
- Salvar e revisar em branch local antes de qualquer publicação remota.

## Abordagem

Um README curto serve de roteiro; documentos temáticos guardam contexto, pré-requisitos, arquitetura, BDD, TDD, estratégia, rastreabilidade, segurança, defeitos, evidências e decisão de qualidade. Exemplos Gherkin ficam em arquivos `.feature` para leitura, sem adicionar um runner BDD. A matriz usa IDs estáveis para ligar regra, risco, cenário, teste e evidência. Um registro de revisão fecha a documentação com verificações observadas e pendências.

## Fontes de verdade

O código e a configuração definem comportamento e comandos. Os logs sanitizados e as execuções da CI definem resultados observados. As referências externas dão contexto metodológico, sem substituir a evidência do case.
