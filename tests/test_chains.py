import unittest

from langchain_core.runnables import RunnableLambda

from langchain.lc_prompts import json_output_parser, planner_executor_chain, simple_chain, with_history_chain


class TestChains(unittest.TestCase):
    def test_simple_chain_invokes(self) -> None:
        llm = RunnableLambda(lambda _: "ok")
        chain = simple_chain("zero_shot", llm)
        output = chain.invoke({"input": "Question"})
        self.assertEqual(output, "ok")

    def test_with_history_chain_invokes(self) -> None:
        llm = RunnableLambda(lambda _: "ok")
        chain = with_history_chain("zero_shot", llm)
        output = chain.invoke({"history": [], "input": "Question"})
        self.assertEqual(output, "ok")

    def test_planner_executor_chain_flow(self) -> None:
        llm = RunnableLambda(lambda x: x)
        chain = planner_executor_chain("zero_shot", "zero_shot", llm)
        output = chain.invoke({"input": "Question"})
        output_text = str(output)
        self.assertIn("USER QUESTION", output_text)
        self.assertIn("PROMPT TITLE", output_text)

    def test_structured_output_chain_parses_json(self) -> None:
        llm = RunnableLambda(
            lambda _: '{"summary":"ok","key_points":[],"risks":[],"confidence":"low"}'
        )
        chain = simple_chain("structured_output", llm, parser=json_output_parser())
        output = chain.invoke({"input": "Question"})
        self.assertEqual(output["confidence"], "low")
