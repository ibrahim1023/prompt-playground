# Contributing

Thanks for contributing to this prompt-engineering playground. Keep changes small,
clear, and deterministic.

## Contents

- Guidelines
- Prompt changes
- Checks

## Guidelines

- Keep prompts in `prompts/` as the source of truth.
- Prefer explicit, minimal Python functions and avoid unnecessary abstractions.
- Update `requirements.txt` when adding dependencies.
- Keep outputs deterministic and formatting consistent.
- Update `README.md` after every task.
- Avoid committing secrets; use `.env` or environment variables.

## Prompt Changes

1. Update or add the prompt in `prompts/`.
2. Update mappings in `langchain/lc_prompts/mappings.py` if needed.
3. Update `prompt_migration.md`.
4. Add or update tests in `tests/`.

## Checks

Run the smoke checks before publishing:

```bash
python3 -m pip install -r requirements.txt
python3 -m pip check
python3 -m compileall .
python3 -m unittest discover -s tests -p "test*.py"
python3 list_models.py
python3 runner.py prompts/zero_shot.txt "Risks of LLMs in healthcare"
```
