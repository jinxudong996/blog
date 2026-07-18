from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek


load_dotenv()


job_info_schema = {
    "title": "JobInfo",
    "description": "从招聘文本中提取职位信息",
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "description": "职位名称",
        },
        "company": {
            "type": [
                "string",
                "null",
            ],
            "description": (
                "公司名称，未知时返回null"
            ),
        },
        "salary_min": {
            "type": [
                "integer",
                "null",
            ],
            "minimum": 0,
            "description": (
                "最低月薪，单位为人民币元；"
                "将25k转换成25000；"
                "未知时返回null"
            ),
        },
        "salary_max": {
            "type": [
                "integer",
                "null",
            ],
            "minimum": 0,
            "description": (
                "最高月薪，单位为人民币元；"
                "将35k转换成35000；"
                "未知时返回null"
            ),
        },
        "skills": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "description": (
                "技能字符串数组，"
                "未知时返回空数组"
            ),
        },
    },
    "required": [
        "title",
        "company",
        "salary_min",
        "salary_max",
        "skills",
    ],
    "additionalProperties": False,
}


model = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
)

structured_model = model.with_structured_output(
    job_info_schema
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            你负责提取招聘信息。
            不要猜测原文中不存在的信息。
            薪资统一转换成以人民币元为单位的整数。
            """,
        ),
        (
            "human",
            "招聘信息：\n\n{text}",
        ),
    ]
)

chain = prompt | structured_model

result = chain.invoke(
    {
        "text": """
        星河科技招聘 Python 后端工程师，
        月薪25k-35k，要求熟悉Python、
        FastAPI和MySQL。
        """
    }
)

print("结果类型：", type(result))
print("完整结果：", result)

print("职位：", result["title"])
print("公司：", result["company"])
print("最低月薪：", result["salary_min"])
print("技能：", result["skills"])