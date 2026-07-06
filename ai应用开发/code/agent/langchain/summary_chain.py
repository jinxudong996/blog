"""
Summary chain demo:

article
  -> PromptTemplate
  -> ChatModel
  -> StrOutputParser
  -> summary

The model config is loaded from agent/.ENV:

LLM_API_KEY=...
LLM_MODEL_ID=...
LLM_BASE_URL=...
LLM_TIMEOUT=60
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_openai import ChatOpenAI


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
) -> ChatOpenAI:
    """Create an OpenAI-compatible chat model from .ENV config."""
    timeout = int(os.getenv("LLM_TIMEOUT", "60"))

    return ChatOpenAI(
        model=model or _required_env("LLM_MODEL_ID"),
        base_url=base_url or _required_env("LLM_BASE_URL"),
        api_key=api_key or _required_env("LLM_API_KEY"),
        temperature=temperature,
        timeout=timeout,
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

model = create_chat_model()
parser = StrOutputParser()
json_parser = JsonOutputParser()

# Core Runnable workflow:
# article -> PromptTemplate -> ChatModel -> StrOutputParser -> summary
summary_chain = summary_prompt | model | parser
keywords_chain = keywords_prompt | model | json_parser
category_chain = category_prompt | model | parser
sentiment_chain = sentiment_prompt | model | parser

analysis_chain = RunnableParallel(
    summary=summary_chain,
    keywords=keywords_chain,
    category=category_chain,
    sentiment=sentiment_chain,
)


def summarize(article: str) -> str:
    """Run summary_chain with a plain article string."""
    return summary_chain.invoke({"article": article})


def analyze_article(article: str) -> dict:
    """Run the parallel article analysis workflow."""
    return analysis_chain.invoke({"article": article})


if __name__ == "__main__":
    article_path = Path(__file__).resolve().parent.parent / "data" / "zhufu.txt"
    demo_article = article_path.read_text(encoding="utf-8")

    print(analyze_article(demo_article))
