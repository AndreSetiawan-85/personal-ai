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
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            message TEXT,
            created_at TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE,
            value TEXT,
            created_at TEXT
        )
        """)

        conn.commit()
        conn.close()

    def save(self, role: str, message: str):

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO conversations(
                role,
                message,
                created_at
            )
            VALUES (?, ?, ?)
            """,
            (
                role,
                message,
                datetime.now().isoformat(),
            ),
        )

        conn.commit()
        conn.close()

    def get_recent(self, limit: int = 10):

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT role, message
            FROM conversations
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        )

        rows = cursor.fetchall()

        conn.close()

        rows.reverse()

        return [
            {
                "role": row[0],
                "message": row[1],
            }
            for row in rows
        ]

    def save_memory(
        self,
        key: str,
        value: str
    ):

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO memories(
                key,
                value,
                created_at
            )
            VALUES (?, ?, ?)

            ON CONFLICT(key)
            DO UPDATE SET
            value=excluded.value
            """,
            (
                key,
                value,
                datetime.now().isoformat(),
            ),
        )

        conn.commit()
        conn.close()

    def get_memories(self):

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT key, value
            FROM memories
            """
        )

        rows = cursor.fetchall()

        conn.close()

        return {
            row[0]: row[1]
            for row in rows
        }


memory_service = MemoryService()