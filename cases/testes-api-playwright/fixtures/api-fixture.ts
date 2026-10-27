import { test as base } from '@playwright/test';
import { z } from 'zod';

export const authBaseURL = process.env.AUTH_BASE_URL?.trim() || 'https://dummyjson.com';

function loginCredentials(): { username: string; password: string } {
  const username = process.env.AUTH_USERNAME?.trim();
  const password = process.env.AUTH_PASSWORD;

  if (Boolean(username) !== Boolean(password)) {
    throw new Error('Configure AUTH_USERNAME e AUTH_PASSWORD juntos.');
  }
  if (username && password) return { username, password };

  // Conta pública de demonstração documentada pelo DummyJSON.
  if (new URL(authBaseURL).origin === 'https://dummyjson.com') {
    return { username: 'emilys', password: 'emilyspass' };
  }
  throw new Error('Configure AUTH_USERNAME e AUTH_PASSWORD para a API de autenticação escolhida.');
}

export const test = base.extend<{}, { authToken: string }>({
  authToken: [async ({ playwright }, use) => {
    const loginContext = await playwright.request.newContext({ baseURL: authBaseURL });
    let token: string;

    try {
      const response = await loginContext.post('/auth/login', { data: loginCredentials() });
      if (response.status() !== 200) {
        throw new Error(`Falha no login de teste (HTTP ${response.status()}).`);
      }
      const body: unknown = await response.json();
      token = z.object({ accessToken: z.string().min(1) }).parse(body).accessToken;
    } finally {
      await loginContext.dispose();
    }

    await use(token);
  }, { scope: 'worker' }],

  request: async ({ playwright, authToken }, use) => {
    const context = await playwright.request.newContext({
      baseURL: authBaseURL,
      extraHTTPHeaders: {
        Accept: 'application/json',
        Authorization: `Bearer ${authToken}`,
      },
    });
    try {
      await use(context);
    } finally {
      await context.dispose();
    }
  },
});

export { expect } from '@playwright/test';
