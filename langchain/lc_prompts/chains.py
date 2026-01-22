from __future__ import annotations

from collections.abc import Callable
import json
from typing import Any

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.runnables import Runnable, RunnableLambda, RunnablePassthrough

from .loaders import load_prompt_by_id
from .output_parsers import (
    FORMAT_INSTRUCTIONS_VAR,
    format_instructions,
    json_output_parser,
)
from src.tools import calculator, mini_search


HISTORY_VAR = "history"
_TOOL_NAMES = {"calculator", "search", "none"}


def _format_instructions_text(parser: Any | None) -> str | None:
    if parser is None:
        return None
    return format_instructions(parser)


def _apply_format_instructions(
    prompt: PromptTemplate | ChatPromptTemplate,
    template_text: str,
    parser: Any | None,
) -> PromptTemplate | ChatPromptTemplate:
    instructions = _format_instructions_text(parser)
    if not instructions:
        return prompt
    placeholder = f"{{{FORMAT_INSTRUCTIONS_VAR}}}"
    if placeholder not in template_text:
        return prompt
    return prompt.partial(**{FORMAT_INSTRUCTIONS_VAR: instructions})


def simple_chain(
    prompt_id: str,
    llm: Runnable,
    *,
    parser: Any | None = None,
    prompts_dir: str | None = None,
) -> Runnable:
    record = load_prompt_by_id(prompt_id, prompts_dir)
    prompt = PromptTemplate.from_template(record.text)
    prompt = _apply_format_instructions(prompt, record.text, parser)
    chain: Runnable = prompt | llm
    if parser is not None:
        chain = chain | parser
    return chain


def with_history_chain(
    prompt_id: str,
    llm: Runnable,
    *,
    parser: Any | None = None,
    prompts_dir: str | None = None,
) -> Runnable:
    record = load_prompt_by_id(prompt_id, prompts_dir)
    prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(HISTORY_VAR),
            ("human", record.text),
        ]
    )
    prompt = _apply_format_instructions(prompt, record.text, parser)
    chain: Runnable = prompt | llm
    if parser is not None:
        chain = chain | parser
    return chain


def planner_executor_chain(
    planner_id: str,
    executor_id: str,
    llm: Runnable,
    *,
    planner_parser: Any | None = None,
    executor_parser: Any | None = None,
    prompts_dir: str | None = None,
    executor_input_key: str = "input",
    map_planner_output: Callable[[Any], Any] | None = None,
) -> Runnable:
    planner = simple_chain(
        planner_id,
        llm,
        parser=planner_parser,
        prompts_dir=prompts_dir,
    )
    executor = simple_chain(
        executor_id,
        llm,
        parser=executor_parser,
        prompts_dir=prompts_dir,
    )

    def default_mapper(output: Any) -> dict[str, Any]:
        return {executor_input_key: output}

    mapper = map_planner_output or default_mapper
    return planner | RunnableLambda(mapper) | executor


def rag_ready_chain(
    prompt_id: str,
    llm: Runnable,
    retriever: Runnable,
    *,
    parser: Any | None = None,
    prompts_dir: str | None = None,
    context_key: str = "context",
    question_key: str = "input",
) -> Runnable:
    record = load_prompt_by_id(prompt_id, prompts_dir)
    prompt = PromptTemplate.from_template(record.text)
    prompt = _apply_format_instructions(prompt, record.text, parser)
    inputs = {
        context_key: retriever,
        question_key: RunnablePassthrough(),
    }
    chain: Runnable = inputs | prompt | llm
    if parser is not None:
        chain = chain | parser
    return chain


def _normalize_router_output(route: Any) -> dict[str, str]:
    if not isinstance(route, dict):
        return {"tool": "none", "tool_input": ""}
    tool = str(route.get("tool", "none")).strip().lower()
    if tool not in _TOOL_NAMES:
        tool = "none"
    tool_input = route.get("tool_input", "")
    if not isinstance(tool_input, str):
        tool_input = str(tool_input)
    if tool == "none":
        tool_input = ""
    return {"tool": tool, "tool_input": tool_input}


def _run_tool(route: dict[str, str]) -> dict[str, Any]:
    tool = route["tool"]
    tool_input = route["tool_input"]
    if tool == "calculator":
        try:
            result = calculator.calculate(tool_input)
            tool_results: dict[str, Any] = {"result": result}
        except ValueError as exc:
            tool_results = {"error": str(exc)}
        return {"tool_used": tool, "tool_results": tool_results, "citations": []}
    if tool == "search":
        results = mini_search.mini_search(tool_input)
        citations = [
            {"source": item["source"], "snippet": item["snippet"]}
            for item in results
        ]
        return {
            "tool_used": tool,
            "tool_results": {"results": results},
            "citations": citations,
        }
    return {"tool_used": "none", "tool_results": None, "citations": []}


def tool_aware_chain(
    router_id: str,
    answer_id: str,
    llm: Runnable,
    *,
    router_parser: Any | None = None,
    answer_parser: Any | None = None,
    prompts_dir: str | None = None,
) -> Runnable:
    chosen_router_parser = router_parser or json_output_parser()
    chosen_answer_parser = answer_parser or json_output_parser()
    router = simple_chain(
        router_id,
        llm,
        parser=chosen_router_parser,
        prompts_dir=prompts_dir,
    )
    answer = simple_chain(
        answer_id,
        llm,
        parser=chosen_answer_parser,
        prompts_dir=prompts_dir,
    )

    def run_with_tools(inputs: dict[str, Any]) -> Any:
        route_output = router.invoke(inputs)
        route = _normalize_router_output(route_output)
        tool_payload = _run_tool(route)
        answer_inputs = dict(inputs)
        answer_inputs.update(
            {
                "tool_used": tool_payload["tool_used"],
                "tool_results": json.dumps(
                    tool_payload["tool_results"], ensure_ascii=True
                ),
                "citations": json.dumps(
                    tool_payload["citations"], ensure_ascii=True
                ),
            }
        )
        return answer.invoke(answer_inputs)

    return RunnableLambda(run_with_tools)
