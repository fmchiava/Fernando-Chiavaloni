# Portfólio de QA e Automação — Fernando Chiavaloni

**Qualidade de software · automação de testes · APIs e dados**

Atuo em QA de aplicações web, mobile e APIs, com experiência em automação, análise de regras de negócio e qualidade de dados. Estou aplicando essa base ao teste de sistemas com IA: respostas de LLM, recuperação de informação e agentes que usam ferramentas.

Este repositório é meu portfólio público em evolução. Ele reúne **artefatos selecionados**, com data, escopo e estado da evidência. Meu caderno de estudo no Obsidian permanece privado.

## Onde começar

| Material | O que mostra | Estado |
| --- | --- | --- |
| [Progresso em QA e IA](aprendizado/progresso.md) | Fontes estudadas, experimentos previstos e critérios para registrar resultados. | Estudos documentados. |
| [Exemplo de estratégia de testes](portfolio/matriz-de-testes.md) | Riscos, regras e casos para um fluxo **fictício** de importação de chamados. | Matriz de testes documentada. |
| [Laboratório executável](laboratorio/importacao_chamados/README.md) | Implementação mínima e testes de qualidade de dados, idempotência e falha em lote. | Testes automatizados com comando de reprodução. |
| [Case de QA RPA: conciliação de sinistros](https://github.com/fmchiava/qa-rpa-conciliacao-sinistros) | Processo sintético com UI, API REST, CSV, SQLite, exceções técnicas e de negócio, evidências auditáveis e arquitetura proposta em A360. | Simulador Python e testes executáveis; bot A360 e homologação corporativa não implementados. |
| [Suíte de testes de API](https://github.com/fmchiava/testes-api-playwright) | Contratos Zod, autenticação Bearer, mocks de falhas, CI e experimento de carga; decisões e limites no README. | [Execuções de CI](https://github.com/fmchiava/testes-api-playwright/actions/workflows/api-tests.yml); carga k6 com limite p95 reprovado e documentado. |

**Reproduza o laboratório:** `python -m unittest discover -s laboratorio/importacao_chamados -p 'test_*.py' -v`. Os 15 testes também são executados em [GitHub Actions](https://github.com/fmchiava/portfolio-qa-automacao/actions/workflows/testes.yml). Consulte o laboratório para regras assumidas e limitações.

## Base profissional

- Testes funcionais e regressivos em web, mobile e APIs.
- Automação de testes e investigação de falhas em colaboração com desenvolvimento e negócio.
- Validação de dados, consultas SQL e análise de integrações e processos.
- Comunicação de riscos, critérios de aceite e resultados de teste.

As ferramentas que usei ao longo da carreira incluem Cypress, Playwright, Selenium e Detox. O laboratório público usa Python e sua biblioteca padrão; cada tecnologia listada como experiência de carreira não implica demonstração dela neste repositório.

## Como registro progresso

Para cada experimento, registro: **problema → risco → critério de qualidade → dados sintéticos → execução → resultado → limite**. Um estudo de leitura aparece como estudo; um teste planejado aparece como planejado. Métricas, projetos de clientes e funcionalidades não são apresentados como entregues sem evidência adequada.

O conteúdo público é revisado para excluir documentos internos, dados pessoais, credenciais e materiais de terceiros. Ferramentas de IA apoiaram a pesquisa, a redação e o laboratório. Os testes verificam o comportamento do código publicado; experiência profissional e autoria manual de cada linha não são inferidas a partir deles.

**Contato:** [perfil no GitHub](https://github.com/fmchiava).
