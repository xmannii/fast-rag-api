// Configuration for RAG API
export const config = {
  // Default Ollama model
  defaultModel: 'gemma3:270m',
  
  // Available models (for validation)
  availableModels: [
    'gemma3:270m',
    'qwen3:4b-thinking-2507-q4_K_M',
    // Add other models here
  ] as string[],
  
  // Ollama settings
  ollama: {
    baseURL: 'http://localhost:11434',
    timeout: 30000, // 30 seconds
  },
  
      // AI SDK settings
      ai: {
        systemPrompt: 'You are a helpful assistant.',
        maxOutputTokens: 8000,
        temperature: 0.7,
        contextPromptTemplate: '📊 DATA:\n{context}\n\n💡 Use this information to answer the question accurately.',
      },
  
  // Embedding settings
  embedding: {
    defaultModel: 'embeddinggemma:latest',
    availableModels: [
      'embeddinggemma:latest',
      'nomic-embed-text',
      // Add other embedding models here
    ] as string[],
  },
  
  // Context database settings
  context: {
    // Database storage location
    storagePath: 'context-db',
    
      // Search parameters
      search: {
        defaultLimit: 5,
        maxLimit: 100,
        defaultThreshold: 0.3,
        minThreshold: 0.0,
        maxThreshold: 1.0,
      },
    
    // Context processing settings
    processing: {
      maxTextLength: 10000, // Maximum text length for context
      autoGenerateId: true, // Auto-generate IDs if not provided
      includeTimestamp: true, // Include creation timestamp in metadata
    },
    
    // Metadata settings
    metadata: {
      allowedFields: ['category', 'source', 'tags', 'author', 'title'], // Allowed metadata fields
      maxMetadataSize: 1000, // Maximum metadata size in characters
    }
  }
} as const;

export type Config = typeof config;
