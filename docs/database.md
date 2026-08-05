# Database Documentation

## Overview

The database layer will store application data, user information, conversations, and AI memory.

Currently:

No database has been implemented yet.

The current version does not store permanent data.

---

# Database Strategy

Personal AI will use two types of databases:

1. Relational Database
2. Vector Database

Each database has a different purpose.

---

# PostgreSQL

## Purpose

Store structured application data.

Technology:

- PostgreSQL
- SQLAlchemy (planned)
- Alembic migrations (planned)

---

## PostgreSQL Responsibilities

Will store:

### Users

Examples:

- User profile
- Preferences
- Settings


### Conversations

Examples:

- Chat sessions
- Messages
- Timestamps


### Projects

Examples:

- Project information
- Tasks
- Status


### Application Data

Examples:

- Configuration
- User preferences
- System settings

---

# Planned PostgreSQL Tables

## users

Fields:

- id
- name
- email
- created_at


## conversations

Fields:

- id
- user_id
- title
- created_at


## messages

Fields:

- id
- conversation_id
- role
- content
- created_at


## projects

Fields:

- id
- user_id
- name
- status
- created_at

---

# Qdrant

## Purpose

Store AI memory and perform semantic search.

Technology:

- Qdrant
- Vector embeddings

---

# Why Qdrant?

Traditional databases search using exact values.

Example:

User searches:

"marketing meeting"

A normal database looks for matching words.

---

Vector databases search based on meaning.

Example:

Stored information:

"Discussed campaign strategy with the marketing team."

Query:

"marketing meeting"

AI can understand that both are related.

---

# Qdrant Responsibilities

Will store:

- Long-term memory
- Document embeddings
- Knowledge base
- Personal notes
- Important conversations

---

# Memory Flow

Future architecture:

User message

↓

Create embedding

↓

Search Qdrant

↓

Retrieve relevant memories

↓

Send context to LLM

↓

Generate response

---

# Embedding Model

Possible options:

Local models:

- nomic-embed-text
- mxbai-embed-large

---

# Data Privacy Principles

Personal AI follows:

- User owns the data
- Local-first approach
- Minimize external storage
- Protect credentials

---

# Future Database Architecture

Personal AI

↓

FastAPI Backend

↓

Two storage systems:

1. PostgreSQL

Purpose:
- Users
- Conversations
- Settings
- Projects


2. Qdrant

Purpose:
- AI Memory
- Knowledge Search
- Document Retrieval

---

# Current Status

Version:

v0.1.0

Completed:

- No database yet
- Local AI chat working

Next:

- Add PostgreSQL
- Store conversations
- Add Qdrant memory system