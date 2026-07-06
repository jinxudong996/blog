# LangChain 实战教程（2026）

> 副标题：
>
> 从 LangChain Core 到 LangGraph，从 API 到生产级 AI Agent
>
> 定位：
>
> 不只是教会 LangChain，而是掌握现代 AI 应用开发。

---

# 学习路线

LangChain Core
        │
        ▼
Core API（Runnable / Prompt / Model / Parser）
        │
        ▼
LCEL 工作流
        │
        ▼
RAG API
        │
        ▼
Tool Calling API
        │
        ▼
Agent API
        │
        ▼
LangGraph API
        │
        ▼
MCP
        │
        ▼
Production

每一章均遵循：

API
↓

原理

↓

最佳实践

↓

实战

↓

总结

========================================================
第一篇
LangChain Core：掌握现代 LangChain API
========================================================

目标：

✔ 理解 LangChain Core 设计思想

✔ 掌握 Core API

✔ 能写出 LCEL Workflow

✔ 能部署 API

--------------------------------------------------------
第一章 LangChain 全景图
--------------------------------------------------------

1.1 为什么需要 LangChain

1.2 LangChain 生态

- LangChain Core
- LangChain
- LangGraph
- LangSmith
- LangServe

1.3 Chain 为什么被 LCEL 取代

1.4 Runnable 为什么成为统一抽象

--------------------------------------------------------
第二章 Runnable API（重点）
--------------------------------------------------------

设计思想

Everything is Runnable

统一接口的意义

核心 API

invoke()

ainvoke()

stream()

astream()

batch()

abatch()

stream_events()

高级 API

bind()

assign()

map()

pick()

pipe()

with_config()

with_retry()

with_fallbacks()

with_types()

Runnable 实现

RunnableLambda

RunnableParallel

RunnableBranch

RunnableAssign

RunnablePassthrough

RunnableSequence

最佳实践

什么时候组合

什么时候拆分

性能建议

实战：

构建一个 Runnable Workflow

--------------------------------------------------------
第三章 Prompt API
--------------------------------------------------------

PromptTemplate

ChatPromptTemplate

MessagesPlaceholder

FewShot

Example Selector

Partial Prompt

Pipeline Prompt

PromptValue

Prompt 最佳实践

Prompt Version

Prompt 复用

Prompt 组合

Prompt Debug

实战：

构建 Prompt Library

--------------------------------------------------------
第四章 Chat Model API
--------------------------------------------------------

ChatOpenAI

ChatAnthropic

ChatGoogle

ChatDeepSeek

统一接口

invoke()

stream()

bind_tools()

with_structured_output()

模型参数

temperature

max_tokens

reasoning

timeout

Provider 差异

OpenAI

Anthropic

Gemini

DeepSeek

Qwen

GLM

实战：

支持多 Provider 的聊天机器人

--------------------------------------------------------
第五章 Structured Output API
--------------------------------------------------------

为什么 Structured Output

OutputParser

StrOutputParser

JsonOutputParser

PydanticOutputParser

XMLOutputParser

OutputFixingParser

RetryOutputParser

with_structured_output()

JSON Schema

Pydantic

最佳实践

实战：

AI 数据提取器

--------------------------------------------------------
第六章 LCEL API
--------------------------------------------------------

LCEL 思想

数据流

声明式

API

|

RunnableSequence

RunnableParallel

RunnableBranch

Streaming

Async

Retry

Fallback

Config

最佳实践

复杂 Workflow

可维护性

实战：

新闻总结 Workflow

--------------------------------------------------------
第七章 Callback & Config
--------------------------------------------------------

Callback

Listener

Trace

Metadata

Tags

Run Name

Configurable

Cache

Logging

Tracing

实战：

观察整个 Workflow

--------------------------------------------------------
第八章 LangServe
--------------------------------------------------------

为什么 API 化

LangServe

FastAPI

Streaming

Swagger

部署

Docker

实战：

部署 AI API

========================================================
第二篇
RAG、Tool Calling 与 Agent API
========================================================

目标：

掌握 LangChain Application API

--------------------------------------------------------
第一章 Document API
--------------------------------------------------------

Document

Metadata

Loader

PDF

Markdown

Word

HTML

JSON

--------------------------------------------------------
第二章 TextSplitter API
--------------------------------------------------------

Character

Recursive

Markdown

Token

Semantic Split

最佳实践

--------------------------------------------------------
第三章 Embedding API
--------------------------------------------------------

Embedding

OpenAI

BGE

Jina

Nomic

Embedding 选择

--------------------------------------------------------
第四章 VectorStore API
--------------------------------------------------------

FAISS

Chroma

Milvus

PGVector

Qdrant

CRUD

Filter

Search

--------------------------------------------------------
第五章 Retriever API
--------------------------------------------------------

BaseRetriever

Similarity

MMR

Parent

SelfQuery

MultiQuery

Context Compression

Ensemble

Hybrid

--------------------------------------------------------
第六章 RAG Workflow
--------------------------------------------------------

Query Rewrite

Rerank

Compression

Citation

Agentic RAG

实战：

企业知识库

--------------------------------------------------------
第七章 Tool API
--------------------------------------------------------

@tool

Schema

Args

Return

ToolNode

HTTP API Tool

Database Tool

Search Tool

最佳实践

--------------------------------------------------------
第八章 Agent API
--------------------------------------------------------

create_react_agent

Tool Calling Agent

Plan Execute

Reflection

Supervisor

Agent Router

Agent 最佳实践

--------------------------------------------------------
第九章 LangSmith
--------------------------------------------------------

Trace

Dataset

Evaluation

Benchmark

Prompt Testing

========================================================
第三篇
LangGraph 与生产级 Agent
========================================================

目标：

掌握企业级 Agent

--------------------------------------------------------
第一章 LangGraph Core API
--------------------------------------------------------

StateGraph

State

Node

Edge

Reducer

Compile

Invoke

--------------------------------------------------------
第二章 Node API
--------------------------------------------------------

Planning Node

Tool Node

Review Node

Summary Node

Parallel Node

--------------------------------------------------------
第三章 Edge API
--------------------------------------------------------

Normal Edge

Conditional Edge

Loop

Command

Send

--------------------------------------------------------
第四章 Persistence API
--------------------------------------------------------

Checkpoint

MemorySaver

SQLite

Redis

Long Memory

--------------------------------------------------------
第五章 Human In The Loop
--------------------------------------------------------

Interrupt

Resume

Approval

--------------------------------------------------------
第六章 Multi Agent
--------------------------------------------------------

Supervisor

Team

Reflection

Research

Coding

--------------------------------------------------------
第七章 MCP
--------------------------------------------------------

MCP 原理

Transport

Client

Server

Tool

Resource

Prompt

FastMCP

LangChain MCP

LangGraph MCP

--------------------------------------------------------
第八章 Production
--------------------------------------------------------

FastAPI

Docker

Redis

Cache

Rate Limit

Retry

Fallback

Observability

Logging

Monitoring

Metrics

Cost

========================================================
终极项目
========================================================

Research Agent

实现：

✓ LangGraph

✓ MCP

✓ RAG

✓ Tool Calling

✓ Multi-Agent

✓ LangSmith

✓ API

✓ Docker

✓ Streaming

✓ Checkpoint

✓ Human Approval

✓ 多模型 Provider

========================================================
最终掌握
========================================================

✓ LangChain Core API

✓ LCEL API

✓ Prompt API

✓ Runnable API

✓ Chat Model API

✓ Output API

✓ RAG API

✓ Tool API

✓ Agent API

✓ LangGraph API

✓ MCP

✓ LangSmith

✓ LangServe

✓ 企业级 AI Agent 开发