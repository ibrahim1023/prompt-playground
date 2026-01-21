# Prompt Engineering Playground: Reliable LLM Outputs

## Thesis

Prompt engineering is a user-interface problem: precise inputs produce predictable, comparable outputs. This repo proves that prompts can be designed, tested, and iterated like interface specs.

## Scope

- Domain: analytical / research-style questions only
- Techniques: zero-shot, few-shot, role prompting, chain-of-thought, structured output, instruction hierarchy
- Out of scope (Part 1): tools, agents, ReAct, ToT

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
│   └── comparison.txt           # balanced pros/cons format
├── results/
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
4. Outputs are saved in results/

## Dependencies

- google-genai (see requirements.txt)

## Model Discovery

To list models available to your API key:

```bash
python3 list_models.py
```

## LangChain Format Instructions

Use `format_instructions` to enforce structured outputs in prompt templates that include
`{{format_instructions}}` (see `prompts/structured_output.txt`):

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
