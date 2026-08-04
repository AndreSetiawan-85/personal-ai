# Deployment Documentation

## Overview

Personal AI is designed as a local-first application.

The first version runs entirely on a personal computer.

Future versions can be deployed so trusted users can access the application remotely.

---

# Current Deployment

Status:

Local Development


Current environment:

Machine:

- Personal MacBook


Running services:

Frontend:

Next.js

Backend:

FastAPI

AI:

Ollama + Qwen3:8B


Architecture:

User

↓

Local Browser

↓

Next.js

↓

FastAPI

↓

Ollama

↓

Local AI Model

---

# Deployment Options

## Option 1 - Local Only

Purpose:

Personal private AI assistant.


Advantages:

- Maximum privacy
- No hosting cost
- Data stays on device
- Works without internet


Disadvantages:

- Only available on the local machine
- Other users cannot access it


Suitable for:

- Personal use
- Development
- Testing


---

# Option 2 - Private Network Deployment

Purpose:

Share Personal AI with trusted people in the same network.


Example:

Home network

Office network


Architecture:

User Device

↓

Local Network

↓

Personal AI Server


Requirements:

- Computer/server always running
- Network access
- Security configuration


---

# Option 3 - Cloud Deployment

Purpose:

Allow access from anywhere.


Possible architecture:


User

↓

Frontend Hosting

↓

Backend Server

↓

AI Service

↓

Database


---

# Frontend Deployment

Possible platform:

- Vercel
- Cloud hosting


Responsibilities:

- Host Next.js application
- Serve user interface
- Handle frontend assets


---

# Backend Deployment

Possible options:

- VPS
- Cloud server
- Container platform


Responsibilities:

- Run FastAPI
- Handle API requests
- Connect to AI services


---

# AI Model Deployment

Options:


## Option A

Run Ollama on the server.


Advantages:

- Full control
- Private
- Same local experience


Requirements:

- Server with enough resources
- GPU recommended for better speed


---

## Option B

Use External AI API.


Examples:

- Cloud LLM providers


Advantages:

- Easier deployment
- Less infrastructure


Disadvantages:

- External data processing
- Possible cost
- Less privacy


---

# Database Deployment

Future requirements:

## PostgreSQL

Used for:

- Users
- Conversations
- Settings
- Projects


Possible hosting:

- Managed database service
- Self-hosted database


---

## Qdrant

Used for:

- AI memory
- Semantic search
- Knowledge retrieval


Possible options:

- Self-hosted Qdrant
- Qdrant Cloud


---

# Security Requirements

Before sharing with other users:

Need to add:

## Authentication

Purpose:

Control who can access the application.


Examples:

- Login system
- User accounts
- Password protection


---

## Environment Variables

Sensitive information should not be stored in code.

Examples:

- API keys
- Database credentials
- Secret tokens


Use:

.env files


---

## API Protection

Required:

- Request validation
- Rate limiting
- Access control


---

# Sharing With Friends

Future scenario:

Friend accesses Personal AI from Jakarta.


Possible architecture:

Friend

↓

Web Browser

↓

Hosted Frontend

↓

Backend Server

↓

AI Model

↓

Database


Requirements:

- Public URL
- Authentication
- Secure backend
- Hosting infrastructure


---

# Recommended Deployment Path

Development:

Local Mac

↓

Testing:

Docker

↓

Private Use:

Personal server

↓

Sharing:

Cloud deployment


---

# Current Status

Version:

v0.1.0


Completed:

- Local deployment
- Local AI model
- Local frontend and backend


Future:

- Docker setup
- Authentication
- Cloud deployment
- Multi-user support