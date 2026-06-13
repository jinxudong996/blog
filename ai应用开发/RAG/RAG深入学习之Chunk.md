之前总结过一篇[文章](https://juejin.cn/post/7598587406706556969#heading-0)，通过`LlamaIndex`的视角来介绍了`RAG`，也知道了一个完整的`RAG`需要这么几个步骤，数据加载，索引构建，索引存储，查询和评估。前面的介绍都是蜻蜓点水的概念介绍，接下来准备写一个系列，对这几个步骤挨个详细的介绍下，对于`RAG`有一个更加深入的理解。

在构建`RAG`的第一个步骤，数据加载环节中，主要干了两件事：将外部数据库接入到我们的`RAG`系统中，然后再将数据通过算法进行分块，接入外部数据库其实比较简单，有各种各样的文档加载器，不管是`PDF`，`word`还是`MarkDown`都有对应的工具，比如`Unstructured`，这就是一个非常专业的文档处理库，提供了统一的接口来处理各种格式的文档，也是目前较为广泛的文档加载解决方案，而`langchain`的` UnstructuredMarkdownLoader `就是对`Unstructured`的封装；在文档加载这个环节，其实没啥太大的区别，直接调用库的接口即可，而分块就不一样了，需要在语义的完整性和检索可分辨性之间找到最优平衡，也可以这么理解，为了保证块的语义完整性，块的大小当然是越大越好，为了检索的可分辨性，块的大小自然是越小越好，最佳的切分应该是满足每个`chunk`自成一个知识单元，同时又只表达一个核心主题。

接下来这篇文章来详细介绍下，希望看完后对于分块有一个更加直观的认识，

##### Chunk策略基础概念

这里的`chunk`就是文本分块，将我们加载后的长篇文档，切分成更小、更易处理的单元，这些切分的文本块，就是后续向量检索和模型处理的基本单元。

为啥要这么处理，直接将长篇文本喂给大模型不是更加省事嘛，最直观的原因就是大模型它是有窗口限制的，不可能接受无限长度的文本，而且文本过长，这个token的成本也难以承受；还有个很重要的原因就是提升检索精度，将长文档切分成语义完整、长度适中的小文本块，系统在检索时更加容易命中和问题直接相关的内容，而不是拖一堆和问题无关的内容来干扰答案。

如何切分呢，有这么几个因素来决定`chunk`的切分

1. 文档长度

   当文档很短，比如几百字这种，就不用太复杂的分块，直接喂给系统都可以；一旦很长，比如一本书这种，就需要细粒度的`chunk`了，

2. 语义密度

   这里的语义密度就是每个`chunk`有多少信息点，也可以理解为每个`chunk`要足够精简，不会包含太多的废话，对于一些高密度文本，比如论文、技术文档、财报、合同这里设计的`chunk`就需要足够的小，因为文本就足够的精简；对于一些低密度，比如小说、故事、日志等，信息散，废话多，`chunk`就可以大一点了。

3. 模型的窗口大小

   这里的模型大小，直接影响一次能够赛多少块进去，`RAG`的流程就是检索出的`chunk`拼接成一个完整的prompt喂给大模型生成答案，所以这里的模型窗口大小，也直接影响了切分的`chunk`大小。

接下来介绍几个常见的分割策略

##### 固定长度切分

这种方法就是按照固定的token数量或者固定的字符数来等长分割长文本，不考虑语义结构，只考虑长度，分割出来的`chunk`长度都是固定的，简单粗暴，实现简单，接下来使用`LlamaIndex`来做一个简易的`RAG`，观察下不同的长度对于检索结果的影响。

长文本采用鲁迅的小说`阿Q正传`，

```python
'''
Author: jinxudong 18751241086@163.com
Date: 2026-02-24 16:52:54
LastEditors: jinxudong 18751241086@163.com
LastEditTime: 2026-02-24 17:16:37
FilePath: \code\RAG初探\002.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from pathlib import Path
from typing import List

from llama_index.core import (
	Document,
	Settings,
	VectorStoreIndex,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data" / "阿Q正传.txt"


def load_document() -> List[Document]:
	"""读取阿Q正传文本，构造为单个 Document。

	这里不用目录读取器，直接控制文本来源，便于演示。
	"""

	if not DATA_FILE.exists():
		raise FileNotFoundError(f"找不到文本文件: {DATA_FILE}")

	text = DATA_FILE.read_text(encoding="utf-8")
	return [Document(text=text, metadata={"source": str(DATA_FILE.name)})]


def build_index_with_chunk_size(documents: List[Document], chunk_size: int) -> VectorStoreIndex:
	"""使用等长分割（按字符数）+ 指定 chunk_size 构建索引。"""

	splitter = SentenceSplitter(
		chunk_size=chunk_size,  # 每个 chunk 最大字符数
		chunk_overlap=0,  # 不重叠，方便观察分割差异
	)

	nodes = splitter.get_nodes_from_documents(documents)
	print(f"chunk_size={chunk_size} 切分得到节点数: {len(nodes)}")

	index = VectorStoreIndex(nodes)
	return index


def demo_retrieval_for_chunk_sizes(query: str, chunk_sizes: List[int], top_k: int = 3) -> None:
	"""对同一个 query，比较不同 chunk_size 的检索结果。"""

	documents = load_document()

	for size in chunk_sizes:
		print("=" * 80)
		print(f"使用 chunk_size={size} 的检索结果（top_k={top_k}）")
		print("-" * 80)

		index = build_index_with_chunk_size(documents, size)
		retriever = VectorIndexRetriever(index=index, similarity_top_k=top_k)

		results = retriever.retrieve(query)

		for i, node_with_score in enumerate(results, start=1):
			node = node_with_score.node
			score = node_with_score.score
			content = node.get_content()

			# 只截取前 200 个字符方便在终端查看
			preview = content[:200].replace("\n", " ")
			print(f"[结果 {i}] 相似度得分: {score:.4f}")
			print(f"内容片段预览: {preview}...")
			print()


def init_settings() -> None:

	# 仅设置向量模型即可完成纯检索实验，不需要 LLM 生成回答。
	Settings.embed_model = HuggingFaceEmbedding(
		model_name="BAAI/bge-small-zh-v1.5"
	)


if __name__ == "__main__":
	# 1. 初始化向量模型等设置
	init_settings()

	# 2. 定义要比较的 chunk_size 列表
	sizes = [512, 1024, 2048, 4096]

	# 3. 定义一个你关心的问题，用来观察检索片段的区别
	user_query = "阿Q为什么会被处决？" 

	# 4. 运行对比实验
	demo_retrieval_for_chunk_sizes(user_query, sizes, top_k=3)


    
 #输出内容
================================================================================         
使用 chunk_size=512 的检索结果（top_k=3）
--------------------------------------------------------------------------------
chunk_size=512 切分得到节点数: 61
[结果 1] 相似度得分: 0.5177
内容片段预览: "看的人们说，大约是解劝的。  "好，好！"看的人们说，不知道是解劝，是颂扬，还是煽动。  然而他们 
都不听。阿Ｑ进三步，小Ｄ便退三步，都站着；小Ｄ进三步，阿Ｑ便退三步，又都站着。大约半点钟，——未庄少有自鸣钟，
所以很难说，或者二十分，——他们的头发里便都冒烟，额上便都流汗，阿Ｑ的手放松了，在同一瞬间，小Ｄ的手也正放松了
，同时直起，同时退开，都挤出人丛去。  "记着罢，妈妈的……"阿Ｑ回过头去说。 ...

[结果 2] 相似度得分: 0.5145
内容片段预览: 于是他渐渐的变换了方针，大抵改为怒目而视了。  谁知道阿Ｑ采用怒目主义之后，未庄的闲人们便愈喜欢
玩笑他。一见面，他们便假作吃惊的说：  "哙，亮起来了。"  阿Ｑ照例的发了怒，他怒目而视了。  "原来有保险灯在这 
里！"他们并不怕。  阿Ｑ没有法，只得另外想出报复的话来：  "你还不配……"这时候，又仿佛在他头上的是一种高尚的光 
容的癞头疮，并非平常的癞头疮了；但上文说过，阿Ｑ是有见识的，他立刻知道和...

[结果 3] 相似度得分: 0.5104
内容片段预览: 至于当时的影响，最大的倒反在举人老爷，因为终于没有追赃，他全家都号啕了。其次是赵府，非特秀才因
为盘上辫子而遭了剪辫之灾，而且还被罚了四块洋钱。  未庄的舆论，在这一点上倒是意见一致的，大家都说阿Ｑ坏，被枪
毙便是他的坏的证据：不坏又何至于被枪毙呢？而城里的舆论却不佳，他们大抵不满意，以为枪毙并无杀头这幺好看；而且
那是怎样的一个可笑的死囚呵，游了那幺久的街，竟没有唱一句戏：他们白跟了一趟了。...
```

这个脚本就是按照固定长度切分`chunk`的，因为目的在于对比这种长度切分的检索效果，所以流程就是接入文本，分割文本，转化向量，相似度检索，最后就是打印检索到的原文片段。

接下来进一步分下下代码：首先在`main`方法中，初始化向量模型，通过`Settings.embed_model`来指定，然后定义一个分块的数组，在前面我们学习过语义密度会影响`chunk`的大小，这里是小说，密度较低的，可以使用较大的`chunk`，然后定义了一个问题`user_query`，随后就执行`demo_retrieval_for_chunk_sizes`方法。

该方法中首先调用`load_document`方法构造一个`docuemnt`，在`LlamaIndex`中`docuemnt`是一个数据容器，而更小的`Node`是从`document`中分割的基本单元，也就是本章的`chunk`，后续的操作就是将`document`分割为一个个的`Node`。首先定义分割的大小，通过`SentenceSplitter`来定义，然后调用`splitter.get_nodes_from_documents`来获取`Node`的列表，有了分割好的`chunk`，下一步就是要构建索引，这里通过` VectorStoreIndex `方法，将`Node`转化为一个个的向量索引，再通过`VectorIndexRetriever`将索引对象构造成一个向量检索器”对象 ，第二个入参`similarity_top_k=top_k`表明使用相似度最高的k个节点，最后就是将问题和我们的所有的`Node`做相速度匹配，按照相似度从高到低取top_k个节点，最后就是打印节点中的文档片段和相似度得分。

可以在控制台看下最终的得分，在512的长度划分中，三个相速度得分分别是0.5177、0.5145和0.5104，看起来这三个`chunk`的相似度区分很低的。

然后开始调用大模型，看下最后的结果

```python
def demo_rag_with_deepseek(query: str, chunk_size: int = 512, top_k: int = 3) -> None:
	"""使用 DeepSeek 作为 LLM，在检索结果基础上生成最终回答。"""

	documents = load_document()
	index = build_index_with_chunk_size(documents, chunk_size)
	query_engine = index.as_query_engine(similarity_top_k=top_k)
	response = query_engine.query(query)

	print("=" * 80)
	print(f"使用 DeepSeek，在 chunk_size={chunk_size}、top_k={top_k} 下的最终回答：")
	print("-" * 80)
	print(str(response))
#输出
阿Q被处决是因为他被认为行为恶劣，而枪毙本身被当成了他品行败坏的证明。
```

可以看到虽然得分很低，但是还是有了正确的结果，应该和我们选择的文档有关，选择的文档应该是大模型自身的知识而不是我们的提供的。这里决定使用一些小众的数据，来再次试验下这个固定长度切分的方法。

我让GPT帮我虚构了一份某新程科技有限公司 2024 年度经营报告，包含营收利润，各个部门的指标，主要是由精准的数字，这样我们来查看我们的分块就简单多了，可以更加直观的查看我们的分块情况，

代码结构完全一致，直接替换下`DATA_FILE`的路径，然后我们的测试文本比较小，切分的长度小一点，`sizes = [64, 128, 256, 512]`，然后我的问题是：user_query = "公司2024 年 Q4 营业收入是多少" ，然后看下最相关的三个块：

```
================================================================================
使用 chunk_size=64 的检索结果（top_k=3）
--------------------------------------------------------------------------------
chunk_size=64 切分得到节点数: 84
[结果 1] 相似度得分: 0.7592
内容片段预览: 营业收入  2024 年度公司实现营业收入 8.72 亿元人民币，同比增长 27.4%。...

[结果 2] 相似度得分: 0.7587
内容片段预览: 5%； - 2024 年 Q2 营业收入 2.05 亿元，同比增长 25.1%； - 2024 年 Q3 营业收入 2....

[结果 3] 相似度得分: 0.7573
内容片段预览: 从季度表现看： - 2024 年 Q1 营业收入 1.83 亿元，同比增长 24....

================================================================================
使用 chunk_size=128 的检索结果（top_k=3）
--------------------------------------------------------------------------------
chunk_size=128 切分得到节点数: 33
[结果 1] 相似度得分: 0.7670
内容片段预览: 1%； - 2024 年 Q3 营业收入 2.34 亿元，同比增长 28.9%； - 2024 年 Q4 营业收入 2.50 亿元，同比增长 30.7%。  2. 利润情况  2024 年度公司
实现归属于母公司股东的净利润 1.26 亿元，同比增长 41....

[结果 2] 相似度得分: 0.7286
内容片段预览: 营业收入  2024 年度公司实现营业收入 8.72 亿元人民币，同比增长 27.4%。其中： - 软件及 SaaS 订阅收入：5.13 亿元，占总收入的 58.84%，同
比增长 34.9%； - 项目实施与技术服务收入：2.47 亿元，占比 28....

[结果 3] 相似度得分: 0.6995
内容片段预览: 经营目标 - 2025 年公司总体营业收入目标为 10.80–11.20 亿元，目标同比增长区间 23%–28%； - 净利润目标为 1.50–1.65 亿元，目标净利率区间 
14.0%–15....

```

我的实际上的文档内容是这样的：

```
从季度表现看：
- 2024 年 Q1 营业收入 1.83 亿元，同比增长 24.5%；
- 2024 年 Q2 营业收入 2.05 亿元，同比增长 25.1%；
- 2024 年 Q3 营业收入 2.34 亿元，同比增长 28.9%；
- 2024 年 Q4 营业收入 2.50 亿元，同比增长 30.7%。
```

可以看到在`chunk_size=128`时，相似度得分最高的块中看到了我们想要的内容。

然后调用大模型，也是正确的回答了我们的问题。

```
chunk_size=128 切分得到节点数: 33
================================================================================
使用 DeepSeek，在 chunk_size=128、top_k=3 下的最终回答：
--------------------------------------------------------------------------------
公司2024年第四季度的营业收入为2.50亿元。
```

这种固定长度切块的方法确实非常的简单方便，对于这种简单的长文档还是非常有效果的，它实际上还有一个参数就是`chunk_overlap`，这个案例中我们设置了0，这个参数表明块中间重复的字符数，就是为了保留语义的完整性而设置的。

##### 递归分块

递归分块就是预先定义一组分隔符，按照优先级从大到小递归拆分，经可能的保留语义的完整性，在满足最大` chunk_size  `的前提下停止拆分。

比如当我们有一个3000字的文档，` chunk_size  `指定的是500，递归分块的逻辑就是首先按照段落去拆分，也就是`\n\n`，如果某一段的字符数超过了` chunk_size  `，再去按照换行`\n`，如果某一行大于` chunk_size  `，再去按照句号去拆分`。`，如果还超过了` chunk_size  `，就按照空格划分，最后还超过，那就直接按照长度去拆分。他的核心思想就是优先保留文本的语义结构。

在`langchain`中是这么来递归分块的：

```python
text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", "。", "，", " ", ""],  # 分隔符优先级
    chunk_size=200,
    chunk_overlap=10,
)
```

来更改下上述的脚本：

先安装下依赖

```python
pip install langchain
pip install langchain-text-splitters
```

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

def build_index_with_recursive_splitter(
    documents: List[Document],
    chunk_size: int = 200,
    chunk_overlap: int = 10,
) -> VectorStoreIndex:
    # 1. 先把所有 Document 合并成一个长文本（也可以按需扩展为多文档）
    full_text = "\n".join(doc.text for doc in documents)

    # 2. 用 RecursiveCharacterTextSplitter 做递归分块
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "。", "，", " ", ""],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    chunks = text_splitter.split_text(full_text)

    print(
        f"使用递归分块：chunk_size={chunk_size}, chunk_overlap={chunk_overlap}, "
        f"得到 chunk 数量: {len(chunks)}"
    )

    # 3. 把每个 chunk 封装成 LlamaIndex 的 TextNode，再构建向量索引
    nodes: List[TextNode] = []
    for i, chunk in enumerate(chunks):
        node = TextNode(text=chunk, metadata={"chunk_id": i})
        nodes.append(node)

    index = VectorStoreIndex(nodes)
    return index
```

只需要改动下我们分块的逻辑，来看下输出：

```
使用递归分块：chunk_size=200, chunk_overlap=10, 得到 chunk 数量: 26
================================================================================
递归分块检索结果：chunk_size=200, chunk_overlap=10, top_k=3
--------------------------------------------------------------------------------
[结果 1] 相似度得分: 0.7475
内容片段预览: 从季度表现看： - 2024 年 Q1 营业收入 1.83 亿元，同比增长 24.5%； - 2024 年 Q2 营业收入 2.05 亿元，同比 
增长 25.1%； - 2024 年 Q3 营业收入 2.34 亿元，同比增长 28.9%； - 2024 年 Q4 营业收入 2.50 亿元，同比增长 30.7%。  2. 
利润情况...

[结果 2] 相似度得分: 0.6690
内容片段预览: 3. 经营目标 - 2025 年公司总体营业收入目标为 10.80–11.20 亿元，目标同比增长区间 23%–28%； - 净利润目标为
 1.50–1.65 亿元，目标净利率区间 14.0%–15.0%； - 持续保持经营性现金流净额为正，并确保销售收现比不低于 105%。...       

[结果 3] 相似度得分: 0.6674
内容片段预览: 二、整体经营情况  2024 年，在复杂多变的宏观环境和激烈的市场竞争下，公司坚持“产品驱动 + 行业深耕”的战略 
方向，实现营业收入和净利润双增长。  （一）收入与利润  1. 营业收入...
```

可以看到相似度得分最高的块，非常精准的找到了我们的问题相关的信息。

##### 基于文件结构或语义

在有些文档处理过程中，单纯凭借换行、标点符号可能无法准确的文档的逻辑结构，比如在论文、报告或者说明书中，段落、标题、表格和列表都有特定的语义，这时不仅需要文本的分隔符号，还需要对文档的排版结构进行分割，这就需要用到更加智能的分割方法了。

` Unstructured `前面介绍过，是一个非常专业的处理文档的工具库，`langchain`也集成了，它支持将文档拆分成结构化语义块，比如`Tutle`、`Table`、`Header`等。他有这么几种分块策略：

1. by_title，按照标题层级划分，可以保持完整的章节语义，特别适合技术文档
2. basic，按照元素顺序合并到指定长度
3. by_page，按照pdf的页数分块
4. none，只返回原始的element

接下来用代码来体验下，使用GPT帮我生成了一个测试文档，是一个较为复杂的文档，包括各种不同字号的标题、无序列表，还有一些具体的数字，大概长这样：

```
（三）研发与技术类

1. 代码仓库与分支管理
- Git 仓库命名规范示例
- 主干开发 / GitFlow / Trunk-Based Development 对比说明

2. 发布流程
- 日常发布流程（工作日 15:00–18:00）
- 紧急发布流程（7×24 小时值班支持）
```

代码的大致结构和前面一致，只是分块的方法需要更换下

```python
from langchain_community.document_loaders import UnstructuredFileLoader

def build_index_with_unstructured_by_title() -> VectorStoreIndex:

    if not DATA_FILE.exists():
        raise FileNotFoundError(f"找不到文本文件: {DATA_FILE}")

    loader = UnstructuredFileLoader(
        str(DATA_FILE),
        mode="elements",  # 返回元素级别的块，而不是整篇文本
        strategy="fast",  # 文本类用 fast 即可
        by_title=True,  # 关键参数：按标题组织块
    )

    docs = loader.load()
    print(f"使用 Unstructured by_title 分块，得到元素数: {len(docs)}")

    nodes: List[TextNode] = []
    for i, doc in enumerate(docs):
        text = doc.page_content
        metadata = dict(doc.metadata or {})
        metadata["chunk_id"] = i

        node = TextNode(text=text, metadata=metadata)
        nodes.append(node)

    index = VectorStoreIndex(nodes)
    return index
```

问题是这样的，user_query = "一周都要随时在线支持的是啥发布流程"，来看下分块的情况

```
Unstructured by_title 分块下的检索结果（top_k=3）
--------------------------------------------------------------------------------
[结果 1] 相似度得分: 0.5341
内容片段预览: 日常发布流程（工作日 15:00–18:00）...

[结果 2] 相似度得分: 0.5218
内容片段预览: 紧急发布流程（7×24 小时值班支持）...

[结果 3] 相似度得分: 0.5070
内容片段预览: 2. 发布流程...
```

可以看到和问题相关的分块已经包含在`top_k=3`里面了，然后调用下大模型看下结果：

```
================================================================================
使用 DeepSeek + Unstructured by_title 分块的 RAG 回答（top_k=3）
--------------------------------------------------------------------------------
紧急发布流程提供7×24小时值班支持，意味着一周内随时在线。
```

也是正确的回答了我们的问题。

上面是`langchain`中的语义分块，在`llamaindex`中也有语义分块的方法` SemanticSplitterNodeParser `，就是利用`embedding`模型计算句子向量，比较相邻句子的相似度，根据阙值决定是否断开。

同样的代码结构保持不变，分块方法是这样的

```python
def build_index_with_semantic_splitter(
    documents: List[Document],
    breakpoint_percentile_threshold: float = 95.0,
    buffer_size: int = 1,
) -> VectorStoreIndex:

    # 依赖 Settings.embed_model 中已经配置好的向量模型，显式传入避免默认走 OpenAI
    splitter = SemanticSplitterNodeParser.from_defaults(
        embed_model=Settings.embed_model,
        breakpoint_percentile_threshold=breakpoint_percentile_threshold,
        buffer_size=buffer_size,
    )

    nodes: List[TextNode] = splitter.get_nodes_from_documents(documents)

    print(
        "使用语义分块："
        f"breakpoint_percentile_threshold={breakpoint_percentile_threshold}, "
        f"buffer_size={buffer_size}, 得到节点数: {len(nodes)}"
    )

    index = VectorStoreIndex(nodes)
    return index

调用方法
demo_semantic_retrieval(
        user_query,
        breakpoint_percentile_threshold=95.0,
        buffer_size=1,
        top_k=3,
    )

```

`SemanticSplitterNodeParser`中的`breakpoint_percentile_threshold`参数表明一个阙值，前面介绍过这种语义分块会将所有的句子来算`embedding`，看相邻句子之间的相似度，低于这个值的被认为是语义变化比较大，可以切断的地方，这里设置成95.0，当某个句子的语义变化，超过所有变化的95%以上时，才算断点； `buffer_size=1`  这个参数是为了语义的完整性而设置的，表明每个块两侧额外捎带的句子数，类似于前面的`chunk_oerlap`。

看下具体的分块：

```python
[chunk 1] 相似度得分: 0.4694
内容片段预览: 标题下方紧跟的段落、列表、表格等内容，会被归类到该标题对应的块中； 3. 遇到下一个同级标题时，结 
束当前块，开始新的块。  （二）混合内容结构示例  下面是一段混合了列表、半结构化表格和普通段落的示例，用于测试 
Unstructured 在 by_title 策略下对复杂内容的处理效果。  1. 关键时间节点 - 方案评审完成时间：2024-03-15 - 试点 
部门上线时间：2024-05-01 ...

[chunk 2] 相似度得分: 0.4574
内容片段预览: 企业内部知识库建设方案（示例文档，用于 Unstructured by_title 分块测试）  一、项目背景  随着公司
业务线不断增加，员工需要查阅的制度、流程、技术文档呈指数级增长。目前主要存在以下问题： 1. 文档分散在网盘、本 
地电脑和邮件附件中，难以及时搜索。 2. 文档缺乏统一命名规范，重复内容较多，版本混乱。 3. 新员工入职后需要向同 
事反复询问相同问题，影响整体效率。  本方案旨在通...
```

这里可以看到，分的块和我们的答案其实不怎么相关，最后我调用大模型，他竟然回答出来了，后续差看了下代码发现我只截取了前200，完全打印出来后还是可以看到问题相关的块是被切出来了。

##### 滑动窗口分块

前面介绍过固定长度切分，就是指定搞一个size大小，然后将一个长文档根据这size来切分，同时还有一个`overlap`参数，这个就是边缘补偿，防止语义被切断。

而滑动窗口就是重叠的固定长度分块，可以保证让在每一个块中，主要的信息是居中的，这样后续的`embedding`中，中间内容的语义权重会大一点，可以非常有效的提升分块的召回率。

```python
def build_index_with_sliding_window(
    documents: List[Document],
    window_size: int = 3,
) -> VectorStoreIndex:
    """使用 SentenceWindowNodeParser（句子滑动窗口）方式分块并构建索引。"""

    node_parser = SentenceWindowNodeParser.from_defaults(
        window_size=window_size,
        window_metadata_key="window",
        original_text_metadata_key="original_sentence",
    )

    nodes = node_parser.get_nodes_from_documents(documents)

    print(
        f"使用 SentenceWindowNodeParser 句子滑动窗口分块：window_size={window_size}, "
        f"得到节点数: {len(nodes)}"
    )

    index = VectorStoreIndex(nodes)
    return index
```

和固定长度分块的用法非常的相似。

当然滑动窗口会导致块的数量暴涨，对于后续的`embedding`成本会变得跟高，包括后续的向量库的成本也会增大



##### 父子结构语义分块

为了提高分块的召回精度和保证上下文的完整性，可以使用父子结构的语义分块。就是将一个长文档先划分成若干个较大的块，称之为父块，然后再将每个父块切分成若干个字块，后续在检索阶段，对字块做`embedding`，用query搜索字块，找到最相似的top_k，在返回阶段，根据child的parent_id，将对应的父块返回给大模型。

```python
def build_index_with_hierarchical_chunks(
    documents: List[Document],
    chunk_sizes: Optional[List[int]] = None,
) -> VectorStoreIndex:

    if chunk_sizes is None:
        chunk_sizes = [2048, 512, 128]

    node_parser = HierarchicalNodeParser.from_defaults(
        chunk_sizes=chunk_sizes,
    )

    nodes = node_parser.get_nodes_from_documents(documents)

    print(
        "使用 HierarchicalNodeParser 父子层级分块："
        f"chunk_sizes={chunk_sizes}, 得到节点数: {len(nodes)}"
    )

    index = VectorStoreIndex(nodes)
    return index
```

这里的分块虽然不是严格意义的父子结构，是根据不同粒度的文本块大小来组织的，比如定义的层级`[2048, 512, 128]`，将文档按照多个层级切成不同大小的节点，这个层级是一个立体的层级，比如第一层全部都是2048长度的大小，第二层级全部都是512层级的大小，第二层切的就是第一层的，而第三层就是128长度的，根据` parent-child `来关联起来。

看下输出的块：

```
================================================================================
父子层级分块检索结果：chunk_sizes=[2048, 512, 128], top_k=3
--------------------------------------------------------------------------------
[结果 1] 相似度得分: 0.5830
内容片段预览: 发布流程 - 日常发布流程（工作日 15:00–18:00） - 紧急发布流程（7×24 小时值班支持）  四、文档分级与命名规 
范  （一）文档分级  文档按重要性和稳定性分为三个等级： - L1：核心制度与关键流程。...

[结果 2] 相似度得分: 0.5193
内容片段预览: 考勤与假期 - 考勤打卡规则说明 - 加班与调休政策（2024 版） - 年假、病假、事假、婚假、产假的申请流程  （二
）财务与报销类  1. 日常报销 - 差旅报销政策（机票、酒店、餐补标准） - 市内交通报销规范（打车、地铁、公交） - 发票合规性
要求及常见问题 FAQ  2. 预算与费用控制 - 各部门年度预算编制指引 - 单笔支出超过 5 万元的审批链路说明  （三）研发与技术类
  1. ...

[结果 3] 相似度得分: 0.5036
内容片段预览: 关键时间节点 - 方案评审完成时间：2024-03-15 - 试点部门上线时间：2024-05-01 - 全公司推广完成时间：2024-09-30  2. 里程碑进度（文字表格形式）  阶段
时间范围        主要产出 阶段一：调研与设计   
```

投喂大模型更多代码是这样：

```python
def demo_hierarchical_rag_with_deepseek(
    query: str,
    chunk_sizes: Optional[List[int]] = None,
    top_k: int = 3,
) -> None:
    """在父子层级分块的基础上，调用 DeepSeek 做 RAG 回答。"""

    documents = load_document()
    index = build_index_with_hierarchical_chunks(
        documents,
        chunk_sizes=chunk_sizes,
    )

    # 与检索 demo 一样，底层用小块做相似度检索，
    # AutoMergingRetriever 负责把若干子块替换成更大的父块，
    # 再作为上下文交给 RAG
    base_retriever = VectorIndexRetriever(index=index, similarity_top_k=top_k)
    retriever = AutoMergingRetriever(base_retriever, index.storage_context)
    query_engine = RetrieverQueryEngine(retriever=retriever)
    response = query_engine.query(query)

```

 这个核心代码就三行，`base_retriever`就是包装一层向量检索器，在索引的所有节点上计算相似度，取top_k返回；`retriever`就是通过`AutoMergingRetriever`，将命中的子节点，通过`index.storage_context`保存的父子关系，找到子节点的父节点，用这些父节点来代替子节点返回；最后就是调用大模型`query_engine.query`，可以看到最终给大模型的就是父节点，而子节点因为因为相似度高，所以召回率就高，所以看起来实际检索的就是那些子块。

有一个说法就是，在`RAG`的效果80%都在卡在分块上，这个说法也蛮有道理的，分块就影响着后续`embedding`的效果，直接影响到数据库能不能读取到正确的知识。

下一篇就开始学习`embedding`，这些分块如何转化为向量，相速度检索是咋做的，路漫漫其修远兮，加油。

























