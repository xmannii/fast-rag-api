# 📚 Examples

This folder contains simple Python examples for testing and using the RAG-Hono API.

## 🚀 Quick Start

1. **Start the server:**
   ```bash
   bun run dev
   ```

2. **Run any example:**
   ```bash
   python examples/basic_test.py
   ```

## 📋 Available Examples

### 🧪 `basic_test.py`
**Basic API Testing**
- Tests all major endpoints
- Health check, chat, context management, embeddings
- Perfect for quick validation

```bash
python examples/basic_test.py
```

### 💬 `simple_chat.py`
**Interactive Chat**
- Simple command-line chat interface
- Toggle RAG on/off
- Basic conversation flow

```bash
python examples/simple_chat.py
```

### 📚 `knowledge_base.py`
**Knowledge Base Management**
- Populate database with sample data
- Test various search queries
- Clean up after testing

```bash
python examples/knowledge_base.py
```

### 🧠 `embedding_example.py`
**Embedding Generation**
- Generate embeddings for texts
- Calculate cosine similarity
- Find most similar content

```bash
python examples/embedding_example.py
```

### 📊 `performance_test.py`
**Performance Testing**
- Measure response times
- Test different endpoints
- Performance statistics

```bash
python examples/performance_test.py
```

## 🔧 Requirements

- **Python 3.6+**
- **requests library**: `pip install requests`
- **RAG-Hono server running** on `http://localhost:3000`

## 💡 Usage Tips

1. **Start with `basic_test.py`** to verify everything works
2. **Use `knowledge_base.py`** to populate test data
3. **Try `simple_chat.py`** for interactive testing
4. **Run `performance_test.py`** to check performance
5. **Use `embedding_example.py`** to understand embeddings

## 🛠️ Customization

All examples use the default configuration:
- **API Base**: `http://localhost:3000`
- **Default Models**: As configured in `src/config.ts`

You can modify the examples to:
- Change the API base URL
- Use different models
- Test with your own data
- Add more functionality

## 📖 Example Output

### Basic Test
```
🚀 Testing RAG API Endpoints
============================

1. Health Check
   Status: 200
   Response: Hello Hono! AI Chat, Embedding & Context Knowledge Base API is running.

2. Basic Chat
   Status: 200
   ✅ Basic chat working

3. RAG Chat
   Status: 200
   ✅ RAG chat working
```

### Knowledge Base
```
📚 Populating Knowledge Base
===========================
Adding item 1/4: company
  ✅ Added: context_1234567890_abc123

🔍 Testing Search Queries
========================

Searching: 'financial results Q3 2024'
  Found 1 results:
    1. Score: 0.856
       Text: Q3 2024 Financial Results: Revenue $2.4M...
       Category: financial
```

## 🎯 Next Steps

After running the examples:
1. **Explore the API** with your own data
2. **Customize the configuration** in `src/config.ts`
3. **Build your own applications** using these examples
4. **Check the main README** for advanced features

---

**Happy coding! 🚀**
