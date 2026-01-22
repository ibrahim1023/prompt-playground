from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict


class Citation(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    source: str
    snippet: str


class ToolRoute(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    tool: Literal["calculator", "search", "none"]
    tool_input: str


class ToolAnswer(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    answer: str
    tool_used: Literal["calculator", "search", "none"]
    tool_results: dict[str, Any] | None
    citations: list[Citation]
