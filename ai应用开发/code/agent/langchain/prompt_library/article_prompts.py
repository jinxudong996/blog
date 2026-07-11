"""Article processing prompts."""

from langchain_core.prompts import ChatPromptTemplate


SUMMARY_PROMPT_VERSION = "summary_v1"
KEYWORDS_PROMPT_VERSION = "keywords_v1"
CATEGORY_PROMPT_VERSION = "category_v1"
SENTIMENT_PROMPT_VERSION = "sentiment_v1"


summary_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一个专业的中文内容编辑，擅长把长文章总结成清晰、准确、易读的摘要。",
        ),
        (
            "human",
            """请阅读下面的文章，并生成摘要。

要求：
1. 用中文回答。
2. 先给出 3-5 条核心要点。
3. 最后给出一句话总结。
4. 只基于文章内容总结，不要编造文章中没有的信息。

文章：
{article}
""",
        ),
    ]
)


keywords_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一个中文文本分析助手，擅长从文章中提取关键词。",
        ),
        (
            "human",
            """请从下面文章中提取 5-8 个关键词。

要求：
1. 只返回 JSON 数组。
2. 不要返回 Markdown。
3. 不要添加解释。

示例：
["关键词1", "关键词2", "关键词3"]

文章：
{article}
""",
        ),
    ]
)


category_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一个中文文章分类助手，擅长判断文章所属类别。",
        ),
        (
            "human",
            """请判断下面文章最适合的一个类别。

要求：
1. 只返回一个简短类别名称。
2. 不要添加解释。
3. 类别可以是：文学、科技、商业、教育、历史、社会、人物、生活、其他。

文章：
{article}
""",
        ),
    ]
)


sentiment_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一个中文情绪分析助手，擅长判断文章整体情绪倾向。",
        ),
        (
            "human",
            """请判断下面文章的整体情绪倾向。

要求：
1. 只返回一个词。
2. 可选值只能是：积极、消极、中性、复杂。
3. 不要添加解释。

文章：
{article}
""",
        ),
    ]
)
