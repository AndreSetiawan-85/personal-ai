import json

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
        schemas = self.tools.get_schemas()

        if not schemas:
            return None, {}

        tool_schema_text = json.dumps(
            schemas,
            ensure_ascii=False,
            indent=2,
        )

        prompt = f"""
Determine whether the user message requires one of the available tools.

Available tools and their parameter schemas:
{tool_schema_text}

Return ONLY a valid JSON object using this format:

{{
    "tool": null,
    "arguments": {{}}
}}

If a tool is required:
- "tool" must contain exactly one available tool name.
- "arguments" must be a JSON object.
- The arguments must use the parameter names defined by that tool's schema.
- Do not invent parameter names.
- Do not include parameters that are not part of the selected tool schema.

If no tool is required:
- "tool" must be null.
- "arguments" must be an empty object.

User message:
{message}
"""

        try:
            response = ollama_service.generate_response(prompt)
            data = memory_parser.parse_object(response)

            if not isinstance(data, dict):
                return None, {}

            tool_name = data.get("tool")

            if not isinstance(tool_name, str):
                return None, {}

            tool_name = tool_name.strip()

            if not tool_name:
                return None, {}

            if tool_name not in schemas:
                return None, {}

            arguments = data.get("arguments", {})

            if not isinstance(arguments, dict):
                return None, {}

            return tool_name, arguments

        except Exception as e:
            print("Tool selection error:", e)
            return None, {}

    def _execute_tool(self, tool_name, arguments):
        if not tool_name:
            return None, []

        tool_definition = self.tools.get_definition(tool_name)

        if not tool_definition:
            return None, []

        if not isinstance(arguments, dict):
            return None, []

        try:
            result = tool_definition.function(
                **arguments
            )

            citations = []

            if isinstance(result, dict):
                citations = format_citations(
                    result.get("results", [])
                )

            return result, citations

        except Exception as e:
            print("Tool execution error:", e)

            return {
                "success": False,
                "error": str(e),
            }, []

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

        tool_name, arguments = self._select_tool(message)

        result, citations = self._execute_tool(
            tool_name,
            arguments,
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
- If a tool returned an error, explain the problem naturally.
- Use sources when they are available.
- Answer naturally and directly.
"""

        return ollama_service.generate_response(prompt)


agent_service = AgentService()