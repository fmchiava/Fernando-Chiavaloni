import type { APIRequestContext, APIResponse } from '@playwright/test';
import type { OrderItem } from './OrderSchema.ts';

export class ApiClient {
  constructor(private readonly request: APIRequestContext) {}

  login(email: string, password: string): Promise<APIResponse> {
    return this.request.post('/login', { data: { email, password } });
  }

  products(search?: string): Promise<APIResponse> {
    return this.request.get('/produtos', { params: search ? { search } : undefined });
  }

  createOrder(token: string, items: OrderItem[]): Promise<APIResponse> {
    return this.request.post('/pedidos', {
      headers: { Authorization: `Bearer ${token}` },
      data: { items },
    });
  }

  getOrder(token: string, id: number): Promise<APIResponse> {
    return this.request.get(`/pedidos/${id}`, { headers: { Authorization: `Bearer ${token}` } });
  }
}
