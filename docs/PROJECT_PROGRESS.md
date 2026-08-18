PERSONAL AI ASSISTANT — PROJECT PROGRESS & DEVELOPMENT PLAN

PROJECT OVERVIEW

Project:
personal-ai

GitHub:
https://github.com/AndreSetiawan-85/personal-ai

Project ini akan dikembangkan menjadi aplikasi Personal AI Assistant yang dapat digunakan oleh banyak pengguna yang memiliki akses ke aplikasi.

Tujuan utama:
- Multi-user
- User memiliki conversation sendiri
- Conversation memiliki messages
- AI memiliki universal memory
- Memory tidak hard-coded satu per satu
- Tools tidak hard-coded satu per satu
- Sistem siap dikembangkan menjadi aplikasi yang benar-benar digunakan orang lain
- Architecture cukup rapi untuk capstone project
- Tidak menggunakan komentar/note berlebihan yang terlihat seperti AI-generated
- Jika comment diperlukan, gunakan bahasa Inggris
- Perubahan coding dilakukan satu file per step
- Setiap file diberikan dalam bentuk full coding
- Jangan memberikan banyak file sekaligus
- Jangan menjalankan migration/database destructive operation tanpa review terlebih dahulu

DEVELOPMENT PHILOSOPHY

MEMORY

Memory AI harus bersifat universal.

Tidak boleh menggunakan logic seperti:

if user_says_coffee:
    remember_coffee()

atau hard-coded rule satu per satu.

Memory harus menggunakan sistem yang dapat menangani berbagai jenis informasi tanpa developer mendefinisikan setiap jenis memory secara manual.

Target:

Conversation
    ↓
Memory extraction
    ↓
Memory representation
    ↓
Storage
    ↓
Retrieval
    ↓
Context injection

TOOLS

Tools juga tidak boleh hard-coded satu per satu.

Target architecture:

Tool Registry
    ↓
Tool Metadata
    ↓
Available Tools
    ↓
AI decides which tool to use
    ↓
Tool Execution

Bukan menggunakan banyak if/else seperti:

if user_asks_weather:
    weather()

if user_asks_search:
    search()

if user_asks_x:
    tool_x()

TECHNOLOGY STACK

Backend saat ini menggunakan:

Python
FastAPI
SQLAlchemy
SQLite
Alembic
Pydantic v2
pydantic-settings
Uvicorn

Important package versions:

fastapi==0.141.1
pydantic==2.13.4
pydantic_core==2.46.4
pydantic-settings==2.14.2
SQLAlchemy==2.0.51
alembic==1.18.5
uvicorn==0.52.1
hpack==4.2.0

Python environment:

Python 3.14

Virtual environment:

backend/venv/

AUDIT PROGRESS

Audit 1 — completed
Audit 2 — completed
Audit 3 — completed
Audit 4 — completed
Audit 5 — completed
Audit 6 — completed
Audit 7 — completed
Audit 8 — completed

IMPORTANT AUDIT DECISIONS

- Application akan menjadi multi-user.
- Memory harus universal dan tidak hard-coded.
- Tools harus dynamic dan tidak hard-coded.
- Existing functionality harus dipertahankan ketika melakukan perubahan.
- Jangan mengganti file existing dengan versi sederhana yang menghilangkan router atau fitur.
- Database lama harus dipertahankan.
- Existing memories dan messages tidak boleh hilang.

IMPLEMENTATION PROGRESS

Step 1 — completed
Initial model/database work dimulai.

Message model awal:

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

Step 2 — completed

Step 3 — completed

Step 4 — completed

Step 5 — completed

Step 6 — completed

Step 7 — backend startup testing completed.

CONFIGURATION PROBLEMS THAT WERE FIXED

DATABASE_URL

Encountered:

AttributeError: 'Settings' object has no attribute 'DATABASE_URL'

Configuration was updated.

PYDANTIC SETTINGS

Encountered:

No module named pydantic_settings

Then:

PydanticImportError:
BaseSettings has been moved to the pydantic-settings package.

Resolved by using pydantic-settings with Pydantic v2.

EMBED_MODEL_NAME

Encountered:

AttributeError: 'Settings' object has no attribute 'EMBED_MODEL_NAME'

Configuration was updated.

INIT_DB

Encountered:

ImportError: cannot import name 'init_db' from 'app.database'

init_db was restored/added.

STEP 8C

Step 8C completed successfully.

STEP 9 — REQUIREMENTS

backend/requirements.txt was updated.

Important dependencies:

alembic==1.18.5
pydantic-settings==2.14.2

There was an incorrect suggestion to use:

hpack==4.2.1

but pip showed that version was unavailable.

Correct version:

hpack==4.2.0

Step 9 completed successfully.

STEP 10 — MAIN.PY

Initially main.py was accidentally simplified and removed the existing chat router.

Swagger then only showed the root endpoint.

This was fixed.

Important existing code:

from app.api.chat import router as chat_router

and:

app.include_router(chat_router)

The model imports are also loaded:

from app.models import Conversation, Message, User

Swagger is working and chat endpoints are visible.

Step 10 completed successfully.

ALEMBIC SETUP

STEP 11

Created:

backend/alembic.ini

Step 11 completed.

STEP 12

Created:

backend/alembic/env.py

Important imports:

from app.models import Conversation, Message, User

Alembic metadata:

target_metadata = Base.metadata

Alembic gets the database URL from:

settings.DATABASE_URL

Step 12 completed.

STEP 13

Created:

backend/alembic/script.py.mako

Step 13 completed.

DATABASE INSPECTION

Database:

backend/personal_ai.db

Alembic successfully connected to SQLite.

Initially:

alembic current

showed no migration revision.

STEP 15 — BASELINE

Created:

backend/alembic/versions/ab1a31523017_baseline.py

Revision:

ab1a31523017

Then executed:

alembic stamp ab1a31523017

No existing application data was deleted.

STEP 16

Confirmed:

ab1a31523017 (head)

Current database baseline is:

ab1a31523017

AUTOGENERATED MIGRATION

Command:

alembic revision --autogenerate -m "add user conversations and message relationships"

Generated:

backend/alembic/versions/cdad530a1797_add_user_conversations_and_message_.py

Revision:

cdad530a1797

Parent:

ab1a31523017

IMPORTANT PROBLEMS FOUND

Autogenerate detected:

Detected removed table 'memories'

This was dangerous because memories still contains data.

The generated migration originally contained:

op.drop_table('memories')

This must NOT happen.

Autogenerate also detected:

messages.user_id
messages.conversation_id

These changes are expected.

However it also attempted:

conversation_id nullable=False

This is unsafe because there are already 14 existing messages without conversation_id.

It also attempted to change created_at to NOT NULL, which is unnecessary for this migration.

CURRENT SAFE MIGRATION

The autogenerated migration was replaced with:

"""add user conversations and message relationships

Revision ID: cdad530a1797
Revises: ab1a31523017
Create Date: 2026-08-18 14:48:11.525845
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "cdad530a1797"
down_revision: Union[str, Sequence[str], None] = "ab1a31523017"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("messages", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "user_id",
                sa.Integer(),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "conversation_id",
                sa.Integer(),
                nullable=True,
            )
        )
        batch_op.create_index(
            "ix_messages_user_id",
            ["user_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_messages_conversation_id",
            ["conversation_id"],
            unique=False,
        )
        batch_op.create_foreign_key(
            "fk_messages_conversation_id",
            "conversations",
            ["conversation_id"],
            ["id"],
            ondelete="CASCADE",
        )


def downgrade() -> None:
    with op.batch_alter_table("messages", schema=None) as batch_op:
        batch_op.drop_constraint(
            "fk_messages_conversation_id",
            type_="foreignkey",
        )
        batch_op.drop_index("ix_messages_conversation_id")
        batch_op.drop_index("ix_messages_user_id")
        batch_op.drop_column("conversation_id")
        batch_op.drop_column("user_id")

IMPORTANT:
This migration has NOT been executed yet.

CURRENT DATABASE STATE

Database inspection showed:

users = 0
conversations = 0
messages = 14
memories = 3

Tables:

alembic_version
conversations
memories
messages
users

Therefore:

14 existing messages
3 existing memories
0 users
0 conversations

CURRENT MESSAGE DATA

Existing messages are one chronological sequence:

1 | user
2 | assistant
3 | user
4 | assistant
5 | user
6 | assistant
7 | user
8 | assistant
9 | user
10 | assistant
11 | user
12 | assistant
13 | user
14 | assistant

They represent an existing conversation.

Messages currently do not have conversation_id in the old schema.

CURRENT DATABASE SAFETY STATUS

IMPORTANT:

Do NOT run:

alembic upgrade head

until the migration/data strategy is confirmed.

The database currently still contains:

14 messages
3 memories

and no users/conversations.

NEXT IMMEDIATE STEP

Inspect existing memories.

Run:

sqlite3 personal_ai.db

Then:

SELECT * FROM memories;

Then:

.quit

Send the result.

If memory content contains sensitive information, redact the content before sending.

The main things we need to understand are:

- columns
- IDs
- structure
- relationships to messages/users
- existing metadata
- embedding storage

NEXT DEVELOPMENT ROADMAP

STEP 17D — MEMORY INSPECTION

Inspect existing memory records.

Goal:

Understand existing memory architecture before changing it.

STEP 18 — SAFE SCHEMA MIGRATION

Apply safe schema migration.

Expected additions:

messages.user_id
messages.conversation_id

Initially nullable.

Do NOT delete memories.

STEP 19 — DATA OWNERSHIP

Because:

users = 0
conversations = 0

we need a deliberate strategy for old data.

Do not silently create fake users or fake credentials.

STEP 20 — BACKFILL OLD MESSAGES

Conceptually:

14 old messages
    ↓
legacy conversation
    ↓
conversation_id assigned

Exact implementation depends on the existing user/memory architecture.

STEP 21 — VERIFY MIGRATION

Check:

SELECT COUNT(*) FROM messages;

Expected:

14

Check:

SELECT COUNT(*) FROM messages
WHERE conversation_id IS NULL;

Eventually expected:

0

STEP 22 — ENFORCE NOT NULL

Only after all existing messages have valid conversation IDs should conversation_id become NOT NULL.

AUTHENTICATION PHASE

After database architecture is stable:

- User registration
- User login
- Password hashing
- JWT/session authentication
- Authenticated API requests

Users must not be able to access another user's:

- conversations
- messages
- memories

MULTI-USER ISOLATION

Target:

User A
 ├── Conversation 1
 ├── Conversation 2
 └── Memories

User B
 ├── Conversation 1
 ├── Conversation 2
 └── Memories

Every authenticated query must be scoped by the current user.

MEMORY SYSTEM

The current memories table contains 3 records.

Memory must become universal.

It should be able to represent:

- preferences
- facts
- habits
- goals
- relationships
- projects
- context
- corrections
- temporal information

without developer manually defining each memory type.

Target memory pipeline:

New message
    ↓
Memory candidate extraction
    ↓
Validation
    ↓
Deduplication
    ↓
Importance/confidence
    ↓
Embedding
    ↓
Storage
    ↓
Retrieval
    ↓
Context injection

Memory lifecycle should eventually support:

- new memory
- updated memory
- superseded memory
- deleted/inactive memory
- confidence
- importance
- last accessed
- access count

TOOL SYSTEM

Tools must be dynamic.

Target:

Tool Registry
    ↓
Tool definitions
    ↓
Tool metadata/schema
    ↓
LLM tool selection
    ↓
Tool execution

Adding a new tool should ideally only require registering the tool rather than editing many if/else statements.

CHAT ARCHITECTURE

Expected final flow:

User
 ↓
API
 ↓
Authentication
 ↓
Conversation
 ↓
Message
 ↓
Memory retrieval
 ↓
Tool selection
 ↓
LLM
 ↓
Response
 ↓
Save message
 ↓
Memory extraction
 ↓
Memory update

CONVERSATION ARCHITECTURE

Target:

User
 └── Conversations
      └── Messages

Conversation should eventually contain:

id
user_id
title
created_at
updated_at

Potential future fields only if needed:

archived
system_prompt
metadata

API ARCHITECTURE

Expected eventual structure:

app/
├── api/
│   ├── auth.py
│   ├── chat.py
│   ├── conversations.py
│   ├── memories.py
│   └── users.py
│
├── core/
│   ├── config.py
│   ├── security.py
│   └── dependencies.py
│
├── models/
│   ├── user.py
│   ├── conversation.py
│   ├── message.py
│   └── memory.py
│
├── schemas/
│   ├── auth.py
│   ├── chat.py
│   ├── conversation.py
│   ├── message.py
│   └── memory.py
│
├── services/
│   ├── chat_service.py
│   ├── memory_service.py
│   ├── tool_service.py
│   └── ...
│
└── main.py

Do not blindly create or replace this structure. Follow the existing repository and modify it incrementally.

DATABASE MIGRATION STRATEGY

Current development database:

SQLite

Migration:

Alembic

Potential production database later:

PostgreSQL

Do not migrate to PostgreSQL prematurely.

First stabilize:

models
relationships
authentication
memory
tools
API

TESTING PHASE

Unit tests should eventually cover:

- authentication
- memory extraction
- memory retrieval
- tool registry
- conversation ownership
- message ownership

Integration tests:

- register
- login
- create conversation
- send message
- retrieve conversation
- retrieve memory
- use tool

Security tests:

- User A cannot access User B data

FRONTEND PHASE

After backend API stabilizes:

- Login
- Register
- Conversation sidebar
- Chat interface
- Message history
- Memory-aware responses
- Tool activity
- Settings

PRODUCTION READINESS

Eventually:

- Environment variables
- Secrets management
- Production database
- Logging
- Error handling
- Rate limiting
- CORS
- Authentication security
- Database backups
- Migration strategy
- Docker
- Deployment

RULES FOR FUTURE CHATGPT SESSIONS

If this project is continued in a new ChatGPT tab, tell ChatGPT:

"This is an ongoing capstone project. Read the project progress document first. Continue from the current step instead of restarting the audit. Modify only one file per step. Always provide the full contents of the file. Do not provide multiple files at once unless explicitly requested. Do not run destructive database operations without reviewing them first. Existing memory and message data must be preserved. Tools and memory must remain dynamic and not hard-coded."

CURRENT EXACT POSITION

AUDIT
Audit 1 — completed
Audit 2 — completed
Audit 3 — completed
Audit 4 — completed
Audit 5 — completed
Audit 6 — completed
Audit 7 — completed
Audit 8 — completed

IMPLEMENTATION
Step 1 — completed
Step 2 — completed
Step 3 — completed
Step 4 — completed
Step 5 — completed
Step 6 — completed
Step 7 — completed
Step 8C — completed
Step 9 — completed
Step 10 — completed
Step 11 — completed
Step 12 — completed
Step 13 — completed
Step 14 — completed
Step 15 — completed
Step 16 — completed
Step 17 — in progress
Step 17A — migration audited
Step 17B — migration revised
Step 17C — existing messages inspected
Step 17D — pending memory inspection

DATABASE
users = 0
conversations = 0
messages = 14
memories = 3
alembic_version = ab1a31523017

MIGRATION
baseline = ab1a31523017
pending migration = cdad530a1797

IMMEDIATE NEXT ACTION

Do NOT run:

alembic upgrade head

First run:

sqlite3 personal_ai.db

Then:

SELECT * FROM memories;

Then:

.quit

Send the result to ChatGPT.

The next step is Step 17D.