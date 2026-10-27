import type { Page } from '@playwright/test';

export class CatalogPage {
  readonly heading;
  readonly cartStatus;

  constructor(private readonly page: Page) {
    this.heading = page.getByRole('heading', { name: 'Catálogo' });
    this.cartStatus = page.locator('#cart-status');
  }

  async addProduct(name: string): Promise<void> {
    await this.page.getByRole('button', { name: `Adicionar ${name}` }).click();
  }

  async goToCheckout(): Promise<void> {
    await this.page.getByRole('link', { name: 'Ir para checkout' }).click();
  }
}
