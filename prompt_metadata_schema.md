# Prompt Metadata Schema

Minimum fields for each prompt mapping.

## Required

- `id`: short, stable identifier (matches filename without extension)
- `title`: human-readable name
- `description`: 1-2 sentence purpose statement
- `input_variables`: list of input variable names (strings)
- `expected_output_type`: `text` | `json` | `schema`
- `version`: semantic version or date tag
- `source_path`: path to the raw prompt file

## Optional

- `output_schema`: schema name or inline schema (if `expected_output_type` is `schema`)
- `examples`: list of `{input, output}` pairs
- `tags`: list of topical or behavioral tags
- `notes`: implementation or usage notes
