import http from 'k6/http';
import { check, sleep } from 'k6';

const baseURL = __ENV.API_URL || 'http://127.0.0.1:4174';
const smoke = __ENV.PROFILE === 'smoke';

export const options = {
  scenarios: {
    create_orders: {
      executor: 'ramping-vus',
      stages: smoke
        ? [{ duration: '3s', target: 1 }, { duration: '3s', target: 0 }]
        : [{ duration: '30s', target: 50 }, { duration: '10s', target: 50 }, { duration: '10s', target: 0 }],
      gracefulRampDown: '5s',
    },
  },
  thresholds: {
    'http_req_duration{endpoint:order}': ['p(95)<500'],
    'http_req_failed{endpoint:order}': ['rate<0.01'],
    checks: ['rate>0.99'],
  },
};

export function setup() {
  const response = http.post(`${baseURL}/login`, JSON.stringify({
    email: 'qa.alfa@example.test', password: 'SenhaDeTeste123!',
  }), { headers: { 'Content-Type': 'application/json' } });
  if (response.status !== 200) throw new Error(`Login de preparo falhou: HTTP ${response.status}`);
  return { token: response.json('token') };
}

export default function ({ token }) {
  const response = http.post(`${baseURL}/pedidos`, JSON.stringify({
    items: [{ productId: 'sku-1', quantity: 1 }],
  }), {
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    tags: { endpoint: 'order' },
  });
  check(response, { 'pedido criado com HTTP 201': result => result.status === 201 });
  sleep(1);
}

export function handleSummary(data) {
  const duration = data.metrics['http_req_duration{endpoint:order}']?.values?.['p(95)'];
  const errorRate = data.metrics['http_req_failed{endpoint:order}']?.values?.rate;
  const checksRate = data.metrics.checks?.values?.rate;
  const report = {
    executedAt: new Date().toISOString(),
    profile: smoke ? 'smoke' : 'load',
    p95Milliseconds: duration,
    httpErrorRate: errorRate,
    checksRate,
    thresholds: { p95Milliseconds: 500, httpErrorRate: 0.01 },
    metrics: data.metrics,
  };
  const html = `<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>k6 — Pedidos</title>
    <h1>k6 — Criação de pedidos</h1><p>Executado em ${report.executedAt}</p>
    <table border="1" cellpadding="8"><tr><th>Métrica</th><th>Resultado</th><th>Critério</th></tr>
    <tr><td>p95</td><td>${duration ?? 'sem dados'} ms</td><td>&lt; 500 ms</td></tr>
    <tr><td>Falhas HTTP</td><td>${errorRate ?? 'sem dados'}</td><td>&lt; 0,01</td></tr>
    <tr><td>Checks</td><td>${checksRate ?? 'sem dados'}</td><td>&gt; 0,99</td></tr></table></html>`;
  return {
    'performance/results/summary.json': JSON.stringify(report, null, 2),
    'performance/results/summary.html': html,
    stdout: `k6 ${report.profile}: p95=${duration}ms, falhas=${errorRate}, checks=${checksRate}\n`,
  };
}
