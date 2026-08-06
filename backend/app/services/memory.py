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
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            memory TEXT NOT NULL,
            category TEXT DEFAULT 'general',
            importance INTEGER DEFAULT 5,
            created_at TEXT
        )
        """)

        conn.commit()
        conn.close()

    def save_memory(
        self,
        memory,
        category="general",
        importance=5
    ):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO memories(
                memory,
                category,
                importance,
                created_at
            )
            VALUES(?,?,?,?)
            """,
            (
                memory,
                category,
                importance,
                datetime.now().isoformat()
            )
        )

        conn.commit()
        conn.close()

    def get_memories(
        self,
        limit=10
    ):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                memory,
                category,
                importance,
                created_at
            FROM memories
            ORDER BY importance DESC
            LIMIT ?
            """,
            (limit,)
        )

        rows = cursor.fetchall()

        conn.close()

        memories = []

        for row in rows:
            memories.append(
                {
                    "memory": row[0],
                    "category": row[1],
                    "importance": row[2],
                    "created_at": row[3]
                }
            )

        return memories

    def delete_memory(
        self,
        memory_id
    ):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM memories
            WHERE id = ?
            """,
            (memory_id,)
        )

        conn.commit()
        conn.close()


memory_service = MemoryService()