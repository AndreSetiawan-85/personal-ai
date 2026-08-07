from app.tools import TOOLS
from app.services.ollama import ollama_service
from app.services.search_router import detect_search_type
from app.services.citation import format_citations
from app.services.memory_extractor import memory_extractor
from app.services.context import context_service
from app.services.memory_router import memory_router

class AgentService:
    def __init__(self):
        self.tools = TOOLS

    def detect_tool(self, message):
        text = message.lower()
        if any(x in text for x in ["+", "-", "*", "/", "berapa", "hitung", "kali", "tambah", "kurang", "bagi"]):
            return "calculator"
        if detect_search_type(message):
            return "web_search"
        return None

    def run(self, message):
        memory_decision = memory_router.route(message)
        user_context = ""

        if memory_decision.get("need_memory"):
            user_context = context_service.build_context(
                memory_decision.get("search_context", message)
            )
            memory_extractor.extract(message)

        tool_name = None
        result = None
        citations = []
        
        if not memory_decision.get("need_memory"):
            tool_name = self.detect_tool(message)

        if tool_name:
            tool = self.tools.get(tool_name)
            if tool:
                if tool_name == "calculator":
                    expression = message.lower().replace("berapa", "").replace("hitung", "").strip()
                    result = tool(expression)
                elif tool_name == "web_search":
                    result = tool(message)
                    if isinstance(result, dict):
                        citations = format_citations(result.get("results", []))

        prompt = f"""
Kamu adalah Gwen, AI assistant pribadi Andre.

INFORMASI MEMORY USER:
{user_context}

WAJIB:
- Gunakan informasi memory di atas sebagai fakta.
- Jika memory berisi nama user, gunakan nama tersebut.
- Jangan mengatakan tidak tahu nama user jika memory tersedia.
- Jangan meminta ulang informasi yang sudah ada.

PERTANYAAN USER:
{message}

HASIL TOOL:
{result}

SUMBER:
{citations}

Jawab singkat, natural, dan personal.
"""

        return ollama_service.generate_response(prompt)

agent_service = AgentService()