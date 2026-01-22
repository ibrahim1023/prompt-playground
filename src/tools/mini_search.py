from __future__ import annotations

from typing import Any

NAME = "search"
DESCRIPTION = "Deterministic stub search over a small local dataset."
INPUT_SCHEMA = {
    "type": "object",
    "properties": {"query": {"type": "string"}},
    "required": ["query"],
}
OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "results": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "snippet": {"type": "string"},
                    "source": {"type": "string"},
                },
                "required": ["snippet", "source"],
            },
        }
    },
    "required": ["results"],
}

_DATASET: list[dict[str, Any]] = [
    {
        "keywords": ["llm", "healthcare"],
        "snippet": "Clinician notes summarization can reduce documentation time but requires strict PHI handling.",
        "source": "local:healthcare-llm-001",
    },
    {
        "keywords": ["inflation", "us"],
        "snippet": "Inflation is measured by CPI and PCE; both track price changes over time.",
        "source": "local:macro-001",
    },
    {
        "keywords": ["renewable", "energy", "capacity"],
        "snippet": "Global renewable capacity has grown rapidly in recent years, led by solar and wind.",
        "source": "local:energy-001",
    },
]


def mini_search(query: str) -> list[dict[str, str]]:
    if not query or not query.strip():
        return []
    tokens = query.lower()
    results: list[dict[str, str]] = []
    for entry in _DATASET:
        keywords = entry["keywords"]
        if all(keyword in tokens for keyword in keywords):
            results.append(
                {"snippet": entry["snippet"], "source": entry["source"]}
            )
    return results
