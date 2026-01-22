import os
import unittest
from tempfile import TemporaryDirectory

from src.reliability.retry import RetryConfig, run_with_retries
from src.reliability.validate import validate_json
from src.schemas import ToolAnswer


class TestRepairFlow(unittest.TestCase):
    def test_run_with_retries_repairs_invalid_json(self) -> None:
        calls = {"invoke": 0, "repair": 0}

        def invoke(_: dict[str, str]) -> str:
            calls["invoke"] += 1
            return "not json"

        def repair_invoke(_: dict[str, str]) -> str:
            calls["repair"] += 1
            return (
                '{"answer":"ok","tool_used":"none","tool_results":null,'
                '"citations":[]}'
            )

        with TemporaryDirectory() as tmp_dir:
            result = run_with_retries(
                invoke=invoke,
                inputs={"input": "Question"},
                validator=lambda text: validate_json(text, ToolAnswer),
                repair_invoke=repair_invoke,
                config=RetryConfig(max_retries=2, log_dir=tmp_dir),
                log_context={"prompt": "tool_answer"},
            )

            self.assertEqual(result.answer, "ok")
            self.assertEqual(calls["invoke"], 1)
            self.assertEqual(calls["repair"], 1)
            self.assertTrue(os.listdir(tmp_dir))
