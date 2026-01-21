import unittest
from pathlib import Path

from langchain_core.prompts import PromptTemplate

from langchain.lc_prompts import FORMAT_INSTRUCTIONS_VAR, get_prompt


class TestGoldenPrompts(unittest.TestCase):
    def _read_golden(self, name: str) -> str:
        path = Path(__file__).parent / "goldens" / f"{name}.txt"
        return path.read_text(encoding="utf-8")

    def test_zero_shot_prompt_render(self) -> None:
        record = get_prompt("zero_shot")
        prompt = PromptTemplate.from_template(record.text)
        rendered = prompt.format(input="Test question").rstrip("\n")
        expected = self._read_golden("zero_shot").rstrip("\n")
        self.assertEqual(rendered, expected)

    def test_structured_output_prompt_render(self) -> None:
        record = get_prompt("structured_output")
        prompt = PromptTemplate.from_template(record.text)
        rendered = prompt.format(
            input="Test question",
            **{FORMAT_INSTRUCTIONS_VAR: ""},
        ).rstrip("\n")
        expected = self._read_golden("structured_output").rstrip("\n")
        self.assertEqual(rendered, expected)
