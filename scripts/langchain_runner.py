#!/usr/bin/env python3
import os
import sys
from typing import Any

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from langchain_core.runnables import RunnableLambda

from langchain.lc_prompts import simple_chain
from langchain.lc_prompts.loaders import load_prompt_by_id
from runner import build_prompt, call_model, load_env_file, save_output


def _invoke_model(prompt: Any) -> str:
    return call_model(str(prompt))


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: langchain_runner.py <prompt_id> <question>")
        return 1

    load_env_file()
    prompt_id = sys.argv[1]
    user_question = " ".join(sys.argv[2:])

    llm = RunnableLambda(_invoke_model)
    chain = simple_chain(prompt_id, llm)
    output = chain.invoke({"input": user_question})
    print(output)
    record = load_prompt_by_id(prompt_id)
    prompt_text = build_prompt(record.text, user_question)
    saved_path = save_output(prompt_text, str(output), "results/output")
    print(f"\nSaved output to {saved_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
