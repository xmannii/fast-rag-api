# 🚀 RAG-Hono API

A powerful **Retrieval Augmented Generation (RAG)** API built with **Hono** and **Vercel AI SDK**, featuring local vector storage with **Vectra** and **Ollama** integration.

[![Built with Hono](https://img.shields.io/badge/Built%20with-Hono-blue)](https://hono.dev/)
[![AI SDK](https://img.shields.io/badge/AI%20SDK-Vercel-green)](https://sdk.vercel.ai/)
[![Vector DB](https://img.shields.io/badge/Vector%20DB-Vectra-purple)](https://github.com/Stevenic/vectra)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20AI-orange)](https://ollama.ai/)
[![Bun](https://img.shields.io/badge/Runtime-Bun-yellow)](https://bun.sh/)

## ✨ Features

- 🤖 **AI Chat** with streaming responses
- 🔍 **Vector Search** with semantic similarity
- 📚 **Knowledge Base** management
- 🎯 **RAG Pipeline** for context-aware responses
- ⚡ **Fast & Lightweight** with Hono framework
- 🔧 **Configurable** prompts and settings
- 📊 **Embedding Generation** with Ollama
- 🛡️ **Type Safety** with Zod validation

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Chat Route    │───▶│  RAG Pipeline   │───▶│  Vector Store   │
│  (Streaming)    │    │  (Context Prep) │    │   (Vectra)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Ollama LLM    │    │ RAG Service     │    │ Embedding Model │
│  (Gemma/Qwen)   │    │ (Context Ret.)  │    │ (EmbeddingGemma)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Bun** runtime ([Install Bun](https://bun.sh/docs/installation))
- **Ollama** with models installed ([Install Ollama](https://ollama.ai/))

### Installation

```bash
# Clone the repository
git clone https://github.com/xmannii/fast-rag-api
cd rag-hono

# Install dependencies
bun install

# Start the development server
bun run dev
```

### Ollama Setup

```bash
# Install your model of choice
ollama pull gemma3:270m
ollama pull embeddinggemma:latest

```

## 📖 API Documentation

### 🗣️ Chat Endpoint

**POST** `/chat`

Stream AI responses with optional RAG context retrieval.

#### Request Body

```json
{
  "messages": [
    {
      "role": "user",
      "parts": [
        {
          "type": "text",
          "text": "What was our Q3 2024 revenue?"
        }
      ]
    }
  ],
  "model": "gemma3:270m",  // Optional, defaults to config
  "getContext": true       // Enable RAG context retrieval
}
```

#### Response

Server-Sent Events stream with AI response:

```
data: {"type":"start"}
data: {"type":"text-start","id":"abc123"}
data: {"type":"text-delta","id":"abc123","delta":"Q3 2024 Revenue: $2.4M"}
data: {"type":"text-end","id":"abc123"}
data: {"type":"finish"}
data: [DONE]
```

### 🔍 Context Management

#### Add Context

**POST** `/context/add`

```json
{
  "text": "Q3 2024 Financial Report: Revenue increased by 15% to $2.4M, operating expenses decreased by 8% to $1.8M, resulting in net profit of $600K.",
  "metadata": {
    "category": "financial",
    "source": "quarterly-report",
    "tags": ["revenue", "profit", "Q3-2024"]
  },
  "id": "q3-2024-financial"  // Optional, auto-generated if not provided
}
```

#### Search Context

**POST** `/context/search`

```json
{
  "query": "revenue Q3 2024",
  "limit": 5,        // Optional, defaults to 5
  "threshold": 0.3    // Optional, defaults to 0.3
}
```

#### Remove Context

**DELETE** `/context/remove`

```json
{
  "id": "q3-2024-financial"
}
```

#### Get Stats

**GET** `/context/stats`

Returns database statistics and configuration.

### 🧠 Embedding Generation

**POST** `/embedding`

```json
{
  "texts": [
    "Q3 2024 Financial Report",
    "Customer Analysis Report"
  ],
  "model": "embeddinggemma:latest"  // Optional
}
```

**GET** `/embedding/models`

Returns available embedding models.

## ⚙️ Configuration

Edit `src/config.ts` to customize your RAG API:

```typescript
export const config = {
  // Default chat model
  defaultModel: 'gemma3:270m',
  
  // Available models for validation
  availableModels: [
    'gemma3:270m',
    'qwen3:4b-thinking-2507-q4_K_M'
  ],
  
  // Ollama settings
  ollama: {
    baseURL: 'http://localhost:11434',
    timeout: 30000
  },
  
  // AI SDK settings
  ai: {
    systemPrompt: 'You are a helpful assistant.',
    maxOutputTokens: 8000,
    temperature: 0.7,
    contextPromptTemplate: '📊 DATA:\n{context}\n\n💡 Use this information to answer the question accurately.'
  },
  
  // Embedding settings
  embedding: {
    defaultModel: 'embeddinggemma:latest',
    availableModels: [
      'embeddinggemma:latest',
      'nomic-embed-text'
    ]
  },
  
  // Context database settings
  context: {
    storagePath: 'context-db',
    search: {
      defaultLimit: 5,
      maxLimit: 100,
      defaultThreshold: 0.3,
      minThreshold: 0.0,
      maxThreshold: 1.0
    },
    processing: {
      maxTextLength: 10000,
      autoGenerateId: true,
      includeTimestamp: true
    },
    metadata: {
      allowedFields: ['category', 'source', 'tags', 'author', 'title'],
      maxMetadataSize: 1000
    }
  }
}
```

## 🎯 Usage Examples

### Basic Chat

```bash
curl -X POST http://localhost:3000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "parts": [
          {
            "type": "text",
            "text": "Hello! How can you help me?"
          }
        ]
      }
    ]
  }'
```

### RAG-Enhanced Chat

```bash
curl -X POST http://localhost:3000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "parts": [
          {
            "type": "text",
            "text": "What was our Q3 2024 profit?"
          }
        ]
      }
    ],
    "getContext": true
  }'
```

### Add Knowledge Base Content

```bash
curl -X POST http://localhost:3000/context/add \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Our company specializes in AI-powered solutions for enterprise clients. We have 50+ employees across engineering, sales, and operations teams.",
    "metadata": {
      "category": "company-info",
      "source": "about-page",
      "tags": ["company", "employees", "AI"]
    }
  }'
```

### Search Knowledge Base

```bash
curl -X POST http://localhost:3000/context/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "company employees",
    "limit": 3,
    "threshold": 0.2
  }'
```

## 🛠️ Development

### Project Structure

```
src/
├── config.ts                 # Configuration settings
├── index.ts                  # Main application entry
├── routes/
│   ├── chat/
│   │   └── route.ts         # Chat endpoint with RAG
│   ├── context/
│   │   └── route.ts         # Context management
│   └── embedding/
│       └── route.ts         # Embedding generation
├── schemas/
│   ├── chat.schema.ts       # Chat request validation
│   ├── context.schema.ts    # Context request validation
│   └── embedding.schema.ts  # Embedding request validation
├── services/
│   └── rag.service.ts       # RAG core functionality
└── pipelines/
    └── rag.pipeline.ts      # RAG preparation pipeline
```

### Available Scripts

```bash
# Development server
bun run dev

# Build for production
bun run build

# Start production server
bun run start

# Type checking
bun run type-check

# Linting
bun run lint
```

### Environment Variables

Create a `.env` file:

```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_TIMEOUT=30000

# Server Configuration
PORT=3000
NODE_ENV=development

# Optional: Custom paths
CONTEXT_DB_PATH=context-db
```

## 🔧 Customization

### Custom Context Prompt Templates

Modify the `contextPromptTemplate` in `config.ts`:

```typescript
// Professional style
contextPromptTemplate: 'Based on the following information:\n\n{context}\n\nAnswer the user\'s question using this data.'

// Emoji style
contextPromptTemplate: '📊 DATA:\n{context}\n\n💡 Use this information to answer the question accurately.'

// Minimal style
contextPromptTemplate: 'Context: {context}\n\nUse this to answer.'

// Detailed style
contextPromptTemplate: 'Here is relevant information from our knowledge base:\n\n{context}\n\nPlease provide a comprehensive answer based on this data.'
```

### Adding New Models

1. Install the model in Ollama:
   ```bash
   ollama pull your-model:latest
   ```

2. Add to `config.ts`:
   ```typescript
   availableModels: [
     'gemma3:270m',
     'your-model:latest'  // Add here
   ]
   ```

### Custom Metadata Fields

Update the `allowedFields` in `config.ts`:

```typescript
metadata: {
  allowedFields: [
    'category', 
    'source', 
    'tags', 
    'author', 
    'title',
    'department',  // Add custom fields
    'priority',
    'status'
  ]
}
```

## 🧪 Testing

### Test RAG Functionality

1. **Add test data:**
   ```bash
   curl -X POST http://localhost:3000/context/add \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Q3 2024 Financial Report: Revenue $2.4M, Profit $600K",
       "metadata": {"category": "financial", "quarter": "Q3-2024"}
     }'
   ```

2. **Test RAG query:**
   ```bash
   curl -X POST http://localhost:3000/chat \
     -H "Content-Type: application/json" \
     -d '{
       "messages": [{"role": "user", "parts": [{"type": "text", "text": "What was our Q3 profit?"}]}],
       "getContext": true
     }'
   ```

3. **Verify context search:**
   ```bash
   curl -X POST http://localhost:3000/context/search \
     -H "Content-Type: application/json" \
     -d '{"query": "Q3 profit", "threshold": 0.3}'
   ```

## 🚨 Troubleshooting

### Common Issues

**1. Ollama Connection Error**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama service
ollama serve
```

**2. Model Not Found**
```bash
# List available models
ollama list

# Pull missing model
ollama pull gemma3:270m
```

**3. Embedding Model Error**
```bash
# Check Ollama version (requires v0.11.10+)
ollama --version

# Update Ollama if needed
curl -fsSL https://ollama.ai/install.sh | sh
```

**4. Vector Database Issues**
```bash
# Clear database (if corrupted)
rm -rf context-db/

# Restart server to recreate index
bun run dev
```

### Debug Mode

Enable debug logging by setting:

```typescript
// In config.ts
debug: true
```

## 📊 Performance

### Benchmarks

- **Chat Response**: ~200-500ms (depending on model)
- **Context Search**: ~50-100ms (5 results)
- **Embedding Generation**: ~100-200ms (per text)

### Optimization Tips

1. **Use smaller models** for faster responses
2. **Limit context results** to reduce processing time
3. **Adjust threshold** for better relevance vs speed
4. **Cache embeddings** for frequently accessed content

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License 

## 🙏 Acknowledgments

- [Hono](https://hono.dev/) - Lightweight web framework
- [Vercel AI SDK](https://sdk.vercel.ai/) - AI integration toolkit
- [Vectra](https://github.com/Stevenic/vectra) - Local vector database
- [Ollama](https://ollama.ai/) - Local AI model runner
- [Bun](https://bun.sh/) - Fast JavaScript runtime


<div align="center">

**Built with ❤️ using Hono, Vercel AI SDK, and Ollama**

[⭐ Star this repo](https://github.com/xmannii/fast-rag-api) | [🐛 Report Bug](https://github.com/xmannii/fast-rag-api/issues) | [💡 Request Feature](https://github.com/xmannii/fast-rag-api/issues)

</div>