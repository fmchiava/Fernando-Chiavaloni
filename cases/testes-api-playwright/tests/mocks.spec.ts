import { test, expect } from '@playwright/test';
import { postSchema } from '../utils/schemas';

const origin = 'https://mock-api.test';
const postURL = `${origin}/posts/1`;

// page.route intercepta fetch/XHR do navegador; APIRequestContext não oferece request.route.
// Mocks isolam a reação do cliente a falhas difíceis de reproduzir. Os testes de contrato
// contra a API real continuam necessários para detectar mudanças do provedor.
test.beforeEach(async ({ page }) => {
  await page.route(`${origin}/`, (route) => route.fulfill({
    status: 200,
    contentType: 'text/html',
    body: '<!doctype html><title>Cliente de teste</title>',
  }));
  await page.goto(`${origin}/`);
});

test('simula erro 500 do serviço externo', async ({ page }) => {
  await page.route(postURL, (route) => route.fulfill({
    status: 500,
    json: { error: 'Serviço temporariamente indisponível' },
  }));

  const result = await page.evaluate(async () => {
    const response = await fetch('/posts/1');
    return { status: response.status, body: await response.json() };
  });

  expect(result).toEqual({
    status: 500,
    body: { error: 'Serviço temporariamente indisponível' },
  });
});

test('simula timeout de rede sem esperar um timeout real', async ({ page }) => {
  await page.route(postURL, (route) => route.abort('timedout'));
  const failedRequest = page.waitForEvent('requestfailed', (request) => request.url() === postURL);

  const result = await page.evaluate(async () => {
    try {
      await fetch('/posts/1');
      return 'sucesso inesperado';
    } catch {
      return 'erro de rede';
    }
  });

  expect(result).toBe('erro de rede');
  expect((await failedRequest).failure()?.errorText).toContain('TIMED_OUT');
});

test('substitui o payload por uma resposta customizada', async ({ page }) => {
  const customPost = {
    userId: 1,
    id: 1,
    title: 'Post devolvido pelo mock',
    body: 'Resposta controlada para um cenário de integração.',
  };
  await page.route(postURL, (route) => route.fulfill({ status: 200, json: customPost }));

  const result = await page.evaluate(async () => {
    const response = await fetch('/posts/1');
    return { status: response.status, body: await response.json() };
  });

  expect(result.status).toBe(200);
  expect(postSchema.parse(result.body)).toEqual(customPost);
});
