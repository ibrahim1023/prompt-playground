from __future__ import annotations

from typing import Any

from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser

FORMAT_INSTRUCTIONS_VAR = "format_instructions"


def json_output_parser() -> JsonOutputParser:
    return JsonOutputParser()


def pydantic_output_parser(model: type[Any]) -> PydanticOutputParser:
    return PydanticOutputParser(pydantic_object=model)


def format_instructions(parser: Any) -> str:
    return parser.get_format_instructions()
