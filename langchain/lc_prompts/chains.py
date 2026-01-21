from __future__ import annotations

from collections.abc import Callable
from typing import Any

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.runnables import Runnable, RunnableLambda, RunnablePassthrough

from .loaders import load_prompt_by_id
from .output_parsers import FORMAT_INSTRUCTIONS_VAR, format_instructions


HISTORY_VAR = "history"


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
    placeholder = f"{{{{{FORMAT_INSTRUCTIONS_VAR}}}}}"
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
