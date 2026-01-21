import unittest

from langchain.lc_prompts import build_registry, get_prompt, list_prompt_ids


class TestRegistry(unittest.TestCase):
    def test_list_ids_includes_known_prompt(self) -> None:
        prompt_ids = list_prompt_ids()
        self.assertIn("zero_shot", prompt_ids)

    def test_metadata_includes_expected_output_type(self) -> None:
        record = get_prompt("structured_output")
        self.assertEqual(record.metadata.expected_output_type, "json")
        self.assertIn("input", record.metadata.input_variables)

    def test_build_registry_lookup(self) -> None:
        registry = build_registry()
        record = registry.get("zero_shot")
        self.assertEqual(record.id, "zero_shot")
