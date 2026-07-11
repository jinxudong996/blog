理解 LangChain Core 的设计思想。
掌握：
Runnable
Prompt
Model
Output
LCEL
能够独立开发简单 AI 工作流。

### 前置

首先安装下环境

首先开启一个虚拟环境，然后安装一些依赖

```python
pip install -U langchain
pip install langchain-deepseek
```

我使用的deepseek的key，就安装的是deepseek的依赖，然后跑一下文档中的例子：

```python
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
```

```
#输出
[{'type': 'text', 'text': 'The weather in San Francisco is **always sunny**! 🌤️ A beautiful day in the City by the Bay!'}]
```

### 一、langchain 技术栈全景图

#### 1、LangChain 在 AI 应用中的定位

LangChain 是目前最主流的大模型应用开发框架，它不负责训练大模型，而是帮助开发者更高效地构建 AI 应用。

刚开始做 AI 项目时，直接调用 OpenAI、Claude 或 DeepSeek 的 API 就能快速写出 Demo。但项目一旦变复杂，各种问题就会接踵而来：

- Prompt 越来越长，越来越难维护；
- 工具越来越多，调用逻辑越来越乱；
- 知识库和 RAG 不知道怎么接；
- 多步骤任务流程难以管理；
- Token 消耗、调用链路和线上问题难排查。

这些问题几乎是所有 AI 项目都会遇到的共性问题。

这就像早期 Web 开发可以直接写原生代码，但随着项目规模变大，大家最终都会选择 Spring、Django 这类框架。因为框架帮你解决了大量重复性的工程问题。

LangChain 在 AI 领域扮演的也是类似角色。它把 Prompt 管理、Tool Calling、RAG、工作流编排以及可观测性等能力进行了统一封装，让开发者不用重复造轮子，可以把更多精力放在业务逻辑上。

对于想从 Demo 走向生产环境的开发者来说，LangChain 已经成为 AI 应用开发的基础。

#### 2 LangChain 生态组成

`langchain`之所以成为目前最主流的AI 应用开发基础框架，在于其非常完善的生态，接下来就详细的介绍下：

##### LangChain Core

这是`langchian`的基石，就是整个生态的统一接口规范，不做具体的实现，定义好大模型、 聊天模型、检索器、工具、消息等核心概念的标准协议 。让上层所有组件都能按同一个标准对接。 

##### LangChain

这部分是工具与生态集成，基于`Core`的标准接口，做了大量的生态对接：上百家大模型的接入封装、几十种向量数据库的适配、各类第三方工具（搜索引擎、代码执行器、业务 API 等）的集成，同时还提供了很多封装好的常用链路（比如检索问答链、总结链）。 

##### LangGraph

这部分负责状态流与Agent编排。将每一步逻辑定义成节点，把判断条件定义成边，轻松搭建出带状态、支持循环分支的工作流，不用自己手写一堆状态管理和循环判断的代码。 

##### LangSmith

这块负责调试与评估，开发阶段它能完整记录每一次调用的全链路：输入输出、Token 消耗、每一步工具的执行结果、中间变量，排查问题一目了然；上线后可以用来做效果评估、版本对比，量化 Prompt 优化、策略调整带来的变化。 

##### LangServe

这块是API部署工具，可以把你写好的链、Agent 快速打包成标准的 REST API，自带流式输出支持，不用你自己从零搭 FastAPI 服务、处理请求响应格式。几行代码就能把本地应用部署成可调用的线上服务，大幅缩短从开发到上线的路径。 

#### 3 从 Chain 到 LCEL

早期 LangChain 靠各类封装好的 Chain（如 LLMChain、RetrievalQA）快速出圈，搭 Demo 很省事，但落地生产时短板明显：一是黑盒感强，逻辑都封死在类里，想改中间逻辑、加自定义处理就得重写，灵活度极低；二是仅支持线性执行，分支、并行、循环这类复杂流程无法原生实现；三是生产能力缺失，流式输出、异步、批处理支持很差，常需要外层额外补逻辑；四是 Chain 种类繁杂，参数用法各不相同，学习和维护成本都高。

LCEL 的核心是把所有组件统一为标准 Runnable 接口，用管道符 `|` 像搭积木一样拼接链路。它成为官方主线，正是解决了旧 Chain 的核心问题：写法直观易读，增改组件灵活；原生自带流式、异步、批处理等生产能力；支持分支、并行、嵌套等复杂组合；和 LangSmith、LangServe 生态天然打通；同时大幅降低了学习心智负担。本质是从 “封装好的成品” 转向 “标准化积木”，换来了生产环境下的可扩展性。

### 二、Runnable：langchian的统一执行模型

#### 2.1 为啥需要Runnable

常规的Python方法，一个输入一个输出，然而在AI调用的时候，通常不是一个函数可以完成的，有很多组件串联起来的，比如：

```python
prompt = ChatPromptTemplate.from_template("请用一句话解释：{topic}")
model = ChatOpenAI()
parser = StrOutputParser()
```

这三行代码本质都像是函数，接受输入，产生输出，但是如果没有一个统一抽象，他们的调用方式就会差距大：

```python
prompt.format(topic="Runnable")
model.predict(...)
parser.parse(...)
```

每个方法都有自己的输入格式、输出格式，如果要串联起来就要手动处理每一步的适配，就需要额外写很多的胶水代码，而`Runnable `的出现就是为了解决胶水代码爆炸的问题，由一个统一的协议，不管是Prompt、Model、parser还是自定义函数，都尽量的表现得像同一种东西，这个就是`Runnable `。

在`LangChain`中，所有可执行组件，都被抽象成了`Runnable`，统一输入，统一输出，还有统一的执行方式，于是AI应用组件就可以轻松的组装成稳定、可组合、可调式、可扩展的工作流，而 `Runnable` 正是这个工作流的基础单位 

前面的例子现在就可以这样写了

```python
chain = prompt | model | parser

chain.invoke({"topic": "LangChain"})
```

这就是 LangChain Expression Language，也就是 LCEL 的核心写法。

这里的 `|` 不是普通管道符的装饰用法，而是在创建一个 `RunnableSequence`：前一个 Runnable 的输出，作为后一个 Runnable 的输入。官方源码文档里也说明，Runnable 可以通过 `|` 组合成序列，也可以通过 dict 组合成并行结构 



#### 2.2 Runnable 的设计思想

`Runnable`可以翻译为可运行对象，不是单纯的python函数，也不是普通类方法，而是Langchain定义的一套标准接口。

普通的方法是这样定义的：

```python
def add_one(x):
    return x + 1

add_one(1)
```

而`Runnable`是这样的：

```python
runnable.invoke(1)
```

从使用者的角度来看，`Runnable`可以理解为：一个接受Input，产生Output的可执行组件。

这里的输入输出，并不是简单的字符串，而是一个泛型，也就是说输入输出的格式，由组件使用时自己声明。

 `Runnable`也是有生命周期的，可以将`Runnable`的一次运行拆成五个阶段：

- 输入：用户传入Input，比如

  ```
  chain.invoke({"topic": "LangChain"})
  ```

  这个Input就会进入`Runnable`

- 执行，`Runnable`开始执行自己的核心逻辑

  不同组件功能也不一样

  ```
  PromptTemplate：格式化提示词
  ChatModel：调用大模型
  OutputParser：解析模型输出
  Retriever：检索文档
  Tool：执行外部动作
  Chain：执行一组 Runnable
  ```

  比如：

  ```
  prompt.invoke({"topic": "Runnable"}) #将变量塞入模板
  model.invoke(prompt_value) #调用聊天模型
  parser.invoke(ai_message) #将模型消息转成目标格式
  ```

  

- 输出

   每个 Runnable 执行完都会返回 Output 

  ```
  PromptTemplate 输出 PromptValue
  ChatModel 输出 AIMessage
  StrOutputParser 输出 str
  Retriever 输出 list[Document]
  Tool 输出任意结果
  Chain 输出最后一步的结果
  ```

  ```
  chain = prompt | model | parser # 这个输出的就是 parser 的输出
  ```

- 异常处理

  在批量调用时，

  ```
  runnable.batch(inputs, return_exceptions=True)
  ```

  某个输入失败，会将异常作为结果返回，而不是将整个批处理中断

  ```
  chain = chain.with_retry()
  ```

  可以给Runnable 加重试能力 

   `try / except` 去包括代码，也可以的

- 配置

   Runnable 的调用可以带 `config` 

所有的可执行组件都是`Runnable`，因为 LangChain 想要建立一个统一的 AI 应用执行模型 ，只要所有的组件都实现了`Runnable`，就可以做到统一调用、统一组合、统一配置、统一追踪。

下面看几个实现了`Runnable`的核心组件：

-  ChatModel  

  这个组件就是输出模型的回复，实现了`Runnable`，就可以轻松的链式调用：

  ```
  chain = prompt | model
  ```

  ChatModel 的输入可以是字符串、消息列表或 PromptValue，输出通常是 BaseMessage / AIMessage。LangChain 源码里的 `BaseChatModel` 文档也列出了 `invoke`、`stream`、`batch` 等标准 Runnable 方法。 

- PromptTemplate 

  这个组件生成prompt，处于链路中的第一步，

- OutputParser

  这个组件是最终模型的结构化输出，是整个链路的最后一步，

  ```
  chain = prompt | model | parser
  ```

   源码里 `BaseOutputParser` 继承自 `RunnableSerializable[LanguageModelOutput, T]`，意思是它接收语言模型输出，返回泛型结果 `T` 

- Retriever

  这个组件输出相关的文档列表，Retriever 成为 Runnable 之后，就可以很自然地进入 RAG 流程。

  源码里 `BaseRetriever` 明确是 `RunnableSerializable[str, list[Document]]`，并且文档说明 Retriever 遵循标准 Runnable 接口，可以通过 `invoke`、`ainvoke`、`batch`、`abatch` 使用。 

- Tool

  这个组件是调用工具的执行结果。

   源码里 `BaseTool` 继承自 `RunnableSerializable[str | dict[str, Any] | ToolCall, Any]`，说明 Tool 也是标准 Runnable。 

- Chain

  这个就是一个链，也是一个Runnable ，而多个 Runnable 组合出来的更大的 Runnable。

   官方源码里也说明，Runnable 可以通过 `|` 组成 `RunnableSequence`，也可以通过 dict 组成并行结构 `RunnableParallel` 

#### 2.3 Runnable核心API

先看一个简单的实例

```
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template("请用一句话解释：{topic}")
model = ChatOpenAI()
parser = StrOutputParser()

chain = prompt | model | parser
result = chain.invoke({"topic": "Runnable"})
print(result)
```

这里的`chain`就是一个最基础的链，后续的API都是基于他的。

###### invoke()

最基础的`chain`同步调用方式，输出这个链的最终结果。

他的返回值取决于链的最后一步，上面的案例，最终输出的就是parser的最终结果。

###### ainvoke()

 `ainvoke()` 是 `invoke()` 的异步版本。 

```python
result = await chain.ainvoke({"topic": "Runnable"})
print(result)
```



###### batch()

 `batch()` 用来批量执行多个输入。 

```python
results = chain.batch([
    {"topic": "Runnable"},
    {"topic": "LCEL"},
    {"topic": "Agent"},
])

print(results)
#输出
[
    "Runnable 是……",
    "LCEL 是……",
    "Agent 是……"
]
```

 LangChain 源码里说明，`batch()` 的默认实现会用线程池并行调用 `invoke()`，适合 IO-bound 的 Runnable，比如模型请求、网络请求、检索请求等 

 默认情况下，只要某个输入报错，整个 `batch()` 可能抛异常。

```python
results = chain.batch(
    inputs,
    return_exceptions=True
)
#这样失败项会以异常对象的形式返回。
```

###### abatch()

  `abatch()` 是 `batch()` 的异步版本。 

它适合异步环境下批量处理。

源码里 `abatch()` 默认通过 `asyncio.gather` 并行运行多个 `ainvoke()`，并且同样支持 `return_exceptions` 和 `max_concurrency`。



###### stream()

 `stream()` 用来流式输出。 

```python
for chunk in chain.stream({"topic": "Runnable"}):
    print(chunk, end="", flush=True)
```

它不会等完整结果生成完才返回，而是边生成边吐出 chunk。

 LangChain 官方 Streaming 文档也强调，流式输出可以在完整结果准备好之前逐步展示内容，从而提升 LLM 应用的响应体验。 

###### astream()

`astream()` 是 `stream()` 的异步版本。

```python
async for chunk in chain.astream({"topic": "Runnable"}):
    print(chunk, end="", flush=True)
```

它适合异步服务中把模型输出实时推给前端。

###### stream_events()

`stream_events()` 用来获取“事件流”。

前面的 `stream()` 更关心最终内容：

```
模型生成了哪些 token？
```

而 `stream_events()` 更关心执行过程：

```
哪一步开始了？
哪一步结束了？
模型什么时候开始？
模型吐出了哪些 chunk？
parser 有没有执行？
retriever 有没有返回？
tool 有没有调用？
```

也就是说：

```
stream() 看输出内容
stream_events() 看执行过程
```

LangChain 当前文档里，新的 agent / graph streaming 推荐使用 event streaming，特别是 `version="v3"` 的 typed projection API；而源码里也能看到，基础 Runnable 的同步 `stream_events()` 对 v1/v2 并不通用，v3 需要具体子类支持，比如 BaseChatModel 或 LangGraph CompiledGraph。实际项目里，如果你用的是普通 Runnable 链，常见选择是用异步的 `astream_events(..., version="v2")`。



#### 2.4 Runnable的组合能力

`Runnable` 的组合能力，就是把多个“可运行单元”拼成一个更大的“可运行单元”。小 Runnable 能组合，大 Runnable 仍然是 Runnable，所以整条链还能继续 `invoke()`、`batch()`、`stream()`。

官方文档里也明确说，Runnable 主要组合原语是 `RunnableSequence` 和 `RunnableParallel`：前者顺序执行，后者并行执行；`|` 会创建 Sequence，dict 会被转换成 Parallel。



###### pipe()

 `pipe()` 是 Runnable 的链式组合方法。 

```python
chain = prompt.pipe(model).pipe(parser)

chain = prompt | model | parser

from langchain_core.runnables import RunnableSequence
chain = RunnableSequence(prompt, model, parser)
```

上面的三种写法完全一样，就是将当前 Runnable 和后面的 Runnable 串起来，形成 RunnableSequence。

###### RunnableParallel

 `RunnableParallel` 是并行组合。就是将一个输入，同时交给多个 Runnable 执行，然后把结果合并成一个 dict。

```python
from langchain_core.runnables import RunnableParallel, RunnableLambda

parallel = RunnableParallel(
    double=RunnableLambda(lambda x: x * 2),
    triple=RunnableLambda(lambda x: x * 3),
)

parallel.invoke(10)
#输出
{
    "double": 20,
    "triple": 30
}
```

 `RunnableParallel` 会并发调用多个 Runnable，并把相同输入提供给每个 Runnable；它可以直接实例化，也可以在 Sequence 中使用 dict 字面量创建。 

###### RunnableBranch

根据输入判断条件，选择其中一条 Runnable 执行。

```python
from langchain_core.runnables import RunnableBranch

branch = RunnableBranch(
    (lambda x: x["type"] == "translate", translate_chain),
    (lambda x: x["type"] == "summary", summary_chain),
    default_chain,
)

branch.invoke({"type": "summary", "text": "..."})

#执行过程
是否 translate？否
是否 summary？是
执行 summary_chain
```

 一个常见例子：简单问题直接回答，复杂问题走 RAG。 

```python
branch = RunnableBranch(
    (
        lambda x: len(x["question"]) < 20,
        simple_qa_chain,
    ),
    rag_chain,
)
```

###### RunnableAssign

 `RunnableAssign` 用来向 dict 数据中追加字段，就是输入一个 dict，计算一些新字段，再把新字段合并回原 dict。

```python
from langchain_core.runnables import RunnablePassthrough

chain = RunnablePassthrough.assign(
    question_length=lambda x: len(x["question"])
)

chain.invoke({"question": "什么是 Runnable？"})
#输出
{
    "question": "什么是 Runnable？",
    "question_length": 13
}
```

###### RunnablePassthrough

 `RunnablePassthrough` 是“原样传递”。 

```python
from langchain_core.runnables import RunnablePassthrough

passthrough = RunnablePassthrough()

passthrough.invoke("hello")
#输出
"hello"
```

 最常见场景：并行时保留用户原始问题。 

```python
from operator import itemgetter
from langchain_core.runnables import RunnablePassthrough

chain = {
    "question": RunnablePassthrough(),
    "context": retriever,
} | prompt | model | parser

#输入
"Runnable 是什么？"
#输出
{
    "question": "Runnable 是什么？",
    "context": [Document(...), Document(...)]
}
```



#### 2.5 Runnable 的增强能力 

增强就是不会改变`Runnable `的核心逻辑，返回一个新的`Runnable `



###### bind()

 `bind()` 用来给 Runnable 绑定固定参数，这个参数以后每次调用都自动带上。

```
model_with_stop = model.bind(stop=["\n\n"])

chain = prompt | model_with_stop | parser

chain.invoke({"topic": "Runnable"})
```

后续再调用model的时候，就会自动带上`stop=["\n\n"]`

比较常见的用法就是绑定工具

```
model_with_tools = model.bind_tools([search_tool, calculator_tool])
```



###### assign()

`assign()` 用来给 Runnable 的输出增加字段，它要求前一个 Runnable 的输出是 dict，然后在这个 dict 上追加新字段。

```python
chain = some_chain.assign(
    length=lambda x: len(x["text"])
)
#输入
{"text": "hello"}
#输出
{
    "text": "hello",
    "length": 5
}
```

使用场景一般在RAG中

```python
from operator import itemgetter

chain = RunnablePassthrough.assign(
    context=itemgetter("question") | retriever
)
#输入
{"question": "Runnable 是什么？"}
#输出
{
    "question": "Runnable 是什么？",
    "context": [Document(...), Document(...)]
}
```

###### map()

 `map()` 用来把一个 Runnable 变成“可以处理列表输入”的 Runnable。 

```python
from langchain_core.runnables import RunnableLambda

add_one = RunnableLambda(lambda x: x + 1)

mapped = add_one.map()

mapped.invoke([1, 2, 3])

#输出
[2, 3, 4]
```

 `map()` 会返回一个新的 Runnable，它接收一组输入，逐个调用原 Runnable，然后返回输出列表 

###### pick()

 `pick()` 用来从 Runnable 的 dict 输出中选择字段。 

```python
chain = chain.pick("answer")
#如果原始输出是这样
{
    "answer": "Runnable 是 LangChain 的统一执行接口",
    "sources": [...],
    "debug": {...}
}
#pick("answer") 后输出就是：
"Runnable 是 LangChain 的统一执行接口"
```



###### with_config()

 `with_config()` 用来给 Runnable 绑定运行配置。 

```python
chain = chain.with_config(
    tags=["lesson-2", "runnable"],
    metadata={"chapter": "2.5"},
    run_name="runnable_enhanced_demo"
)

chain.invoke({"topic": "Runnable"})
#这些配置会跟着本次运行进入 tracing / callbacks / 子链。
```

###### with_retry()

 `with_retry()` 用来给 Runnable 增加失败自动重试。 

```python
chain = chain.with_retry(
    stop_after_attempt=3
)
```

如果 chain 执行失败，最多尝试 3 次。

常见的配置：

```python
chain = chain.with_retry(
    retry_if_exception_type=(TimeoutError, ConnectionError),
    stop_after_attempt=3,
    wait_exponential_jitter=True,
)

#含义
只在 TimeoutError 或 ConnectionError 时重试
最多尝试 3 次
重试间隔使用指数退避加随机抖动
```

###### with_fallbacks()

 `with_fallbacks()` 用来给 Runnable 增加备用方案。 

```python
chain = primary_chain.with_fallbacks([backup_chain])
#含义
先执行 primary_chain
如果失败，执行 backup_chain
如果还失败，再执行下一个 fallback
```



#### 2.6 Runnable 的执行过程

这一节很多教程没有讲，其实非常重要。

一次 invoke 到底发生了什么？

Input

↓

Runnable

↓

Transform

↓

Next Runnable

↓

Output

数据在 Runnable 之间如何流动

为什么 LCEL 可以无限组合







#### 2.7 Runnable 最佳实践

会写`chain = prompt | model | parser`只是很基础的认知，真正重要的是：怎么拆、怎么组合、怎么复用、怎么调试、怎么优化性能。 

######  什么时候拆 Runnable 

 当某一步逻辑有明确职责时，就应该拆成独立 Runnable。 

比如一个 RAG 流程：

```
用户问题
  -> 查询改写
  -> 检索文档
  -> 格式化上下文
  -> 构造 Prompt
  -> 调用模型
  -> 解析输出
```

不要写成一个巨大函数：

```
def rag(question):
    # 改写问题
    # 检索文档
    # 拼 prompt
    # 调模型
    # 解析结果
    # 返回答案
```

更好的方式是拆成多个 Runnable：

```
query_rewrite_chain = rewrite_prompt | model | parser
retrieval_chain = query_rewrite_chain | retriever
answer_chain = prompt | model | parser
```

拆 Runnable 的判断标准：

```
这一步能不能单独测试？
这一步能不能被别的链复用？
这一步出错时，我是否希望单独定位？
这一步是否有独立输入和输出？
```

如果答案是“是”，就适合拆出来。

######  什么时候组合 Runnable 

 当多个 Runnable 共同完成一个业务流程时，就应该组合。 

 组合 Runnable 的判断标准： 

```
这些步骤是不是天然有先后顺序？
上一步输出是不是下一步输入？
调用方是否只关心最终结果？
这组流程是否经常一起出现？
```

如果是，就组合成一个新的 chain。

组合后的 chain 本身仍然是 Runnable，所以可以继续组合：

```
answer_chain = prompt | model | parser
stable_answer_chain = answer_chain.with_retry()
api_chain = stable_answer_chain.with_config(run_name="answer_api")
```

这就是 Runnable 最舒服的地方：

```
小组件组合成大组件，大组件仍然能当小组件使用。
```

######  如何保证可维护性 

第一，给关键 Runnable 命名。

```
retriever = retriever.with_config(run_name="knowledge_retriever")
answer_chain = answer_chain.with_config(run_name="answer_chain")
```

这样在 tracing 或事件流里能看清楚每一步。

第二，保持输入输出清晰。

不要让一个链的输入格式忽左忽右。

推荐：

```
{
    "question": "...",
    "context": "...",
    "history": [...]
}
```

不推荐一会儿传字符串，一会儿传 dict，一会儿传复杂对象。

第三，中间状态尽量用 dict 表达。

比如：

```
chain = RunnablePassthrough.assign(
    context=itemgetter("question") | retriever
) | prompt | model | parser
```

这样数据流很清楚：

```
先有 question
再追加 context
然后进入 prompt
```

第四，不要把业务逻辑藏在匿名 lambda 里太多。

少量可以：

```
lambda x: x["question"]
```

复杂逻辑应该拆成函数：

```
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
```

然后再包成 Runnable：

```
format_docs_runnable = RunnableLambda(format_docs)
```

######  如何提高复用性 

复用性的核心是：不要让 Runnable 绑定太多具体业务上下文。

比如这个不太好复用：

```
customer_service_chain = prompt | model | parser
```

如果 prompt 里写死了某个产品、某个用户、某个场景，那它只能服务一个地方。

更好的方式是把变量暴露出来：

```
prompt = ChatPromptTemplate.from_template("""
你是一个{role}。
请用{tone}的语气回答用户问题：

{question}
""")
```

这样同一个 Runnable 可以用于多个场景：

```
chain.invoke({
    "role": "客服助手",
    "tone": "友好",
    "question": "怎么退款？"
})
```

提高复用性的几个方法：

```
Prompt 参数化，不要写死变量。
Parser 独立出来，不要混在模型调用后面。
Retriever 独立出来，方便替换知识库。
Model 独立出来，方便换模型或 fallback。
格式化逻辑独立出来，方便复用和测试。
```

######  避免一个 Runnable 做太多事情 

一个 Runnable 最好只做一类事情。

不推荐：

```
一个 Runnable 同时负责：
清洗输入
检索文档
拼 prompt
调用模型
解析 JSON
写数据库
返回 API 响应
```

这会导致几个问题：

```
难测试
难复用
难调试
难替换
难定位性能瓶颈
```

更好的方式：

```
clean_input
  -> retrieve_docs
  -> format_context
  -> prompt
  -> model
  -> parser
  -> save_result
```

每一步都很小，但组合起来很强。

######  保持单一职责 

单一职责可以这样判断：

```
这个 Runnable 的名字能不能用一个动词说清楚？
```

好名字：

```
rewrite_query
retrieve_docs
format_context
generate_answer
parse_json
rank_documents
```

不好的名字：

```
do_everything
process
main_chain
handle_user_request
```

如果一个 Runnable 的名字只能叫 `process`，通常说明它做太多了。

一个好的 Runnable 应该像这样：

```
format_docs = RunnableLambda(lambda docs: "\n\n".join(
    doc.page_content for doc in docs
))
```

职责非常清楚：

```
输入 docs
输出格式化后的 context 字符串
```

###### 最佳实践总结

```
拆 Runnable：
当某一步有独立职责、可测试、可复用时拆。

组合 Runnable：
当多个步骤构成稳定业务流程时组合。

维护性：
命名清楚，输入输出稳定，中间状态用 dict，复杂逻辑不要藏在 lambda 里。

复用性：
Prompt 参数化，模型独立，Parser 独立，Retriever 独立。

单一职责：
一个 Runnable 只做一类事情。

性能：
批量任务用 batch。
异步服务用 ainvoke / abatch。
独立分支用 Parallel。
用户界面用 Streaming。
成本敏感时减少 token。
重复计算用缓存。
```



#### 2.9 实战：构建一个 Runnable Workflow

本章节打算做一个只能文章助手，用户输入一篇文章或一段文本，系统自动判断任务类型，并完成摘要、关键词提取、分类、风险提示或改写等处理，最后以流式方式输出结果。

这个智能助手，当用户输入一段文字时，需要做这些事情

```
理解用户输入
判断用户想做什么
根据任务类型选择不同处理流程
并行生成多个辅助结果
调用模型生成最终结果
失败时自动重试
主模型不可用时切换备用模型
最终支持流式输出
```

接下来分为这么几步

###### 基础链路

首先这一节会写一个最基础的chain，按照如下流程：

```

用户输入 article
  ↓
PromptTemplate 构造摘要提示词
  ↓
ChatModel 生成摘要
  ↓
StrOutputParser 解析成字符串
  ↓
返回 summary
```

看下代码：

```python
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


ENV_PATH = Path(__file__).resolve().parent.parent / ".ENV"
load_dotenv(dotenv_path=ENV_PATH)


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required env variable: {name}")
    return value


def create_chat_model(
    *,
    model: str | None = None,
    base_url: str | None = None,
    api_key: str | None = None,
    temperature: float = 0.2,
) -> ChatOpenAI:
    """Create an OpenAI-compatible chat model from .ENV config."""
    timeout = int(os.getenv("LLM_TIMEOUT", "60"))

    return ChatOpenAI(
        model=model or _required_env("LLM_MODEL_ID"),
        base_url=base_url or _required_env("LLM_BASE_URL"),
        api_key=api_key or _required_env("LLM_API_KEY"),
        temperature=temperature,
        timeout=timeout,
    )


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

model = create_chat_model()
parser = StrOutputParser()

# Core Runnable workflow:
# article -> PromptTemplate -> ChatModel -> StrOutputParser -> summary
summary_chain = summary_prompt | model | parser


def summarize(article: str) -> str:
    """Run summary_chain with a plain article string."""
    return summary_chain.invoke({"article": article})


if __name__ == "__main__":
    article_path = Path(__file__).resolve().parent.parent / "data" / "zhufu.txt"
    demo_article = article_path.read_text(encoding="utf-8")

    print(summarize(demo_article))

#输出
### 一句话总结
鲁迅通过祥林嫂的悲剧，深刻揭示了封建礼教、迷信思想和社会冷漠如何一步步将一个勤劳善良的农村妇女推向死亡，同时批判了知识分子的软弱与旁观。
```

核心代码就是这行`summary_chain = summary_prompt | model | parser`

`summary_prompt`是手写的一个提示词，告知agent身份、角色，`model`是调用`ChatOpenAI`来创建的，通过`load_dotenv`加载.env文件中设置的base和key，`StrOutputParser`是最基础的输出解析器。

最后` summary_chain.invoke({"article": article})`，article是加载本地的一个txt文本，最后输出总结。





###### 增加并行执行

现在文章只有一个摘要总结，现在需要文章的关键字、分类以及文章的情绪倾向，就需要额外再创建三个chian

```python
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
#提取关键字的chain
keywords_chain = keywords_prompt | model | json_parser

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
#判断文章所属类别的chain
category_chain = category_prompt | model | parser
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
#分析文章情绪倾向的chian
sentiment_chain = sentiment_prompt | model | parser

```

然后就可以使用前面介绍过的`RunnableParallel`，并行创建这四个chain

```python
analysis_chain = RunnableParallel(
    summary=summary_chain,
    keywords=keywords_chain,
    category=category_chain,
    sentiment=sentiment_chain,
)
```

本节输出：

```
{'summary': '### 核心要点\n\n1. **故事背景与叙述者**：故事发生在旧历年底的鲁镇，叙述者“我”回到故乡，暂住在鲁四老爷家，感受到浓厚的“祝福”氛围，但内心不安，决定离开。\n\n2. **祥林嫂的悲惨遭遇**：祥林嫂是一个勤劳的寡妇，先后经历丈夫去世、被婆婆强迫改嫁、第二任丈夫死于伤寒、儿子阿毛被狼叼走等打击，最终沦为乞丐，在祝福之夜冻饿而死。\n\n3. **社会冷漠与封建礼教**：鲁镇的人们对祥林嫂的苦难从同情转为厌烦，鲁四老爷视她为“谬种”，禁止她参与祭祀，认为她“败坏风俗”；柳妈以“阴司锯开”的迷信恐吓她，导致她捐门槛赎罪却仍被排斥。\n\n4. **祥林嫂的精神崩溃**：在反复讲述儿子被狼吃的故事遭人厌弃后，祥林嫂捐门槛仍不被接纳，彻底失去希望，变得麻木、胆怯，最终被赶出家门，沦为乞丐。\n\n5. **叙述者的反思**：叙述者面对祥林嫂关于“魂灵有无”的追问，含糊其辞，事后感到不安，最终在祝福的爆竹声中，以“懒散且舒适”的心态结束故事，暗示对现实的无奈与逃避。\n\n### 一句话总结\n\n鲁迅通过祥林嫂的悲剧，深刻揭露了封建礼教、迷信思想和社会冷漠对底层妇女的摧残，以及知识分子在残酷现实面前的无力与自欺。', 'keywords': ['祥林嫂', '鲁镇', '祝福', '四叔', '阿毛', '捐门槛', '魂灵', '封建礼教'], 'category': '文学', 'sentiment': '消极'}
```



######  增加条件分支 

有了这四个chain，就可以根据用户的输入，来判断用户的任务类型，然后再去执行不同的chian，这就需要用到前面介绍的`RunnableBranch`，根据输入判断条件，选择其中一条 Runnable 执行。

具体的流程是这样的，首先用户输入一段文本，有一个任务识别的chain作为路由分发，根据任务的类型分别调用不同的chain。

```python
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
#任务分发的chain'
task_identify_chain = task_identify_prompt | model | parser | RunnableLambda(normalize_task)

def normalize_task(text: str) -> str:
    """Normalize model output into one of the supported route names."""
    task = text.strip().lower()
    allowed_tasks = ("summarize", "keywords", "category", "sentiment", "analysis")

    for allowed_task in allowed_tasks:
        if allowed_task in task:
            return allowed_task

    return "analysis"

```

这个chain就是一个判断任务类型的，根据用户的输入会返回一个类别，`"summarize", "keywords", "category", "sentiment", "analysis"`就是这里面的其中一个，如果没有就默认返回`"analysis"`

```python
def run_article_workflow(article: str, instruction: str) -> dict:
    """Identify the task and route to the matching RunnableBranch."""
    return article_workflow.invoke(
        {
            "article": article,
            "instruction": instruction,
        }
    )
article_workflow = routed_input_chain | RunnableParallel(
    task=lambda x: x["task"],
    result=branch_chain,
)
routed_input_chain = RunnableParallel(
    article=lambda x: x["article"],
    task=task_identify_chain,
)
branch_chain = RunnableBranch(
    (lambda x: x["task"] == "summarize", article_only | summary_chain),
    (lambda x: x["task"] == "keywords", article_only | keywords_chain),
    (lambda x: x["task"] == "category", article_only | category_chain),
    (lambda x: x["task"] == "sentiment", article_only | sentiment_chain),
    article_only | analysis_chain,
)
article_only = RunnableLambda(article_input)

#调用方
demo_instruction = "请提取这篇文章的关键词"
print(run_article_workflow(demo_article, demo_instruction))
#输出
{'task': 'keywords', 'result': ['祥林嫂', '鲁镇', '祝福', '四叔', '阿毛', '捐门槛', '魂灵', '封建礼教']}
```

`run_article_workflow`方法调用时，传递了原本和用户的问题，然后执行`article_workflow`将这两个参数透传下去，`article_workflow`会先去执行`routed_input_chain`,这个chain就是最终的输出结果，将入参转化成{task：‘’，result：‘’}，`routed_input_chain`会将入参转换成{article：‘’，task：‘’}，`branch_chain`这个chain就是chain的转发。

###### 增加重试机制

接着给关键链路加 `with_retry()`，比如网络超时、模型返回的格式不稳定，可以多试几次

```python
RETRYABLE_EXCEPTIONS = (
    TimeoutError,
    ConnectionError,
    APIConnectionError,
    APITimeoutError,
    RateLimitError,
    InternalServerError,
    OutputParserException,
)


def with_temporary_retry(runnable):
    """Retry temporary model/network/parser failures, then re-raise."""
    return runnable.with_retry(
        retry_if_exception_type=RETRYABLE_EXCEPTIONS,
        stop_after_attempt=3,
        wait_exponential_jitter=True,
    )

#关键的chain都被包裹着
summary_chain = with_temporary_retry(summary_prompt | model | parser)
keywords_chain = with_temporary_retry(keywords_prompt | model | json_parser)
category_chain = with_temporary_retry(category_prompt | model | parser)
sentiment_chain = with_temporary_retry(sentiment_prompt | model | parser)
task_identify_chain = with_temporary_retry(
    task_identify_prompt | model | parser | RunnableLambda(normalize_task)
)

final_chain = with_temporary_retry(article_workflow)
```



###### 增加Fallback

当 `with_retry` 继续失败后，接着引入 `with_fallbacks()`，选用备用模型继续处理。

```python
def create_backup_chat_model() -> ChatOpenAI:
    """Create a backup model for fallback; defaults to primary config if unset."""
    return create_chat_model(
        model=os.getenv("BACKUP_LLM_MODEL_ID")
        or os.getenv("LLM_BACKUP_MODEL_ID")
        or _required_env("LLM_MODEL_ID"),
        base_url=os.getenv("BACKUP_LLM_BASE_URL")
        or os.getenv("LLM_BACKUP_BASE_URL")
        or _required_env("LLM_BASE_URL"),
        api_key=os.getenv("BACKUP_LLM_API_KEY")
        or os.getenv("LLM_BACKUP_API_KEY")
        or _required_env("LLM_API_KEY"),
        timeout=int(
            os.getenv("BACKUP_LLM_TIMEOUT")
            or os.getenv("LLM_BACKUP_TIMEOUT")
            or os.getenv("LLM_TIMEOUT", "60")
        ),
    )
def with_retry_then_fallback(primary_runnable, backup_runnable):
    """Retry the primary runnable first, then switch to the backup runnable."""
    primary_with_retry = with_temporary_retry(primary_runnable)
    backup_with_retry = with_temporary_retry(backup_runnable)

    return primary_with_retry.with_fallbacks(
        [backup_with_retry],
        exceptions_to_handle=RETRYABLE_EXCEPTIONS,
    )
summary_chain = with_retry_then_fallback(
    summary_prompt | primary_model | parser,
    summary_prompt | backup_model | parser,
)
keywords_chain = with_retry_then_fallback(
    keywords_prompt | primary_model | json_parser,
    keywords_prompt | backup_model | json_parser,
)
category_chain = with_retry_then_fallback(
    category_prompt | primary_model | parser,
    category_prompt | backup_model | parser,
)
sentiment_chain = with_retry_then_fallback(
    sentiment_prompt | primary_model | parser,
    sentiment_prompt | backup_model | parser,
)
```

核心方法就是`with_retry_then_fallback`，主链先 retry 3 次，如果失败了，就使用备用链 retry 3 次。

###### 增加Streaming

最后引入 `stream()`。

最终结果生成时，不再等完整答案生成完，而是边生成边输出。



```python
def final_answer_input(workflow_output: dict) -> dict:
    """Format routed workflow output for the final answer prompt."""
    return {
        "task": workflow_output["task"],
        "result": json.dumps(
            workflow_output["result"],
            ensure_ascii=False,
            indent=2,
        ),
    }

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

final_answer_chain = with_retry_then_fallback(
    final_answer_prompt | primary_model | parser,
    final_answer_prompt | backup_model | parser,
)
streaming_workflow_chain = final_chain | RunnableLambda(final_answer_input) | final_answer_chain
def stream_article_workflow(article: str, instruction: str):
    """Stream the final user-facing answer."""
    return streaming_workflow_chain.stream(
        {
            "article": article,
            "instruction": instruction,
        }
    )

```

就是在之前的基础上，在继续调用chian，将结果转换成流失输出，最终的执行流程如下：

```
用户输入
  ↓
输入预处理
  ↓
任务识别
  ↓
RunnableBranch 路由
      ├─ 摘要流程
      ├─ 改写流程
      ├─ 要点提取流程
      └─ 通用分析流程
  ↓
RunnableParallel 并行补充分析
      ├─ 摘要
      ├─ 关键词
      ├─ 分类
      └─ 情绪
  ↓
最终 Prompt 整合结果
  ↓
主模型生成
  ↓
Parser 解析
  ↓
with_retry 保证临时失败可恢复
  ↓
with_fallbacks 保证主模型失败时可降级
  ↓
stream() 流式输出
```





### 三、Prompt API

####  3.1 为什么需要 Prompt API 

·`Prompt`实际上就是提示词，投喂给大模型的文本字符串，大模型根据输入的提示词来做输出，`Langchain`提供了大量的API来操作`prompt`，而不是单纯的将`prompt`当做字符串去操作，目的就是为了将提示词工程化，能够更好的适应一些复杂的场景：

- 适配不同的大模型

  不同厂商的大模型输入格式是不一样的， OpenAI：`[{"role":"system"},{"role":"user"}]` ； 阿里通义：`system:xxx\nuser:xxx` ，如果使用单纯的字符串就需要写大量的代码去适配

- 复杂的工程能力手动写字符串无法实现

  涉及到根据输入动态增减提示词片段、自动追加输出格式约束、多段提示词分层组合，这些场景手写字符串是无法实现的

- Token管控，上下文窗口安全

  大模型有最大输入长度限制的，裸字符串无法自动计算token，自动截断冗余内容

- 标准化对接上下游组件

  根据前面的最基础的chain学习，我们知道`Prompt`它实际上也是一个`Runnable`，它的输出是要喂给`model`的。

所以`Langchain`提供了大量的API，让`prompt`有了工程化的能力，可以适配各种复杂场景。

接下来详细的介绍下这些API



####  3.2 PromptTemplate 

 `PromptTemplate` 是 LangChain 中最基础的 Prompt 模板，适用一些普通文本模型或简单字符串 Prompt。

```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template("请总结下面文章：{article}")
```

这里的prompt，是一个符合` Runnable `格式的模板对象，接受一个article参数，当它调用invoke时，需要传入这个参数：

```python
result = prompt.invoke({"article": "测试文本"})
```

此时result是一个 `PromptValue`  

```python
text = prompt.format(article="这里是一篇文章")
```

这个text就是一个标准的字符串了

 在 LangChain 工作流中，更推荐理解和使用 `invoke()`，因为它能自然接入stream、with_config和LCEL。 

当涉及到一些简单的场景，`PromptTemplate` 可以把普通字符串 Prompt 变成可复用、可组合、可执行的模板组件

####  3.3 ChatPromptTemplate 

 `PromptTemplate`  适合一些简单的文本，`ChatPromptTemplate`就更加适合一些聊天场景。ChatModel他不只是接受一个字符串，更加适合接受一个消息结构的列表，包含SystemMessage、HumanMessage和AIMessage

比如下面这个代码：

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的中文写作助手。"),
    ("human", "请总结下面文章：{article}")
])
```

这个结构就更加适合真实的对话，有system定义角色、边界和规则；human代表用户的输入；ai代表模型的实例或者历史回复。

`ChatPromptTemplate`和`PromptTemplate`最大的区别就是，前者将 Prompt 从“字符串模板”升级成了“消息结构模板”

#### 3.4 MessagesPlaceholder 

 `MessagesPlaceholder` 用来在 `ChatPromptTemplate` 中动态插入一组消息，常常用于多轮对话场景。

普通的`ChatPromptTemplate`他的结构是固定的，比如前面章节的实例：

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个智能助手。"),
    ("human", "{question}")
])
```

但真实聊天里，通常还有历史记录：

```
用户：什么是 Runnable？
助手：Runnable 是 LangChain 的统一执行接口。
用户：那它和普通函数有什么区别？
```

这些历史消息不是写死在 Prompt 里的，而是运行时传入。

这时就需要 `MessagesPlaceholder`：

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个智能助手。"),
    MessagesPlaceholder("history"),
    ("human", "{question}")
])
```

调用时：

```python
prompt.invoke({
    "history": [
        ("human", "什么是 Runnable？"),
        ("ai", "Runnable 是 LangChain 的统一执行接口。"),
    ],
    "question": "那它和普通函数有什么区别？"
})
```

最终消息结构会变成：

```
system：你是一个智能助手。
human：什么是 Runnable？
ai：Runnable 是 LangChain 的统一执行接口。
human：那它和普通函数有什么区别？
```

如果历史消息为空，还可以这样设置，避免报错

```python
MessagesPlaceholder("history", optional=True)
```

同样也可以设置保留最近的几条历史记录

```python
MessagesPlaceholder("history", n_messages=4)
```



####  3.5 FewShot Prompt 

 `FewShot Prompt` 指的是：在正式问题之前，先给模型几个示例，让模型模仿示例的格式、风格和推理方式。 也可以理解为，不知告诉模型要怎么做，而是直接给模型看正确答案。

看下这个案例：

```python
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

examples = [
    {
        "article": "这篇文章介绍了大语言模型的发展。",
        "category": "科技",
    },
    {
        "article": "这篇文章讲述了鲁迅的文学创作。",
        "category": "文学",
    },
]

example_prompt = PromptTemplate.from_template(
    "输入：{article}\n输出：{category}"
)

prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="请判断文章类别。参考下面示例：",
    suffix="输入：{article}\n输出：",
    input_variables=["article"],
)
prompt.invoke({
    "article": "这篇文章分析了一家公司的商业模式。"
})
```

最终输出的prompt是这样

```
请判断文章类别。参考下面示例：

输入：这篇文章介绍了大语言模型的发展。
输出：科技

输入：这篇文章讲述了鲁迅的文学创作。
输出：文学

输入：这篇文章分析了一家公司的商业模式。
输出：
```

这里使用 `FewShot Prompt`的好处主要在于约束输出格式、稳定模型的行为

如果是文本`Prompt`可以使用前面的`FewShotPromptTemplate`，如果是对话类的， 更推荐使用 `FewShotChatMessagePromptTemplate` 

```python
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)

examples = [
    {"input": "什么是 Runnable？", "output": "Runnable 是 LangChain 的统一执行接口。"},
    {"input": "什么是 PromptTemplate？", "output": "PromptTemplate 是用于构造 Prompt 的模板。"},
]

example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}"),
    ("ai", "{output}"),
])

few_shot_prompt = FewShotChatMessagePromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个 LangChain 教学助手。"),
    few_shot_prompt,
    ("human", "{input}"),
])
```

最终消息结构类似：

```python
system：你是一个 LangChain 教学助手。
human：什么是 Runnable？
ai：Runnable 是 LangChain 的统一执行接口。
human：什么是 PromptTemplate？
ai：PromptTemplate 是用于构造 Prompt 的模板。
human：{input}
```

这种方式更适合 ChatModel，因为它保留了对话结构。



#### 3.6 Example Selector 

`FewShot Prompt` 是通过示例教模型做事，比单纯写规则可以得到大模型更加直观、稳定的输出。但是案例都会进入prompt，一起投喂给大模型，一旦案例过长，就会造成token额外的消耗，而且无关的案例还会干扰模型。

`langchain`还提供了一个 `Example Selector` ，当面对大量的案例时，会根据输入，动态的选择几个最合适的案例来塞入`prompt`，具体流程是这样的

```
用户问题
      │
      ▼
Example Selector
      │
挑选最相关 Example
      │
      ▼
FewShotPromptTemplate
      │
拼接 Prompt
      │
      ▼
LLM
```

常见的选择器主要有下面几种：

- LengthBasedExampleSelector

  这个是最简单的一个选择器，根据长度来控制prompt。比如设置prompt长度为4000token，他就会一直塞案例到prompt中，知道塞满为止。

  看下这个案例

  ```python
  from langchain_core.example_selectors import LengthBasedExampleSelector
  from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
  
  examples = [
      {"input": "1+1", "output": "2"},
      {"input": "2+3", "output": "5"},
      {"input": "123 + 456", "output": "579"},
      {"input": "请把“我喜欢学习 LangChain”翻译成英文", "output": "I like learning LangChain."},
  ]
  
  example_prompt = PromptTemplate(
      input_variables=["input", "output"],
      template="输入: {input}\n输出: {output}"
  )
  
  selector = LengthBasedExampleSelector(
      examples=examples,
      example_prompt=example_prompt,
      max_length=30
  )
  
  print(selector.select_examples({"input": "3+4"}))
  ```

  这个案例库比较小，他只会选择一些比较短的案例，因为这样比较节省token，如果案例库够长，他只会塞入比较短的30个案例

- SemanticSimilarityExampleSelector

  这是企业项目最常见选择器，实际上就是和RAG的流程一模一样，先转换成向量，然后在做语义相似度匹配，找到和用户输入最相似的案例。

  看下这个案例

  ```python
  from langchain_core.example_selectors import SemanticSimilarityExampleSelector
  from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
  from langchain_openai import OpenAIEmbeddings
  from langchain_community.vectorstores import FAISS
  
  examples = [
      {"question": "怎么重置密码？", "answer": "点击登录页的忘记密码。"},
      {"question": "怎么修改头像？", "answer": "进入个人中心，点击头像上传新图片。"},
      {"question": "怎么删除账号？", "answer": "进入设置页面，找到账号注销入口。"},
      {"question": "怎么绑定手机号？", "answer": "进入安全设置，选择绑定手机号。"},
  ]
  
  example_prompt = PromptTemplate(
      input_variables=["question", "answer"],
      template="问题: {question}\n回答: {answer}"
  )
  
  selector = SemanticSimilarityExampleSelector.from_examples(
      examples=examples,
      embeddings=OpenAIEmbeddings(),
      vectorstore_cls=FAISS,
      k=2
  )
  
  selected = selector.select_examples({"question": "如何更换我的头像？"})
  print(selected)
  ```

  这里就会根据用户的输入，去案例库中匹配语义最相似的案例去投喂给大模型

- MaxMarginalRelevanceExampleSelector

  这个是兼容多样性和相关性的，尽量在案例库中挑选一些相关又不重复的案例。

  ```python
  from langchain_core.example_selectors import MaxMarginalRelevanceExampleSelector
  from langchain_core.prompts import PromptTemplate
  from langchain_openai import OpenAIEmbeddings
  from langchain_community.vectorstores import FAISS
  
  examples = [
      {"topic": "头像", "question": "怎么修改头像？", "answer": "进入个人中心更换头像。"},
      {"topic": "头像", "question": "怎么上传新头像？", "answer": "点击头像区域并选择图片。"},
      {"topic": "昵称", "question": "怎么修改昵称？", "answer": "进入资料编辑页修改昵称。"},
      {"topic": "手机号", "question": "怎么绑定手机号？", "answer": "进入安全设置绑定手机号。"},
      {"topic": "密码", "question": "怎么重置密码？", "answer": "点击忘记密码进行重置。"},
  ]
  
  example_prompt = PromptTemplate(
      input_variables=["topic", "question", "answer"],
      template="主题: {topic}\n问题: {question}\n回答: {answer}"
  )
  
  selector = MaxMarginalRelevanceExampleSelector.from_examples(
      examples=examples,
      embeddings=OpenAIEmbeddings(),
      vectorstore_cls=FAISS,
      k=2,
      fetch_k=5
  )
  
  selected = selector.select_examples({"question": "我想修改个人资料里的头像和昵称"})
  print(selected)
  ```

  



#### 3.7 Partial Prompt 

 `Partial Prompt` 指的是：提前固定 Prompt 中的一部分变量。 比如在传递prompt时，如果在prompt中有很多变量，就可以通过 partial 来固定某一些变量，后续传参中就可以不传那些被固定的变量了，有点类似于函数式编程中的函数柯里化，起到一个节约传参的目的。

```python
base_prompt = PromptTemplate.from_template("你是{role}，针对{topic}回答：{question}")

# 第一步绑定role，生成半成品1
step1 = base_prompt.partial(role="资深后端工程师")
# 第二步再绑定topic，生成半成品2，只剩question需要传入
step2 = step1.partial(topic="Python异步")

# 最终只传question
print(step2.format(question="asyncio原理"))
```



#### 3.8 Pipeline Prompt 

一个复杂的prompt会由好几个部分组成，比如角色说明、任务说明、输出格式等，如果全部写在一个大的字符串中，会很难维护，`langchian`推出了 Pipeline Prompt 这个api，可以将多个prompt片段组合成一个prompt。

```python
from langchain_core.prompts import PromptTemplate

role_prompt = PromptTemplate.from_template(
    "你是一个专业的{domain}助手。"
)

task_prompt = PromptTemplate.from_template(
    "你的任务是：{task}"
)

format_prompt = PromptTemplate.from_template(
    "输出格式：{format_instruction}"
)

final_prompt = PromptTemplate.from_template("""
{role}

{task}

{format_instruction}

用户输入：
{input}
""")

data = {
    "domain": "文章分析",
    "task": "总结文章并提取关键词",
    "format_instruction": "请输出 JSON",
    "input": "这里是文章内容..."
}

prompt_input = {
    "role": role_prompt.invoke(data).to_string(),
    "task": task_prompt.invoke(data).to_string(),
    "format_instruction": format_prompt.invoke(data).to_string(),
    "input": data["input"],
}

result = final_prompt.invoke(prompt_input)
```



#### 3.9 Prompt 最佳实践

一个优秀的prompt，需要让模型清楚的知道他的角色、目标、参考对象、需要遵守的规则，还有就是输入和输出的格式，而不是一大坨自然语言。

可以根据下面的规范来编写prompt

###### 结构化

推荐结构：

```
角色
任务
上下文
约束
输出格式
示例
用户输入
```

比如文章摘要的prompt可以这么写：

```
summary_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "你是一个专业的中文内容编辑，擅长把长文章总结成清晰、准确、易读的摘要。"
    ),
    (
        "human",
        """
任务：
请阅读下面文章，并生成摘要。

要求：
1. 用中文回答。
2. 提取 3-5 条核心要点。
3. 最后给出一句话总结。
4. 只基于文章内容，不要编造信息。

输出格式：
核心要点：
- ...
- ...

一句话总结：
...

文章：
{article}
"""
    )
])
```

不推荐：

```
你是一个助手，请帮我分析这篇文章，要求准确、专业、简洁，还要输出关键词……
```

推荐拆成：

```
角色：
你是一个专业的文章分析助手。

任务：
请分析用户提供的文章。

要求：
1. 只基于文章内容回答。
2. 不要编造信息。
3. 用中文输出。

输出格式：
{
  "summary": "...",
  "keywords": ["...", "..."],
  "category": "...",
  "sentiment": "..."
}

输入：
{article}
```

###### 明确输出格式

```
只返回 JSON
只返回列表
只返回一个类别
不要添加解释
不要返回 Markdown
```

比如关键词提取的prompt

```
keywords_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个中文关键词提取助手。"),
    (
        "human",
        """
请从文章中提取 5-8 个关键词。

要求：
1. 只返回 JSON 数组。
2. 不要返回 Markdown。
3. 不要添加解释。

示例：
["关键词1", "关键词2", "关键词3"]

文章：
{article}
"""
    )
])
```

###### 控制变量边界

不推荐这种prompt

```
请总结这篇文章：{article}
```

 如果文章很长，或者文章里本身包含指令，模型可能混淆“系统任务”和“文章内容”。 

可以这么做

```
请总结下面文章。

文章开始：
{article}
文章结束。
```

###### 避免过度 Prompt

prompt并不是越长越好，比如下面这样：

```
你必须非常准确、非常专业、非常认真、非常仔细、非常有逻辑……
```

并不一定会带来稳定的提升，反而会增加token的消耗

更好的写法是明确约束条件：

```
只基于文章内容回答
如果文章没有提到，回答“文章未提及”
输出 3 条以内
只返回 JSON

少写情绪化形容词
多写可执行约束
```



#### 3.10 Prompt 组合

 Prompt 组合指的是：把多个 Prompt 片段或 Prompt 组件组合成更复杂的 Prompt 或工作流。 

常见的组合方式有下面几种：

###### 字符串片段组合

这是最简单的组合方式

```python
role = "你是一个专业的中文文章分析助手。"

task = """
任务：
请分析下面文章。
"""

format_instruction = """
输出格式：
{
  "summary": "...",
  "keywords": ["...", "..."]
}
"""

template = f"""
{role}

{task}

{format_instruction}

文章：
{{article}}
"""

prompt = ChatPromptTemplate.from_messages([
    ("human", template)
])
```

 这种方式简单直接，但如果片段越来越多，就容易失控。 

######  消息结构组合 

```
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的中文文章分析助手。"),
    ("human", "任务：请总结下面文章。"),
    ("human", "要求：只基于文章内容，不要编造信息。"),
    ("human", "文章：{article}")
])
```

这种结构更加推荐

###### 

#### 3.11 实战：构建 Prompt Library

在第二章中，我们写了一个workflow，里面的prompt都写在业务代码中，后续如果业务代码再复杂，就会导致文件越来越长，这里根据前面学习的，把 Prompt 从业务流程里抽出来，形成 Prompt Library。

###### 第一步：设计目录结构

新建目录结构：

```
langchain/
    prompt_library/
      __init__.py
      article_prompts.py
      router_prompts.py
      output_prompts.py
      debug.py
```

具体职责划分：

```
article_prompts.py：文章处理 Prompt
router_prompts.py：任务识别 Prompt
output_prompts.py：最终回答 Prompt
debug.py：Prompt 调试工具
```



###### 第二步：抽取文章处理 Prompt

文件：article_prompts.py 

里面放文章处理相关 Prompt：

```
SUMMARY_PROMPT_VERSION = "summary_v1"
KEYWORDS_PROMPT_VERSION = "keywords_v1"
CATEGORY_PROMPT_VERSION = "category_v1"
SENTIMENT_PROMPT_VERSION = "sentiment_v1"

summary_prompt = ChatPromptTemplate.from_messages([...])
keywords_prompt = ChatPromptTemplate.from_messages([...])
category_prompt = ChatPromptTemplate.from_messages([...])
sentiment_prompt = ChatPromptTemplate.from_messages([...])
```

这样 `summary_prompt`、`keywords_prompt` 不再散落在 workflow 文件里。

###### 第三步：抽取任务路由 Prompt

文件：router_prompts.py 

```
TASK_IDENTIFY_PROMPT_VERSION = "task_identify_v1"

task_identify_prompt = ChatPromptTemplate.from_messages([...])
```

这个 Prompt 只负责一件事：

```
根据用户指令判断任务类型
```

比如：

```
请总结这篇文章 -> summarize
请提取关键词 -> keywords
请判断类别 -> category
```

###### 第四步：抽取最终回答 Prompt

文件：output_prompts.py

```
FINAL_ANSWER_PROMPT_VERSION = "final_answer_v1"

final_answer_prompt = ChatPromptTemplate.from_messages([...])
```

它负责把 workflow 的结构化结果整理成最终用户可读回答。

###### 第五步：在 workflow 中复用 Prompt

现在 `summary_chain.py` 里不再定义 Prompt，而是导入：

```
from prompt_library import (
    category_prompt,
    final_answer_prompt,
    keywords_prompt,
    sentiment_prompt,
    summary_prompt,
    task_identify_prompt,
)
```

原来的 chain 逻辑基本不变：

```
summary_chain = with_retry_then_fallback(
    summary_prompt | primary_model | parser,
    summary_prompt | backup_model | parser,
)
```

这说明一次好的重构不一定要改业务流程。

这次只是把 Prompt 管理方式变清晰了

###### 第六步：增加 Prompt Version

Prompt Library 里统一维护版本：

```
SUMMARY_PROMPT_VERSION = "summary_v1"
KEYWORDS_PROMPT_VERSION = "keywords_v1"
TASK_IDENTIFY_PROMPT_VERSION = "task_identify_v1"
```

并在 `__init__.py` 里汇总：

```
PROMPT_VERSIONS = {
    "summary": SUMMARY_PROMPT_VERSION,
    "keywords": KEYWORDS_PROMPT_VERSION,
    "category": CATEGORY_PROMPT_VERSION,
    "sentiment": SENTIMENT_PROMPT_VERSION,
    "task_identify": TASK_IDENTIFY_PROMPT_VERSION,
    "final_answer": FINAL_ANSWER_PROMPT_VERSION,
}
```

在 chain 中也可以写入 metadata：

```
summary_chain = summary_chain.with_config(
    metadata={"prompt_version": SUMMARY_PROMPT_VERSION}
)
```

这样后续调试、追踪、评测时，可以知道本次调用用了哪个 Prompt 版本。

###### 第七步：增加 Debug 方法

文件：[debug.py (line 1)](H:/project/blog/blog/ai应用开发/code/agent/langchain/prompt_library/debug.py:1)

```
def preview_prompt(prompt, input_data: dict) -> None:
    prompt_value = prompt.invoke(input_data)

    print("=== Prompt String ===")
    print(prompt_value.to_string())

    print("\n=== Prompt Messages ===")
    for message in prompt_value.to_messages():
        print(f"[{message.type}] {message.content}")
```

使用方式：

```
preview_prompt(task_identify_prompt, {
    "article": demo_article[:500],
    "instruction": demo_instruction,
})
```

调试 Prompt 时，不要只看模型输出。

更重要的是先看：

```
真正发给模型的 Prompt 长什么样
变量有没有填进去
消息结构是否正确
```

然后运行` python summary_chain.py `

```
#输出
Prompt versions: {'summary': 'summary_v1', 'keywords': 'keywords_v1', 'category': 'category_v1', 'sentiment': 'sentiment_v1', 'task_identify': 'task_identify_v1', 'final_answer': 'final_answer_v1'}
=== Prompt String ===
System: 你是一个任务路由助手，根据用户指令选择最合适的文章处理链。
Human: 请根据用户指令判断任务类型。

只能返回下面 5 个值之一：
summarize
keywords
category
sentiment
analysis
```

最终我们将prompt从散落在业务代码里的代码块抽离出来，变成了可以统一维护、单独测试、版本化迭代的工程化资产，为后续的agent健壮的工程能力打下了一个坚实的基础。



### 三、Model I/O：输入与输出体系







#### 1 Chat Model

模型统一调用接口
模型参数管理

#### 2 Prompt 模板

PromptTemplate
ChatPromptTemplate
MessagesPlaceholder
Few-Shot Prompt

#### 3 Structured Output

为什么结构化输出越来越重要
StrOutputParser
JsonOutputParser
PydanticOutputParser
with_structured_output

### 四、LCEL：声明式工作流编排

#### 1 LCEL 核心思想

数据流驱动
声明式开发

#### 2 管道表达式

Prompt → Model → Parser

#### 3 常见编排模式

顺序执行
并行执行
数据透传
条件分支

#### 4 LCEL 高级能力

Streaming
Async
Retry
Fallback