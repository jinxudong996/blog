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

现在文章只有一个摘要总结，现在需要文章的关键字、分类以及文章的情绪倾向，







接着引入 `RunnableParallel`。

现在不只生成摘要，还要同时生成：

```
summary：文章摘要
keywords：关键词
category：文章分类
sentiment：情绪倾向
```

流程：

```
article
  ├─> summary_chain
  ├─> keywords_chain
  ├─> category_chain
  └─> sentiment_chain
        ↓
合并成 dict
```

输出结构：

```
{
    "summary": "...",
    "keywords": ["...", "..."],
    "category": "...",
    "sentiment": "..."
}
```

这一阶段重点说明：

```
多个任务之间没有依赖关系，所以可以并行。
RunnableParallel 会把同一个输入交给多个 Runnable。
最终结果会合并成一个 dict。
```

######  增加条件分支 

接着引入 `RunnableBranch`。

系统先判断用户任务类型，然后走不同流程。

任务类型可以设计成：

```
summarize：总结文章
rewrite：改写文章
extract：提取要点
risk_check：检查风险或敏感内容
```

流程：

```
用户输入
  ↓
任务识别 chain
  ↓
RunnableBranch
      ├─ 如果 task = summarize -> 摘要流程
      ├─ 如果 task = rewrite -> 改写流程
      ├─ 如果 task = extract -> 要点提取流程
      └─ 默认 -> 通用分析流程
```

这一阶段重点说明：

```
RunnableBranch 类似 if / elif / else。
它根据输入内容选择不同 Runnable。
不同分支可以是完全不同的链。
```

###### 增加重试机制

接着给关键链路加 `with_retry()`。

适合加重试的位置：

```
模型调用链
任务识别链
结构化解析链
最终生成链
```

比如：

```
final_chain.with_retry()
```

设计说明：

```
模型调用可能超时
模型返回格式可能偶发不稳定
网络请求可能失败
Parser 可能解析失败
```

重试策略：

```
最多重试 3 次
只对临时异常重试
重试失败后继续抛出异常
```

这一阶段重点说明：

```
with_retry 是对同一个 Runnable 再试几次。
它适合处理临时性失败，不适合修复逻辑错误。
```

###### 增加Fallback

接着引入 `with_fallbacks()`。

设计两个模型：

```
primary_model：主模型，效果更好
backup_model：备用模型，速度快或成本低
```

当主模型失败时，自动切换备用模型。

流程：

```
primary_chain
  ↓ 如果成功
返回结果

primary_chain
  ↓ 如果失败
fallback_chain
  ↓
返回备用结果
```

可以设计成：

```
主模型：用于高质量分析
备用模型：用于基础摘要和回答

先 retry，再 fallback

主链先重试几次
如果仍然失败
切换备用链
```

###### 增加Streaming

最后引入 `stream()`。

最终结果生成时，不再等完整答案生成完，而是边生成边输出。

适合流式输出的部分：

```
最终总结
改写结果
长文章分析报告
风险分析说明

用户输入
  ↓
完整 Workflow
  ↓
最终生成链 stream()
  ↓
chunk 1
```

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