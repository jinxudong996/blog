"""Chapter 4.2-4.7 examples for the LangChain Chat Model API.

Examples:
    python agent/langchain/model_test.py
    python agent/langchain/model_test.py input
    python agent/langchain/model_test.py params
    python agent/langchain/model_test.py stream
    python agent/langchain/model_test.py batch
    python agent/langchain/model_test.py async
    python agent/langchain/model_test.py provider
    python agent/langchain/model_test.py factory
    python agent/langchain/model_test.py lcel
"""

import argparse
import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


ENV_PATH = Path(__file__).resolve().parent.parent / ".ENV"
load_dotenv(dotenv_path=ENV_PATH)


def required_env(name: str) -> str:
    """Read a required setting and report a clear configuration error."""
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def create_chat_model(
    provider: str | None = None,
    model: str | None = None,
    **model_kwargs,
) -> BaseChatModel:
    """Create one Chat Model without exposing Provider details to callers."""
    provider_name = (provider or os.getenv("LLM_PROVIDER", "openai_compatible"))
    provider_name = provider_name.lower().replace("-", "_")
    model_name = model or required_env("LLM_MODEL_ID")

    if provider_name in {"openai_compatible", "compatible"}:
        return ChatOpenAI(
            model=model_name,
            api_key=required_env("LLM_API_KEY"),
            base_url=required_env("LLM_BASE_URL"),
            **model_kwargs,
        )

    if provider_name == "openai":
        return ChatOpenAI(
            model=model_name,
            api_key=required_env("OPENAI_API_KEY"),
            **model_kwargs,
        )

    if provider_name in {"deepseek", "deep_seek"}:
        try:
            from langchain_deepseek import ChatDeepSeek
        except ImportError as exc:
            raise ImportError(
                "DeepSeek integration is not installed. "
                "Run: pip install langchain-deepseek"
            ) from exc

        return ChatDeepSeek(
            model=model_name,
            api_key=required_env("DEEPSEEK_API_KEY"),
            **model_kwargs,
        )

    if provider_name in {"anthropic", "claude"}:
        try:
            from langchain_anthropic import ChatAnthropic
        except ImportError as exc:
            raise ImportError(
                "Anthropic integration is not installed. "
                "Run: pip install langchain-anthropic"
            ) from exc

        return ChatAnthropic(
            model=model_name,
            api_key=required_env("ANTHROPIC_API_KEY"),
            **model_kwargs,
        )

    if provider_name in {"gemini", "google"}:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
        except ImportError as exc:
            raise ImportError(
                "Google integration is not installed. "
                "Run: pip install langchain-google-genai"
            ) from exc

        return ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=required_env("GOOGLE_API_KEY"),
            **model_kwargs,
        )

    supported = "openai, openai_compatible, deepseek, anthropic, gemini"
    raise ValueError(f"Unsupported provider: {provider_name}. Supported: {supported}")


def create_model(**overrides) -> BaseChatModel:
    """Create the OpenAI-compatible model used by sections 4.2-4.4."""
    return create_chat_model(provider="openai_compatible", **overrides)


def demo_first_call() -> None:
    """4.2: Make the smallest useful Chat Model call."""
    model = create_model()
    response = model.invoke("请介绍一下 LangChain")

    print(response.content)


def demo_input_and_output() -> None:
    """4.3: Compare string and message-list inputs, then inspect AIMessage."""
    model = create_model()

    string_response = model.invoke("你好")
    print("=== 字符串输入 ===")
    print(string_response.content)

    message_response = model.invoke(
        [
            ("system", "你是一名 Python 教师，请用简洁的语言回答。"),
            ("human", "介绍一下 Runnable。"),
        ]
    )

    print("\n=== 消息列表输入 ===")
    print("message type:", message_response.type)
    print("content:", message_response.content)
    print("tool_calls:", message_response.tool_calls)
    print("usage_metadata:", message_response.usage_metadata)
    print("response_metadata:", message_response.response_metadata)


def demo_model_parameters() -> None:
    """4.4: Configure common generation and client parameters."""
    model = create_model(
        temperature=0.2,
        max_tokens=300,
        timeout=60,
        max_retries=2,
    )
    response = model.invoke("用三点说明 temperature 参数的作用。")

    print(response.content)


def demo_stream() -> None:
    """4.4: Print response chunks as soon as the model produces them."""
    model = create_model()

    for chunk in model.stream("用简短的例子解释 LangChain Runnable。"):
        print(chunk.content, end="", flush=True)
    print()


def demo_batch() -> None:
    """4.4: Process multiple independent inputs with one batch call."""
    model = create_model()
    responses = model.batch(
        [
            "一句话解释 Chat Model。",
            "一句话解释 Prompt。",
            "一句话解释 Output Parser。",
        ]
    )

    for index, response in enumerate(responses, start=1):
        print(f"{index}. {response.content}")


async def demo_async() -> None:
    """4.4: Use ainvoke in an asynchronous application."""
    model = create_model()
    response = await model.ainvoke("为什么异步调用适合 Web 服务？")

    print(response.content)


def demo_provider() -> None:
    """4.5: Call the configured Provider through the common interface."""
    model = create_chat_model()
    response = model.invoke("请用一句话说明 Chat Model 的作用。")

    print("provider:", os.getenv("LLM_PROVIDER", "openai_compatible"))
    print("message type:", response.type)
    print("content:", response.content)


def demo_model_factory() -> None:
    """4.6: Keep Provider selection outside the business code."""
    provider = os.getenv("LLM_PROVIDER", "openai_compatible")
    model = create_chat_model(
        provider=provider,
        model=required_env("LLM_MODEL_ID"),
        temperature=0.2,
    )

    response = model.invoke("为什么业务代码不应该写死模型厂商？")
    print(response.content)


def demo_lcel() -> None:
    """4.7: Compose Prompt, Model, and Parser into one LCEL chain."""
    prompt = ChatPromptTemplate.from_template(
        "请用三句话总结下面的文章：\n\n{article}"
    )
    model = create_chat_model(temperature=0.2)
    parser = StrOutputParser()
    summary_chain = prompt | model | parser

    article = (
        "LangChain 为大模型应用提供了统一的组件接口。"
        "开发者可以使用 Prompt 构造输入，使用 Chat Model 调用模型，"
        "再通过 Output Parser 将模型消息转换为业务需要的数据。"
    )
    result = summary_chain.invoke({"article": article})

    print(result)


def main() -> None:
    examples = {
        "first": demo_first_call,
        # "input": demo_input_and_output,
        # "params": demo_model_parameters,
        # "stream": demo_stream,
        # "batch": demo_batch,
        "provider": demo_provider,
        "factory": demo_model_factory,
        "lcel": demo_lcel,
    }

    parser = argparse.ArgumentParser(description="Run a Chat Model API example.")
    parser.add_argument(
        "example",
        nargs="?",
        choices=[*examples, "async"],
        default="first",
        help="Example to run (default: first)",
    )
    args = parser.parse_args()

    if args.example == "async":
        asyncio.run(demo_async())
        return

    examples[args.example]()


if __name__ == "__main__":
    main()
