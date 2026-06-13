'''
Author: jinxudong 18751241086@163.com
Date: 2026-03-28 15:30:39
LastEditors: jinxudong 18751241086@163.com
LastEditTime: 2026-03-28 15:30:49
FilePath: \code\agent\main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict

# 加载 .env 文件中的环境变量
load_dotenv()

class DeepSeekLLM:
    """
    DeepSeek 客户端（基于 OpenAI 兼容接口）。
    默认使用流式响应。
    """
    def __init__(self, model: str = None, apiKey: str = None, baseUrl: str = None, timeout: int = None):
        """
        初始化 DeepSeek 客户端。
        优先使用传入参数；如果未提供，则从环境变量加载。

        推荐环境变量：
        - DEEPSEEK_API_KEY
        - DEEPSEEK_MODEL（默认 deepseek-chat）
        - DEEPSEEK_BASE_URL（默认 https://api.deepseek.com）
        - DEEPSEEK_TIMEOUT（默认 60）

        同时兼容旧变量：
        - LLM_API_KEY / LLM_MODEL_ID / LLM_BASE_URL / LLM_TIMEOUT
        """
        self.model = model or os.getenv("DEEPSEEK_MODEL") or os.getenv("LLM_MODEL_ID") or "deepseek-chat"
        apiKey = apiKey or os.getenv("DEEPSEEK_API_KEY") or os.getenv("LLM_API_KEY")
        baseUrl = baseUrl or os.getenv("DEEPSEEK_BASE_URL") or os.getenv("LLM_BASE_URL") or "https://api.deepseek.com"
        timeout = timeout or int(os.getenv("DEEPSEEK_TIMEOUT") or os.getenv("LLM_TIMEOUT", 60))
        
        if not all([self.model, apiKey, baseUrl]):
            raise ValueError("请提供 DeepSeek 的模型、API Key 和服务地址（可在 .env 中配置）。")

        self.client = OpenAI(api_key=apiKey, base_url=baseUrl, timeout=timeout)

    def think(self, messages: List[Dict[str, str]], temperature: float = 0) -> str:
        """
        调用大语言模型进行思考，并返回其响应。
        """
        print(f"🧠 正在调用 DeepSeek 模型：{self.model} ...")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True,
            )
            
            # 处理流式响应
            print("✅ 大语言模型响应成功:")
            collected_content = []
            for chunk in response:
                content = chunk.choices[0].delta.content or ""
                print(content, end="", flush=True)
                collected_content.append(content)
            print()  # 在流式输出结束后换行
            return "".join(collected_content)

        except Exception as e:
            print(f"❌ 调用LLM API时发生错误: {e}")
            return None

# --- 客户端使用示例 ---
if __name__ == '__main__':
    try:
        llmClient = DeepSeekLLM()
        
        exampleMessages = [
            {"role": "system", "content": "You are a helpful assistant that writes Python code."},
            {"role": "user", "content": "写一个快速排序算法"}
        ]
        
        print("--- 调用LLM ---")
        responseText = llmClient.think(exampleMessages)
        if responseText:
            print("\n\n--- 完整模型响应 ---")
            print(responseText)

    except ValueError as e:
        print(e)


