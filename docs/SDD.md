# Software Design Document (SDD)

## Project Name

Context Memory Engine (CME)

---

## Project Description

Context Memory Engine (CME) is an LLM-independent middleware that enhances interactions with Large Language Models by maintaining persistent context across conversations.

Instead of directly sending prompts to an LLM, CME retrieves relevant information from previous conversations, user preferences, and uploaded documents, builds an enriched prompt, and forwards it to the selected LLM.

The system is designed to support multiple LLM providers without changing the core memory engine.

---

## Technology Stack

### Frontend
- React
- Vite

### Backend
- FastAPI

### Database
- SQLite
- SQLAlchemy

### Future Technologies
- FAISS
- OpenAI API
- Anthropic API
- Google Gemini API
- Ollama

---

## Current Development Phase

**Phase 1 – Project Initialization**

Completed:
- React setup
- FastAPI setup
- Backend folder structure
- Working backend APIs

Next:
- Database layer