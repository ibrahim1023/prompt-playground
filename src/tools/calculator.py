from __future__ import annotations

import ast
import operator
import re
from typing import Any

NAME = "calculator"
DESCRIPTION = "Deterministic arithmetic evaluator for math expressions."
INPUT_SCHEMA = {
    "type": "object",
    "properties": {"expression": {"type": "string"}},
    "required": ["expression"],
}
OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {"result": {"type": "number"}},
    "required": ["result"],
}

_OPERATORS: dict[type[ast.AST], Any] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _normalize_expression(expression: str) -> str:
    normalized = expression.strip().lower()
    normalized = re.sub(
        r"(\d+(?:\.\d+)?)\s*%\s*of\s*",
        r"(\1/100) * ",
        normalized,
    )
    normalized = re.sub(
        r"(\d+(?:\.\d+)?)\s*%",
        r"(\1/100)",
        normalized,
    )
    return normalized


def _eval_node(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.BinOp):
        operator_fn = _OPERATORS.get(type(node.op))
        if operator_fn is None:
            raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
        return operator_fn(_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp):
        operator_fn = _OPERATORS.get(type(node.op))
        if operator_fn is None:
            raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
        return operator_fn(_eval_node(node.operand))
    raise ValueError(f"Unsupported expression node: {type(node).__name__}")


def calculate(expression: str) -> float:
    if not expression or not expression.strip():
        raise ValueError("Expression cannot be empty.")
    normalized = _normalize_expression(expression)
    try:
        parsed = ast.parse(normalized, mode="eval")
        return _eval_node(parsed)
    except (SyntaxError, ValueError, TypeError) as exc:
        raise ValueError(f"Invalid expression: {expression}") from exc
