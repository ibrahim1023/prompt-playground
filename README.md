# Prompt Engineering Playground: Reliable LLM Outputs

## Thesis

Prompt engineering is a user-interface problem: precise inputs produce predictable, comparable outputs. This repo proves that prompts can be designed, tested, and iterated like interface specs.

## Scope

- Domain: analytical / research-style questions only
- Techniques: zero-shot, few-shot, role prompting, chain-of-thought, structured output, instruction hierarchy
- Out of scope (Part 1): agents, ReAct, ToT

## Repo Structure

```
.
├── prompts/
│   ├── zero_shot.txt            # baseline instruction-only prompt
│   ├── few_shot.txt             # format control with examples
│   ├── role_based.txt           # role conditioning
│   ├── cot.txt                  # explicit reasoning steps
│   ├── structured_output.txt    # JSON-only output
│   ├── instruction_hierarchy.txt# rule priority stress test
│   ├── constraints.txt          # strict formatting compliance
│   ├── refusal.txt              # scope refusal behavior
│   ├── ambiguity.txt            # clarification vs answer behavior
│   ├── calibration.txt          # confidence + rationale
│   ├── comparison.txt           # balanced pros/cons format
│   ├── router.txt               # JSON-only tool routing
│   └── tool_answer.txt          # tool-aware JSON response
├── results/
│   └── output/                # Runner outputs
│   └── comparisons.md           # manual prompt comparisons
├── runner.py                    # minimal runner
├── list_models.py               # list available models for key
├── requirements.txt             # dependencies
└── README.md
```

## How To Use

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set your API key in `.env` or export GEMINI_API_KEY=...
   Set GEMINI_MODEL to a model from list_models.py (example: models/gemini-2.0-flash-001)
3. Run a prompt:
   ```bash
   python3 runner.py prompts/zero_shot.txt "Risks of LLMs in healthcare"
   ```
4. Outputs are saved in results/output/

## Testing

Run the lightweight test suite:

```bash
python3 -m unittest discover -s tests -p "test*.py"
```

If imports fail, make sure you run tests from the repo root so the local
`langchain/` package is on `PYTHONPATH`.

## Dependencies

- google-genai (see requirements.txt)
- langchain (see requirements.txt)

## Model Discovery

To list models available to your API key:

```bash
python3 list_models.py
```

## LangChain Format Instructions

Use `format_instructions` to enforce structured outputs in prompt templates that include
`{format_instructions}` (see `prompts/structured_output.txt`). Templates use the default
f-string format.

```python
from langchain_core.prompts import PromptTemplate
from langchain.lc_prompts import (
    FORMAT_INSTRUCTIONS_VAR,
    format_instructions,
    get_prompt,
    json_output_parser,
)

record = get_prompt("structured_output")
parser = json_output_parser()
prompt = PromptTemplate.from_template(record.text).partial(
    **{FORMAT_INSTRUCTIONS_VAR: format_instructions(parser)}
)
```

Pydantic example (swap in your own model):

```python
from pydantic import BaseModel


class Analysis(BaseModel):
    summary: str
    key_points: list[str]
    risks: list[str]
    confidence: str


record = get_prompt("structured_output")
parser = pydantic_output_parser(Analysis)
prompt = PromptTemplate.from_template(record.text).partial(
    **{FORMAT_INSTRUCTIONS_VAR: format_instructions(parser)}
)
```

## LangChain Chains

Basic chain usage:

```python
from langchain.lc_prompts import simple_chain, with_history_chain


chain = simple_chain("zero_shot", llm)
history_chain = with_history_chain("zero_shot", llm)
```

Planner → executor composition:

```python
from langchain.lc_prompts import planner_executor_chain


chain = planner_executor_chain("planner_prompt", "executor_prompt", llm)
```

RAG-ready chain (prompt must accept `{context}` and `{input}`, or pass custom
keys when calling `rag_ready_chain`):

```python
from langchain.lc_prompts import rag_ready_chain


chain = rag_ready_chain("rag_prompt", llm, retriever)
```

Tool-aware routing chain:

```python
from langchain.lc_prompts import json_output_parser, tool_aware_chain


router_parser = json_output_parser()
answer_parser = json_output_parser()
chain = tool_aware_chain(
    "router",
    "tool_answer",
    llm,
    router_parser=router_parser,
    answer_parser=answer_parser,
)
```

## Tools

Deterministic tools live in `src/tools/` and include a calculator and a stub
search utility. Use `src/tools/registry.py` to retrieve LangChain Tool objects
or read the tool schemas for routing decisions.

```python
from src.tools import get_tools, tool_specs

tools = get_tools()
schemas = tool_specs()
```

## Prompt Mapping

Prompt-specific mappings are centralized in `langchain/lc_prompts/mappings.py` with
categories and defaults:

```python
from langchain.lc_prompts import PROMPT_CATEGORIES, map_prompt


chain = map_prompt("structured_output", llm)
category = PROMPT_CATEGORIES["structured_output"]
```

Migration status lives in `prompt_migration.md`.

## Docs

- Mapping guide: `mapping-guide.md`
- Contributing: `CONTRIBUTING.md`

## What To Look For

- Where structured output improves reliability
- When few-shot formatting improves clarity
- Whether chain-of-thought improves reasoning depth
- Failure modes that repeat across prompts

## Findings (fill in)

- Why prompt engineering matters:
- What failed and why:
- When CoT helped:
- Why structured output is superior:
- What you’d change in v2:

## Notes

- The comparisons in results/comparisons.md are the primary evidence.
- This project favors clarity over abstraction.
