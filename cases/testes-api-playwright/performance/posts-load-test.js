import http from 'k6/http';
import { check, sleep } from 'k6';

const baseUrl = (__ENV.BASE_URL || 'https://jsonplaceholder.typicode.com').replace(/\/+$/, '');
const profile = (__ENV.PROFILE || 'smoke').toLowerCase();
const p95Ms = Number(__ENV.P95_MS || 200);

if (!['smoke', 'load'].includes(profile)) {
  throw new Error('PROFILE deve ser smoke ou load.');
}
if (!Number.isFinite(p95Ms) || p95Ms <= 0) {
  throw new Error('P95_MS deve ser um número positivo em milissegundos.');
}

// Carga pequena por padrão: JSONPlaceholder é uma API pública compartilhada.
// Use um ambiente sob seu controle antes de aumentar VUs ou duração.
const stages = profile === 'smoke'
  ? [
      { duration: '1s', target: 1 },
      { duration: '4s', target: 1 },
      { duration: '1s', target: 0 },
    ]
  : [
      { duration: '5s', target: 2 },
      { duration: '15s', target: 2 },
      { duration: '5s', target: 0 },
    ];

export const options = {
  scenarios: {
    [profile]: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages,
      gracefulRampDown: '5s',
    },
  },
  thresholds: {
    'http_req_duration{endpoint:get_post}': [`p(95)<${p95Ms}`],
    'http_req_duration{endpoint:create_post}': [`p(95)<${p95Ms}`],
    http_req_failed: ['rate<0.01'],
    checks: ['rate>0.99'],
  },
};

export default function () {
  const getResponse = http.get(`${baseUrl}/posts/1`, {
    tags: { name: 'GET /posts/1', endpoint: 'get_post' },
    timeout: '5s',
  });
  check(getResponse, {
    'GET /posts/1 retorna 200': (response) => response.status === 200,
    'GET /posts/1 retorna o ID correto': (response) =>
      response.status === 200 && response.json('id') === 1,
  });

  const title = `k6-vu-${__VU}-iter-${__ITER}`;
  const postResponse = http.post(
    `${baseUrl}/posts`,
    JSON.stringify({ title, body: 'Teste de carga do portfólio QA/SDET', userId: 1 }),
    {
      headers: { 'Content-Type': 'application/json; charset=UTF-8' },
      tags: { name: 'POST /posts', endpoint: 'create_post' },
      timeout: '5s',
    },
  );
  check(postResponse, {
    'POST /posts retorna 201': (response) => response.status === 201,
    'POST /posts devolve o título enviado': (response) =>
      response.status === 201 && response.json('title') === title,
  });

  // Cada VU faz no máximo um par GET/POST por segundo, além do tempo da rede.
  sleep(1);
}
