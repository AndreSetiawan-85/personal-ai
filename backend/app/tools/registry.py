from dataclasses import dataclass
from importlib import import_module
from pkgutil import iter_modules
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
    ) -> None:
        normalized_name = self._normalize_name(name)
        normalized_description = self._normalize_description(description)

        if not callable(function):
            raise TypeError("Tool function must be callable.")

        if normalized_name in self._tools:
            raise ValueError(
                f"Tool '{normalized_name}' is already registered."
            )

        self._tools[normalized_name] = ToolDefinition(
            name=normalized_name,
            description=normalized_description,
            function=function,
        )

    def get(self, name: str):
        definition = self.get_definition(name)

        if definition is None:
            return None

        return definition.function

    def get_definition(self, name: str):
        if not isinstance(name, str):
            return None

        return self._tools.get(name.strip())

    def get_all(self) -> dict[str, ToolDefinition]:
        return dict(self._tools)

    def get_names(self) -> list[str]:
        return list(self._tools.keys())

    def get_descriptions(self) -> dict[str, str]:
        return {
            name: definition.description
            for name, definition in self._tools.items()
        }

    def clear(self) -> None:
        self._tools.clear()

    @staticmethod
    def _normalize_name(name: str) -> str:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Tool name is required.")

        return name.strip()

    @staticmethod
    def _normalize_description(description: str) -> str:
        if not isinstance(description, str) or not description.strip():
            raise ValueError("Tool description is required.")

        return description.strip()


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


def discover_tools() -> ToolRegistry:
    package_name = __package__
    package_module = import_module(package_name)

    for module_info in iter_modules(
        package_module.__path__,
        package_module.__name__ + ".",
    ):
        module_name = module_info.name

        if module_name == __name__:
            continue

        import_module(module_name)

    return tool_registry