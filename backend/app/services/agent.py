from app.tools import TOOLS
from app.services.ollama import ollama_service
from app.services.search_router import detect_search_type
from app.services.citation import format_citations

class AgentService:
    def __init__(self):
        self.tools = TOOLS

    def detect_tool(
        self,
        message: str
    ):
        text = message.lower()

        calculator_words = [
            "+",
            "-",
            "*",
            "/",
            "berapa",
            "hitung",
            "kali",
            "tambah",
            "kurang",
            "bagi"
        ]

        if any(
            word in text
            for word in calculator_words
        ):
            return "calculator"

        category = detect_search_type(
            message
        )

        if category:
            return "web_search"

        return None

    def run(
        self,
        message: str
    ):
        tool_name = self.detect_tool(
            message
        )

        result = None
        citations = []
        category = None

        if not tool_name:
            return ollama_service.generate_response(
                message
            )

        tool = self.tools.get(
            tool_name
        )

        if not tool:
            return ollama_service.generate_response(
                message
            )

        if tool_name == "calculator":
            expression = (
                message.lower()
                .replace(
                    "berapa",
                    ""
                )
                .replace(
                    "hitung",
                    ""
                )
                .replace(
                    "hasil",
                    ""
                )
                .strip()
            )

            result = tool(
                expression
            )

        elif tool_name == "web_search":
            category = detect_search_type(
                message
            )

            result = tool(
                message
            )

            citations = format_citations(
                result.get(
                    "results",
                    []
                )
            )

        prompt = f"""
Kamu adalah Gwen,
AI assistant pribadi.

Pertanyaan user:
{message}

Kategori:
{category}

Data hasil pencarian:
{result}

Informasi sumber:
{citations}

Aturan:
- Jawab langsung.
- Jangan menyebut proses internal.
- Jangan mengatakan "saya mencari".
- Gunakan bahasa natural.
- Jika berita, tampilkan ringkasan.
- Jika ada sumber tampilkan:
  nama sumber,
  url,
  waktu pengecekan.
- Jangan membuat informasi tambahan yang tidak ada.
- Jangan mengulang kalimat penutup.
"""

        return ollama_service.generate_response(
            prompt
        )

agent_service = AgentService()