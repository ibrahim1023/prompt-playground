from __future__ import annotations

import json
from typing import Any, TypeVar

from pydantic import BaseModel, ValidationError


ModelT = TypeVar("ModelT", bound=BaseModel)


def parse_json(text: str) -> Any:
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        message = f"Invalid JSON: {exc.msg} (line {exc.lineno}, column {exc.colno})"
        raise ValueError(message) from exc


def validate_with_model(data: Any, model: type[ModelT]) -> ModelT:
    try:
        return model.model_validate(data)
    except ValidationError as exc:
        raise ValueError(f"Schema validation failed: {exc}") from exc


def validate_json(text: str, model: type[ModelT]) -> ModelT:
    data = parse_json(text)
    return validate_with_model(data, model)
