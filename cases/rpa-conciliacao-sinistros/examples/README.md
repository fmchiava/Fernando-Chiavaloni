# Exemplos de evidência sintética

- `go/`: falha 503 somente na primeira consulta, recuperação por retry, um item conciliado e dois encaminhados à revisão.
- `no-go/`: falha 503 persistente, item mantido pendente e gate técnico `NO_GO`.
- `unverified/`: decisão aceita no SQLite, mas leitura de confirmação indisponível; relatório `UNVERIFIED` e gate `NO_GO` até reconciliação.

Os IDs, horários e hashes são próprios destas execuções locais. Para conferir integridade, recalcule o SHA-256 de cada arquivo e compare com `manifest.json`. Esses pacotes ilustram o formato de evidência; não equivalem a homologação em A360 nem contêm screenshots da plataforma.
O hash do código-fonte no manifesto identifica a versão usada na geração de cada pacote; ele pode diferir da versão atual do repositório após correções. O analisador confere a integridade dos artefatos do pacote, não a equivalência com o código atual.

Atalho: `python analyze_logs.py examples/go`, `python analyze_logs.py examples/no-go` ou `python analyze_logs.py examples/unverified` na raiz do projeto.

Para gerar pacotes novos com o código atual, execute `python -m tools.generate_examples`. O comando sobrescreve somente `examples/go`, `examples/no-go` e `examples/unverified` com dados sintéticos e bancos temporários isolados. Identificadores de execução e horários mudam a cada geração. Os arquivos de evidência são gravados com finais de linha LF para preservar os hashes em Windows e Linux.
