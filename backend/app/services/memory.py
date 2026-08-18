import json
import sqlite3
from datetime import datetime

DB_PATH = "personal_ai.db"


class MemoryService:
    def __init__(self):
        self.init_db()

    def _connect(self):
        return sqlite3.connect(DB_PATH)

    def init_db(self):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS memories(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                content TEXT NOT NULL,
                embedding TEXT,
                tags TEXT DEFAULT '',
                importance INTEGER DEFAULT 5,
                confidence REAL DEFAULT 0.8,
                status TEXT DEFAULT 'active',
                source TEXT DEFAULT 'conversation',
                superseded_id INTEGER,
                created_at TEXT,
                updated_at TEXT,
                last_accessed_at TEXT,
                access_count INTEGER DEFAULT 0
            )
            """
        )

        cursor.execute("PRAGMA table_info(memories)")
        existing_cols = {row[1] for row in cursor.fetchall()}

        migrations = {
            "user_id": "ALTER TABLE memories ADD COLUMN user_id INTEGER",
            "embedding": "ALTER TABLE memories ADD COLUMN embedding TEXT",
            "superseded_id": "ALTER TABLE memories ADD COLUMN superseded_id INTEGER",
            "updated_at": "ALTER TABLE memories ADD COLUMN updated_at TEXT",
            "source": "ALTER TABLE memories ADD COLUMN source TEXT DEFAULT 'conversation'",
        }

        for col, ddl in migrations.items():
            if col not in existing_cols:
                cursor.execute(ddl)

        conn.commit()
        conn.close()

    def save_memory(
        self,
        content,
        user_id=None,
        embedding=None,
        tags=None,
        importance=5,
        confidence=0.8,
        source="conversation",
    ):
        if tags is None:
            tags = []

        conn = self._connect()
        cursor = conn.cursor()

        if user_id is None:
            cursor.execute(
                """
                SELECT id
                FROM memories
                WHERE user_id IS NULL
                  AND content = ?
                  AND status = 'active'
                """,
                (content,),
            )
        else:
            cursor.execute(
                """
                SELECT id
                FROM memories
                WHERE user_id = ?
                  AND content = ?
                  AND status = 'active'
                """,
                (user_id, content),
            )

        if cursor.fetchone():
            conn.close()
            return None

        now = datetime.now().isoformat()
        embedding_json = json.dumps(embedding) if embedding is not None else None

        cursor.execute(
            """
            INSERT INTO memories(
                user_id,
                content,
                embedding,
                tags,
                importance,
                confidence,
                status,
                source,
                created_at,
                updated_at,
                last_accessed_at,
                access_count
            )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                user_id,
                content,
                embedding_json,
                ",".join(tags),
                importance,
                confidence,
                "active",
                source,
                now,
                now,
                now,
                0,
            ),
        )

        conn.commit()
        new_id = cursor.lastrowid
        conn.close()

        return new_id

    def get_memories(self, user_id=None, status="active", limit=1000):
        conn = self._connect()
        cursor = conn.cursor()

        if user_id is None:
            cursor.execute(
                """
                SELECT
                    id,
                    user_id,
                    content,
                    embedding,
                    tags,
                    importance,
                    confidence,
                    status,
                    source,
                    superseded_id,
                    created_at,
                    updated_at,
                    last_accessed_at,
                    access_count
                FROM memories
                WHERE user_id IS NULL
                  AND status = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (status, limit),
            )
        else:
            cursor.execute(
                """
                SELECT
                    id,
                    user_id,
                    content,
                    embedding,
                    tags,
                    importance,
                    confidence,
                    status,
                    source,
                    superseded_id,
                    created_at,
                    updated_at,
                    last_accessed_at,
                    access_count
                FROM memories
                WHERE user_id = ?
                  AND status = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (user_id, status, limit),
            )

        rows = cursor.fetchall()
        conn.close()

        return [self._row_to_dict(row) for row in rows]

    def get_all_active_with_embeddings(self, user_id=None):
        memories = self.get_memories(
            user_id=user_id,
            status="active",
            limit=5000,
        )

        return [
            memory
            for memory in memories
            if memory["embedding"] is not None
        ]

    def _row_to_dict(self, row):
        tags = [
            tag.strip()
            for tag in (row[4] or "").split(",")
            if tag.strip()
        ]

        embedding = json.loads(row[3]) if row[3] else None

        return {
            "id": row[0],
            "user_id": row[1],
            "content": row[2],
            "embedding": embedding,
            "tags": tags,
            "importance": row[5],
            "confidence": row[6],
            "status": row[7],
            "source": row[8],
            "superseded_id": row[9],
            "created_at": row[10],
            "updated_at": row[11],
            "last_accessed_at": row[12],
            "access_count": row[13],
        }

    def touch_memory(self, memory_id, user_id=None):
        conn = self._connect()
        cursor = conn.cursor()

        if user_id is None:
            cursor.execute(
                """
                UPDATE memories
                SET access_count = access_count + 1,
                    last_accessed_at = ?
                WHERE id = ?
                  AND user_id IS NULL
                """,
                (datetime.now().isoformat(), memory_id),
            )
        else:
            cursor.execute(
                """
                UPDATE memories
                SET access_count = access_count + 1,
                    last_accessed_at = ?
                WHERE id = ?
                  AND user_id = ?
                """,
                (datetime.now().isoformat(), memory_id, user_id),
            )

        conn.commit()
        conn.close()

    def supersede_memory(self, old_id, new_id, user_id=None):
        conn = self._connect()
        cursor = conn.cursor()

        if user_id is None:
            cursor.execute(
                """
                UPDATE memories
                SET status = 'superseded',
                    supersedes_id = ?,
                    updated_at = ?
                WHERE id = ?
                  AND user_id IS NULL
                """,
                (new_id, datetime.now().isoformat(), old_id),
            )
        else:
            cursor.execute(
                """
                UPDATE memories
                SET status = 'superseded',
                    supersedes_id = ?,
                    updated_at = ?
                WHERE id = ?
                  AND user_id = ?
                """,
                (
                    new_id,
                    datetime.now().isoformat(),
                    old_id,
                    user_id,
                ),
            )

        conn.commit()
        conn.close()

    def archive_memory(self, memory_id, user_id=None):
        conn = self._connect()
        cursor = conn.cursor()

        if user_id is None:
            cursor.execute(
                """
                UPDATE memories
                SET status = 'archived',
                    updated_at = ?
                WHERE id = ?
                  AND user_id IS NULL
                """,
                (datetime.now().isoformat(), memory_id),
            )
        else:
            cursor.execute(
                """
                UPDATE memories
                SET status = 'archived',
                    updated_at = ?
                WHERE id = ?
                  AND user_id = ?
                """,
                (
                    datetime.now().isoformat(),
                    memory_id,
                    user_id,
                ),
            )

        conn.commit()
        conn.close()

    def update_confidence(self, memory_id, confidence, user_id=None):
        conn = self._connect()
        cursor = conn.cursor()

        if user_id is None:
            cursor.execute(
                """
                UPDATE memories
                SET confidence = ?,
                    updated_at = ?
                WHERE id = ?
                  AND user_id IS NULL
                """,
                (
                    confidence,
                    datetime.now().isoformat(),
                    memory_id,
                ),
            )
        else:
            cursor.execute(
                """
                UPDATE memories
                SET confidence = ?,
                    updated_at = ?
                WHERE id = ?
                  AND user_id = ?
                """,
                (
                    confidence,
                    datetime.now().isoformat(),
                    memory_id,
                    user_id,
                ),
            )

        conn.commit()
        conn.close()

    def delete_memory(self, memory_id, user_id=None):
        conn = self._connect()
        cursor = conn.cursor()

        if user_id is None:
            cursor.execute(
                """
                DELETE FROM memories
                WHERE id = ?
                  AND user_id IS NULL
                """,
                (memory_id,),
            )
        else:
            cursor.execute(
                """
                DELETE FROM memories
                WHERE id = ?
                  AND user_id = ?
                """,
                (memory_id, user_id),
            )

        conn.commit()
        conn.close()


memory_service = MemoryService()