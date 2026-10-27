import { fileURLToPath } from 'node:url';
import { defineConfig } from '@playwright/test';
import dotenv from 'dotenv';

// Variáveis do processo (incluindo CI) têm prioridade sobre o arquivo local.
dotenv.config({ path: fileURLToPath(new URL('.env', import.meta.url)), quiet: true });

const baseURL = process.env.BASE_URL?.trim()
  || process.env.API_BASE_URL?.trim()
  || 'https://jsonplaceholder.typicode.com';
const environment = process.env.ENVIRONMENT?.trim() || 'demo';

export default defineConfig({
  metadata: { environment },
  testDir: './tests',
  timeout: 30_000,
  retries: 0,
  forbidOnly: Boolean(process.env.CI),
  reporter: [
    ['list'],
    ['html', { open: 'never', outputFolder: 'playwright-report' }],
  ],
  use: {
    baseURL,
    // API_KEY é opcional e não é enviada ao JSONPlaceholder, que não usa autenticação.
    extraHTTPHeaders: { Accept: 'application/json' },
  },
});
