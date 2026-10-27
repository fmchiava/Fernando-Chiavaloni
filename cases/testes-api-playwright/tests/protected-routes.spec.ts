import { z } from 'zod';
import { authBaseURL, test, expect } from '../fixtures/api-fixture';

const userSchema = z.object({
  id: z.number().int().positive(),
  username: z.string().min(1),
  email: z.email(),
});

test('GET /auth/me retorna o usuário autenticado', async ({ request }) => {
  const response = await request.get('/auth/me');

  expect(response.status()).toBe(200);
  const user = userSchema.parse(await response.json());
  expect(user.username).toBe(process.env.AUTH_USERNAME?.trim() || 'emilys');
});

test('GET /auth/products permite consultar recursos com o mesmo token', async ({ request }) => {
  const response = await request.get('/auth/products', { params: { limit: 1 } });

  expect(response.status()).toBe(200);
  const body = z.object({
    products: z.array(z.object({ id: z.number().int().positive() })),
  }).parse(await response.json());
  expect(body.products).toHaveLength(1);
});

test('GET /auth/me sem token retorna 401', async ({ playwright }) => {
  const unauthenticated = await playwright.request.newContext({ baseURL: authBaseURL });
  try {
    const response = await unauthenticated.get('/auth/me');
    expect(response.status()).toBe(401);
  } finally {
    await unauthenticated.dispose();
  }
});
