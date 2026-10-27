import { spawn } from 'node:child_process';
import { existsSync, mkdirSync } from 'node:fs';
import { setTimeout as delay } from 'node:timers/promises';

const port = 4174;
const url = `http://127.0.0.1:${port}`;
mkdirSync('performance/results', { recursive: true });

const server = spawn(process.execPath, ['src/utils/mock-server.ts'], {
  env: { ...process.env, PORT: String(port), DB_PATH: '.data/performance.sqlite' },
  stdio: ['ignore', 'inherit', 'inherit'],
});

try {
  let ready = false;
  for (let attempt = 0; attempt < 50; attempt++) {
    if (server.exitCode !== null) throw new Error('Servidor local terminou antes do teste');
    try {
      ready = (await fetch(`${url}/health`)).ok;
      if (ready) break;
    } catch { /* ainda iniciando */ }
    await delay(200);
  }
  if (!ready) throw new Error('Servidor local não respondeu em 10 segundos');

  const args = ['run', '-e', `API_URL=${url}`, '-e', `PROFILE=${process.env.PROFILE || 'load'}`,
    'performance/scenarios/order-load-test.js'];
  const code = await new Promise((resolve, reject) => {
    const localK6 = process.platform === 'win32' ? '.tools/k6/k6.exe' : '.tools/k6/k6';
    const k6 = spawn(existsSync(localK6) ? localK6 : 'k6', args, { stdio: 'inherit' });
    k6.once('error', reject);
    k6.once('exit', resolve);
  });
  if (code !== 0) process.exitCode = code || 1;
} finally {
  server.kill();
}
