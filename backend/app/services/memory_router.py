from app.services.ollama import ollama_service
from app.services.memory_parser import memory_parser


class MemoryRouter:

    def route(self, message):

        if not message or not message.strip():
            return {
                "need_memory": False,
                "search_context": ""
            }

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

Jika pertanyaan membahas user sendiri, gunakan memory.

Contoh membutuhkan memory:

"Apa proyek saya?"
"Apa yang sedang saya kerjakan?"
"Apa yang saya suka?"
"Bagaimana kebiasaan saya?"
"Siapa nama saya?"

Contoh tidak membutuhkan memory:

"Berapa 10 + 10?"
"Apa itu Python?"
"Jelaskan FastAPI"

Balas HANYA JSON.

Format:

[
{{
"need_memory": true,
"search_context": "kategori informasi yang dicari"
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

                    msg = message.lower()

                    if (
                        "proyek" in msg
                        or "project" in msg
                        or "kerja" in msg
                        or "pekerjaan" in msg
                        or "sedang membuat" in msg
                    ):
                        data["search_context"] = (
                            "project proyek "
                            "AI software FastAPI pekerjaan"
                        )

                    elif (
                        "kebiasaan" in msg
                        or "habit" in msg
                        or "fokus" in msg
                        or "rutinitas" in msg
                    ):
                        data["search_context"] = (
                            "habit kebiasaan "
                            "productivity work"
                        )

                    elif (
                        "nama" in msg
                        or "siapa saya" in msg
                    ):
                        data["search_context"] = (
                            "identity nama user"
                        )

                    elif (
                        "suka" in msg
                        or "favorit" in msg
                        or "preferensi" in msg
                    ):
                        data["search_context"] = (
                            "preference favorit suka"
                        )

                    else:
                        search_context = data.get(
                            "search_context",
                            ""
                        ).strip()

                        if not search_context:
                            search_context = message

                        data["search_context"] = search_context

                return data

        except Exception as e:
            print("Memory router error:", e)

        return {
            "need_memory": False,
            "search_context": ""
        }


memory_router = MemoryRouter()