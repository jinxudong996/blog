"""ReAct 的 Observation Module（观察组件）演示：数据采集与解析。

ReAct 的基本循环是：Thought -> Action -> Observation -> Thought...
其中 Observation Module 的核心职责是：
1) 数据采集：把 action 的执行结果（工具返回、环境状态、错误信息、耗时等）收集起来
2) 数据解析：把“原始输出(raw)”转换为“结构化、可读、可控”的 observation
3) 数据标准化：统一 schema，便于后续 prompt 拼接、日志、评估与回放

本 demo 不依赖任何在线服务，不调用 LLM：
- 模拟 2 个工具：天气查询（返回 JSON 字符串）、网页抓取（返回半结构化文本）
- ObservationModule 会把它们解析成统一的 Observation 对象

运行：
  python agent/observation_module_demo.py
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field
from typing import Any, Literal


@dataclass
class Observation:
    """统一的观察结果结构（建议你在项目里固定一个 schema）。"""

    tool_name: str
    args: dict[str, Any]
    ok: bool
    timestamp_ms: int
    latency_ms: int

    raw: str
    parsed: dict[str, Any] = field(default_factory=dict)
    parse_error: str | None = None

    # 额外元信息：方便追踪来源、做调试/回放
    source: Literal["tool", "env", "system"] = "tool"
    content_type: str = "text/plain"  # e.g. application/json


class ObservationModule:
    """观察组件：采集(action结果) + 解析(raw->structured) + 标准化(schema)。"""

    def collect_and_parse(self, *, tool_name: str, args: dict[str, Any], raw_output: str, latency_ms: int) -> Observation:
        now_ms = int(time.time() * 1000)
        obs = Observation(
            tool_name=tool_name,
            args=args,
            ok=True,
            timestamp_ms=now_ms,
            latency_ms=latency_ms,
            raw=raw_output,
        )

        try:
            if self._looks_like_json(raw_output):
                obs.content_type = "application/json"
                data = json.loads(raw_output)
                obs.parsed = self._parse_json(tool_name, data)
            else:
                obs.content_type = "text/plain"
                obs.parsed = self._parse_text(tool_name, raw_output)
        except Exception as exc:  # noqa: BLE001
            obs.ok = False
            obs.parse_error = f"{type(exc).__name__}: {exc}"
            obs.parsed = {"summary": "解析失败，保留原始输出", "raw_excerpt": raw_output[:200]}

        return obs

    def _looks_like_json(self, s: str) -> bool:
        s = s.strip()
        return (s.startswith("{") and s.endswith("}")) or (s.startswith("[") and s.endswith("]"))

    def _parse_json(self, tool_name: str, data: Any) -> dict[str, Any]:
        """把 JSON 解析成 agent 更容易用的字段。"""

        if tool_name == "get_current_weather" and isinstance(data, dict):
            location = data.get("location")
            temperature = data.get("temperature")
            condition = data.get("condition")
            return {
                "summary": f"{location} 当前 {condition}，温度 {temperature}",
                "location": location,
                "temperature": temperature,
                "condition": condition,
            }

        # 默认：原样放入，外加一个简短 summary
        return {
            "summary": f"{tool_name} 返回 JSON（已解析）",
            "data": data,
        }

    def _parse_text(self, tool_name: str, text: str) -> dict[str, Any]:
        """解析半结构化文本：提取关键信息，避免把大段噪声塞回 LLM。"""

        if tool_name == "fetch_webpage":
            title = self._extract_title(text)
            keywords = self._extract_keywords(text)
            return {
                "summary": f"网页抓取完成：{title or '未知标题'}",
                "title": title,
                "keywords": keywords,
                "raw_excerpt": text[:240],
            }

        return {
            "summary": f"{tool_name} 返回文本（未做专用解析）",
            "raw_excerpt": text[:240],
        }

    def _extract_title(self, text: str) -> str | None:
        m = re.search(r"^TITLE:\s*(.+)$", text, flags=re.MULTILINE)
        if m:
            return m.group(1).strip()
        return None

    def _extract_keywords(self, text: str) -> list[str]:
        m = re.search(r"^KEYWORDS:\s*(.+)$", text, flags=re.MULTILINE)
        if not m:
            return []
        return [w.strip() for w in m.group(1).split(",") if w.strip()]


# -----------------------
# 下面是“工具层”模拟：返回 raw output
# -----------------------

def tool_get_current_weather(location: str) -> str:
    """模拟工具：返回 JSON 字符串（更贴近 function calling 场景）。"""

    if "北京" in location:
        result = {"location": "北京", "temperature": 15, "condition": "晴"}
    elif "上海" in location:
        result = {"location": "上海", "temperature": 18, "condition": "多云"}
    else:
        result = {"location": location, "temperature": "未知", "condition": "未知"}
    return json.dumps(result, ensure_ascii=False)


def tool_fetch_webpage(url: str) -> str:
    """模拟工具：返回半结构化文本（像日志/抓取结果）。"""

    # 这里故意做成“文本”，让 ObservationModule 演示解析。
    return (
        "TITLE: Milvus Documentation\n"
        "KEYWORDS: Milvus, Vector Database, gRPC, Search\n"
        f"URL: {url}\n"
        "BODY: ...（省略大量正文/HTML）...\n"
    )


def run_demo() -> None:
    observer = ObservationModule()

    scenarios: list[tuple[str, dict[str, Any], str]] = [
        ("get_current_weather", {"location": "上海"}, tool_get_current_weather("上海")),
        ("fetch_webpage", {"url": "https://milvus.io/docs"}, tool_fetch_webpage("https://milvus.io/docs")),
    ]

    for tool_name, args, raw in scenarios:
        t0 = time.perf_counter()
        # 这里 raw 是“工具层”返回；真实系统中 raw 来自：HTTP/gRPC 响应、stdout、文件等
        latency_ms = int((time.perf_counter() - t0) * 1000)

        obs = observer.collect_and_parse(tool_name=tool_name, args=args, raw_output=raw, latency_ms=latency_ms)

        print("\n=" * 30)
        print(f"Tool: {obs.tool_name} | ok={obs.ok} | latency={obs.latency_ms}ms | type={obs.content_type}")
        print("Args:", obs.args)
        print("Raw:", obs.raw)
        print("Parsed:", json.dumps(obs.parsed, ensure_ascii=False, indent=2))
        if obs.parse_error:
            print("ParseError:", obs.parse_error)

    print("\n--- 如何把 Observation 喂回 LLM（示例）---")
    example_obs = observer.collect_and_parse(
        tool_name="get_current_weather",
        args={"location": "上海"},
        raw_output=tool_get_current_weather("上海"),
        latency_ms=3,
    )
    tool_message = {
        "role": "tool",
        "name": example_obs.tool_name,
        "content": json.dumps(example_obs.parsed, ensure_ascii=False),
    }
    print(json.dumps(tool_message, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    run_demo()
