import { z } from 'zod';

export const OrderRequestSchema = z.object({
  items: z.array(z.object({
    productId: z.string().min(1),
    quantity: z.number().int().min(1).max(10),
  })).min(1),
});

export const OrderSchema = z.object({
  id: z.number().int().positive(),
  owner: z.string().email(),
  status: z.literal('APROVADO'),
  totalCents: z.number().int().positive(),
  items: OrderRequestSchema.shape.items,
  createdAt: z.string().datetime(),
});

export type Order = z.infer<typeof OrderSchema>;
export type OrderItem = z.infer<typeof OrderRequestSchema>['items'][number];
