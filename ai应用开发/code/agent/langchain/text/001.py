'''
Author: jinxudong 18751241086@163.com
Date: 2026-07-16 10:31:33
LastEditors: jinxudong 18751241086@163.com
LastEditTime: 2026-07-16 10:31:39
FilePath: \code\agent\langchain\text\001.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from dotenv import load_dotenv
from langchain_core.output_parsers import XMLOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek


load_dotenv()

model = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
)

parser = XMLOutputParser(
    tags=[
        "job",
        "title",
        "company",
        "salary",
        "min",
        "max",
        "skills",
        "skill",
    ]
)

prompt = ChatPromptTemplate.from_template(
    """
    从下面的招聘信息中提取职位信息。

    要求：
    - 只返回 XML
    - 不要返回 Markdown 代码块
    - 不要添加解释
    - 薪资统一转换为人民币元
    - 不要补充原文中没有的信息

    {format_instructions}

    XML 结构必须为：

    <job>
        <title>职位名称</title>
        <company>公司名称</company>
        <salary>
            <min>最低月薪</min>
            <max>最高月薪</max>
        </salary>
        <skills>
            <skill>技能名称</skill>
        </skills>
    </job>

    招聘信息：
    {text}
    """
).partial(
    format_instructions=(
        parser.get_format_instructions()
    )
)

chain = prompt | model | parser

result = chain.invoke(
    {
        "text": """
        星河科技招聘 Python 后端工程师，
        月薪 25k-35k，要求熟悉 Python、
        FastAPI 和 MySQL。
        """
    }
)

print("结果类型：", type(result))
print("解析结果：", result)