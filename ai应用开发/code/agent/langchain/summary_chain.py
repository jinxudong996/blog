"""
Summary and analysis chain demo.

Base flow:

article
  -> PromptTemplate
  -> ChatModel
  -> StrOutputParser
  -> summary

Parallel flow:

article
  -> summary_chain
  -> keywords_chain
  -> category_chain
  -> sentiment_chain
  -> dict

Branch flow:

instruction + article
  -> task_identify_chain
  -> RunnableBranch
  -> selected chain
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableBranch, RunnableLambda, RunnableParallel
from langchain_openai import ChatOpenAI
from openai import APIConnectionError, APITimeoutError, InternalServerError, RateLimitError


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


summary_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一个专业的中文内容编辑，擅长把长文章总结成清晰、准确、易读的摘要。",
        ),
        (
            "human",
            """请阅读下面的文章，并生成摘要。

要求：
1. 用中文回答。
2. 先给出 3-5 条核心要点。
3. 最后给出一句话总结。
4. 只基于文章内容总结，不要编造文章中没有的信息。

文章：
{article}
""",
        ),
    ]
)

keywords_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一个中文文本分析助手，擅长从文章中提取关键词。",
        ),
        (
            "human",
            """请从下面文章中提取 5-8 个关键词。

要求：
1. 只返回 JSON 数组。
2. 不要返回 Markdown。
3. 不要添加解释。

示例：
["关键词1", "关键词2", "关键词3"]

文章：
{article}
""",
        ),
    ]
)

category_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一个中文文章分类助手，擅长判断文章所属类别。",
        ),
        (
            "human",
            """请判断下面文章最适合的一个类别。

要求：
1. 只返回一个简短类别名称。
2. 不要添加解释。
3. 类别可以是：文学、科技、商业、教育、历史、社会、人物、生活、其他。

文章：
{article}
""",
        ),
    ]
)

sentiment_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一个中文情绪分析助手，擅长判断文章整体情绪倾向。",
        ),
        (
            "human",
            """请判断下面文章的整体情绪倾向。

要求：
1. 只返回一个词。
2. 可选值只能是：积极、消极、中性、复杂。
3. 不要添加解释。

文章：
{article}
""",
        ),
    ]
)

task_identify_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一个任务路由助手，根据用户指令选择最合适的文章处理链。",
        ),
        (
            "human",
            """请根据用户指令判断任务类型。

只能返回下面 5 个值之一：
summarize
keywords
category
sentiment
analysis

判断规则：
- 用户想总结、概括、摘要文章时，返回 summarize。
- 用户想提取关键词、标签、主题词时，返回 keywords。
- 用户想判断文章类型、类别、题材时，返回 category。
- 用户想分析情绪、态度、倾向时，返回 sentiment。
- 用户想要完整分析，或者无法判断时，返回 analysis。

用户指令：
{instruction}

文章：
{article}
""",
        ),
    ]
)

final_answer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一个中文文章处理助手，负责把工作流结果整理成清晰、自然、适合直接展示给用户的回答。",
        ),
        (
            "human",
            """请根据下面的工作流结果，生成最终回答。

要求：
1. 用中文回答。
2. 不要提及内部 chain、Runnable、workflow 等实现细节。
3. 如果 result 是列表，整理成简洁列表。
4. 如果 result 是对象，按字段含义组织成易读内容。
5. 如果 task 是 analysis，输出摘要、关键词、分类、情绪四部分。

任务类型：
{task}

工作流结果：
{result}
""",
        ),
    ]
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
)
keywords_chain = with_retry_then_fallback(
    keywords_prompt | primary_model | json_parser,
    keywords_prompt | backup_model | json_parser,
)
category_chain = with_retry_then_fallback(
    category_prompt | primary_model | parser,
    category_prompt | backup_model | parser,
)
sentiment_chain = with_retry_then_fallback(
    sentiment_prompt | primary_model | parser,
    sentiment_prompt | backup_model | parser,
)

analysis_chain = RunnableParallel(
    summary=summary_chain,
    keywords=keywords_chain,
    category=category_chain,
    sentiment=sentiment_chain,
)

task_identify_chain = with_retry_then_fallback(
    task_identify_prompt | primary_model | parser | RunnableLambda(normalize_task),
    task_identify_prompt | backup_model | parser | RunnableLambda(normalize_task),
)
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
)
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
    for chunk in stream_article_workflow(demo_article, demo_instruction):
        print(chunk, end="", flush=True)
