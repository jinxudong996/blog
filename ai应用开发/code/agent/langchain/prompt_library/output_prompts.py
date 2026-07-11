"""Final output prompts."""

from langchain_core.prompts import ChatPromptTemplate


FINAL_ANSWER_PROMPT_VERSION = "final_answer_v1"


final_answer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一个中文文章处理助手，负责把工作流结果整理成清晰、自然、适合直接展示给用户的回答。",
        ),
        (
            "human",
            """请根据下面的工作流结果，生成最终回答。

要求：
1. 用中文回答。
2. 不要提及内部 chain、Runnable、workflow 等实现细节。
3. 如果 result 是列表，整理成简洁列表。
4. 如果 result 是对象，按字段含义组织成易读内容。
5. 如果 task 是 analysis，输出摘要、关键词、分类、情绪四部分。

任务类型：
{task}

工作流结果：
{result}
""",
        ),
    ]
)
