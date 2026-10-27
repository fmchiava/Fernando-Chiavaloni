import { expect, type Page } from '@playwright/test';

export class CheckoutPage {
  readonly total;
  readonly confirmation;

  constructor(private readonly page: Page) {
    this.total = page.locator('#total');
    this.confirmation = page.getByRole('status');
  }

  async placeOrder(): Promise<number> {
    await this.page.getByRole('button', { name: 'Finalizar compra' }).click();
    await expect(this.confirmation).toHaveAttribute('data-order-id', /^\d+$/);
    return Number(await this.confirmation.getAttribute('data-order-id'));
  }
}
