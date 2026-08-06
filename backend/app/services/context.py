from app.services.memory import memory_service

class ContextService:
    def build(self, message: str):
        memories = memory_service.get_memories()
        history = memory_service.get_recent(limit=10)

        memory_text = "Tidak ada memory."
        if memories:
            memory_text = "\n".join(
                [
                    f"{key}: {value}"
                    for key, value in memories.items()
                ]
            )

        history_text = "Tidak ada riwayat."
        if history:
            history_text = "\n".join(
                [
                    f"{item['role']}: {item['message']}"
                    for item in history
                ]
            )

        return f"""
Kamu adalah Gwen,
AI assistant pribadi.

Memory pengguna:
{memory_text}

Riwayat percakapan:
{history_text}

Pesan terbaru:
{message}
"""

context_service = ContextService()