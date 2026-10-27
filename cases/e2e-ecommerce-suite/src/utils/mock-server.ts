import { randomBytes } from 'node:crypto';
import { createServer, type IncomingMessage, type ServerResponse } from 'node:http';
import { OrderRequestSchema } from '../api/OrderSchema.ts';
import {
  all, authenticate, createOrder, get, getOrderById, initializeDatabase, openDatabase,
  type Database,
} from '../db/database.ts';

type Product = { id: string; name: string; price_cents: number };
const db = await openDatabase();
await initializeDatabase(db);
const sessions = new Map<string, string>();

function json(response: ServerResponse, status: number, body: unknown): void {
  response.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' });
  response.end(JSON.stringify(body));
}

function html(response: ServerResponse, body: string): void {
  response.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store' });
  response.end(body);
}

function authenticatedUser(request: IncomingMessage): string | undefined {
  const token = /^Bearer ([a-f0-9]+)$/.exec(request.headers.authorization || '')?.[1];
  return token ? sessions.get(token) : undefined;
}

async function readJson(request: IncomingMessage): Promise<unknown> {
  let body = '';
  for await (const chunk of request) {
    body += chunk.toString();
    if (body.length > 16_384) throw new Error('invalid_json');
  }
  try { return JSON.parse(body); } catch { throw new Error('invalid_json'); }
}

async function pricedItems(database: Database, input: unknown): Promise<{ totalCents: number; items: { productId: string; quantity: number }[] } | undefined> {
  const parsed = OrderRequestSchema.safeParse(input);
  if (!parsed.success) return undefined;
  let totalCents = 0;
  for (const item of parsed.data.items) {
    const product = await get<Product>(database, 'SELECT * FROM products WHERE id = ?', [item.productId]);
    if (!product) return undefined;
    totalCents += product.price_cents * item.quantity;
  }
  return { totalCents, items: parsed.data.items };
}

const server = createServer(async (request, response) => {
  const url = new URL(request.url || '/', 'http://127.0.0.1');
  const method = request.method || 'GET';
  try {
    if (method === 'GET' && url.pathname === '/health') return json(response, 200, { ok: true });
    if (method === 'GET' && url.pathname === '/login') return html(response, loginPage);
    if (method === 'GET' && url.pathname === '/catalogo') return html(response, catalogPage);
    if (method === 'GET' && url.pathname === '/checkout') return html(response, checkoutPage);

    if (method === 'POST' && url.pathname === '/login') {
      const body = await readJson(request) as Record<string, unknown>;
      if (typeof body?.email !== 'string' || typeof body?.password !== 'string') return json(response, 400, { error: 'invalid_credentials' });
      if (!await authenticate(db, body.email, body.password)) return json(response, 401, { error: 'invalid_credentials' });
      const token = randomBytes(24).toString('hex');
      sessions.set(token, body.email);
      return json(response, 200, { token });
    }

    if (method === 'GET' && url.pathname === '/produtos') {
      const search = url.searchParams.get('search') || '';
      const rows = await all<Product>(db,
        'SELECT * FROM products WHERE name LIKE ? ORDER BY id', [`%${search}%`]);
      return json(response, 200, rows.map(row => ({ id: row.id, name: row.name, priceCents: row.price_cents })));
    }

    if (method === 'POST' && (url.pathname === '/carrinho' || url.pathname === '/pedidos')) {
      const owner = authenticatedUser(request);
      if (!owner) return json(response, 401, { error: 'unauthorized' });
      const priced = await pricedItems(db, await readJson(request));
      if (!priced) return json(response, 400, { error: 'invalid_order' });
      if (url.pathname === '/carrinho') return json(response, 200, priced);
      return json(response, 201, await createOrder(db, owner, priced.items, priced.totalCents));
    }

    const orderMatch = /^\/pedidos\/(\d+)$/.exec(url.pathname);
    if (method === 'GET' && orderMatch) {
      const owner = authenticatedUser(request);
      if (!owner) return json(response, 401, { error: 'unauthorized' });
      const order = await getOrderById(db, Number(orderMatch[1]));
      if (!order || order.owner !== owner) return json(response, 404, { error: 'not_found' });
      return json(response, 200, order);
    }

    return json(response, 404, { error: 'not_found' });
  } catch (error) {
    if (error instanceof Error && error.message === 'invalid_json') return json(response, 400, { error: 'invalid_json' });
    console.error('Mock server error:', error instanceof Error ? error.message : 'unknown');
    return json(response, 500, { error: 'internal_error' });
  }
});

const port = Number(process.env.PORT || 4173);
server.listen(port, '127.0.0.1', () => console.log(`Mock e-commerce em http://127.0.0.1:${port}`));

const loginPage = `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Login | Loja QA</title></head>
<body><main><h1>Entrar na Loja QA</h1><form id="login-form">
<label>E-mail <input name="email" type="email" required></label>
<label>Senha <input name="password" type="password" required></label>
<button type="submit">Entrar</button></form><p role="alert" id="error"></p></main>
<script>document.querySelector('#login-form').addEventListener('submit', async event => {
  event.preventDefault(); const form = new FormData(event.target);
  const response = await fetch('/login', { method: 'POST', headers: {'Content-Type':'application/json'},
    body: JSON.stringify({email: form.get('email'), password: form.get('password')}) });
  if (!response.ok) { document.querySelector('#error').textContent = 'Credenciais inválidas'; return; }
  const {token} = await response.json(); sessionStorage.setItem('token', token); location.href = '/catalogo';
});</script></body></html>`;

const catalogPage = `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Catálogo | Loja QA</title></head>
<body><main><h1>Catálogo</h1><ul id="products"></ul><p id="cart-status">Carrinho vazio</p>
<a href="/checkout">Ir para checkout</a></main><script>
if (!sessionStorage.getItem('token')) location.href = '/login';
fetch('/produtos').then(response => response.json()).then(products => {
  const list = document.querySelector('#products');
  for (const product of products) {
    const item = document.createElement('li'); const title = document.createElement('span');
    title.textContent = product.name + ' — R$ ' + (product.priceCents / 100).toFixed(2);
    const button = document.createElement('button'); button.textContent = 'Adicionar ' + product.name;
    button.addEventListener('click', async () => {
      const items = [{productId: product.id, quantity: 1}];
      const response = await fetch('/carrinho', {method:'POST', headers:{'Content-Type':'application/json',
        Authorization:'Bearer ' + sessionStorage.getItem('token')}, body:JSON.stringify({items})});
      if (!response.ok) return;
      const cart = await response.json(); sessionStorage.setItem('cart', JSON.stringify({...cart, items}));
      document.querySelector('#cart-status').textContent = 'Carrinho: 1 item';
    });
    item.append(title, button); list.append(item);
  }
});</script></body></html>`;

const checkoutPage = `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Checkout | Loja QA</title></head>
<body><main><h1>Checkout</h1><p id="total"></p><button id="finish">Finalizar compra</button>
<p role="status" id="confirmation"></p></main><script>
if (!sessionStorage.getItem('token')) location.href = '/login';
const cart = JSON.parse(sessionStorage.getItem('cart') || 'null');
document.querySelector('#total').textContent = cart ? 'Total: R$ ' + (cart.totalCents / 100).toFixed(2) : 'Carrinho vazio';
document.querySelector('#finish').addEventListener('click', async () => {
  if (!cart) return; const response = await fetch('/pedidos', {method:'POST', headers:{'Content-Type':'application/json',
    Authorization:'Bearer ' + sessionStorage.getItem('token')}, body:JSON.stringify({items:cart.items})});
  if (!response.ok) { document.querySelector('#confirmation').textContent = 'Falha no pedido'; return; }
  const order = await response.json(); const confirmation = document.querySelector('#confirmation');
  confirmation.dataset.orderId = String(order.id); confirmation.textContent = 'Pedido #' + order.id + ' aprovado';
  sessionStorage.removeItem('cart');
});</script></body></html>`;
