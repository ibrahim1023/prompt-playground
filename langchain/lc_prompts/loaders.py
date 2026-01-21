from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterable


PROMPT_TITLE_RE = re.compile(r"^PROMPT TITLE:\s*(.+)$", re.MULTILINE)
TEMPLATE_VAR_RE = re.compile(r"{{\s*([a-zA-Z0-9_]+)\s*}}")


@dataclass(frozen=True)
class PromptMetadata:
    id: str
    title: str
    description: str
    input_variables: list[str]
    expected_output_type: str
    version: str
    source_path: str

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "input_variables": list(self.input_variables),
            "expected_output_type": self.expected_output_type,
            "version": self.version,
            "source_path": self.source_path,
        }


@dataclass(frozen=True)
class PromptRecord:
    id: str
    text: str
    metadata: PromptMetadata


def default_prompts_dir() -> Path:
    for parent in Path(__file__).resolve().parents:
        prompts_dir = parent / "prompts"
        if prompts_dir.is_dir():
            return prompts_dir
    raise FileNotFoundError(
        "Unable to locate prompts directory from loaders.py")


def extract_section(text: str, header: str) -> str:
    lines = text.splitlines()
    header_index = None
    for idx, line in enumerate(lines):
        if line.strip() == header:
            header_index = idx
            break
    if header_index is None:
        return ""
    buffer: list[str] = []
    for line in lines[header_index + 1:]:
        stripped = line.strip()
        if stripped and stripped == stripped.upper():
            break
        buffer.append(line)
    return "\n".join(buffer).strip()


def infer_output_type(text: str) -> str:
    if "REQUIRED JSON SCHEMA" in text or "Output JSON only" in text:
        return "json"
    return "text"


def parse_input_variables(text: str) -> list[str]:
    seen: set[str] = set()
    variables: list[str] = []
    for match in TEMPLATE_VAR_RE.finditer(text):
        name = match.group(1)
        if name not in seen:
            seen.add(name)
            variables.append(name)
    return variables


def build_metadata(prompt_id: str, text: str, source_path: Path) -> PromptMetadata:
    title_match = PROMPT_TITLE_RE.search(text)
    title = title_match.group(1).strip(
    ) if title_match else prompt_id.replace("_", " ").title()
    description = extract_section(text, "INTENT") or "No description provided."
    input_variables = parse_input_variables(text)
    expected_output_type = infer_output_type(text)
    version = "v1"
    return PromptMetadata(
        id=prompt_id,
        title=title,
        description=description,
        input_variables=input_variables,
        expected_output_type=expected_output_type,
        version=version,
        source_path=str(source_path.as_posix()),
    )


def load_prompt_file(path: Path) -> PromptRecord:
    prompt_id = path.stem
    text = path.read_text(encoding="utf-8")
    metadata = build_metadata(prompt_id, text, path)
    return PromptRecord(id=prompt_id, text=text, metadata=metadata)


def load_all_prompts(prompts_dir: Path | None = None) -> list[PromptRecord]:
    if prompts_dir is None:
        prompts_dir = default_prompts_dir()
    records: list[PromptRecord] = []
    for path in sorted(prompts_dir.glob("*.txt")):
        records.append(load_prompt_file(path))
    return records


def load_prompt_by_id(prompt_id: str, prompts_dir: Path | None = None) -> PromptRecord:
    if prompts_dir is None:
        prompts_dir = default_prompts_dir()
    path = prompts_dir / f"{prompt_id}.txt"
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {path}")
    return load_prompt_file(path)


def iter_prompt_ids(prompts_dir: Path | None = None) -> Iterable[str]:
    if prompts_dir is None:
        prompts_dir = default_prompts_dir()
    for path in sorted(prompts_dir.glob("*.txt")):
        yield path.stem
