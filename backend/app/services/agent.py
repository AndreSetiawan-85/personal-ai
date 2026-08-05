from app.tools import TOOLS
from app.services.ollama import ollama_service
from app.services.streaming import StreamEvent


class AgentService:

    def __init__(self):
        self.tools = TOOLS


    def detect_tool(self, message: str):

        text = message.lower()


        math_symbols = [
            "+",
            "-",
            "*",
            "/",
        ]


        if any(
            symbol in text
            for symbol in math_symbols
        ):
            return "calculator"



        keywords = [
            "berita",
            "terbaru",
            "hari ini",
            "latest",
            "news",
            "update",
            "sekarang",
        ]


        if any(
            keyword in text
            for keyword in keywords
        ):
            return "web_search"



        return None



    def prepare_tool_result(
        self,
        message: str,
        tool_name: str
    ):

        tool = self.tools[tool_name]


        if tool_name == "calculator":

            expression = (
                message
                .lower()
                .replace("berapa", "")
                .replace("hitung", "")
                .replace("hasil", "")
                .strip()
            )

            return tool(expression)



        return tool(message)



    def build_prompt(
        self,
        message: str,
        tool_name: str,
        result
    ):

        return f"""
Kamu adalah Gwen, AI assistant.

User bertanya:
{message}


Tool yang digunakan:
{tool_name}


Hasil tool:
{result}


Jawab user dengan bahasa natural.
Jika ada sumber atau link, tampilkan sumbernya.
"""



    # ============================
    # Non streaming
    # ============================

    def run(
        self,
        message: str
    ):

        tool_name = self.detect_tool(message)


        if not tool_name:

            return ollama_service.generate_response(
                message
            )


        result = self.prepare_tool_result(
            message,
            tool_name
        )


        prompt = self.build_prompt(
            message,
            tool_name,
            result
        )


        return ollama_service.generate_response(
            prompt
        )



    # ============================
    # Streaming Agent
    # ============================

    def run_stream(
        self,
        message: str
    ):

        tool_name = self.detect_tool(message)



        if tool_name == "web_search":

            yield StreamEvent.status(
                "Searching web..."
            )


        elif tool_name == "calculator":

            yield StreamEvent.status(
                "Calculating..."
            )


        else:

            yield StreamEvent.status(
                "Thinking..."
            )



        if tool_name:

            result = self.prepare_tool_result(
                message,
                tool_name
            )


            prompt = self.build_prompt(
                message,
                tool_name,
                result
            )


        else:

            prompt = message



        yield StreamEvent.status(
            "Generating answer..."
        )



        for chunk in ollama_service.stream_response(
            prompt
        ):

            yield StreamEvent.chunk(
                chunk
            )



        yield StreamEvent.done()



agent_service = AgentService()