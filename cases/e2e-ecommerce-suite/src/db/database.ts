import { randomBytes, scryptSync, timingSafeEqual } from 'node:crypto';
import { mkdirSync } from 'node:fs';
import { dirname } from 'node:path';
import sqlite3 from 'sqlite3';
import type { OrderItem } from '../api/OrderSchema.ts';

export type Database = sqlite3.Database;

export function openDatabase(path = process.env.DB_PATH || '.data/ecommerce.sqlite'): Promise<Database> {
  if (path !== ':memory:') mkdirSync(dirname(path), { recursive: true });
  return new Promise((resolve, reject) => {
    const db = new sqlite3.Database(path, error => error ? reject(error) : resolve(db));
  });
}

export function closeDatabase(db: Database): Promise<void> {
  return new Promise((resolve, reject) => db.close(error => error ? reject(error) : resolve()));
}

export function exec(db: Database, sql: string): Promise<void> {
  return new Promise((resolve, reject) => db.exec(sql, error => error ? reject(error) : resolve()));
}

export function run(db: Database, sql: string, params: unknown[] = []): Promise<number> {
  return new Promise((resolve, reject) => {
    db.run(sql, params, function (this: sqlite3.RunResult, error) {
      if (error) reject(error);
      else resolve(this.lastID);
    });
  });
}

export function get<T>(db: Database, sql: string, params: unknown[] = []): Promise<T | undefined> {
  return new Promise((resolve, reject) => {
    db.get(sql, params, (error, row) => error ? reject(error) : resolve(row as T | undefined));
  });
}

export function all<T>(db: Database, sql: string, params: unknown[] = []): Promise<T[]> {
  return new Promise((resolve, reject) => {
    db.all(sql, params, (error, rows) => error ? reject(error) : resolve(rows as T[]));
  });
}

type UserRow = { email: string; salt: string; password_hash: string };
type OrderRow = { id: number; owner: string; status: string; total_cents: number; items_json: string; created_at: string };

export async function initializeDatabase(db: Database): Promise<void> {
  await exec(db, `
    PRAGMA busy_timeout = 5000;
    CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, salt TEXT NOT NULL, password_hash TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS products (id TEXT PRIMARY KEY, name TEXT NOT NULL, price_cents INTEGER NOT NULL);
    CREATE TABLE IF NOT EXISTS orders (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      owner TEXT NOT NULL REFERENCES users(email),
      status TEXT NOT NULL CHECK (status = 'APROVADO'),
      total_cents INTEGER NOT NULL CHECK (total_cents > 0),
      items_json TEXT NOT NULL,
      created_at TEXT NOT NULL
    );
  `);
  for (const email of ['qa.alfa@example.test', 'qa.beta@example.test']) {
    const existing = await get<UserRow>(db, 'SELECT email FROM users WHERE email = ?', [email]);
    if (!existing) {
      const salt = randomBytes(16).toString('hex');
      const hash = scryptSync('SenhaDeTeste123!', salt, 64).toString('hex');
      await run(db, 'INSERT INTO users (email, salt, password_hash) VALUES (?, ?, ?)', [email, salt, hash]);
    }
  }
  await run(db, 'INSERT OR IGNORE INTO products (id, name, price_cents) VALUES (?, ?, ?)', ['sku-1', 'Fone de ouvido', 12990]);
  await run(db, 'INSERT OR IGNORE INTO products (id, name, price_cents) VALUES (?, ?, ?)', ['sku-2', 'Mouse sem fio', 7990]);
}

export async function authenticate(db: Database, email: string, password: string): Promise<boolean> {
  const user = await get<UserRow>(db, 'SELECT * FROM users WHERE email = ?', [email]);
  if (!user) return false;
  const supplied = scryptSync(password, user.salt, 64);
  return timingSafeEqual(supplied, Buffer.from(user.password_hash, 'hex'));
}

export async function getOrderById(db: Database, id: number) {
  const row = await get<OrderRow>(db, 'SELECT * FROM orders WHERE id = ?', [id]);
  if (!row) return undefined;
  return {
    id: row.id,
    owner: row.owner,
    status: row.status,
    totalCents: row.total_cents,
    items: JSON.parse(row.items_json) as OrderItem[],
    createdAt: row.created_at,
  };
}

export async function createOrder(db: Database, owner: string, items: OrderItem[], totalCents: number) {
  const createdAt = new Date().toISOString();
  const id = await run(db,
    'INSERT INTO orders (owner, status, total_cents, items_json, created_at) VALUES (?, ?, ?, ?, ?)',
    [owner, 'APROVADO', totalCents, JSON.stringify(items), createdAt],
  );
  return { id, owner, status: 'APROVADO' as const, totalCents, items, createdAt };
}
