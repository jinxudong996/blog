"""单 Agent（ReAct/工具调用风格）示例：DeepSeek(OpenAI 兼容接口) + Function Calling。

这是把《第一个ReAct智能体.ipynb》转换成可直接运行的 Python 脚本版本。

说明：为避免你本地环境缺少 `openai` SDK，本脚本使用 `requests` 直接请求 DeepSeek
的 OpenAI 兼容接口（/v1/chat/completions），同样支持 tools/function calling。

依赖：
- pip install requests

配置环境变量：
- DEEPSEEK_API_KEY：必填
- DEEPSEEK_BASE_URL：可选，默认 https://api.deepseek.com（无需带 /v1）
- DEEPSEEK_MODEL：可选，默认 deepseek-chat

运行：
- python agent/react_agent_deepseek.py
- 输入 quit 退出
"""

from __future__ import annotations

import json
import os
from typing import Any, Callable

import requests

try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    pass


def get_current_weather(location: str) -> dict:
    """获取指定地点当前的天气信息（Demo：返回模拟数据）。"""

    print(f"调用工具:get_current_weather, location: {location}")
    if "北京" in location:
        return {"location": "北京", "temperature": 15, "condition": "晴"}
    if "上海" in location:
        return {"location": "上海", "temperature": 18, "condition": "多云"}
    return {"location": location, "temperature": "未知", "condition": "未知"}


class ReActAgent:
    def __init__(self) -> None:
        """构造客户端，完成智能体初始化。"""

        api_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
        if not api_key:
            raise ValueError("未检测到环境变量 DEEPSEEK_API_KEY。请先设置后再运行。")

        base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com").strip()
        model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat").strip()

        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model

        self.messages: list[dict[str, Any]] = [
            {
                "role": "system",
                "content": (
                    "你是一个乐于助人的AI助手。你可以调用工具来获取实时信息。"
                    "请优先使用工具回答问题。回答尽可能简洁，如果不知道或无法回答请直接说明。"
                ),
            }
        ]

        self.tools: dict[str, Callable[..., Any]] = {"get_current_weather": get_current_weather}
        self.available_tools: list[dict[str, Any]] = [
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "获取指定地点当前的天气信息",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "需要查询天气的城市名字，例如：北京市",
                            }
                        },
                        "required": ["location"],
                    },
                },
            }
        ]

    def _chat_completions(self, messages: list[dict[str, Any]], tools: list[dict[str, Any]] | None = None) -> dict:
        url = f"{self.base_url}/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
        }
        if tools is not None:
            payload["tools"] = tools

        resp = requests.post(url, headers=headers, json=payload, timeout=60)
        if resp.status_code >= 400:
            raise RuntimeError(f"DeepSeek API 请求失败: HTTP {resp.status_code} - {resp.text}")
        return resp.json()

    def invoke(self, query: str) -> str:
        self.messages.append({"role": "user", "content": query})

        response = self._chat_completions(messages=self.messages, tools=self.available_tools)
        response_message = response["choices"][0]["message"]
        tool_calls = response_message.get("tool_calls")

        if tool_calls:
            self.messages.append(response_message)

            for tool_call in tool_calls:
                tool_name = tool_call["function"]["name"]
                tool_args = json.loads(tool_call["function"].get("arguments") or "{}")

                if tool_name not in self.tools:
                    raise ValueError(f"模型请求了未知工具: {tool_name}")

                result = self.tools[tool_name](**tool_args)

                self.messages.append(
                    {
                        "tool_call_id": tool_call["id"],
                        "role": "tool",
                        "name": tool_name,
                        "content": json.dumps(result, ensure_ascii=False),
                    }
                )

            second_response = self._chat_completions(messages=self.messages, tools=None)
            second_message = second_response["choices"][0]["message"]
            self.messages.append(second_message)
            return "Assistant: " + (second_message.get("content") or "")

        self.messages.append(response_message)
        return "Assistant: " + (response_message.get("content") or "")

    def chat_loop(self) -> None:
        """运行循环对话(多轮对话)。"""

        while True:
            query = input("\nQuery: ").strip()
            if query.lower() == "quit":
                break

            try:
                response = self.invoke(query)
                print(response)
            except Exception as exc:  # noqa: BLE001
                print(f"\nError: {exc}")


def main() -> None:
    agent = ReActAgent()
    agent.chat_loop()


if __name__ == "__main__":
    main()
