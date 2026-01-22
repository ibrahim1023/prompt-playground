# Prompt Migration Table

| prompt_id             | category          | mapped | tests | notes                       |
| --------------------- | ----------------- | ------ | ----- | --------------------------- |
| zero_shot             | single_turn_text  | y      | n     |                             |
| few_shot              | single_turn_text  | y      | n     |                             |
| role_based            | single_turn_text  | y      | n     |                             |
| cot                   | single_turn_text  | y      | n     |                             |
| constraints           | single_turn_text  | y      | n     |                             |
| calibration           | single_turn_text  | y      | n     |                             |
| comparison            | single_turn_text  | y      | n     |                             |
| instruction_hierarchy | single_turn_text  | y      | n     | refusal format branch       |
| refusal               | single_turn_text  | y      | n     | refusal format branch       |
| structured_output     | structured_json   | y      | n     | JSON output parser default  |
| router                | router_json       | n      | n     | tool routing decisions      |
| tool_answer           | tool_aware_json   | n      | n     | tool-aware output schema    |
