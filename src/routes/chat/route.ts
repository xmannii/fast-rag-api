import { ollama } from 'ollama-ai-provider-v2';
import { streamText, convertToModelMessages } from 'ai';
import { Hono } from 'hono';
import { config } from '../../config';
import { ChatRequestSchema } from '../../schemas/chat.schema';
import { RAGPipeline } from '../../pipelines/rag.pipeline';

const chat = new Hono();

// POST /chat - Stream UI messages for chat interface
chat.post('/', async (c) => {
  try {
    const body = await c.req.json();
    
    // Validate request body with Zod
    const validationResult = ChatRequestSchema.safeParse(body);
    
    if (!validationResult.success) {
      return c.json({ 
        error: 'Invalid request format', 
        details: validationResult.error.issues 
      }, 400);
    }

    const { messages, model, getContext } = validationResult.data;

    // Use provided model or fall back to default
    const selectedModel = model || config.defaultModel;

    // Validate model is available
    if (!config.availableModels.includes(selectedModel)) {
      return c.json({ 
        error: 'Model not available', 
        availableModels: config.availableModels 
      }, 400);
    }

    // RAG Pipeline: Get relevant context if requested
    const contextPrompt = await RAGPipeline.prepareContext(messages, getContext);

    // Prepare system prompt with context
    const systemPrompt = config.ai.systemPrompt + contextPrompt;

    const result = streamText({
      model: ollama(selectedModel),
      system: systemPrompt,
      messages: convertToModelMessages(messages),
      maxOutputTokens: config.ai.maxOutputTokens, 
      temperature: config.ai.temperature,
    });

    return result.toUIMessageStreamResponse({
      headers: {
        'Transfer-Encoding': 'chunked',
        'Connection': 'keep-alive',
        'Content-Encoding': 'none',
      },
    });
  } catch (error) {
    console.error('Error in chat route:', error);
    return c.json({ error: 'Failed to process chat request' }, 500);
  }
});

export default chat;
