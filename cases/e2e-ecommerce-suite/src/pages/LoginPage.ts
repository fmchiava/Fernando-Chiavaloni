import type { Page } from '@playwright/test';

export class LoginPage {
  constructor(private readonly page: Page) {}

  async goto(): Promise<void> {
    await this.page.goto('/login');
  }

  async signIn(email: string, password: string): Promise<void> {
    await this.page.getByRole('textbox', { name: 'E-mail' }).fill(email);
    await this.page.getByLabel('Senha').fill(password);
    await Promise.all([
      this.page.waitForURL('**/catalogo'),
      this.page.getByRole('button', { name: 'Entrar' }).click(),
    ]);
  }
}
