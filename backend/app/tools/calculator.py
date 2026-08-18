import ast
import operator

from app.tools.registry import tool


_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _evaluate(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value

        raise ValueError("Invalid mathematical expression.")

    if isinstance(node, ast.BinOp):
        operator_function = _OPERATORS.get(type(node.op))

        if operator_function is None:
            raise ValueError("Unsupported mathematical operator.")

        left = _evaluate(node.left)
        right = _evaluate(node.right)

        if isinstance(node.op, ast.Div) and right == 0:
            raise ValueError("Division by zero is not allowed.")

        return operator_function(left, right)

    if isinstance(node, ast.UnaryOp):
        operator_function = _OPERATORS.get(type(node.op))

        if operator_function is None:
            raise ValueError("Unsupported mathematical operator.")

        operand = _evaluate(node.operand)

        return operator_function(operand)

    raise ValueError("Invalid mathematical expression.")


@tool(
    name="calculator",
    description="Evaluates mathematical expressions and returns the numerical result.",
)
def calculate(expression: str):
    try:
        expression = expression.strip()

        if not expression:
            return {
                "success": False,
                "error": "Mathematical expression is required.",
            }

        tree = ast.parse(
            expression,
            mode="eval",
        )

        result = _evaluate(tree.body)

        return {
            "success": True,
            "result": result,
        }

    except ZeroDivisionError:
        return {
            "success": False,
            "error": "Division by zero is not allowed.",
        }

    except Exception:
        return {
            "success": False,
            "error": "Invalid mathematical expression.",
        }