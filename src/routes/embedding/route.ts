import { ollama } from 'ollama-ai-provider-v2';
import { embedMany } from 'ai';
import { Hono } from 'hono';
import { config } from '../../config';
import { EmbeddingRequestSchema } from '../../schemas/embedding.schema';

const embedding = new Hono();

// POST /embedding - Generate embeddings for texts
embedding.post('/', async (c) => {
  try {
    const body = await c.req.json();
    
    // Validate request body with Zod
    const validationResult = EmbeddingRequestSchema.safeParse(body);
    
    if (!validationResult.success) {
      return c.json({ 
        error: 'Invalid request format', 
        details: validationResult.error.issues 
      }, 400);
    }

    const { texts, model } = validationResult.data;

    // Use provided model or fall back to default
    const selectedModel = model || config.embedding.defaultModel;

    // Validate model is available
    if (!config.embedding.availableModels.includes(selectedModel)) {
      return c.json({ 
        error: 'Embedding model not available', 
        availableModels: config.embedding.availableModels 
      }, 400);
    }

    // Create embedding model
    const embeddingModel = ollama.textEmbeddingModel(selectedModel);

    // Generate embeddings
    const { embeddings } = await embedMany({
      model: embeddingModel,
      values: texts,
    });

    return c.json({
      embeddings,
      model: selectedModel,
      count: embeddings.length
    });

  } catch (error) {
    console.error('Error in embedding route:', error);
    return c.json({ error: 'Failed to generate embeddings' }, 500);
  }
});

// GET /embedding/models - Get available embedding models
embedding.get('/models', async (c) => {
  return c.json({
    models: config.embedding.availableModels,
    defaultModel: config.embedding.defaultModel
  });
});

export default embedding;