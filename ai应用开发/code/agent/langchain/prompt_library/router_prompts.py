"""Task routing prompts."""

from langchain_core.prompts import ChatPromptTemplate


TASK_IDENTIFY_PROMPT_VERSION = "task_identify_v1"


task_identify_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一个任务路由助手，根据用户指令选择最合适的文章处理链。",
        ),
        (
            "human",
            """请根据用户指令判断任务类型。

只能返回下面 5 个值之一：
summarize
keywords
category
sentiment
analysis

判断规则：
- 用户想总结、概括、摘要文章时，返回 summarize。
- 用户想提取关键词、标签、主题词时，返回 keywords。
- 用户想判断文章类型、类别、题材时，返回 category。
- 用户想分析情绪、态度、倾向时，返回 sentiment。
- 用户想要完整分析，或者无法判断时，返回 analysis。

用户指令：
{instruction}

文章：
{article}
""",
        ),
    ]
)
