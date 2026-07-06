"""
LangChain Runnable 基础类示例
演示如何自定义 Runnable 及其基本操作：invoke、batch、stream
"""
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from langchain_core.runnables import RunnableLambda, Runnable
from langchain_core.language_models.chat_model import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek


load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".ENV")


# ============ 方式1: 用 RunnableLambda 包装函数 ============
def add_one(x: int) -> int:
    """简单的 +1 函数"""
    return x + 1


def multiply_two(x: int) -> int:
    """简单的 *2 函数"""
    return x * 2


# 创建 Runnable
runnable_add = RunnableLambda(add_one)
runnable_mul = RunnableLambda(multiply_two)


# ============ 方式2: 使用管道组合（|）============
# 这里演示链式调用：先 +1，再 *2
chain = runnable_add | runnable_mul

print("=" * 60)
print("1. 单个 invoke（调用）")
print("=" * 60)
result = chain.invoke(5)  # (5 + 1) * 2 = 12
print(f"chain.invoke(5) = {result}")

print("\n" + "=" * 60)
print("2. batch（批处理）")
print("=" * 60)
results = chain.batch([1, 2, 3, 4, 5])  # 对多个输入并行处理
print(f"chain.batch([1, 2, 3, 4, 5]) = {results}")

print("\n" + "=" * 60)
print("3. stream（流式输出）")
print("=" * 60)
print("chain.stream(10):")
for chunk in chain.stream(10):
    print(f"  {chunk}")


# ============ 方式3: 自定义 Runnable 类 ============
class CustomRunnable(Runnable):
    """自定义 Runnable 类的示例"""

    def __init__(self, multiply_factor: int = 2):
        super().__init__()
        self.multiply_factor = multiply_factor

    def invoke(self, input: int) -> int:
        """必须实现的 invoke 方法"""
        return input * self.multiply_factor

    def batch(self, inputs: List[int], **kwargs):
        """可选：自定义 batch 以获得更好的性能"""
        return [self.invoke(x) for x in inputs]

    def stream(self, input: int, **kwargs):
        """可选：自定义 stream"""
        yield self.invoke(input)


custom_runnable = CustomRunnable(multiply_factor=3)

print("\n" + "=" * 60)
print("4. 自定义 Runnable")
print("=" * 60)
print(f"custom_runnable.invoke(5) = {custom_runnable.invoke(5)}")
print(f"custom_runnable.batch([1, 2, 3]) = {custom_runnable.batch([1, 2, 3])}")


# ============ 方式4: 与 LLM 组合 ============
print("\n" + "=" * 60)
print("5. 与 LLM 组合（Prompt + LLM）")
print("=" * 60)

# 定义 prompt
prompt = ChatPromptTemplate.from_template("告诉我关于 {topic} 的一个有趣事实。")

# 初始化 DeepSeek LLM
llm = ChatDeepSeek(model="deepseek-chat")

# 组合成链
llm_chain = prompt | llm

# 调用
try:
    response = llm_chain.invoke({"topic": "Python 编程语言"})
    print(f"LLM 响应: {response.content}")
except Exception as e:
    print(f"LLM 调用出错（可能是未配置 DEEPSEEK_API_KEY）: {e}")


# ============ 方式5: 链式操作示例 ============
print("\n" + "=" * 60)
print("6. 链式组合多个 Runnable")
print("=" * 60)

# 创建一个复杂的链：input | add_one | multiply_two | custom_runnable
complex_chain = runnable_add | runnable_mul | custom_runnable

result = complex_chain.invoke(2)
# ((2 + 1) * 2) * 3 = (3 * 2) * 3 = 6 * 3 = 18
print(f"complex_chain.invoke(2) = {result}")
print(f"expected: ((2 + 1) * 2) * 3 = 18")
