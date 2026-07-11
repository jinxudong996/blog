"""
Article workflow demo with a reusable Prompt Library.

The workflow still demonstrates:
- Prompt -> Model -> Parser
- RunnableParallel
- RunnableBranch
- with_retry
- with_fallbacks
- stream

Prompts live in agent/langchain/prompt_library.
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnableLambda, RunnableParallel
from langchain_openai import ChatOpenAI
from openai import APIConnectionError, APITimeoutError, InternalServerError, RateLimitError
from prompt_library import (
    CATEGORY_PROMPT_VERSION,
    FINAL_ANSWER_PROMPT_VERSION,
    KEYWORDS_PROMPT_VERSION,
    PROMPT_VERSIONS,
    SENTIMENT_PROMPT_VERSION,
    SUMMARY_PROMPT_VERSION,
    TASK_IDENTIFY_PROMPT_VERSION,
    category_prompt,
    final_answer_prompt,
    keywords_prompt,
    sentiment_prompt,
    summary_prompt,
    task_identify_prompt,
)
from prompt_library.debug import preview_prompt


ENV_PATH = Path(__file__).resolve().parent.parent / ".ENV"
load_dotenv(dotenv_path=ENV_PATH)


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required env variable: {name}")
    return value


def create_chat_model(
    *,
    model: str | None = None,
    base_url: str | None = None,
    api_key: str | None = None,
    temperature: float = 0.2,
    timeout: int | None = None,
) -> ChatOpenAI:
    """Create an OpenAI-compatible chat model from .ENV config."""
    timeout = timeout or int(os.getenv("LLM_TIMEOUT", "60"))

    return ChatOpenAI(
        model=model or _required_env("LLM_MODEL_ID"),
        base_url=base_url or _required_env("LLM_BASE_URL"),
        api_key=api_key or _required_env("LLM_API_KEY"),
        temperature=temperature,
        timeout=timeout,
    )


def create_backup_chat_model() -> ChatOpenAI:
    """Create a backup model for fallback; defaults to primary config if unset."""
    return create_chat_model(
        model=os.getenv("BACKUP_LLM_MODEL_ID")
        or os.getenv("LLM_BACKUP_MODEL_ID")
        or _required_env("LLM_MODEL_ID"),
        base_url=os.getenv("BACKUP_LLM_BASE_URL")
        or os.getenv("LLM_BACKUP_BASE_URL")
        or _required_env("LLM_BASE_URL"),
        api_key=os.getenv("BACKUP_LLM_API_KEY")
        or os.getenv("LLM_BACKUP_API_KEY")
        or _required_env("LLM_API_KEY"),
        timeout=int(
            os.getenv("BACKUP_LLM_TIMEOUT")
            or os.getenv("LLM_BACKUP_TIMEOUT")
            or os.getenv("LLM_TIMEOUT", "60")
        ),
    )


primary_model = create_chat_model()
backup_model = create_backup_chat_model()
parser = StrOutputParser()
json_parser = JsonOutputParser()

RETRYABLE_EXCEPTIONS = (
    TimeoutError,
    ConnectionError,
    APIConnectionError,
    APITimeoutError,
    RateLimitError,
    InternalServerError,
    OutputParserException,
)


def with_temporary_retry(runnable):
    """Retry temporary model/network/parser failures, then re-raise."""
    return runnable.with_retry(
        retry_if_exception_type=RETRYABLE_EXCEPTIONS,
        stop_after_attempt=3,
        wait_exponential_jitter=True,
    )


def with_retry_then_fallback(primary_runnable, backup_runnable):
    """Retry the primary runnable first, then switch to the backup runnable."""
    primary_with_retry = with_temporary_retry(primary_runnable)
    backup_with_retry = with_temporary_retry(backup_runnable)

    return primary_with_retry.with_fallbacks(
        [backup_with_retry],
        exceptions_to_handle=RETRYABLE_EXCEPTIONS,
    )


def normalize_task(text: str) -> str:
    """Normalize model output into one of the supported route names."""
    task = text.strip().lower()
    allowed_tasks = ("summarize", "keywords", "category", "sentiment", "analysis")

    for allowed_task in allowed_tasks:
        if allowed_task in task:
            return allowed_task

    return "analysis"


def article_input(data: dict) -> dict:
    """Keep only the article field before entering a task chain."""
    return {"article": data["article"]}


def final_answer_input(workflow_output: dict) -> dict:
    """Format routed workflow output for the final answer prompt."""
    return {
        "task": workflow_output["task"],
        "result": json.dumps(
            workflow_output["result"],
            ensure_ascii=False,
            indent=2,
        ),
    }


summary_chain = with_retry_then_fallback(
    summary_prompt | primary_model | parser,
    summary_prompt | backup_model | parser,
).with_config(metadata={"prompt_version": SUMMARY_PROMPT_VERSION})

keywords_chain = with_retry_then_fallback(
    keywords_prompt | primary_model | json_parser,
    keywords_prompt | backup_model | json_parser,
).with_config(metadata={"prompt_version": KEYWORDS_PROMPT_VERSION})

category_chain = with_retry_then_fallback(
    category_prompt | primary_model | parser,
    category_prompt | backup_model | parser,
).with_config(metadata={"prompt_version": CATEGORY_PROMPT_VERSION})

sentiment_chain = with_retry_then_fallback(
    sentiment_prompt | primary_model | parser,
    sentiment_prompt | backup_model | parser,
).with_config(metadata={"prompt_version": SENTIMENT_PROMPT_VERSION})

analysis_chain = RunnableParallel(
    summary=summary_chain,
    keywords=keywords_chain,
    category=category_chain,
    sentiment=sentiment_chain,
)

task_identify_chain = with_retry_then_fallback(
    task_identify_prompt | primary_model | parser | RunnableLambda(normalize_task),
    task_identify_prompt | backup_model | parser | RunnableLambda(normalize_task),
).with_config(metadata={"prompt_version": TASK_IDENTIFY_PROMPT_VERSION})

article_only = RunnableLambda(article_input)

branch_chain = RunnableBranch(
    (lambda x: x["task"] == "summarize", article_only | summary_chain),
    (lambda x: x["task"] == "keywords", article_only | keywords_chain),
    (lambda x: x["task"] == "category", article_only | category_chain),
    (lambda x: x["task"] == "sentiment", article_only | sentiment_chain),
    article_only | analysis_chain,
)

routed_input_chain = RunnableParallel(
    article=lambda x: x["article"],
    task=task_identify_chain,
)

article_workflow = routed_input_chain | RunnableParallel(
    task=lambda x: x["task"],
    result=branch_chain,
)

final_chain = with_temporary_retry(article_workflow)

final_answer_chain = with_retry_then_fallback(
    final_answer_prompt | primary_model | parser,
    final_answer_prompt | backup_model | parser,
).with_config(metadata={"prompt_version": FINAL_ANSWER_PROMPT_VERSION})

streaming_workflow_chain = final_chain | RunnableLambda(final_answer_input) | final_answer_chain


def summarize(article: str) -> str:
    """Run summary_chain with a plain article string."""
    return summary_chain.invoke({"article": article})


def analyze_article(article: str) -> dict:
    """Run the parallel article analysis workflow."""
    return analysis_chain.invoke({"article": article})


def run_article_workflow(article: str, instruction: str) -> dict:
    """Identify the task and route to the matching RunnableBranch."""
    return final_chain.invoke(
        {
            "article": article,
            "instruction": instruction,
        }
    )


def stream_article_workflow(article: str, instruction: str):
    """Stream the final user-facing answer."""
    return streaming_workflow_chain.stream(
        {
            "article": article,
            "instruction": instruction,
        }
    )


if __name__ == "__main__":
    article_path = Path(__file__).resolve().parent.parent / "data" / "zhufu.txt"
    demo_article = article_path.read_text(encoding="utf-8")
    demo_instruction = "请提取这篇文章的关键词"

    print("Prompt versions:", PROMPT_VERSIONS)
    preview_prompt(task_identify_prompt, {"article": demo_article[:500], "instruction": demo_instruction})

    print("\n=== Streaming Answer ===")
    for chunk in stream_article_workflow(demo_article, demo_instruction):
        print(chunk, end="", flush=True)
