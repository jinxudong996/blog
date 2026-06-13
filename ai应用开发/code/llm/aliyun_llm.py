import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Union

import requests


Message = Dict[str, str]


@dataclass
class AliyunLLM:
    model: str
    api_key: Optional[str] = None
    region: str = "cn"
    base_url: Optional[str] = None
    timeout: float = 60.0

    def __post_init__(self) -> None:
        if self.api_key is None:
            self.api_key = os.getenv("QWEN_API_KEY")

        if not self.base_url:
            # DashScope OpenAI-compatible endpoint ("compatible-mode").
            # If you use a different gateway, set BASE_URL explicitly.
            self.base_url = os.getenv(
                "QWEN_BASE_URL",
                "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
            )

    def call(self, messages: Sequence[Message], stop: Optional[Union[str, List[str]]] = None) -> str:
        if not self.api_key:
            raise ValueError("缺少 API Key：请在环境变量中设置 QWEN_API_KEY")

        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": list(messages),
        }
        if stop:
            payload["stop"] = stop

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        resp = requests.post(self.base_url, headers=headers, json=payload, timeout=self.timeout)
        if resp.status_code >= 400:
            raise ValueError(f"LLM 请求失败: HTTP {resp.status_code}: {resp.text}")

        data = resp.json()
        try:
            return (data["choices"][0]["message"]["content"] or "").strip()
        except Exception as e:
            raise ValueError(f"无法解析 LLM 响应: {data}") from e
