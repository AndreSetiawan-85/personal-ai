from dataclasses import dataclass
from importlib import import_module
from pathlib import Path
from typing import Callable


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    function: Callable


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, ToolDefinition] = {}

    def register(
        self,
        name: str,
        description: str,
        function: Callable,
    ):
        if not name or not name.strip():
            raise ValueError("Tool name is required.")

        if not description or not description.strip():
            raise ValueError("Tool description is required.")

        if not callable(function):
            raise TypeError("Tool function must be callable.")

        normalized_name = name.strip()

        if normalized_name in self._tools:
            raise ValueError(
                f"Tool '{normalized_name}' is already registered."
            )

        self._tools[normalized_name] = ToolDefinition(
            name=normalized_name,
            description=description.strip(),
            function=function,
        )

    def get(self, name: str):
        definition = self._tools.get(name)

        if definition is None:
            return None

        return definition.function

    def get_definition(self, name: str):
        return self._tools.get(name)

    def get_all(self):
        return dict(self._tools)

    def get_names(self):
        return list(self._tools.keys())

    def get_descriptions(self):
        return {
            name: definition.description
            for name, definition in self._tools.items()
        }


tool_registry = ToolRegistry()


def tool(
    name: str,
    description: str,
):
    def decorator(function: Callable):
        tool_registry.register(
            name=name,
            description=description,
            function=function,
        )

        return function

    return decorator


def discover_tools():
    tools_directory = Path(__file__).parent

    for path in sorted(tools_directory.glob("*.py")):
        if path.name.startswith("_"):
            continue

        module_name = path.stem

        if module_name == "registry":
            continue

        import_module(
            f"app.tools.{module_name}"
        )

    return tool_registry