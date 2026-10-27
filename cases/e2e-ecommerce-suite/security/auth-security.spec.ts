import { expect, test } from '@playwright/test';
import { ApiClient } from '../src/api/client.ts';

const password = 'SenhaDeTeste123!';

test('rotas de carrinho e pedido recusam requisição sem Bearer', async ({ request }) => {
  for (const route of ['/carrinho', '/pedidos']) {
    const response = await request.post(route, { data: { items: [{ productId: 'sku-1', quantity: 1 }] } });
    expect(response.status(), route).toBe(401);
    expect(await response.json()).toMatchObject({ error: 'unauthorized' });
  }
});

test('IDOR: outro usuário não consegue consultar pedido pelo ID', async ({ request }) => {
  const api = new ApiClient(request);
  const { token: alphaToken } = await (await api.login('qa.alfa@example.test', password)).json() as { token: string };
  const { token: betaToken } = await (await api.login('qa.beta@example.test', password)).json() as { token: string };
  const created = await api.createOrder(alphaToken, [{ productId: 'sku-1', quantity: 1 }]);
  expect(created.status()).toBe(201);
  const { id } = await created.json() as { id: number };

  expect((await api.getOrder(betaToken, id)).status()).toBe(404);
  expect((await api.getOrder(alphaToken, id)).status()).toBe(200);
});

test('SQL Injection em login e busca não altera autenticação nem catálogo', async ({ request }) => {
  const api = new ApiClient(request);
  const attemptedLogin = await api.login("' OR 1=1 --", password);
  expect(attemptedLogin.status()).toBe(401);

  const injectedSearch = await api.products("' OR 1=1 --");
  expect(injectedSearch.status()).toBe(200);
  expect(await injectedSearch.json()).toEqual([]);
  expect((await (await api.products()).json()).length).toBe(2);
});
