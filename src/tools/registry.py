from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from langchain_core.tools import Tool

from . import calculator, mini_search


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    input_schema: dict[str, Any]
    output_schema: dict[str, Any]


_TOOL_SPECS = [
    ToolSpec(
        name=calculator.NAME,
        description=calculator.DESCRIPTION,
        input_schema=calculator.INPUT_SCHEMA,
        output_schema=calculator.OUTPUT_SCHEMA,
    ),
    ToolSpec(
        name=mini_search.NAME,
        description=mini_search.DESCRIPTION,
        input_schema=mini_search.INPUT_SCHEMA,
        output_schema=mini_search.OUTPUT_SCHEMA,
    ),
]


def tool_specs() -> list[ToolSpec]:
    return list(_TOOL_SPECS)


def get_tools() -> list[Tool]:
    return [
        Tool(
            name=calculator.NAME,
            description=calculator.DESCRIPTION,
            func=calculator.calculate,
        ),
        Tool(
            name=mini_search.NAME,
            description=mini_search.DESCRIPTION,
            func=mini_search.mini_search,
        ),
    ]


def get_tool(name: str) -> Tool | None:
    for tool in get_tools():
        if tool.name == name:
            return tool
    return None
