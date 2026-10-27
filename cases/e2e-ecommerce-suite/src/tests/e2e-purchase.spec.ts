import { expect, test } from '@playwright/test';
import { ApiClient } from '../api/client.ts';
import { closeDatabase, getOrderById, openDatabase } from '../db/database.ts';
import { LoginPage } from '../pages/LoginPage.ts';
import { CatalogPage } from '../pages/CatalogPage.ts';
import { CheckoutPage } from '../pages/CheckoutPage.ts';

const user = process.env.TEST_USER || 'qa.alfa@example.test';
const password = process.env.TEST_PASS || 'SenhaDeTeste123!';

test('compra na UI gera pedido aprovado com valor correto na API e no SQLite', async ({ page, request }) => {
  const login = new LoginPage(page);
  await login.goto();
  await login.signIn(user, password);

  const catalog = new CatalogPage(page);
  await expect(catalog.heading).toBeVisible();
  await catalog.addProduct('Fone de ouvido');
  await expect(catalog.cartStatus).toHaveText('Carrinho: 1 item');
  await catalog.goToCheckout();

  const checkout = new CheckoutPage(page);
  await expect(checkout.total).toHaveText('Total: R$ 129.90');
  const orderId = await checkout.placeOrder();
  await expect(checkout.confirmation).toHaveText(`Pedido #${orderId} aprovado`);

  const api = new ApiClient(request);
  const { token } = await (await api.login(user, password)).json() as { token: string };
  const response = await api.getOrder(token, orderId);
  expect(response.status()).toBe(200);
  expect(await response.json()).toMatchObject({ id: orderId, status: 'APROVADO', totalCents: 12990 });

  const db = await openDatabase();
  try {
    const persisted = await getOrderById(db, orderId);
    expect(persisted).toMatchObject({ id: orderId, owner: user, status: 'APROVADO', totalCents: 12990 });
  } finally {
    await closeDatabase(db);
  }
});
