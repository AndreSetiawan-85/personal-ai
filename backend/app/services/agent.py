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

    def _build_tool_prompt(self, message):
        schemas = self.tools.get_schemas()

        return f"""
Determine whether the user message requires one of the available tools.

Available tool schemas:
{json.dumps(
    schemas,
    indent=2,
    ensure_ascii=False,
    default=str,
)}

Return ONLY a JSON object using this format:

{{
    "tool": null,
    "arguments": {{}}
}}

If a tool is required:

- "tool" must contain exactly one available tool name.
- "arguments" must be a JSON object.
- Argument names must match the selected tool schema.
- Required arguments must be provided.
- Optional arguments may be omitted.
- Do not invent arguments.
- Do not include arguments that are not defined by the selected tool.

If no tool is required:

{{
    "tool": null,
    "arguments": {{}}
}}

User message:
{message}
"""

    def _select_tool(self, message):
        if not self.tools.get_names():
            return None, {}

        prompt = self._build_tool_prompt(message)

        try:
            response = ollama_service.generate_response(prompt)
            data = memory_parser.parse_object(response)

            tool_name = data.get("tool")
            arguments = data.get("arguments", {})

            if not tool_name:
                return None, {}

            if not isinstance(arguments, dict):
                return None, {}

            definition = self.tools.get_definition(tool_name)

            if definition is None:
                return None, {}

            validated_arguments = self._validate_arguments(
                definition,
                arguments,
            )

            if validated_arguments is None:
                return None, {}

            return tool_name, validated_arguments

        except Exception as e:
            print("Tool selection error:", e)
            return None, {}

    @staticmethod
    def _validate_arguments(definition, arguments):
        parameters = {
            parameter.name: parameter
            for parameter in definition.parameters
        }

        unknown_arguments = set(arguments) - set(parameters)

        if unknown_arguments:
            return None

        validated = {}

        for parameter in definition.parameters:
            if parameter.name in arguments:
                validated[parameter.name] = arguments[
                    parameter.name
                ]
                continue

            if parameter.required:
                return None

        return validated

    def _execute_tool(self, tool_name, arguments):
        if not tool_name:
            return None, []

        definition = self.tools.get_definition(tool_name)

        if definition is None:
            return None, []

        try:
            result = definition.function(**arguments)

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

        tool_name, tool_arguments = self._select_tool(message)

        result, citations = self._execute_tool(
            tool_name,
            tool_arguments,
        )

        prompt = f"""
You are a personal AI assistant.

Application:
{settings.APP_NAME}

User memory:
{user_context}

User message:
{message}

Selected tool:
{tool_name}

Tool arguments:
{tool_arguments}

Tool result:
{result}

Sources:
{citations}

Instructions:
- Use relevant user memory when available.
- Treat user memory as information about the current user.
- Do not invent personal information about the user.
- Use tool results when they are available.
- Do not claim that a tool was used when no tool was executed.
- Answer naturally and directly.
"""

        return ollama_service.generate_response(prompt)


agent_service = AgentService()