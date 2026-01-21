from __future__ import annotations

from typing import Any

from langchain_core.runnables import Runnable

from .chains import simple_chain
from .output_parsers import json_output_parser


PROMPT_CATEGORIES: dict[str, str] = {
    "zero_shot": "single_turn_text",
    "few_shot": "single_turn_text",
    "role_based": "single_turn_text",
    "cot": "single_turn_text",
    "constraints": "single_turn_text",
    "calibration": "single_turn_text",
    "comparison": "single_turn_text",
    "instruction_hierarchy": "single_turn_text",
    "refusal": "single_turn_text",
    "structured_output": "structured_json",
}


def map_zero_shot(llm: Runnable, *, prompts_dir: str | None = None) -> Runnable:
    return simple_chain("zero_shot", llm, prompts_dir=prompts_dir)


def map_few_shot(llm: Runnable, *, prompts_dir: str | None = None) -> Runnable:
    return simple_chain("few_shot", llm, prompts_dir=prompts_dir)


def map_role_based(llm: Runnable, *, prompts_dir: str | None = None) -> Runnable:
    return simple_chain("role_based", llm, prompts_dir=prompts_dir)


def map_cot(llm: Runnable, *, prompts_dir: str | None = None) -> Runnable:
    return simple_chain("cot", llm, prompts_dir=prompts_dir)


def map_constraints(llm: Runnable, *, prompts_dir: str | None = None) -> Runnable:
    return simple_chain("constraints", llm, prompts_dir=prompts_dir)


def map_calibration(llm: Runnable, *, prompts_dir: str | None = None) -> Runnable:
    return simple_chain("calibration", llm, prompts_dir=prompts_dir)


def map_comparison(llm: Runnable, *, prompts_dir: str | None = None) -> Runnable:
    return simple_chain("comparison", llm, prompts_dir=prompts_dir)


def map_instruction_hierarchy(
    llm: Runnable, *, prompts_dir: str | None = None
) -> Runnable:
    return simple_chain("instruction_hierarchy", llm, prompts_dir=prompts_dir)


def map_refusal(llm: Runnable, *, prompts_dir: str | None = None) -> Runnable:
    return simple_chain("refusal", llm, prompts_dir=prompts_dir)


def map_structured_output(
    llm: Runnable,
    *,
    prompts_dir: str | None = None,
    parser: Any | None = None,
) -> Runnable:
    chosen_parser = parser or json_output_parser()
    return simple_chain(
        "structured_output",
        llm,
        parser=chosen_parser,
        prompts_dir=prompts_dir,
    )


PROMPT_MAPPERS: dict[str, Any] = {
    "zero_shot": map_zero_shot,
    "few_shot": map_few_shot,
    "role_based": map_role_based,
    "cot": map_cot,
    "constraints": map_constraints,
    "calibration": map_calibration,
    "comparison": map_comparison,
    "instruction_hierarchy": map_instruction_hierarchy,
    "refusal": map_refusal,
    "structured_output": map_structured_output,
}


def map_prompt(
    prompt_id: str,
    llm: Runnable,
    *,
    prompts_dir: str | None = None,
    parser: Any | None = None,
) -> Runnable:
    if prompt_id not in PROMPT_MAPPERS:
        raise KeyError(f"Unknown prompt id: {prompt_id}")
    mapper = PROMPT_MAPPERS[prompt_id]
    if prompt_id == "structured_output":
        return mapper(llm, prompts_dir=prompts_dir, parser=parser)
    return mapper(llm, prompts_dir=prompts_dir)
