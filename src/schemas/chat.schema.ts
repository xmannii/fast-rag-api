import { z } from 'zod';

// Zod schema for chat request validation
export const ChatRequestSchema = z.object({
  messages: z.array(z.object({
    role: z.enum(['user', 'assistant', 'system']),
    parts: z.array(z.object({
      type: z.literal('text'),
      text: z.string()
    }))
  })),
  model: z.string().optional(),
  getContext: z.boolean().optional().default(false)
});

export type ChatRequest = z.infer<typeof ChatRequestSchema>;
