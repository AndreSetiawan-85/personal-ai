from app.services.ollama import ollama_service
from app.services.memory_parser import memory_parser

class MemoryRouter:
    def route(self, message):
        if not message or not message.strip():
            return {"need_memory": False, "search_context": ""}

        prompt = f"""
Kamu adalah memory gate untuk AI assistant pribadi.

Tentukan apakah pertanyaan user membutuhkan akses ke long-term memory.

Long-term memory berisi:
- identitas user
- proyek user
- pekerjaan user
- kebiasaan user
- preferensi user
- hubungan user
- tujuan user
- pengalaman user sebelumnya

ATURAN:
Jika pertanyaan membahas user sendiri, selalu gunakan memory.

Contoh yang membutuhkan memory:
"Apa proyek saya?"
"Apa yang sedang saya kerjakan?"
"Apa yang saya suka?"
"Bagaimana kebiasaan saya?"
"Siapa nama saya?"

Contoh yang tidak membutuhkan memory:
"Berapa 10 + 10?"
"Apa itu Python?"
"Jelaskan FastAPI"

Balas HANYA JSON.

Format:
[
  {{
    "need_memory": true,
    "search_context": "informasi yang perlu dicari"
  }}
]

atau

[
  {{
    "need_memory": false,
    "search_context": ""
  }}
]

Pertanyaan user:
{message}
"""

        try:
            response = ollama_service.generate_response(prompt)
            result = memory_parser.parse(response)

            if result and isinstance(result[0], dict):
                data = result[0]

                if data.get("need_memory"):
                    data["search_context"] = (
                        data.get("search_context", "")
                        + " user project pekerjaan personal AI FastAPI"
                    )

            return data

        except Exception as e:
            print("Memory router error:", e)

        return {
            "need_memory": False,
            "search_context": ""
        }

memory_router = MemoryRouter()