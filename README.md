# Personal AI Agent

Personal AI Agent adalah aplikasi AI chat berbasis web dengan arsitektur:

* Frontend: Next.js
* Backend: FastAPI
* AI Engine: Ollama
* Database: SQLite

Project ini dibangun bertahap menuju personal AI assistant yang memiliki memory, context, dan kemampuan menjalankan task.

---

# Project Structure

personal-ai/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── services/
│   │   ├── database.py
│   │   └── main.py
│   └── venv/
│
└── frontend/
    ├── app/
    ├── public/
    └── package.json

---

# Current Features

## Chat with AI

Backend menyediakan:

POST /chat

Untuk mengirim pesan ke AI dan mendapatkan response.

Contoh:

bash
curl -X POST http://localhost:8000/chat \
-H "Content-Type: application/json" \
-d '{"message":"Hello"}'

---

## Streaming Response

Endpoint:

POST /chat/stream

Response AI dikirim secara streaming sehingga frontend dapat menampilkan jawaban secara bertahap.

Frontend menggunakan:

* ReadableStream
* response.body.getReader()

---

## Chat Persistence

Chat history disimpan menggunakan SQLite.

Database:

personal_ai.db

Table:

messages

Schema:

| Column     | Type     |
| ---------- | -------- |
| id         | Integer  |
| role       | String   |
| content    | Text     |
| created_at | DateTime |

Role yang disimpan:

user
assistant

---

## Chat History

Endpoint:

GET /chat/history

Mengambil seluruh percakapan dari database.

Contoh:

bash
curl http://localhost:8000/chat/history

Response:

json[
  {
    "role": "user",
    "content": "Hello"
  },
  {
    "role": "assistant",
    "content": "Hello! How can I assist you?"
  }
]

---

# Frontend Features

Frontend sudah mendukung:

* Chat interface
* Loading state
* Streaming AI response
* Conversation history loading
* Chat bubble UI

---

# Development Setup

## Backend

Masuk folder:

bash
cd backend

Aktifkan virtual environment:

bash
source venv/bin/activate

Run server:

bash
uvicorn app.main:app --reload

Backend berjalan di:

http://localhost:8000

---

## Frontend

Masuk folder:

bash
cd frontend

Install dependency:

bash
npm install

Run:

bash
npm run dev

Frontend berjalan di:

http://localhost:3000

---

# Development Progress

## Phase 1 — Setup

Completed:

* Project structure
* FastAPI setup
* Next.js setup
* Virtual environment

Status:

✅ Done

---

## Phase 2 — AI Chat

Completed:

* FastAPI API
* Ollama integration
* Basic chat endpoint

Status:

✅ Done

---

## Phase 3 — Streaming & Persistence

Completed:

* Streaming AI response
* SQLite database
* Message model
* Save user messages
* Save assistant messages

Status:

✅ Done

---

## Phase 4 — Chat History UI

Completed:

* History endpoint
* Load previous conversations
* Chat message UI
* Streaming chat display

Status:

✅ Done

---

# Next Development Phase

## Phase 5 — AI Memory & Context

Target:

AI tidak hanya menyimpan history, tetapi menggunakan history sebagai context ketika menjawab.

Example:

User:
Nama saya Andre

AI:
Baik, saya ingat.

User:
Siapa nama saya?

AI:
Nama Anda Andre.

Planned improvements:

* Retrieve previous messages
* Build conversation context
* Send context ke Ollama
* Improve memory behavior

---

# Git History

Current milestones:

401ed62 feat: add chat message persistence with sqlite

943d6a3 feat: add chat history endpoint

f6aeb2d fix: handle text streaming response in frontend

---

# Future Roadmap

Planned features:

* Long-term memory
* Personal knowledge base
* Document upload
* RAG system
* Tool execution
* Autonomous workflows
* Personal assistant capabilities
