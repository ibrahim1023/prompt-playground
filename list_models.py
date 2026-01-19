#!/usr/bin/env python3
import os
import sys


def main() -> int:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY is not set")
        return 1

    try:
        from google import genai
    except ImportError:
        print("google-genai package is required")
        return 1

    client = genai.Client(api_key=api_key)
    for model in client.models.list():
        name = getattr(model, "name", "")
        actions = getattr(model, "supported_actions", None)
        print(f"{name} methods: {actions}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
