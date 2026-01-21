# Prompt Mapping Guide

This guide explains how to map prompts in `prompts/` to LangChain chains.

## Contents

- Mapping checklist
- Categories
- Example mapping
- Category examples

## Mapping Checklist

1. Identify the prompt category (single-turn, structured JSON, history, planner).
2. Decide the chain shape (`simple_chain`, `with_history_chain`, etc.).
3. If structured output, choose a parser (JSON or Pydantic) and ensure the prompt
   includes `{format_instructions}`.
4. Add a mapping function in `langchain/lc_prompts/mappings.py`.
5. Update `PROMPT_CATEGORIES` and `PROMPT_MAPPERS`.
6. Update `prompt_migration.md` with status and notes.
7. Add or update tests in `tests/`.

## Categories

- `single_turn_text`: one input, text output
- `structured_json`: one input, JSON output
- `history`: includes conversation history
- `planner_executor`: two prompts composed

## Example Mapping

```python
from langchain_core.runnables import Runnable

from langchain.lc_prompts import simple_chain, json_output_parser


def map_structured_output(llm: Runnable) -> Runnable:
    return simple_chain("structured_output", llm, parser=json_output_parser())
```

## Category Examples

- `single_turn_text`: `zero_shot`, `few_shot`, `role_based`
- `structured_json`: `structured_output`
- `history`: add when a prompt explicitly expects conversation history
- `planner_executor`: use only when prompts are designed as separate planner/executor steps
