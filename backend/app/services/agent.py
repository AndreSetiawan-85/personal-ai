from app.core.config import settings
from app.services.citation import format_citations
from app.services.context import context_service
from app.services.memory_engine import memory_engine
from app.services.memory_parser import memory_parser
from app.services.ollama import ollama_service
from app.tools.registry import discover_tools


class AgentService:
    def __init__(self):
        self.tools = discover_tools()

    def _select_tool(self, message):
        tool_names = self.tools.get_names()

        if not tool_names:
            return None, message

        prompt = f"""
Determine whether the user message requires one of the available tools.

Available tools:
{tool_names}

Return only a JSON object using this format:
{{
    "tool": null,
    "input": ""
}}

If a tool is needed, "tool" must contain exactly one name from the available tools.
If no tool is needed, use null.

The "input" field must contain the value that should be passed to the selected tool.

User message:
{message}
"""

        try:
            response = ollama_service.generate_response(prompt)
            data = memory_parser.parse_object(response)

            tool_name = data.get("tool")
            tool_input = data.get("input") or message

            if tool_name not in tool_names:
                return None, message

            return tool_name, tool_input

        except Exception as e:
            print("Tool selection error:", e)
            return None, message

    def _execute_tool(self, tool_name, tool_input):
        if not tool_name:
            return None, []

        tool = self.tools.get(tool_name)

        if not tool:
            return None, []

        try:
            result = tool(tool_input)

            citations = []

            if isinstance(result, dict):
                citations = format_citations(
                    result.get("results", [])
                )

            return result, citations

        except Exception as e:
            print("Tool execution error:", e)
            return None, []

    def run(self, user_id, message):
        if not message or not message.strip():
            return ""

        try:
            memory_decision = memory_engine.process(
                user_id=user_id,
                message=message,
            )
        except Exception as e:
            print("Memory engine error:", e)

            memory_decision = {
                "need_memory": False,
                "search_query": "",
            }

        user_context = ""

        if memory_decision.get("need_memory"):
            user_context = context_service.build_context(
                user_id=user_id,
                query=memory_decision.get(
                    "search_query",
                    message,
                ),
            )

        tool_name, tool_input = self._select_tool(message)

        result, citations = self._execute_tool(
            tool_name,
            tool_input,
        )

        prompt = f"""
You are a personal AI assistant.

Application:
{settings.APP_NAME}

User memory:
{user_context}

User message:
{message}

Tool result:
{result}

Sources:
{citations}

Instructions:
- Use relevant user memory when available.
- Treat user memory as information about the current user.
- Do not invent personal information about the user.
- Use tool results when they are available.
- Answer naturally and directly.
"""

        return ollama_service.generate_response(prompt)


agent_service = AgentService()