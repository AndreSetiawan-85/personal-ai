import inspect

from dataclasses import dataclass
from importlib import import_module
from pkgutil import iter_modules
from typing import Any, Callable, get_args, get_origin


@dataclass(frozen=True)
class ToolParameter:
    name: str
    type: str
    required: bool
    default: Any = None


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    function: Callable
    parameters: tuple[ToolParameter, ...]


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

        parameters = self._build_parameters(function)

        self._tools[normalized_name] = ToolDefinition(
            name=normalized_name,
            description=normalized_description,
            function=function,
            parameters=parameters,
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

    def get_schemas(self) -> dict[str, dict]:
        return {
            name: self._definition_to_schema(definition)
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

    @classmethod
    def _build_parameters(
        cls,
        function: Callable,
    ) -> tuple[ToolParameter, ...]:
        signature = inspect.signature(function)
        parameters = []

        for parameter in signature.parameters.values():
            if parameter.kind in (
                inspect.Parameter.VAR_POSITIONAL,
                inspect.Parameter.VAR_KEYWORD,
            ):
                continue

            annotation = parameter.annotation

            parameter_type = cls._annotation_to_string(annotation)

            required = (
                parameter.default is inspect.Parameter.empty
            )

            default = (
                None
                if required
                else parameter.default
            )

            parameters.append(
                ToolParameter(
                    name=parameter.name,
                    type=parameter_type,
                    required=required,
                    default=default,
                )
            )

        return tuple(parameters)

    @staticmethod
    def _annotation_to_string(annotation) -> str:
        if annotation is inspect.Parameter.empty:
            return "string"

        origin = get_origin(annotation)

        if origin is not None:
            args = get_args(annotation)

            if args:
                return " | ".join(
                    ToolRegistry._annotation_to_string(arg)
                    for arg in args
                )

            return str(origin)

        if annotation is Any:
            return "any"

        if isinstance(annotation, type):
            return annotation.__name__

        return str(annotation)

    @staticmethod
    def _definition_to_schema(
        definition: ToolDefinition,
    ) -> dict:
        return {
            "name": definition.name,
            "description": definition.description,
            "parameters": [
                {
                    "name": parameter.name,
                    "type": parameter.type,
                    "required": parameter.required,
                    "default": parameter.default,
                }
                for parameter in definition.parameters
            ],
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