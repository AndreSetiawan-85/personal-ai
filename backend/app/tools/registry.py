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
    annotation: Any = None


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

    def validate_arguments(
        self,
        name: str,
        arguments: dict[str, Any],
    ) -> tuple[bool, dict[str, Any], str | None]:
        definition = self.get_definition(name)

        if definition is None:
            return False, {}, f"Unknown tool: {name}"

        if not isinstance(arguments, dict):
            return (
                False,
                {},
                "Tool arguments must be a JSON object.",
            )

        parameters = {
            parameter.name: parameter
            for parameter in definition.parameters
        }

        unknown_arguments = [
            key
            for key in arguments
            if key not in parameters
        ]

        if unknown_arguments:
            return (
                False,
                {},
                (
                    "Unknown tool arguments: "
                    + ", ".join(sorted(unknown_arguments))
                ),
            )

        normalized_arguments = {}

        for parameter in definition.parameters:
            if parameter.name not in arguments:
                if parameter.required:
                    return (
                        False,
                        {},
                        (
                            f"Missing required argument: "
                            f"{parameter.name}"
                        ),
                    )

                if parameter.default is not None:
                    normalized_arguments[
                        parameter.name
                    ] = parameter.default

                continue

            value = arguments[parameter.name]

            try:
                normalized_value = self._normalize_argument(
                    value=value,
                    annotation=parameter.annotation,
                    parameter_name=parameter.name,
                )
            except ValueError as exc:
                return (
                    False,
                    {},
                    str(exc),
                )

            normalized_arguments[
                parameter.name
            ] = normalized_value

        return True, normalized_arguments, None

    def execute(
        self,
        name: str,
        arguments: dict[str, Any],
    ) -> dict[str, Any]:
        definition = self.get_definition(name)

        if definition is None:
            return {
                "success": False,
                "error": f"Unknown tool: {name}",
            }

        valid, normalized_arguments, error = (
            self.validate_arguments(
                name,
                arguments,
            )
        )

        if not valid:
            return {
                "success": False,
                "error": error,
            }

        try:
            result = definition.function(
                **normalized_arguments
            )

            if isinstance(result, dict):
                return result

            return {
                "success": True,
                "result": result,
            }

        except Exception as exc:
            return {
                "success": False,
                "error": str(exc),
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
        if (
            not isinstance(description, str)
            or not description.strip()
        ):
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

            parameter_type = cls._annotation_to_string(
                annotation
            )

            required = (
                parameter.default
                is inspect.Parameter.empty
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
                    annotation=annotation,
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

    @classmethod
    def _normalize_argument(
        cls,
        value: Any,
        annotation: Any,
        parameter_name: str,
    ) -> Any:
        if annotation is inspect.Parameter.empty:
            return value

        if annotation is Any:
            return value

        origin = get_origin(annotation)
        args = get_args(annotation)

        if origin is not None:
            if origin is type(None):
                if value is None:
                    return None

                raise ValueError(
                    f"Argument '{parameter_name}' must be null."
                )

            if args:
                for candidate_type in args:
                    if candidate_type is type(None):
                        if value is None:
                            return None

                        continue

                    try:
                        return cls._normalize_argument(
                            value=value,
                            annotation=candidate_type,
                            parameter_name=parameter_name,
                        )
                    except ValueError:
                        continue

            raise ValueError(
                f"Invalid type for argument "
                f"'{parameter_name}'."
            )

        if annotation is str:
            if isinstance(value, str):
                return value

            if isinstance(value, (int, float, bool)):
                return str(value)

            raise ValueError(
                f"Argument '{parameter_name}' "
                f"must be a string."
            )

        if annotation is int:
            if isinstance(value, bool):
                raise ValueError(
                    f"Argument '{parameter_name}' "
                    f"must be an integer."
                )

            if isinstance(value, int):
                return value

            if isinstance(value, float):
                if value.is_integer():
                    return int(value)

                raise ValueError(
                    f"Argument '{parameter_name}' "
                    f"must be an integer."
                )

            if isinstance(value, str):
                try:
                    return int(value.strip())
                except ValueError:
                    raise ValueError(
                        f"Argument '{parameter_name}' "
                        f"must be an integer."
                    )

            raise ValueError(
                f"Argument '{parameter_name}' "
                f"must be an integer."
            )

        if annotation is float:
            if isinstance(value, bool):
                raise ValueError(
                    f"Argument '{parameter_name}' "
                    f"must be a number."
                )

            if isinstance(value, (int, float)):
                return float(value)

            if isinstance(value, str):
                try:
                    return float(value.strip())
                except ValueError:
                    raise ValueError(
                        f"Argument '{parameter_name}' "
                        f"must be a number."
                    )

            raise ValueError(
                f"Argument '{parameter_name}' "
                f"must be a number."
            )

        if annotation is bool:
            if isinstance(value, bool):
                return value

            if isinstance(value, str):
                normalized = value.strip().lower()

                if normalized in {
                    "true",
                    "1",
                    "yes",
                }:
                    return True

                if normalized in {
                    "false",
                    "0",
                    "no",
                }:
                    return False

            raise ValueError(
                f"Argument '{parameter_name}' "
                f"must be a boolean."
            )

        if isinstance(annotation, type):
            if isinstance(value, annotation):
                return value

        return value

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