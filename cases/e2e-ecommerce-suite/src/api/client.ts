import type { APIRequestContext, APIResponse } from '@playwright/test';
import type { OrderItem } from './OrderSchema.ts';

export class ApiClient {
  private readonly baseURL = process.env.API_URL || process.env.BASE_URL || 'http://127.0.0.1:4173';

  constructor(private readonly request: APIRequestContext) {}

  private url(path: string): string {
    return new URL(path, this.baseURL).toString();
  }

  login(email: string, password: string): Promise<APIResponse> {
    return this.request.post(this.url('/login'), { data: { email, password } });
  }

  products(search?: string): Promise<APIResponse> {
    return this.request.get(this.url('/produtos'), { params: search ? { search } : undefined });
  }

  createOrder(token: string, items: OrderItem[]): Promise<APIResponse> {
    return this.request.post(this.url('/pedidos'), {
      headers: { Authorization: `Bearer ${token}` },
      data: { items },
    });
  }

  getOrder(token: string, id: number): Promise<APIResponse> {
    return this.request.get(this.url(`/pedidos/${id}`), { headers: { Authorization: `Bearer ${token}` } });
  }
}
