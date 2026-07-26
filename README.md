# Context Memory Engine (CME)

## An LLM-Independent Memory Middleware for Persistent Context Preservation

## 📖 Overview

Context Memory Engine (CME) is a full-stack web application that acts as an intelligent middleware between users and Large Language Models (LLMs). Instead of sending user prompts directly to an LLM, CME enriches every prompt with persistent context retrieved from previous conversations, user preferences, and uploaded documents.

The system is designed to be **LLM-independent**, allowing integration with multiple providers such as OpenAI, Anthropic, Google Gemini, and local models in the future.

---

## 🎯 Objectives

- Maintain long-term conversation memory
- Store and retrieve user preferences
- Support document-based contextual retrieval
- Build enriched prompts before sending them to an LLM
- Remain independent of any specific LLM provider

---

## 🛠️ Tech Stack

### Frontend
- React
- Vite

### Backend
- FastAPI
- Python

### Database
- SQLite
- SQLAlchemy *(Upcoming)*

### Future Integrations
- FAISS
- OpenAI
- Anthropic Claude
- Google Gemini
- Ollama

---

## 📂 Project Structure

```
Context-Memory-Engine/
│
├── backend/
├── frontend/
├── docs/
├── .gitignore
└── README.md
```

---

## 🚀 Current Status

### ✅ Phase 1 - Project Initialization

- React frontend created
- FastAPI backend created
- Backend folder structure organized
- Backend running successfully
- Health API implemented

---

## 🗺️ Roadmap

- Phase 1 — Project Initialization ✅
- Phase 2 — Database Layer
- Phase 3 — Context Memory Engine Core
- Phase 4 — Conversation Memory
- Phase 5 — Preference Memory
- Phase 6 — Document Memory
- Phase 7 — Semantic Search
- Phase 8 — LLM Integration
- Phase 9 — Frontend Dashboard
- Phase 10 — Testing & Deployment

---

## 👨‍💻 Author

Developed by **Srikanth NAS**
