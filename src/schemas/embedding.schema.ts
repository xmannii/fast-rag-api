import { z } from 'zod';

// Zod schema for embedding request validation
export const EmbeddingRequestSchema = z.object({
  texts: z.array(z.string()).min(1, 'At least one text is required'),
  model: z.string().optional()
});

export type EmbeddingRequest = z.infer<typeof EmbeddingRequestSchema>;
