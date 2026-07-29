# 🧠 Context Memory Engine

A modular AI Context Memory Engine that enables Large Language Models (LLMs) to remember conversations, uploaded documents, and user preferences across interactions.

The project is designed to provide persistent, relevant, and optimized context to an LLM instead of relying only on the current prompt, making AI conversations more continuous, personalized, and reliable.

---

# ✨ Features

## ✅ Conversation Memory
- Stores conversations in SQLite
- Retrieves recent conversations
- Maintains conversation history
- Supports multiple conversations per user

---

## ✅ Message Memory
- Stores chat messages
- Retrieves recent messages
- Semantic retrieval using embeddings
- ChromaDB vector search

---

## ✅ Document Memory
- Upload and index documents
- Semantic document retrieval
- Automatic document ranking
- Metadata tracking
    - Importance
    - Access count
    - Last accessed timestamp

---

## ✅ User Preference Memory
Stores user-specific preferences such as:

- Language
- Interaction preferences
- Personal settings

These preferences are automatically injected into the LLM context.

---

## ✅ Embedding Pipeline

Uses Sentence Transformers for semantic embeddings.

Current pipeline:

```
Text
   │
   ▼
Embedding Manager
   │
   ▼
Sentence Transformer
   │
   ▼
ChromaDB
```

---

## ✅ Vector Database

Uses ChromaDB for semantic retrieval.

Collections:

- Documents
- Messages

Supports:

- Similarity Search
- Metadata Filtering
- Top-K Retrieval

---

## ✅ Memory Optimization

Before sending context to the LLM, the engine:

- Removes unnecessary memory
- Combines multiple memory sources
- Reduces context size
- Optimizes retrieval quality

---

## ✅ Unified Context Manager

Combines:

- Conversation Memory
- Message Memory
- Document Memory
- User Preferences

into a single unified memory representation.

---

## ✅ Memory Ranking

Uses a dedicated Memory Selector that ranks memories based on relevance before sending them to the LLM.

---

## ✅ Context Builder

Constructs the final prompt for the LLM by combining:

- Current user question
- Selected memories
- Retrieved documents
- Conversation history
- Preferences

---

## ✅ LLM Integration

Current provider:

- Google Gemini

The architecture is provider-independent and can be extended to support:

- OpenAI
- Claude
- Local LLMs
- Ollama

---

# 🏗 Architecture

```
Frontend/API
      │
      ▼
ChatService
      │
      ▼
MemoryEngine
      │
      ├──────── PromptManager
      ├──────── ConversationMemory
      ├──────── MessageMemory
      ├──────── DocumentMemory
      ├──────── PreferenceMemory
      ├──────── ContextOptimizer
      ├──────── UnifiedContextManager
      ├──────── MemorySelector
      ├──────── ContextBuilder
      └──────── LLMManager
                     │
                     ▼
                 Gemini API
```

---

# ⚙️ Tech Stack

### Backend

- Python
- FastAPI
- SQLAlchemy

### Database

- SQLite

### Vector Database

- ChromaDB

### Embeddings

- Sentence Transformers

### LLM

- Google Gemini API

---

# 📂 Project Structure

```
backend/
│
├── database/
├── embeddings/
├── llm/
├── memory/
│   ├── conversation_memory.py
│   ├── message_memory.py
│   ├── document_memory.py
│   ├── preference_memory.py
│   ├── context_optimizer.py
│   ├── unified_context_manager.py
│   ├── context_builder.py
│   ├── memory_selector.py
│   └── memory_engine.py
│
├── retrieval/
├── services/
└── test_memory_engine.py
```

---

# 🧩 Memory Engine Workflow

```
User Prompt
      │
      ▼
Prepare Prompt
      │
      ▼
Retrieve Memories
      │
      ▼
Optimize Memory
      │
      ▼
Build Unified Memory
      │
      ▼
Select Relevant Memory
      │
      ▼
Build Context
      │
      ▼
Generate AI Response
```

---

# 🚀 Current Progress

## ✅ Completed

- Conversation Memory
- Message Memory
- Document Memory
- Preference Memory
- Embedding Manager
- ChromaDB Integration
- Semantic Search
- Context Optimizer
- Unified Context Manager
- Memory Ranking
- Context Builder
- Gemini Integration
- Modular Memory Engine Refactor
- End-to-End Memory Pipeline

---

# 🔄 In Progress

- Duplicate memory removal
- Improved semantic ranking
- Better memory filtering
- Error handling and fallback for LLM providers

---

# 📋 Planned Features

- Multi-document conversations
- Long-term memory
- Memory aging and decay
- Hybrid keyword + semantic retrieval
- Streaming responses
- Multi-LLM support
- Memory visualization dashboard
- Memory analytics
- User memory editing
- Context compression
- Conversation summarization
- REST API endpoints
- Frontend dashboard

---

# 📊 Current Status

| Module | Status |
|---------|--------|
| Conversation Memory | ✅ Complete |
| Message Memory | ✅ Complete |
| Document Memory | ✅ Complete |
| Preference Memory | ✅ Complete |
| Embedding Manager | ✅ Complete |
| ChromaDB Integration | ✅ Complete |
| Context Optimizer | ✅ Complete |
| Unified Context Manager | ✅ Complete |
| Memory Selector | ✅ Complete |
| Context Builder | ✅ Complete |
| Gemini Integration | ✅ Complete |
| Memory Engine Refactor | ✅ Complete |
| Duplicate Removal | 🚧 In Progress |
| Long-Term Memory | ⏳ Planned |
| Memory Dashboard | ⏳ Planned |

---

# 🎯 Vision

The goal of this project is to build a reusable Context Memory Engine that allows LLM-powered applications to maintain persistent, relevant, and personalized memory across long conversations while remaining modular enough to integrate with different AI models and applications.

---

# 👨‍💻 Author

**Srikanth NAS**

Information Science & Engineering

AI • LLMs • Full Stack Development • Data Science
