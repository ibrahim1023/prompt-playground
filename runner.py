#!/usr/bin/env python3
import os
import sys
from datetime import datetime


def load_prompt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def build_prompt(template: str, user_input: str, format_instructions: str = "") -> str:
    prompt = template.replace("{{input}}", user_input.strip())
    return prompt.replace("{{format_instructions}}", format_instructions.strip())


def load_env_file(path: str = ".env") -> None:
    if not os.path.exists(path):
        return

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("\"'")
            if key and key not in os.environ:
                os.environ[key] = value


def call_model(prompt: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set")

    try:
        from google import genai
    except ImportError as exc:
        raise RuntimeError("google-genai package is required") from exc

    model_name = os.getenv("GEMINI_MODEL", "models/gemini-2.0-flash-001")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
    )
    if response.text:
        return response.text
    return str(response)


def save_output(prompt: str, text: str, output_dir: str) -> str:
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = os.path.join(output_dir, f"output-{timestamp}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("PROMPT\n")
        f.write(prompt)
        if not prompt.endswith("\n"):
            f.write("\n")
        f.write("\nOUTPUT\n")
        f.write(text)
        if not text.endswith("\n"):
            f.write("\n")
    return path


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: runner.py <prompt_file> <question>")
        return 1

    load_env_file()
    prompt_path = sys.argv[1]
    user_question = " ".join(sys.argv[2:])

    template = load_prompt(prompt_path)
    prompt = build_prompt(template, user_question)
    output = call_model(prompt)
    print(output)

    saved_path = save_output(prompt, output, "results")
    print(f"\nSaved output to {saved_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
