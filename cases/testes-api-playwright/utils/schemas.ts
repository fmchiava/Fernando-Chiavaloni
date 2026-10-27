import { z } from 'zod';

// Campos obrigatórios e sem propriedades extras: uma mudança no payload quebra o contrato.
export const postSchema = z.strictObject({
  userId: z.number().int().positive(),
  id: z.number().int().positive(),
  title: z.string().min(1),
  body: z.string().min(1),
});

export const postsSchema = z.array(postSchema);

export const commentSchema = z.strictObject({
  postId: z.number().int().positive(),
  id: z.number().int().positive(),
  name: z.string().min(1),
  email: z.email(),
  body: z.string().min(1),
});

export const commentsSchema = z.array(commentSchema);
export const emptyResponseSchema = z.strictObject({});

export type Post = z.infer<typeof postSchema>;
