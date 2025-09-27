import { z } from 'zod';

// Zod schema for adding context to knowledge base
export const AddContextSchema = z.object({
  text: z.string().min(1, 'Text is required'),
  metadata: z.record(z.any(), z.any()).optional(),
  id: z.string().optional()
});

// Zod schema for searching context database
export const QueryContextSchema = z.object({
  query: z.string().min(1, 'Query is required'),
  limit: z.number().min(1).max(100).optional(),
  threshold: z.number().min(0).max(1).optional()
});

// Zod schema for removing context
export const DeleteContextSchema = z.object({
  id: z.string().min(1, 'ID is required')
});

export type AddContextRequest = z.infer<typeof AddContextSchema>;
export type QueryContextRequest = z.infer<typeof QueryContextSchema>;
export type DeleteContextRequest = z.infer<typeof DeleteContextSchema>;
