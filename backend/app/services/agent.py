from app.tools import TOOLS
from app.services.ollama import ollama_service
from app.services.search_router import detect_search_type
from app.services.citation import format_citations
from app.services.context import context_service
from app.services.memory_extractor import memory_extractor


class AgentService:

    def __init__(self):
        self.tools = TOOLS

    def is_memory_statement(
        self,
        message: str
    ):

        patterns = [
            "nama saya",
            "saya suka",
            "saya bekerja sebagai",
            "saya tinggal",
            "saya adalah",
            "umur saya",
        ]

        text = message.lower()

        return any(
            pattern in text
            for pattern in patterns
        )

    def detect_tool(
        self,
        message: str
    ):

        if self.is_memory_statement(
            message
        ):
            return None

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
            "bagi",
        ]

        if any(
            word in text
            for word in calculator_words
        ):
            return "calculator"

        category = detect_search_type(
            message
        )

        if category != "general":
            return "web_search"

        return None

    def run(
        self,
        message: str
    ):

        memory_extractor.extract(
            message
        )

        tool_name = self.detect_tool(
            message
        )

        result = None
        citations = []
        category = None

        if not tool_name:

            prompt = context_service.build(
                message
            )

            return ollama_service.generate_response(
                prompt
            )

        tool = self.tools.get(
            tool_name
        )

        if not tool:

            prompt = context_service.build(
                message
            )

            return ollama_service.generate_response(
                prompt
            )

        if tool_name == "calculator":

            expression = (
                message.lower()
                .replace("berapa", "")
                .replace("hitung", "")
                .replace("hasil", "")
                .replace("adalah", "")
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
                message,
                category=category
            )

            citations = format_citations(
                result.get(
                    "results",
                    []
                )
            )

        context = context_service.build(
            message
        )

        prompt = f"""
{context}

Kategori:
{category}

Data hasil tool:
{result}

Informasi sumber:
{citations}

Instruksi:

- Kamu adalah Gwen, AI assistant pribadi.
- Gunakan memory pengguna jika relevan.
- Gunakan hasil tool jika tersedia.
- Jangan membuat informasi yang tidak ada.
- Jangan membuat URL atau sumber palsu.
- Jawab dengan bahasa Indonesia natural.
"""

        return ollama_service.generate_response(
            prompt
        )


agent_service = AgentService()