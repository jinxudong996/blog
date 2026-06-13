最近打算往ai应用开发这个方向上转一转，之前也简单的回顾了下py的基础语法，然后就开始ai这个方向的学习了。

ai应用开发目前最火的当然是Agent应用开发，这个对于没基础的还是很有难度的， 相当于RAG，这个可能稍微简单点。

##### 简介

 **RAG** 的全称是 **Retrieval-Augmented Generation**，中文是 **“检索增强生成”**。 其核心思想就是在生成答案之前，先从外部知识库中检索相关信息，然后将这些信息作为上下文提供给大模型，从而指导模型生成更加准确、相关、及时的答案。

一个典型的RAG系统主要分为两个阶段：数据预处理和查询

###### 数据预处理

这一步是为提前准备的资料简历索引，方便快速查找

主要分为这么几个步骤

1. 加载： 从各种数据源（如PDF、Word、网页、数据库）加载原始文档。 
2. 分割： 将长文档切分成更小的、语义完整的文本块。这是因为大模型有上下文长度限制，且小文本块更容易被精准检索。 
3. 向量化： 使用“嵌入模型”将每个文本块转换成一串数字（即向量）。这个向量可以代表文本的语义信息。语义相近的文本，其向量在空间中的距离也更近。 
4. 存储： 将这些向量及其对应的原始文本存储到专门的数据库中，这种数据库被称为 向量数据库

##### 查询

这一步是当用户提问时，系统实时工作的过程

1. 检索：用户提出一个问题， 系统使用同样的“嵌入模型”将这个问题也转换为一个向量，在向量数据库中进行相似性搜索，找出与问题向量最相似的几个文本块
2. 增强：将用户原始问题和检索到的文本块组合到一起，构建成一个完善的提示
3. 生成：然后就将这个精心构建的提示词发送给大语言模型，大模型给予提供的上下文来生成最终答案。

##### 基础搭建

这里首先要介绍一个python框架，` LlamaIndex`，专门设计用于构建由大型语言模型驱动的应用程序。他可以非常方便的帮我们连接私有数据域和通用大模型，从而创建出知识渊博、能够根据提供的数据进行推理和回答的智能应用。

它可以帮我们解决这么几个问题：

1. 数据接入：提供了统一的接口来处理各个数据格式，比如pdf，ppt，word等。
2. 数据机构化： 原始的非结构化文本数据无法被 LLM 有效利用。LlamaIndex 能将其结构化成 LLM 能够理解和推理的格式。 
3. 高效检索： 当你的数据量很大时，如何快速、准确地找到最相关的信息片段是 RAG 系统的关键。LlamaIndex 提供了先进的检索和查询接口。 
4. 与LLM集成： 它无缝衔接了数据检索部分和 LLM 生成部分，让开发者无需关心底层复杂的交互细节 

接下来写一个实例来体验下LlamaIndex的强大

```python
# 第一行代码：导入相关的库
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.deepseek import DeepSeek
from dotenv import load_dotenv
import os

def _get_deepseek_key() -> str:
    load_dotenv()  # 允许在当前目录读取 .env
    key = os.getenv("DEEPSEEK_API_KEY")
    return key

DEEPSEEK_KEY = _get_deepseek_key()

# 加载本地嵌入模型
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-zh")

# 创建 DeepSeek LLM (不在代码中硬编码密钥)
llm = DeepSeek(model="deepseek-chat", api_key=DEEPSEEK_KEY)

# 加载数据（使用规范路径，避免相对路径错误）
base_dir = os.path.dirname(os.path.abspath(__file__))  # 当前脚本所在目录
doc_path = os.path.normpath(os.path.join(base_dir, "..", "data", "黑神话悟空设定.txt"))
if not os.path.exists(doc_path):
    raise FileNotFoundError(f"文档未找到: {doc_path} 请确认文件存在并名称匹配。")
documents = SimpleDirectoryReader(input_files=[doc_path]).load_data()

# 构建索引
index = VectorStoreIndex.from_documents(
    documents,
    embed_model=embed_model
)

# 创建问答引擎
query_engine = index.as_query_engine(
    llm=llm
)

# 开始问答
# print(query_engine.query("黑神话悟空中有哪些战斗工具?"))
print(query_engine.query("帮我介绍下黑神话悟空?"))
《黑神话：悟空》是一款以中国文化和自然景观为背景的游戏，故事分为六个章节，分别是“火照黑云
”、“风起黄昏”、“夜生白露”、“曲度紫鸳”、“日落红尘”和“未竟”。游戏设有两个结局，玩家的选择和
经历将决定最终结局的走向。

每个章节结束时，会通过二维和三维动画过场来展现游戏的叙事和主题元素。游戏设定中融入了许多 
中国文化和自然地标，例如重庆的大足石刻、山西省的小西天、南禅寺、铁佛寺、广胜寺和鹳雀楼等 
。此外，游戏还结合了佛教和道教的哲学元素。
```

这里首先就是导入一些所需要的库，然后读取API_KEY，接着读取我们的私有数据域黑神话悟空设定.txt

运行这个实例有点小坑：python环境不能太高，14就不太行，会冲突，我用的12；需要科学上网，如果个给虚拟环境设置代理就更好了



下面就开始正式的学习了



##### 文档加载



###### 简单文本读取

首先用`langchain`来读取一段文字

```python
from langchain_community.document_loaders import TextLoader
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.normpath(os.path.join(base_dir, "..", "..", "data", "黑神话悟空设定.txt"))
if not os.path.exists(data_path):
	raise FileNotFoundError(f"目标文件不存在: {data_path} 请确认名称是否为 '黑神话悟空设定.txt'")

loader = TextLoader(data_path, encoding="utf-8")
documents = loader.load()
print(documents)
#输出
[Document(metadata={'source': 'H:\\project\\blog\\blog\\ai应用开发\\code\\data\\黑神话悟空设定.txt'}, page_content='《黑神话：悟空》的故事可分为六个章节，名为“火照黑云”、“风起黄昏”、“夜生白露”、“曲度紫鸳”、“日落红尘”和“未竟”，
并且拥有两个结局，玩家的选择和经历将影响最终的结局。\n\n每个章节结尾，附有二维和三维的动画过场，展示和探索《黑神 
话：悟空》中的叙事和主题元素。\n\n游戏的设定融合了中国的文化和自然地标。例如重庆的大足石刻、山西省的小西天、南禅 
寺、铁佛寺、广胜寺和鹳雀楼等，都在游戏中出现。游戏也融入了佛教和道教的哲学元素。')]
```

其中`metadata`就是元数据，存储与文档相关的元信息，例如文档的来源、作者、日期等。

当然`langchain`有各种各样的loader，可以看下文档 地址[https://docs.langchain.com/oss/python/langchain/retrieval#document-loaders]

然后使用`llama_index`来读取文本

```python
from llama_index.core import SimpleDirectoryReader
import os

# 构建规范路径：当前脚本 -> 上级(code) -> data -> 文件名
base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.normpath(os.path.join(base_dir, "..", "..", "data", "黑神话悟空设定.txt"))

if not os.path.exists(data_path):
    raise FileNotFoundError(f"目标文件不存在: {data_path} 请确认名称是否为 '黑神话悟空设定.txt'")

# 使用 LlamaIndex 的文件读取器加载文档
reader = SimpleDirectoryReader(input_files=[data_path])
docs = reader.load_data()

print(f"读取到 {len(docs)} 个文档")
print("第一段内容预览:\n")
print(docs[0].text[:300])
#输出
有两个结局，玩家的选择和经历将影响最终的结局。

每个章节结尾，附有二维和三维的动画过场，展示和探索《黑神话：悟空》中的叙事和主题元素。

游戏的设定融合了中国的文化和自然地标。例如重庆的大足石刻、山西省的小西天、南禅寺、铁佛寺、广胜寺和鹳雀楼等， 
都在游戏中出现。游戏也融入了佛教和道教的哲学元素。
```



###### 结构化文本读取

结构化文本就是保留了文本数据结构的，比如`json`、`markdown`、网页等。

读取json

```python
from langchain_community.document_loaders import JSONLoader


def print_docs(title, docs):
	print(title)
	if not docs:
		print("(无结果)")
		return
	for i, d in enumerate(docs, 1):
		print(f"{i}. {d.page_content}")


if __name__ == "__main__":
	print("=== JSONLoader 加载结果 ===")

	# 1. 主角信息
	print("\n1. 主角信息：")
	main_loader = JSONLoader(
		file_path="../../data/人物.json",
		jq_schema='.mainCharacter | "姓名：" + .name + "，背景：" + .backstory',
		text_content=True,
	)
	main_docs = main_loader.load()
	print_docs("主角：", main_docs)

	# 2. 支持角色信息
	print("\n2. 支持角色信息：")
	support_loader = JSONLoader(
		file_path="../../data/人物.json",
		jq_schema='.supportCharacters[] | "姓名：" + .name + "，背景：" + .background',
		text_content=True,
	)
	support_docs = support_loader.load()
	print_docs("支持角色：", support_docs)

	# 3. 基本信息（可选）
	print("\n3. 基本信息：")
	info_loader = JSONLoader(
		file_path="../../data/人物.json",
		jq_schema='"标题：" + .gameTitle + "，引擎：" + .basicInfo.engine + "，发行：" + .basicInfo.releaseDate',
		text_content=True,
	)
	info_docs = info_loader.load()
	print_docs("游戏信息：", info_docs)

```

需要安装下`jq`这个包， 用 `jq` 表达式从 JSON 中选择/转换数据。JSONLoader 会用这个表达式提取片段，并将结果作为文档的 `page_content`（当 `text_content=True` 时为纯文本）。 

网页抓取就有点爬虫的意味了，

```python
import bs4
from langchain_community.document_loaders import WebBaseLoader
page_url = "https://zh.wikipedia.org/wiki/黑神话：悟空"
# loader = WebBaseLoader(web_paths=[page_url])
# docs = []
# docs = loader.load()
# assert len(docs) == 1
# doc = docs[0]
# print(f"{doc.metadata}\n")
# print(doc.page_content.strip()[:3000])


# 只解析文章的主体部分
loader = WebBaseLoader(
    web_paths=[page_url],
    bs_kwargs={
        "parse_only": bs4.SoupStrainer(id="bodyContent"),
    },
    # bs_get_text_kwargs={"separator": " | ", "strip": True},
)
docs = []
docs = loader.load()
assert len(docs) == 1
doc = docs[0]
print(f"{doc.metadata}\n")
print(doc.page_content)
```



###### 解析图文

```python
from langchain_community.document_loaders import UnstructuredImageLoader
image_path = "../../data/黑悟空/黑悟空英文.jpg"
loader = UnstructuredImageLoader(image_path)

data = loader.load()
print(data)
```

这里就是ocr识别图片

###### 解析PDF

pdf解析其实还蛮复杂的，主要源于格式的复杂，有图文结构

主要有三大类别：



###### 表格数据导入