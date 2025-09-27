import { ollama } from 'ollama-ai-provider-v2';
import { embedMany } from 'ai';
import { LocalIndex } from 'vectra';
import { Hono } from 'hono';
import { config } from '../../config';
import { AddContextSchema, QueryContextSchema, DeleteContextSchema } from '../../schemas/context.schema';
import * as path from 'path';

const context = new Hono();

// Initialize context database
const contextIndex = new LocalIndex(path.join(process.cwd(), config.context.storagePath));

// Initialize index if it doesn't exist
const initializeIndex = async () => {
  if (!(await contextIndex.isIndexCreated())) {
    await contextIndex.createIndex();
  }
};

// POST /context/add - Add context to knowledge base
context.post('/add', async (c) => {
  try {
    const body = await c.req.json();
    
    // Validate request body with Zod
    const validationResult = AddContextSchema.safeParse(body);
    
    if (!validationResult.success) {
      return c.json({ 
        error: 'Invalid request format', 
        details: validationResult.error.issues 
      }, 400);
    }

    const { text, metadata = {}, id } = validationResult.data;

    // Validate text length
    if (text.length > config.context.processing.maxTextLength) {
      return c.json({ 
        error: 'Text too long', 
        maxLength: config.context.processing.maxTextLength,
        currentLength: text.length
      }, 400);
    }

    // Validate metadata size
    const metadataString = JSON.stringify(metadata);
    if (metadataString.length > config.context.metadata.maxMetadataSize) {
      return c.json({ 
        error: 'Metadata too large', 
        maxSize: config.context.metadata.maxMetadataSize,
        currentSize: metadataString.length
      }, 400);
    }

    // Initialize index if needed
    await initializeIndex();

    // Generate embedding for the text
    const embeddingModel = ollama.textEmbeddingModel(config.embedding.defaultModel);
    const { embeddings } = await embedMany({
      model: embeddingModel,
      values: [text],
    });

    // Add to context database
    const itemId = id || (config.context.processing.autoGenerateId ? 
      `context_${Date.now()}_${Math.random().toString(36).substring(2, 11)}` : 
      null);
    
    if (!itemId) {
      return c.json({ error: 'ID is required when autoGenerateId is disabled' }, 400);
    }
    
    const contextMetadata = {
      text,
      ...metadata,
      ...(config.context.processing.includeTimestamp && { createdAt: new Date().toISOString() })
    };
    
    await contextIndex.insertItem({
      id: itemId,
      vector: embeddings[0],
      metadata: contextMetadata,
    });

    return c.json({
      success: true,
      id: itemId,
      message: 'Context added to knowledge base'
    });

  } catch (error) {
    console.error('Error adding context:', error);
    return c.json({ error: 'Failed to add context to knowledge base' }, 500);
  }
});

// POST /context/search - Search context database for similar content
context.post('/search', async (c) => {
  try {
    const body = await c.req.json();
    
    // Validate request body with Zod
    const validationResult = QueryContextSchema.safeParse(body);
    
    if (!validationResult.success) {
      return c.json({ 
        error: 'Invalid request format', 
        details: validationResult.error.issues 
      }, 400);
    }

    const { query, limit, threshold } = validationResult.data;

    // Use config defaults if not provided
    const searchLimit = limit !== undefined ? limit : config.context.search.defaultLimit;
    const searchThreshold = threshold !== undefined ? threshold : config.context.search.defaultThreshold;

    // Validate limits
    if (searchLimit > config.context.search.maxLimit) {
      return c.json({ 
        error: 'Limit too high', 
        maxLimit: config.context.search.maxLimit,
        requestedLimit: searchLimit
      }, 400);
    }

    if (searchThreshold < config.context.search.minThreshold || searchThreshold > config.context.search.maxThreshold) {
      return c.json({ 
        error: 'Threshold out of range', 
        minThreshold: config.context.search.minThreshold,
        maxThreshold: config.context.search.maxThreshold,
        requestedThreshold: searchThreshold
      }, 400);
    }

    // Initialize index if needed
    await initializeIndex();

    // Generate embedding for the query
    const embeddingModel = ollama.textEmbeddingModel(config.embedding.defaultModel);
    const { embeddings } = await embedMany({
      model: embeddingModel,
      values: [query],
    });

    // Search context database
    const results = await contextIndex.queryItems(embeddings[0], query, searchLimit);

    // Filter by threshold and format results
    const filteredResults = results
      .filter(result => result.score >= searchThreshold)
      .map(result => ({
        id: result.item.id,
        text: result.item.metadata.text,
        score: result.score,
        metadata: result.item.metadata
      }));

    return c.json({
      query,
      results: filteredResults,
      count: filteredResults.length,
      threshold: searchThreshold,
      limit: searchLimit
    });

  } catch (error) {
    console.error('Error searching context database:', error);
    return c.json({ error: 'Failed to search context database' }, 500);
  }
});

// DELETE /context/remove - Remove context from knowledge base
context.delete('/remove', async (c) => {
  try {
    const body = await c.req.json();
    
    // Validate request body with Zod
    const validationResult = DeleteContextSchema.safeParse(body);
    
    if (!validationResult.success) {
      return c.json({ 
        error: 'Invalid request format', 
        details: validationResult.error.issues 
      }, 400);
    }

    const { id } = validationResult.data;

    // Initialize index if needed
    await initializeIndex();

    // Delete from context database
    await contextIndex.deleteItem(id);

    return c.json({
      success: true,
      message: `Context with ID ${id} removed from knowledge base`
    });

  } catch (error) {
    console.error('Error removing context:', error);
    return c.json({ error: 'Failed to remove context from knowledge base' }, 500);
  }
});

// GET /context/stats - Get context database statistics
context.get('/stats', async (c) => {
  try {
    await initializeIndex();
    
    return c.json({
      message: 'Context database is initialized',
      config: {
        storagePath: config.context.storagePath,
        embeddingModel: config.embedding.defaultModel,
        searchDefaults: config.context.search,
        processingSettings: config.context.processing,
        metadataSettings: config.context.metadata
      }
    });

  } catch (error) {
    console.error('Error getting context database stats:', error);
    return c.json({ error: 'Failed to get context database stats' }, 500);
  }
});

export default context;
