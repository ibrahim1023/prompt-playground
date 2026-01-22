from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable


@dataclass(frozen=True)
class RetryConfig:
    max_retries: int = 2
    log_dir: str = "results/logs"


def _write_log(payload: dict[str, Any], log_dir: str) -> str:
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = os.path.join(log_dir, f"retry-{timestamp}.json")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=True, indent=2))
        handle.write("\n")
    return path


def run_with_retries(
    *,
    invoke: Callable[[dict[str, Any]], str],
    inputs: dict[str, Any],
    validator: Callable[[str], Any],
    repair_invoke: Callable[[dict[str, Any]], str] | None = None,
    repair_context: dict[str, Any] | None = None,
    config: RetryConfig | None = None,
    log_context: dict[str, Any] | None = None,
) -> Any:
    chosen_config = config or RetryConfig()
    errors: list[str] = []
    raw_output = invoke(inputs)

    for attempt in range(chosen_config.max_retries + 1):
        try:
            validated = validator(raw_output)
            _write_log(
                {
                    "prompt": (log_context or {}).get("prompt"),
                    "prompt_version": (log_context or {}).get("prompt_version"),
                    "model": (log_context or {}).get("model"),
                    "temperature": (log_context or {}).get("temperature"),
                    "attempts": attempt + 1,
                    "raw_output": raw_output,
                    "errors": errors,
                    "final": validated.model_dump() if hasattr(validated, "model_dump") else validated,
                    "success": True,
                },
                chosen_config.log_dir,
            )
            return validated
        except ValueError as exc:
            errors.append(str(exc))
            if repair_invoke is None or attempt >= chosen_config.max_retries:
                _write_log(
                    {
                        "prompt": (log_context or {}).get("prompt"),
                        "prompt_version": (log_context or {}).get("prompt_version"),
                        "model": (log_context or {}).get("model"),
                        "temperature": (log_context or {}).get("temperature"),
                        "attempts": attempt + 1,
                        "raw_output": raw_output,
                        "errors": errors,
                        "final": raw_output,
                        "success": False,
                    },
                    chosen_config.log_dir,
                )
                raise
            repair_inputs = {
                "raw_output": raw_output,
                "error": str(exc),
            }
            if repair_context:
                repair_inputs.update(repair_context)
            raw_output = repair_invoke(repair_inputs)

    raise RuntimeError("Retry loop exceeded without returning")
