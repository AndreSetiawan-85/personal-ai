import sqlite3
from datetime import datetime

DB_PATH = "personal_ai.db"

class MemoryService:
    def __init__(self):
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            tags TEXT DEFAULT '',
            importance INTEGER DEFAULT 5,
            confidence REAL DEFAULT 0.8,
            status TEXT DEFAULT 'active',
            created_at TEXT,
            last_accessed_at TEXT,
            access_count INTEGER DEFAULT 0
        )
        """)
        conn.commit()
        conn.close()

    def save_memory(self, content, tags=None, importance=5, confidence=0.8):
        if tags is None:
            tags = []

        now = datetime.now().isoformat()

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO memories(
                content,
                tags,
                importance,
                confidence,
                status,
                created_at,
                last_accessed_at,
                access_count
            )
            VALUES(?,?,?,?,?,?,?,?)
            """,
            (
                content,
                ",".join(tags),
                importance,
                confidence,
                "active",
                now,
                now,
                0
            )
        )
        conn.commit()
        conn.close()

    def get_memories(self, limit=100):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                content,
                tags,
                importance,
                confidence,
                status,
                created_at,
                last_accessed_at,
                access_count
            FROM memories
            WHERE status='active'
            LIMIT ?
            """,
            (limit,)
        )

        rows = cursor.fetchall()
        conn.close()

        memories = []

        for row in rows:
            tags = []

            if row[2]:
                tags = [
                    tag.strip()
                    for tag in row[2].split(",")
                    if tag.strip()
                ]

            memories.append({
                "id": row[0],
                "content": row[1],
                "tags": tags,
                "importance": row[3],
                "confidence": row[4],
                "status": row[5],
                "created_at": row[6],
                "last_accessed_at": row[7],
                "access_count": row[8]
            })

        return memories

    def touch_memory(self, memory_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE memories
            SET
                access_count = access_count + 1,
                last_accessed_at = ?
            WHERE id = ?
            """,
            (
                datetime.now().isoformat(),
                memory_id
            )
        )

        conn.commit()
        conn.close()

    def archive_memory(self, memory_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE memories
            SET status='archived'
            WHERE id=?
            """,
            (memory_id,)
        )

        conn.commit()
        conn.close()

    def delete_memory(self, memory_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM memories
            WHERE id=?
            """,
            (memory_id,)
        )

        conn.commit()
        conn.close()

memory_service = MemoryService()