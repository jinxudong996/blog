'''
Author: jinxudong 18751241086@163.com
Date: 2026-06-15 16:38:34
LastEditors: jinxudong 18751241086@163.com
LastEditTime: 2026-06-15 16:39:55
FilePath: \code\agent\langchain\wherther,py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent


load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".ENV")


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="deepseek:deepseek-chat",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)