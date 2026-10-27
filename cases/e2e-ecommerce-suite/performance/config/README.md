# Perfil de carga

`npm run test:performance` inicia a aplicação local na porta 4174 com banco próprio, executa o k6, salva `performance/results/summary.{json,html}` e encerra o servidor.

O perfil padrão sobe de 0 a 50 VUs em 30 s, mantém 50 por 10 s e desce em 10 s. Os critérios são p95 da criação de pedidos < 500 ms, taxa de falha HTTP < 1% e checks > 99%. Para uma conferência rápida, use `PROFILE=smoke` no ambiente. A carga é aplicada somente ao mock local e seus resultados não representam capacidade de produção.
