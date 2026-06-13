"""ReAct 的 Reasoning Module（思考组件）演示：决策下一步 Action。

ReAct 循环：Thought -> Action -> Observation -> Thought -> ... -> Final

这个 demo 的目的：把“思考组件”做成可运行、可观察的代码，而不是只讲概念。
- 不依赖 LLM：用规则/策略模拟推理（你把它换成 LLM 也很自然）
- 复用 observation_module_demo.py 的 Observation/ObservationModule 思路：
  Action 执行后得到 raw，再由观察组件标准化成 Observation，供思考组件使用。

运行：
  python agent/reasoning_module_demo.py
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Any, Literal


# -----------------------
# 1) 定义 Action（思考组件的输出）
# -----------------------


@dataclass
class Action:
    """思考组件输出：下一步要执行的动作。"""

    type: Literal["tool", "final"]
    tool_name: str | None = None
    tool_args: dict[str, Any] | None = None
    final_answer: str | None = None


# -----------------------
# 2) 观察组件（最小版）：把 raw 工具输出 -> 结构化 observation
# -----------------------


@dataclass
class Observation:
    tool_name: str
    args: dict[str, Any]
    ok: bool
    latency_ms: int
    raw: str
    parsed: dict[str, Any]
    error: str | None = None


class ObservationModule:
    def collect_and_parse(self, *, tool_name: str, args: dict[str, Any], raw_output: str, latency_ms: int) -> Observation:
        try:
            parsed = self._parse(tool_name, raw_output)
            return Observation(
                tool_name=tool_name,
                args=args,
                ok=True,
                latency_ms=latency_ms,
                raw=raw_output,
                parsed=parsed,
                error=None,
            )
        except Exception as exc:  # noqa: BLE001
            return Observation(
                tool_name=tool_name,
                args=args,
                ok=False,
                latency_ms=latency_ms,
                raw=raw_output,
                parsed={"summary": "解析失败", "raw_excerpt": raw_output[:200]},
                error=f"{type(exc).__name__}: {exc}",
            )

    def _parse(self, tool_name: str, raw: str) -> dict[str, Any]:
        raw_strip = raw.strip()
        if raw_strip.startswith("{") and raw_strip.endswith("}"):
            data = json.loads(raw_strip)
        else:
            data = raw_strip

        if tool_name == "get_current_weather" and isinstance(data, dict):
            return {
                "summary": f"{data.get('location')} 当前 {data.get('condition')}，温度 {data.get('temperature')}",
                **data,
            }

        if tool_name == "calculator" and isinstance(data, dict):
            return {
                "summary": f"计算结果：{data.get('result')}",
                **data,
            }

        return {"summary": f"{tool_name} 返回：{str(data)[:120]}", "data": data}


# -----------------------
# 3) 工具层（Action Module 执行的目标）
# -----------------------


def tool_get_current_weather(location: str) -> str:
    if "北京" in location:
        result = {"location": "北京", "temperature": 15, "condition": "晴"}
    elif "上海" in location:
        result = {"location": "上海", "temperature": 18, "condition": "多云"}
    else:
        result = {"location": location, "temperature": "未知", "condition": "未知"}
    return json.dumps(result, ensure_ascii=False)


def tool_calculator(expression: str) -> str:
    """极简计算器：只演示。真实项目不要 eval，改用安全解析器。"""

    allowed = set("0123456789+-*/(). ")
    if any(ch not in allowed for ch in expression):
        return json.dumps({"ok": False, "error": "表达式包含非法字符"}, ensure_ascii=False)
    try:
        result = eval(expression, {"__builtins__": {}}, {})  # noqa: S307
        return json.dumps({"ok": True, "result": result}, ensure_ascii=False)
    except Exception as exc:  # noqa: BLE001
        return json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False)


TOOLS = {
    "get_current_weather": tool_get_current_weather,
    "calculator": tool_calculator,
}


# -----------------------
# 4) 思考组件（Reasoning Module）
# -----------------------


class ReasoningModule:

    def decide(self, query: str, observations: list[Observation]) -> tuple[str, Action]:
        # ---- 1) 先“读” observation（这一步是 reasoning 最容易做差的地方）
        if observations:
            last = observations[-1]
            if not last.ok:
                thought = f"上一次工具调用失败({last.tool_name})，先给用户说明并停止。"
                return thought, Action(type="final", final_answer=f"工具执行/解析失败：{last.error}，我先停止。")

            # 如果上一轮已经拿到足够信息，就收敛输出 final
            if last.tool_name == "get_current_weather":
                thought = "已经获取到天气信息，直接组织最终回答。"
                summary = last.parsed.get("summary", "")
                return thought, Action(type="final", final_answer=summary)

            if last.tool_name == "calculator":
                thought = "已经计算完成，直接返回结果。"
                return thought, Action(type="final", final_answer=last.parsed.get("summary", "计算完成"))

        # ---- 2) 再决定要不要用工具，以及选哪个工具
        q = query.strip()

        # 规则：问天气就调用天气工具
        if "天气" in q:
            location = "北京" if "北京" in q else "上海" if "上海" in q else "你所在城市"
            thought = f"用户在问天气，调用 get_current_weather(location={location}) 获取实时信息。"
            return thought, Action(type="tool", tool_name="get_current_weather", tool_args={"location": location})

        # 规则：能识别出简单算式就调用计算器
        if any(ch.isdigit() for ch in q) and any(op in q for op in ["+", "-", "*", "/"]):
            expr = self._extract_expression(q)
            thought = f"用户像是在求值，调用 calculator(expression={expr})。"
            return thought, Action(type="tool", tool_name="calculator", tool_args={"expression": expr})

        # 否则直接回答
        thought = "不需要工具，直接回答。"
        return thought, Action(type="final", final_answer="我可以帮你查天气或做简单计算，你可以直接问：上海天气怎么样？或 12*(3+4)=多少")

    def _extract_expression(self, text: str) -> str:
        allowed = set("0123456789+-*/(). ")
        expr = "".join(ch for ch in text if ch in allowed).strip()
        return expr or text


# -----------------------
# 5) 把三件套串起来：ReAct Loop
# -----------------------


def react_loop(query: str) -> str:
    reasoner = ReasoningModule()
    observer = ObservationModule()

    observations: list[Observation] = []

    for step in range(1, 6):
        thought, action = reasoner.decide(query, observations)
        print(f"\n[Step {step}] Thought: {thought}")

        if action.type == "final":
            answer = action.final_answer or ""
            print(f"[Step {step}] Final: {answer}")
            return answer

        if action.type == "tool":
            tool_name = action.tool_name or ""
            tool_args = action.tool_args or {}
            print(f"[Step {step}] Action: call {tool_name} args={tool_args}")

            t0 = time.perf_counter()
            raw = TOOLS[tool_name](**tool_args)
            latency_ms = int((time.perf_counter() - t0) * 1000)

            obs = observer.collect_and_parse(tool_name=tool_name, args=tool_args, raw_output=raw, latency_ms=latency_ms)
            observations.append(obs)

            print(f"[Step {step}] Observation: ok={obs.ok} latency={obs.latency_ms}ms summary={obs.parsed.get('summary')}")
            continue

    return "达到最大步数，停止。"


def main() -> None:
    examples = [
        "上海天气怎么样？",
        "帮我算一下 12*(3+4) 等于多少",
        "你是谁",
    ]

    for q in examples:
        print("\n" + "-" * 60)
        print("Query:", q)
        react_loop(q)


if __name__ == "__main__":
    main()
