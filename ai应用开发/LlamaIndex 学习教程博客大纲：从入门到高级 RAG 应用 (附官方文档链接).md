# LlamaIndex 学习教程-概念篇 

## 一. 引言：为什么选择 LlamaIndex？
有一句话描`RAG`非常到位： 从本质上讲，RAG（Retrieval-Augmented Generation）是一种旨在解决大语言模型（LLM）“知其然不知其所以然”问题的技术范式。它的核心是将模型内部学到的“**参数化知识**”（模型权重中固化的、模糊的“记忆”），与来自外部知识库的“**非参数化知识**”（精准、可随时更新的外部数据）相结合。 

 在软件工程领域上有个专业名字叫做：`Trade-off`，就是我们没有办法既要又要，没有最佳方案，只有最适合的，我们要做的就是在适合的场景，选择出最贴合业务的方案。比如在llm应用开发中，如何避免大模型乱回答，成本最小的就是prompt工程，选择合适的提示字让他回答出我们想要的回答，而不一上来就换模型，prompt做不到，就回去使用`RAG`，给他外挂一个知识库，当前两者都无法解决问题，微调才会成为一个值得考虑的选项。

`LlamaIndex`是一个专注数据层的llm应用框架，其初衷就是为了简化`RAG`流程，更加专注于数据如何被组织、索引和检索，强调数据接入、索引结构和查询质量。

其实llm应用开发首选实际上是`langchain`，尤其是社区成熟度方面，`langchain`都不可避免的成为首选，但是做`RAG`的关键不是有没有接向量数据库，而是检索是否真的为模型提供了有用的上下文。`LlamaIndex`将`RAG`的复杂性前移到数据与检索层进行系统化抽象处理，因此`RAG`场景下`LlamaIndex`比langchain更自然和高效。

### 1.1 概览

 [文档入口地址](https://developers.llamaindex.ai/python/framework/getting_started/concepts/)

一个完善的`RAG`系统可以被简化为下面这三个步骤：

1. 数据准备与清洗

   当接收到用户输入的信息时，不会立马抛给llm，而是将收集到的信息，比如PDF、word和网页等，转换成标准化文本，按照语义段落或者句子切分，生成`Document`或者`Node`，这里的`Document`是`LlamaIndex`中的一个通用容器，用来封装各种数据源的数据，本质上是一个完整的数据单元。

   ```python
   from llama_index.core import Document
   documents = [Document(text="这是一个文档的文本。", metadata={"source": "file1.pdf"})]
   ```

   实际上就是将用户的输入构建成一个`LlamaIndex`可以处理的对象

   而`Node`是从`Document`中抽出来的块，比如一个段落、句子等。

2. 索引构建

   使用嵌入模型将文本`Node`转为向量，默认就是` text-embedding-ada-002 `，转化为向量后，就可以使用向量相似度来判断语义相关性，而不是靠关键词去匹配。

   有了向量后，就可以将向量存储到向量数据库中，这是为了增加检索效率，而不是每次都去遍历全部文本

3. 检索与增强

   用户在系统输入问题，`LlamaIndex`使用同样的模型将问题转化为向量，然后用之前构建好的索引找出与查询向量最相似的K个`Node`；然后对 Top-K 的结果再用轻量 LLM 或 BERT 类模型重新排序 ，来提高检索的准确性和相关性。

   有了相关的`Node`后，结合用户的问题和系统提示来拼接成一个增强的prompt，送给llm

4. 生成与提示工程

   问题经过检索和增强提示后，得到的prompt包含原始问题、检索得到的top-k和系统角色提示，llm接收到这个增强的提示词，在上下文的基础上生成回答。

## 二. LlamaIndex 快速入门与实战

### 2.1 环境准备

* 安装命令：`pip install llama-index`

* API Key 配置。

  新建`.env`文件在根目录，然后写上你的key

  `DEEPSEEK_API_KEY=xxx`

### 2.2 最小化 RAG 示例

```python
from dotenv import load_dotenv
from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.deepseek import DeepSeek


# 读取 .env 中的环境变量（例如 DEEPSEEK_API_KEY）
load_dotenv()

# 显式指定 LLM 和 Embedding，避免使用默认的 OpenAI
Settings.llm = DeepSeek(
    model="deepseek-chat",  # 如有需要可改成其它 DeepSeek 模型
)

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-zh-v1.5"  # 适合中文的向量模型
)

documents = [
    Document(
        text="LlamaIndex 是一个用于构建 RAG 应用的数据框架。",
        metadata={"source": "intro"},
    ),
    Document(
        text="RAG 的核心思想是通过检索外部知识来增强 LLM 的回答能力。",
        metadata={"source": "rag"},
    ),
]


index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

response = query_engine.query("什么是 RAG？")

print(response)
```

这里先加载定义在环境变量中的key，显示的指定模型。然后定义了文档数据数组，由`Document`对象构成，前面也介绍过，`Document`对象就是一个基本的数据单元。`VectorStoreIndex.from_documents(documents)`这行代码就是构建向量索引，和用户的输入做相似度检测。

一开始我以为将文本转化成向量，是一个有一个统一的标准，后来了解才发现不是这样的，将文本转化成向量，这是一种通用的思想，用一个多维数字向量来表示这段文字，但是具体使用多少维度的向量、那些语义更加接近，这都是向量模型来决定的，比如我们这个实例中选用的就是` model_name="BAAI/bge-small-zh-v1.5"`，还有个问题需要注意：这里的模型和我们最后的llm模型是两码事，`BAAI/bge-small-zh-v1.5`模型是` embedding `模型，将我们的用户输入和文档转换成向量，做相似度匹配的，而llm模型才是最终的推理模型。

构建好向量索引后，就可以借此来构建查询引擎，`index.as_query_engine()`，`query_engine`的职责就是将用户的输入构建成向量来和文档向量做相似度匹配，将检索到的内容和问题一起给llm总结回答。

最后调用`query_engine.query`来发起查询。

## 三. RAG 流程的五大阶段 

[文档地址](https://developers.llamaindex.ai/python/framework/understanding/rag/)

### 3.1 阶段一：加载 (Loading)

加载阶段是整个RAG流程的第一步，将用户输入的数据引入系统，转化为`LlamaIndex`可以理解和处理的结构。这里主要有两个核心概念

* **Document / Node**：数据容器和原子数据块的抽象。

  这里前面已经介绍过了，[文档](https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes/)也很清晰，`Document`本身就是一个原始的数据容器，用于存储加载的文本和内容，比如：

  ```python
  from llama_index import Document
  
  doc = Document(
      text="LlamaIndex 是一个连接 LLM 与外部数据的框架。",
      metadata={"source": "官方文档", "type": "tutorial"}
  )
  
  ```

  而`Node`是从`Document`切分出来的最小单元信息，通常是按照段落、句子或者语义进行切分的，是向量化和索引的基本粒度。

  ```python
  from llama_index.node_parser import SimpleNodeParser
  
  parser = SimpleNodeParser()
  nodes = parser.get_nodes_from_documents([doc])
  ```

  这里就是将`Document` 切分成的多个 `Node` 

  

* **Data Connectors (LlamaHub)**：数据源连接器集合。

  就是一个类似于数据接口库，可以快速从各种外部数据源加载文档。有一个说法就是：LlamaHub的设计是`LlamaIndex`可以工程化的核心设计之一，就是因为他实现了所有的`Reader`都遵循统一模式：

  ```
  reader = SomeReader(...)
  documents = reader.load_data()
  # -> List[Document]
  ```

  也就是说不管读取任何数据，最终都会输出一个统一的`Document`的列表。

  读取`Notion`数据库

  ```python
  from llama_index.readers.notion import NotionReader
  
  reader = NotionReader(
      notion_token="YOUR_TOKEN",
      database_id="DATABASE_ID"
  )
  
  documents = reader.load_data()
  ```

  读取word/PDF

  ```python
  from llama_index import SimpleDirectoryReader
  
  reader = SimpleDirectoryReader(
      input_files=["design.pdf", "api.docx"]
  )
  
  documents = reader.load_data()
  ```

  读取github

  ```python
  from llama_index.readers.github import GithubRepositoryReader
  
  reader = GithubRepositoryReader(
      owner="openai",
      repo="openai-python",
      use_parser=True
  )
  
  documents = reader.load_data()
  ```

  `LlamaIndex`用过这种设计，是的所有的`Reader`统一返回`Document`数组，使得不同的数据源能够以零适配成本接入同一RAG与Agent管道
### 3.2 阶段二：索引 (Indexing)

索引的目标只有一个，即将不可检索的原始文本，转换为可高效检索的结构化表示，这一步由三个核心抽象类来协作完成：

* **NodeParser**：负责将 `Document` 切分为 Node 的工具。

  他的职责主要有下面几个：负责切分`Document`，控制chunk的大小，保留上下级关系和维护metadata中的继承关系。

  看下这个实例：

  ```python
  from llama_index.core.node_parser import SentenceSplitter
  
  parser = SentenceSplitter(
      chunk_size=512,
      chunk_overlap=50
  )
  
  nodes = parser.get_nodes_from_documents(documents)
  ```

  `SentenceSplitter`是`LlamaIndex`核心库中提供基于语义、句子边界的文档分割器，而不是简单的按照字符数硬切割，他的核心特点就是优先以自然句子为分割边界，比如段落中的分隔符，句号、逗号和感叹号等，避免切割到句子中间导致语义断裂；同时还兼顾预设的分块大小限制，在语义完整和分块尺寸之间做平衡，这个也是`LlamaIndex`中最常用、最推荐的文档分割器。

  `SentenceSplitter`的两个参数，`chunk_size`就是写个文本块(chunk)的最大令牌数限制，通常根据llm上下文窗口的大小设定的；`chunk_overlap`是相邻两个文本块之间的重叠令牌数量，目的就是为了保持文本上下文的连续性，避免因为分块导致的语义断层。

  最终输出的`nodes`就是一个`Node`的列表

* **Embeddings**：将文本转化为向量表示。

  这里就是使用模型将`Node`数组转换为向量，比如之前的例子：

  ```python
  Settings.embed_model = HuggingFaceEmbedding(
      model_name="BAAI/bge-small-zh-v1.5"  # 适合中文的向量模型
  )
  ```

* **Index**：可查询的数据结构。

  这里的`Index`是一种将`Node`组织为可查询结构的数据结构，`LlamaIndex`提供了很多种索引类型，

  - `VectorStoreIndex`  将文本块转为高维稠密向量（Embedding），基于语义相似性检索，这里的语义相似度检索就是余弦相似度检索，通过计算向量的夹角来对比匹配的相关内容，实现懂意图的语义检索。这个适合绝大多数的`RAG`场景，也是最通用的一个`Index`索引类型 
  - `SummaryIndex`  无复杂检索逻辑，直接将全量文档 / Node 输入 LLM 进行总结或问答 ，配置极简、无需嵌入模型、保留文本完整上下文，适合超短文档（几百字内）的场景。
  - `KeywordTableIndex`  从文档中提取核心关键词，构建「关键词 - 文档块」映射表，基于字面关键词匹配检索 ， 适合关键词明确的短文档检索 ，比如基于产品编号、订单号查询

  
### 3.3 阶段三：存储 (Storing)

存储阶段是将构建好的索引数据持久化的环节，主要基于这两个类来实现的：

* **StorageContext**：持久化索引的机制。

  `StorageContext`是专门用于封装、管理所有索引相关存储组件的上下文容器，也是实现索引持久化、从存储中加载索引的核心机制。

  看下文档中给的例子：

  ```python
  from llama_index.storage.storage_context import StorageContext
  from llama_index.vector_stores import ChromaVectorStore
  from llama_index import VectorStoreIndex
  
  # 初始化向量存储（Chroma）
  vector_store = ChromaVectorStore(collection_name="my_docs")
  
  # 创建 StorageContext
  storage_context = StorageContext.from_defaults(vector_store=vector_store)
  
  # 使用 StorageContext 构建 Index
  index = VectorStoreIndex.from_documents(
      documents,
      storage_context=storage_context
  )
  
  # 持久化 Index
  index.storage_context.persist()
  ```

  `ChromaVectorStore`是`LlamaIndex`对开源向量库`Chroma `的封装，`ChromaVectorStore(collection_name="my_docs")`就是创建一个名字叫做`my_docs`的集合，用来存储向量；`StorageContext.from_defaults(vector_store=vector_store)`就是快速创建一个`StorageContext`，后续在构建索引的时候，传入创建的`storage_context`，这样就知道向量要存储的地方；而`VectorStoreIndex`就是前面介绍的将文本转换为向量的`Index`类型， 最终返回的`index` 是一个可以用来 `as_query_engine()` / `as_retriever()` 的索引对象 ；`index.storage_context`就是前面传递的`storage_context`，`persist()`方法就是将向量存储到磁盘中；这样下次程序启动时，可以重新创建同样的`ChromaVectorStore`，就不用在从原始的`Document`中重新创建索引。

* **Vector Store**：向量数据库

  向量数据库就是用来做向量的插入和删除操作，然后持久化存储向量，后续避免重复创建，同时也会做相速度搜索。

  常见的有

  - Chroma 一个开源的向量数据库，支持本地嵌入，可以快速部署
  - Pinecone  运行量数据库，支持高性能检索和自动扩容
  - FAISS 本地向量数据库，适合大规模快速计算
### 3.4 阶段四：查询 (Querying)

这个是对用户真正产生价值的阶段，就是在已有索引的基础上，检索最相关的上下文，结合用户问题，生成可控、可追溯的回答。

* **Retriever**

  根据一些指定的策略来检索相关的`Node`，主要有这样一些策略

  -  Similarity Search   基于向量相速度
  - Top-K  返回最相似的K个Node
  - Metadata Filter  按照metadata过滤
  - Hybrid Search  向量加关键字

* **Response Synthesizer**

  将检索到的上下文和查询结合，生成最终答案。它关注的问题是如何组织上下文，如何调用llm和如何避免幻觉。

  在 LlamaIndex 中，查询阶段通过 Retriever 精准召回相关 Node，再由 Response Synthesizer 组织上下文并生成回答，实现了检索与生成的清晰解耦，是 RAG 系统可控性与质量的核心保障。 
### 3.5 阶段五：评估 (Evaluation)
当构建一个`RAG`系统后，一个很核心的问题就是如何科学的评估它的表现，如何量化的追踪、迭代并提升`RAG`应用的性能，当系统出现幻觉时如何快速的定位问题，这都是对于开发者来说非常关键的。

文档对于`RAG`系统的评估主要聚焦于解决三个核心问题：

- 检索质量

  检索是否把与问题最相关的信息找出来，有没有遗漏关键信息，有这么几个衡量指标：Recall@K，在检索返回的前`k`个文档块中是否包含至少一个于query相关的正确文档，衡量检索的召回能力

- 生成质量

  生成质量主要有这么几个评估维度：回答事实一致性，主要看生成的内容是否严格基于检索上下文，而非模型自身的幻觉补全；回答相关性：看回答是否真正解决了用户的问题，是否存在看似合理但答非所问的情况；覆盖度与简洁性：是否遗漏相关信息，或者引入与问题无关的冗余内容

- 端到端RAG性能

  端到端关注的问题是：从用户提问到最终答案，系统整体是否看起来像一个可靠的专家，这里需要关注一些最终答案的正确率、可用性，错误类型分布和响应时间与成本等。当系统出现幻觉或者错误时，可以反向拆解定位问题究竟出现在检索层、生成层，还是两者的协同策略上，从而指导下一轮的优化。

这里都是一些概念性的东西，自己看的时候也是混个眼熟，终归还是要落到代码环节。后面做一个菜谱的智能问题系统实战，应该对RAG有个更加深入的理解。这里推荐一个[教程](https://datawhalechina.github.io/all-in-rag/#/)，我也是通读了一遍，但是这种好文章看几遍都不为过，应该是阿里搞得社区，很不错。







