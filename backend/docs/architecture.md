# Personal AI Architecture

## Current Architecture

User

↓

Next.js Frontend

↓

FastAPI Backend

↓

Ollama

↓

Qwen3:8B Local Model


---

# Future Architecture

User

↓

Next.js Application

↓

FastAPI API Layer

↓

Agent Orchestrator

↓

+----------------+
|                |
|    Memory      |
|                |
|    Tools       |
|                |
+----------------+

↓

PostgreSQL + Qdrant

↓

LLM (Ollama)


---

# Component Responsibilities

## Frontend

Technology:
- Next.js
- TypeScript
- React

Responsibilities:
- User interface
- Chat interaction
- Display AI responses
- Manage client-side state


---

## Backend

Technology:
- FastAPI
- Python

Responsibilities:
- API endpoints
- Business logic
- AI communication
- Database communication
- Agent execution


---

## AI Layer

Technology:
- Ollama
- Qwen3:8B

Responsibilities:
- Natural language understanding
- Response generation
- Reasoning
- Future tool calling


---

## Memory Layer

Planned:

Qdrant:
- Vector storage
- Semantic search
- Knowledge retrieval

PostgreSQL:
- Structured data
- User information
- Conversation history


---

# Design Principles

## Modular Architecture

Each component should have one clear responsibility.

Example:

API handles requests.

Services handle business logic.

Database layer handles storage.


---

## Local First

The system should prioritize:

- Privacy
- Offline capability
- User data ownership


---

## Scalable Design

The architecture should allow future additions:

- New agents
- New tools
- New integrations
- Multiple users


---

# Current Version

v0.1.0

Status:

Local AI Chat completed.


# Current Phase

v0.2.0

Professional Architecture Refactor