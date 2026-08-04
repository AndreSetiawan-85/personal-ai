# Personal AI - Project Context

## Project Overview

**Project Name:** Personal AI

**Goal:**
Build a private AI workspace that helps manage knowledge, projects, planning, notes, and daily tasks using multiple AI agents.

This project is designed to run primarily on a local machine and later be deployable for trusted users.

---

# Tech Stack

## Frontend

* Next.js
* TypeScript
* React

## Backend

* FastAPI
* Python

## AI

* Ollama
* Qwen3:8B (Local LLM)

## Planned

* PostgreSQL
* Qdrant
* n8n
* Docker
* Authentication

---

# Development Principles

## Language

* UI: English
* Source Code: English
* Database: English
* API: English
* Documentation: English

Communication with ChatGPT may be in Indonesian.

---

# Git Convention

Conventional Commits

Examples:

* feat:
* fix:
* refactor:
* docs:
* chore:
* style:
* test:

Semantic Versioning

Current Version:

v0.1.0

---

# Completed

✅ GitHub Repository

✅ Next.js Frontend

✅ FastAPI Backend

✅ FastAPI ↔ Next.js Communication

✅ Ollama Installed

✅ Qwen3:8B Installed

✅ Local AI Chat

✅ CORS Configuration

---

# Current Architecture

Browser

↓

Next.js

↓

FastAPI

↓

Ollama

↓

Qwen3:8B

---

# Current Phase

Phase 2

Professional Backend Architecture

---

# Next Tasks

1. Refactor backend structure.
2. Improve frontend chat interface.
3. Add streaming responses.
4. Integrate Qdrant.
5. Build memory system.
6. Implement multi-agent architecture.
7. Integrate n8n.
8. Deploy application.

---

# Coding Style

* Keep code clean and modular.
* Prefer services over large controller files.
* Keep business logic out of API routes.
* Write reusable components.
* Keep configuration inside dedicated config files.

---

# Long-Term Vision

Personal AI should become a complete private AI workspace with:

* Chat
* Knowledge Base
* Memory
* Planner
* Finance
* Projects
* Calendar
* Automation
* Multi-Agent System

The architecture should remain scalable and maintainable as new capabilities are added.
