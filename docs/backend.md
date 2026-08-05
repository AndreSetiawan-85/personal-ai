# Backend Documentation

## Overview

The backend is responsible for handling API requests, business logic, AI communication, and future integrations.

Technology:

- Python
- FastAPI
- Uvicorn
- Ollama


---

# Current Architecture

Current flow:

User

↓

Next.js Frontend

↓

FastAPI Backend

↓

Ollama API

↓

Qwen3:8B


---

# Responsibilities

## API Layer

Location:

app/api/


Responsibilities:

- Receive HTTP requests
- Validate input
- Return responses
- Handle API routing


Example:

Chat endpoint:

POST /chat


Request:

{
  "message": "Hello"
}


Response:

{
  "reply": "Hello! How can I help you?"
}


---

## Service Layer

Location:

app/services/


Responsibilities:

- Handle business logic
- Communicate with external services
- Keep API routes clean


Current service:

Ollama Service


Future services:

- Memory Service
- Embedding Service
- Agent Service
- Notification Service


---

## Model Layer

Location:

app/models/


Responsibilities:

- Define request format
- Define response format
- Data validation


Technology:

Pydantic


---

## Core Layer

Location:

app/core/


Responsibilities:

- Application configuration
- Environment variables
- Security settings


Future:

- Authentication config
- Database config
- API keys


---

# Planned Backend Structure

backend/

app/

main.py

api/
- chat.py

services/
- ollama.py
- memory.py
- agents.py

models/
- chat.py
- user.py

core/
- config.py


---

# Development Rules

## Keep Routes Simple

API files should not contain complex logic.

Bad:

API route calls AI, database, and processing directly.


Good:

API route calls service.


Example:

API

↓

Service

↓

Database / AI


---

# Future Improvements

## Database

Add:

- PostgreSQL
- Conversation storage
- User management


## Memory

Add:

- Qdrant
- Embeddings
- Semantic search


## Agents

Add:

- Planner
- Tool execution
- Multi-agent workflow


---

# Current Status

Version:

v0.1.0


Completed:

- FastAPI setup
- Ollama integration
- Chat endpoint


Next:

- Backend refactoring
- Service separation
- Better architecture