import { expect, test } from '@playwright/test';
import { ApiClient } from '../api/client.ts';
import { OrderSchema } from '../api/OrderSchema.ts';
import { closeDatabase, getOrderById, openDatabase } from '../db/database.ts';

const user = process.env.TEST_USER || 'qa.alfa@example.test';
const password = process.env.TEST_PASS || 'SenhaDeTeste123!';

test('GET /produtos retorna 200 e catálogo com preço em centavos', async ({ request }) => {
  const response = await new ApiClient(request).products();
  expect(response.status()).toBe(200);
  expect(await response.json()).toContainEqual({ id: 'sku-1', name: 'Fone de ouvido', priceCents: 12990 });
});

test('POST /pedidos retorna 201, contrato válido e GET retorna 200', async ({ request }) => {
  const api = new ApiClient(request);
  const login = await api.login(user, password);
  expect(login.status()).toBe(200);
  const { token } = await login.json() as { token: string };
  const created = await api.createOrder(token, [{ productId: 'sku-1', quantity: 1 }]);
  expect(created.status()).toBe(201);
  const order = OrderSchema.parse(await created.json());
  expect(order.status).toBe('APROVADO');
  expect(order.totalCents).toBe(12990);
  const fetched = await api.getOrder(token, order.id);
  expect(fetched.status()).toBe(200);
  expect(OrderSchema.parse(await fetched.json())).toEqual(order);
});

test('POST /pedidos rejeita quantidade inválida com 400', async ({ request }) => {
  const api = new ApiClient(request);
  const { token } = await (await api.login(user, password)).json() as { token: string };
  const response = await api.createOrder(token, [{ productId: 'sku-1', quantity: 0 }]);
  expect(response.status()).toBe(400);
  expect(await response.json()).toMatchObject({ error: 'invalid_order' });
});

test('POST /pedidos ignora total adulterado e persiste preço do catálogo', async ({ request }) => {
  const api = new ApiClient(request);
  const { token } = await (await api.login(user, password)).json() as { token: string };
  const response = await request.post('/pedidos', {
    headers: { Authorization: `Bearer ${token}` },
    data: { items: [{ productId: 'sku-1', quantity: 1 }], totalCents: 1 },
  });
  expect(response.status()).toBe(201);
  const { id, totalCents } = OrderSchema.parse(await response.json());
  expect(totalCents).toBe(12990);
  const db = await openDatabase();
  try {
    expect((await getOrderById(db, id))?.totalCents).toBe(12990);
  } finally {
    await closeDatabase(db);
  }
});
