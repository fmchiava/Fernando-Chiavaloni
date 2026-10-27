import { randomUUID } from 'node:crypto';
import { test, expect } from '@playwright/test';
import { z } from 'zod';
import testData from '../fixtures/test-data.json' with { type: 'json' };
import { commentsSchema, emptyResponseSchema, postSchema, postsSchema } from '../utils/schemas';

// O JSON não preserva tipos literais do TypeScript; valide a fixture antes de registrar os testes.
const fixtures = z.object({
  lookup: z.array(z.object({
    name: z.string(),
    id: z.number().int().positive(),
    expectedStatus: z.union([z.literal(200), z.literal(404)]),
  })),
  create: z.array(z.object({
    name: z.string(),
    payload: z.object({
      userId: z.union([z.number(), z.string()]),
      title: z.union([z.string(), z.number()]),
      body: z.string(),
    }),
    expectedStatus: z.literal(201),
    expectedContractValid: z.boolean(),
  })),
}).parse(testData);

test.describe('Contrato da API /posts', () => {
  test('GET /posts lista posts com o contrato esperado', async ({ request }) => {
    const response = await request.get('/posts');

    expect(response.status()).toBe(200);
    const posts = postsSchema.parse(await response.json());
    expect(posts).toHaveLength(100);
  });

  test('GET /posts?userId=1 filtra os posts do usuário', async ({ request }) => {
    const response = await request.get('/posts', { params: { userId: 1 } });

    expect(response.status()).toBe(200);
    const posts = postsSchema.parse(await response.json());
    expect(posts).toHaveLength(10);
    expect(posts.every((post) => post.userId === 1)).toBe(true);
  });

  test('GET /posts?userId=999999 retorna lista vazia', async ({ request }) => {
    const response = await request.get('/posts', { params: { userId: 999999 } });

    expect(response.status()).toBe(200);
    expect(postsSchema.parse(await response.json())).toEqual([]);
  });

  fixtures.lookup.forEach((scenario) => {
    test(`GET /posts/${scenario.id}: ${scenario.name}`, async ({ request }) => {
      const response = await request.get(`/posts/${scenario.id}`);

      expect(response.status()).toBe(scenario.expectedStatus);
      const body: unknown = await response.json();
      if (scenario.expectedStatus === 200) {
        expect(postSchema.parse(body).id).toBe(scenario.id);
      } else {
        emptyResponseSchema.parse(body);
      }
    });
  });

  test('GET /posts/1/comments retorna comentários relacionados ao post', async ({ request }) => {
    const response = await request.get('/posts/1/comments');

    expect(response.status()).toBe(200);
    const comments = commentsSchema.parse(await response.json());
    expect(comments).toHaveLength(5);
    expect(comments.every((comment) => comment.postId === 1)).toBe(true);
  });

  fixtures.create.forEach((scenario) => {
    test(`POST /posts: ${scenario.name}`, async ({ request }) => {
      const response = await request.post('/posts', { data: scenario.payload });

      expect(response.status()).toBe(scenario.expectedStatus);
      const body: unknown = await response.json();
      expect(body).toEqual({ ...scenario.payload, id: 101 });
      expect(postSchema.safeParse(body).success).toBe(scenario.expectedContractValid);
    });
  });

  test('PUT /posts/1 retorna a substituição completa simulada', async ({ request }) => {
    const data = {
      id: 1,
      userId: 1,
      title: `Post substituído ${randomUUID()}`,
      body: 'Conteúdo atualizado integralmente.',
    };

    const response = await request.put('/posts/1', { data });

    expect(response.status()).toBe(200);
    const post = postSchema.parse(await response.json());
    expect(post).toEqual(data);
  });

  test('PATCH /posts/1 altera apenas o campo enviado na resposta simulada', async ({ request }) => {
    const originalResponse = await request.get('/posts/1');
    expect(originalResponse.status()).toBe(200);
    const original = postSchema.parse(await originalResponse.json());
    const title = `Título parcial ${randomUUID()}`;

    const response = await request.patch('/posts/1', { data: { title } });

    expect(response.status()).toBe(200);
    const updated = postSchema.parse(await response.json());
    expect(updated).toEqual({ ...original, title });
  });

  test('DELETE /posts/1 retorna sucesso e corpo vazio', async ({ request }) => {
    const response = await request.delete('/posts/1');

    expect(response.status()).toBe(200);
    emptyResponseSchema.parse(await response.json());
  });
});
