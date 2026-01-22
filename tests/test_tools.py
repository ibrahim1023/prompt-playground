import unittest

from langchain.lc_prompts.chains import _normalize_router_output, _run_tool


class TestToolsRouting(unittest.TestCase):
    def test_normalize_router_output_enforces_none(self) -> None:
        route = _normalize_router_output({"tool": "bogus", "tool_input": 123})
        self.assertEqual(route["tool"], "none")
        self.assertEqual(route["tool_input"], "")

    def test_run_tool_calculator(self) -> None:
        payload = _run_tool({"tool": "calculator", "tool_input": "2+2"})
        self.assertEqual(payload["tool_used"], "calculator")
        self.assertEqual(payload["tool_results"]["result"], 4.0)

    def test_run_tool_search(self) -> None:
        payload = _run_tool({"tool": "search", "tool_input": "llm healthcare"})
        self.assertEqual(payload["tool_used"], "search")
        self.assertTrue(payload["tool_results"]["results"])
        self.assertTrue(payload["citations"])
