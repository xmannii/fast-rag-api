import { ollama } from 'ollama-ai-provider-v2';
import { embedMany } from 'ai';
import { LocalIndex } from 'vectra';
import { config } from '../config';
import * as path from 'path';

// Initialize context database
const contextIndex = new LocalIndex(path.join(process.cwd(), config.context.storagePath));

// Initialize index if it doesn't exist
const initializeIndex = async () => {
  if (!(await contextIndex.isIndexCreated())) {
    await contextIndex.createIndex();
  }
};

export class RAGService {
  /**
   * Get relevant context for a user message
   */
  static async getRelevantContext(userMessage: string): Promise<string> {
    try {
      await initializeIndex();
      
      // Generate embedding for the user message
      const embeddingModel = ollama.textEmbeddingModel(config.embedding.defaultModel);
      const { embeddings } = await embedMany({
        model: embeddingModel,
        values: [userMessage],
      });

    // Search for relevant context
    const results = await contextIndex.queryItems(
      embeddings[0], 
      userMessage,
      config.context.search.defaultLimit
    );

    // Filter by threshold and format results
    const relevantContext = results
      .filter(result => result.score >= config.context.search.defaultThreshold)
      .map(result => result.item.metadata.text)
      .join('\n\n');

      return relevantContext;
    } catch (error) {
      console.error('Error getting context:', error);
      return '';
    }
  }
}
