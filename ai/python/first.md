##### langchian

环境安装
安装最新的python即可，在vscode上安装jupyter插件。
需要一个openai的key，由于墙的原因需要找一个代理，

```python
import os
os.environ["OPENAI_KEY"] = "sk-I23bFbiP6pUIX4Fo2934BfAb93814745883eB82a5f994bD1"
os.environ["OPENAI_API_BASE"] = "https://ai-yyds.com/v1"
```

 在Python中，os模块提供了与操作系统进行交互的功能。通过os模块，你可以执行文件和目录操作，如创建、删除、移动文件和目录，获取文件属性，执行系统命令等。 
这里设置了两个环境变量， 以便在程序的其他部分中访问和使用 。

```python
import openai
import os

openai.api_key = os.getenv("OPENAI_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")

messages = [
{"role": "user", "content": "介绍下你自己"}
]

res = openai.ChatCompletion.create(
model="gpt-4-1106-preview",
messages=messages,
stream=False,
)

print(res['choices'][0]['message']['content'])
```

可以看到输出了一段话： 您好！我是一个由 OpenAI 开发的人工智能，名称是 ChatGPT。我的存在是基于 GPT-3 技术，这是一种先 ...

这里是官方的例子，也比较简单的调用了`gpt-4-1106-preview`模型，接下来更进一步的学习langchian框架。



##### prompts模板输入工程



```python
from langchain.llms import OpenAI
import os
# OPENAI_KEY
api_base = os.getenv("OPENAI_API_BASE")
api_key = os.getenv("OPENAI_KEY")
llm = OpenAI(
    model="gpt-3.5-turbo-instruct",
    temperature=0,
    openai_api_key=api_key,
    openai_api_base=api_base
    )
llm.predict("介绍下你自己")

输出： '\n\n我是一名来自广东的大学生，性格开朗、乐观向上。我喜欢阅读、旅行和运动，对新事物充满好奇心，喜欢不断学习和挑战自己。在校期间，我担任 。。。
```



llm.predict方法是用来向OpenAI模型发送输入文本，并获取模型生成的文本预测结果的方法。在这段代码中，传入的文本是"介绍下你自己"，模型会基于这个输入生成一个文本输出作为预测结果。这个方法可以用于生成文本、回答问题、完成句子等各种自然语言处理任务。



###### 字符串模板



```python
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import os
api_base = os.getenv("OPENAI_API_BASE")
api_key = os.getenv("OPENAI_KEY")
llm = OpenAI(
    model="gpt-3.5-turbo-instruct",
    temperature=0,
    openai_api_key=api_key,
    openai_api_base=api_base
    )
prompt = PromptTemplate.from_template("你是一个起名大师,请模仿示例起3个{county}名字,比如男孩经常被叫做{boy},女孩经常被叫做{girl}")
message = prompt.format(county="中国特色的",boy="狗蛋",girl="翠花")
print(message)
llm.predict(message)

输出：你是一个起名大师,请模仿示例起3个中国特色的名字,比如男孩经常被叫做狗蛋,女孩经常被叫做翠花
'\n\n男孩: 龙飞、铁柱、小虎\n女孩: 玉兰、梅子、小红梅'
```

langchain.prompts模块是用来提供预定义的文本模板，帮助用户生成各种文本输入，以便用于向OpenAI模型发送请求。

PromptTemplate类是用来创建和管理这些文本模板的工具，可以根据具体需求定制模板，然后将模板传递给OpenAI模型进行文本生成或处理。通过使用PromptTemplate类，用户可以更方便地构建输入文本，以获得更准确和符合预期的模型输出。

上面就通过from_template方法传入了一个模板，通过format方法将具体的值填充到模板上，最后将最终的信息投喂给模型，来获取指定的数据



###### 对话模板

```python
from langchain.prompts import ChatPromptTemplate

chat_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个老师. 你的名字叫{name}."),
        ("human", "你好{name},天王盖地虎，下面一句是啥？"),
        ("ai", "你好！宝塔镇河妖!"),
        ("human", "你叫什么名字呢?"),
        ("ai", "你好！我叫{name}"),
        ("human", "{user_input}"),
    ]
)

chat_template.format_messages(name="teacher王", user_input="哦，晓得了！")

输出：
[SystemMessage(content='你是一个老师. 你的名字叫teacher王.', additional_kwargs={}),
 HumanMessage(content='你好teacher王,天王盖地虎，下面一句是啥？', additional_kwargs={}, example=False),
 AIMessage(content='你好！宝塔镇河妖!', additional_kwargs={}, example=False),
 HumanMessage(content='你叫什么名字呢?', additional_kwargs={}, example=False),
 AIMessage(content='你好！我叫teacher王', additional_kwargs={}, example=False),
 HumanMessage(content='哦，晓得了！', additional_kwargs={}, example=False)]

```

这里使用了ChatPromptTemplate对话模板，入参就是一个list，list中有三个默认的系统角色，ai、system和human。

这里langchian是非常灵活的，可以直接去创建消息类型：

```python

from langchain.schema import SystemMessage
from langchain.schema import HumanMessage
from langchain.schema import AIMessage

# 直接创建消息
sy = SystemMessage(
  content="你是一个起名大师",
  additional_kwargs={"大师姓名": "陈瞎子"}
)

hu = HumanMessage(
  content="请问大师叫什么?"
)
ai = AIMessage(
  content="我叫陈瞎子"
)
[sy,hu,ai]

```



###### 自定义模板

当字符串模板和对话模板不能满足我们的需求时，就可以使用自定义模板。

```python
from langchain.prompts import StringPromptTemplate


# 定义一个简单的函数作为示例效果
def hello_world(abc):
    print("Hello, world!")
    return abc


PROMPT = """\
你是一个非常有经验和天赋的程序员，现在给你如下函数名称，你会按照如下格式，输出这段代码的名称、源代码、中文解释。
函数名称: {function_name}
源代码:
{source_code}
代码解释:
"""

import inspect


def get_source_code(function_name):
    #获得源代码
    return inspect.getsource(function_name)

#自定义的模板class
class CustmPrompt(StringPromptTemplate):

    
    def format(self, **kwargs) -> str:
        # 获得源代码
        source_code = get_source_code(kwargs["function_name"])

        # 生成提示词模板
        prompt = PROMPT.format(
            function_name=kwargs["function_name"].__name__, source_code=source_code
        )
        return prompt

a = CustmPrompt(input_variables=["function_name"])
pm = a.format(function_name=hello_world)

print(pm)

#和LLM连接起来
from langchain.llms import OpenAI
import os
api_base = os.getenv("OPENAI_PROXY")
api_key = os.getenv("OPENAI_API_KEY")

llm = OpenAI(
    model="gpt-3.5-turbo-instruct",
    temperature=0,
    openai_api_key=api_key,
    openai_api_base=api_base
    )
msg = llm.predict(pm)
print(msg)

输出：
你是一个非常有经验和天赋的程序员，现在给你如下函数名称，你会按照如下格式，输出这段代码的名称、源代码、中文解释。
函数名称: hello_world
源代码:
def hello_world(abc):
    print("Hello, world!")
    return abc

代码解释:

函数名称: hello_world
源代码:
def hello_world(abc):
    print("Hello, world!")
    return abc

代码解释:
这是一个名为hello_world的函数，它接受一个参数abc，并打印出"Hello, world!"，最后返回参数abc。它的作用是打印出"Hello, world!"这句话，并将参数abc返回。
```

 定义了一个函数`get_source_code`和一个自定义的模板类`CustmPrompt` ，`get_source_code`函数接受一个函数名作为参数，然后使用Python的inspect模块来获取该函数的源代码，最后将源代码作为字符串返回。

CustmPrompt类是一个自定义的提示词模板类，它继承自`StringPromptTemplate`类。该类中包含一个`format`方法，该方法接受关键字参数`kwargs`，其中应该包含一个名为`function_name`的函数对象。



###### F-string，jinji2与组合模板

f-string时python内置的一个代码引擎。

```python
from langchain.prompts import PromptTemplate

fstring_template = """
给我讲一个关于{name}的{what}故事
"""

prompt = PromptTemplate.from_template(fstring_template)

prompt.format(name="翠花", what="悲伤")

输出：
'\n给我讲一个关于翠花的悲伤故事\n'
```

这里直接用`"""`来用f-string模板

Jinja2是一个灵活、高效的Python模板引擎，可以方便地生成各种标记格式的文档。需要使用`pip install Jinja2 `安装一下

```python
from langchain.prompts import PromptTemplate

jinja2_template = "给我讲一个关于{{name}}的{{what}}故事"
prompt = PromptTemplate.from_template(jinja2_template, template_format="jinja2")

prompt.format(name="狗剩", what="高兴")

输出：
'给我讲一个关于狗剩的高兴故事'
```



组合模板，比如常见的三层性格设计：第一次层性格设计，第二层行为设计，第三层不允许的行为

```python
# Final Prompt由一系列变量构成
full_template = """{Character}
{behavior}
{prohibit}"""
full_prompt = PromptTemplate.from_template(full_template)

Character_template = """你是{person}，你有着{xingge}."""
Character_prompt = PromptTemplate.from_template(Character_template)

behavior_template = """你遵从以下的行为:
{behavior_list}
"""
behavior_prompt = PromptTemplate.from_template(behavior_template)

prohibit_template = """你不允许有以下行为:
{prohibit_list}
"""
prohibit_prompt = PromptTemplate.from_template(prohibit_template)

input_prompts = [
    ("Character", Character_prompt),
    ("behavior", behavior_prompt),
    ("prohibit", prohibit_prompt)
]
pipeline_prompt = PipelinePromptTemplate(final_prompt=full_prompt, pipeline_prompts=input_prompts)

pipeline_prompt.input_variables

pm = pipeline_prompt.format(
    person="埃隆马斯克",
    xingge="钢铁般的意志，你是世界首富，精通物理、天文、商业，你是商业奇才，你的终极梦想是殖民火星.",
    behavior_list="1.你喜欢冒险 \n 2.你非常崇拜爱因斯坦 \n 3.你总是乐于助人，回答用户各种问题.",
    prohibit_list="1.你不可以说自己是一个人工智能助手或者机器人 \n 2.当你不知道答案的时候，可以说让我再想想. "
)
print(pm)

输出：
你是埃隆马斯克，你有着钢铁般的意志，你是世界首富，精通物理、天文、商业，你是商业奇才，你的终极梦想是殖民火星..
你遵从以下的行为:
1.你喜欢冒险 
 2.你非常崇拜爱因斯坦 
 3.你总是乐于助人，回答用户各种问题.

你不允许有以下行为:
1.你不可以说自己是一个人工智能助手或者机器人 
 2.当你不知道答案的时候，可以说让我再想想. 
```





###### 序列化

使用文件来管理提示器有这么几个好处：

1. 便于共享
2. 便于版本管理
3. 便于存储

常见的格式就是yaml和json的格式

比如

。

```yaml
_type: prompt
input_variables:
    ["name","what"]
template:
    给我讲一个关于{name}的{what}故事
```

json

```json
{
    "_type":"prompt",
    "input_variables":["name","what"],
    "template":"给我讲一个关于{name}的{what}故事"
}
```

```python
from langchain.prompts import load_prompt

prompt = load_prompt("prompt.yaml")
print(prompt.format(name="小黑",what="恐怖的"))
```

```python
prompt = load_prompt("simple_prompt.json")
print(prompt.format(name="小红",what="搞笑的"))
```



###### 根据长度

```python
import os
os.environ["OPENAI_API_KEY"] = "sk-I23bFbiP6pUIX4Fo2934BfAb93814745883eB82a5f994bD1"
os.environ["OPENAI_PROXY"] = "https://ai-yyds.com/v1"

#使用openai的官方sdk
import openai
import os

openai.api_base = os.getenv("OPENAI_PROXY")
openai.api_key = os.getenv("OPENAI_API_KEY")

messages = [
{"role": "user", "content": "介绍下你自己"}
]

res = openai.ChatCompletion.create(
model="gpt-4-1106-preview",
messages=messages,
stream=False,
)

print(res['choices'][0]['message']['content'])

输出：
您好！我是一个人工智能助手，由OpenAI开发，使用了GPT-3技术。我的设计目的是帮助用户回答问题、提供信
```



```python
#根据输入的提示词长度综合计算最终长度，智能截取或者添加提示词的示例

from langchain.prompts import PromptTemplate
from langchain.prompts import FewShotPromptTemplate
from langchain.prompts.example_selector import LengthBasedExampleSelector

#假设已经有这么多的提示词示例组：
examples = [
    {"input":"happy","output":"sad"},
    {"input":"tall","output":"short"},
    {"input":"sunny","output":"gloomy"},
    {"input":"windy","output":"calm"},
    {"input":"高兴","output":"悲伤"}
]

#构造提示词模板
example_prompt = PromptTemplate(
    input_variables=["input","output"],
    template="原词：{input}\n反义：{output}"
)

#调用长度示例选择器
example_selector = LengthBasedExampleSelector(
    #传入提示词示例组
    examples=examples,
    #传入提示词模板
    example_prompt=example_prompt,
    #设置格式化后的提示词最大长度
    max_length=25,
    #内置的get_text_length,如果默认分词计算方式不满足，可以自己扩展
    #get_text_length:Callable[[str],int] = lambda x:len(re.split("\n| ",x))
)

#使用小样本提示词模版来实现动态示例的调用
dynamic_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix="给出每个输入词的反义词",
    suffix="原词：{adjective}\n反义：",
    input_variables=["adjective"]
)

#小样本获得所有示例
print(dynamic_prompt.format(adjective="big"))

输出：
给出每个输入词的反义词

原词：happy
反义：sad

原词：tall
反义：short

原词：sunny
反义：gloomy

原词：windy
反义：calm

原词：高兴
反义：悲伤

原词：big
反义：
```



```
#如果输入长度很长，则最终输出会根据长度要求减少
long_string = "big and huge adn massive and large and gigantic and tall and much much much much much much bigger then everyone"
print(dynamic_prompt.format(adjective=long_string))

输出：
给出每个输入词的反义词

原词：happy
反义：sad

原词：tall
反义：short

原词：big and huge adn massive and large and gigantic and tall and much much much much much much bigger then everyone
反义：
```





###### 根据mmr

根据输入相似度选择示例(最大边际相关性)



\- MMR是一种在信息检索中常用的方法，它的目标是在相关性和多样性之间找到一个平衡

\- MMR会首先找出与输入最相似（即余弦相似度最大）的样本

\- 然后在迭代添加样本的过程中，对于与已选择样本过于接近（即相似度过高）的样本进行惩罚

\- MMR既能确保选出的样本与输入高度相关，又能保证选出的样本之间有足够的多样性

\- 关注如何在相关性和多样性之间找到一个平衡





###### llms和chat models



###### 花销控制



###### 流式输出



##### 文档对话







#####  LangChain链与记忆处理 







