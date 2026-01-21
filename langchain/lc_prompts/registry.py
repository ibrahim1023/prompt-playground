from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .loaders import PromptRecord, load_all_prompts, load_prompt_by_id


@dataclass
class PromptRegistry:
    records: dict[str, PromptRecord]

    def get(self, prompt_id: str) -> PromptRecord:
        if prompt_id not in self.records:
            raise KeyError(f"Unknown prompt id: {prompt_id}")
        return self.records[prompt_id]

    def list_ids(self) -> list[str]:
        return sorted(self.records.keys())

    def validate_id(self, prompt_id: str) -> bool:
        return prompt_id in self.records


def build_registry(prompts_dir: Path | None = None) -> PromptRegistry:
    records = {record.id: record for record in load_all_prompts(prompts_dir)}
    return PromptRegistry(records=records)


def get_prompt(prompt_id: str, prompts_dir: Path | None = None) -> PromptRecord:
    return load_prompt_by_id(prompt_id, prompts_dir)


def list_prompt_ids(prompts_dir: Path | None = None) -> list[str]:
    return build_registry(prompts_dir).list_ids()


def validate_prompt_id(prompt_id: str, prompts_dir: Path | None = None) -> bool:
    return build_registry(prompts_dir).validate_id(prompt_id)
