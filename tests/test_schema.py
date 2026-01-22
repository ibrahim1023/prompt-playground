import unittest

from src.reliability.validate import validate_json
from src.schemas import ToolAnswer, ToolRoute


class TestSchemaValidation(unittest.TestCase):
    def test_tool_route_accepts_expected_fields(self) -> None:
        payload = '{"tool":"calculator","tool_input":"2+2"}'
        result = validate_json(payload, ToolRoute)
        self.assertEqual(result.tool, "calculator")
        self.assertEqual(result.tool_input, "2+2")

    def test_tool_answer_rejects_extra_keys(self) -> None:
        payload = (
            '{"answer":"ok","tool_used":"none","tool_results":null,'
            '"citations":[],"extra":"nope"}'
        )
        with self.assertRaises(ValueError):
            validate_json(payload, ToolAnswer)
