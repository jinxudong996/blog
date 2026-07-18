"""Chapter 4.8: a streaming chatbot that can switch model providers.

Run:
    python agent/langchain/multi_provider_chat.py
    python agent/langchain/multi_provider_chat.py --model gpt

Commands inside the chat:
    /model gpt
    /model deepseek
    /models
    /clear
    /help
    /exit
"""

import argparse
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI


ENV_PATH = Path(__file__).resolve().parent.parent / ".ENV"
load_dotenv(dotenv_path=ENV_PATH)

SUPPORTED_PROVIDERS = ("deepseek", "gpt")
SYSTEM_PROMPT = "你是一名可靠、简洁的中文 AI 助手。"


def required_env(*names: str) -> str:
    """Return the first configured environment variable from names."""
    for name in names:
        value = os.getenv(name)
        if value:
            return value

    joined_names = ", ".join(names)
    raise ValueError(f"Missing environment variable. Configure one of: {joined_names}")


def create_chat_model(provider: str) -> ChatOpenAI:
    """Create GPT or DeepSeek through their OpenAI-compatible endpoints."""
    provider = provider.strip().lower()
    timeout = int(os.getenv("LLM_TIMEOUT", "60"))

    if provider == "deepseek":
        return ChatOpenAI(
            model=required_env("LLM_MODEL_ID", "DEEPSEEK_MODEL_ID"),
            api_key=required_env("LLM_API_KEY", "DEEPSEEK_API_KEY"),
            base_url=required_env("LLM_BASE_URL", "DEEPSEEK_BASE_URL"),
            timeout=timeout,
        )

    if provider == "gpt":
        return ChatOpenAI(
            model=required_env("LLM_MODEL_ID_GPT", "GPT_MODEL_ID"),
            api_key=required_env("LLM_API_KEY_GPT", "OPENAI_API_KEY"),
            base_url=required_env("LLM_BASE_URL_GPT", "OPENAI_BASE_URL"),
            timeout=int(os.getenv("LLM_TIMEOUT_GPT", str(timeout))),
        )

    supported = ", ".join(SUPPORTED_PROVIDERS)
    raise ValueError(f"Unsupported provider: {provider}. Supported: {supported}")


class ChatSession:
    """Manage the selected model and a provider-independent message history."""

    def __init__(self, provider: str) -> None:
        self.provider = ""
        self.model: ChatOpenAI
        self.messages: list[BaseMessage] = []
        self.clear()
        self.switch_model(provider)

    def switch_model(self, provider: str) -> None:
        """Switch models while preserving the current conversation history."""
        model = create_chat_model(provider)
        self.provider = provider.strip().lower()
        self.model = model

    def clear(self) -> None:
        """Clear conversation history but retain the system instruction."""
        self.messages = [SystemMessage(content=SYSTEM_PROMPT)]

    def stream_reply(self, user_input: str) -> str:
        """Stream one answer and append the completed turn to history."""
        user_message = HumanMessage(content=user_input)
        self.messages.append(user_message)
        answer_parts: list[str] = []

        try:
            print(f"{self.provider}> ", end="", flush=True)
            for chunk in self.model.stream(self.messages):
                if not isinstance(chunk.content, str):
                    continue
                answer_parts.append(chunk.content)
                print(chunk.content, end="", flush=True)
            print()
        except Exception:
            self.messages.pop()
            raise

        answer = "".join(answer_parts)
        self.messages.append(AIMessage(content=answer))
        return answer


def print_help() -> None:
    print("/model gpt       切换到 GPT")
    print("/model deepseek  切换到 DeepSeek")
    print("/models          查看当前模型和可选模型")
    print("/clear           清空对话历史")
    print("/help            查看命令")
    print("/exit            退出程序")


def handle_command(command: str, session: ChatSession) -> bool:
    """Handle a slash command and return False when the program should exit."""
    command, _, argument = command.partition(" ")
    command = command.lower()
    argument = argument.strip().lower()

    if command in {"/exit", "/quit"}:
        return False

    if command == "/help":
        print_help()
        return True

    if command == "/models":
        print("当前模型：", session.provider)
        print("可选模型：", ", ".join(SUPPORTED_PROVIDERS))
        return True

    if command == "/clear":
        session.clear()
        print("对话历史已清空。")
        return True

    if command == "/model":
        if not argument:
            print("用法：/model gpt 或 /model deepseek")
            return True

        try:
            session.switch_model(argument)
        except (ImportError, ValueError) as exc:
            print(f"切换失败：{exc}")
            return True

        print(f"已切换到 {session.provider}，当前对话历史已保留。")
        return True

    print(f"未知命令：{command}。输入 /help 查看可用命令。")
    return True


def run_chat(initial_provider: str) -> None:
    session = ChatSession(initial_provider)
    print(f"当前模型：{session.provider}。输入 /help 查看命令。")

    while True:
        try:
            user_input = input("\nyou> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n聊天已结束。")
            break

        if not user_input:
            continue

        if user_input.startswith("/"):
            if not handle_command(user_input, session):
                print("聊天已结束。")
                break
            continue

        try:
            session.stream_reply(user_input)
        except Exception as exc:
            print(f"调用失败：{type(exc).__name__}: {exc}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Chat with GPT or DeepSeek and switch models at runtime."
    )
    parser.add_argument(
        "--model",
        choices=SUPPORTED_PROVIDERS,
        default=os.getenv("CHAT_PROVIDER", "deepseek").lower(),
        help="Initial model provider (default: deepseek)",
    )
    args = parser.parse_args()

    try:
        run_chat(args.model)
    except (ImportError, ValueError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
