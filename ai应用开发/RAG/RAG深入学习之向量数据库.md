

##### 一、向量数据库简介

前面我们了解到RAG的流程是，先将长文本切块，然后将这些块通过嵌入模型转换成向量，然后通过对比用户的问题，计算向量的相似性来找出和用户问题最相关的文本，当向量的数量级别增长到百万、千万甚至上亿级别，如何快速的、准确的从海量向量中找到和用户查询最相关的那几个呢，

传荣的数据库，比如`MySQL`他们就很擅长处理结构化数据的精准匹配查询，比如`WHERE age = 18`，或者模糊匹配` WHERE name LIKE '%张%' `，但是他们并非为处理高维向量的相似性搜索而设计的，在庞大的向量集合中进行暴力、线性的相似度计算，传统数据库的计算成本和时间延迟根本无法接受。向量数据库的出现，就很好的解决了这一问题，他就是专门设计用于高效存储、管理和查询高维向量的数据库系统。

##### 二、主流索引结构

向量数据库的核心价值在于高效处理海量高维数据的能力，其高效处理的能力主要来源于高效的相似性搜索。

这里先来介绍下` ANN  `，也就是` Approximate Nearest Neighbo `，近似最近邻搜索，就是不追求绝对精准，允许一点点的精度损失来换取数量级的搜索速度。这里有一个权衡：速度、精度和内存，你不可能同时拥有三个，最多只能同时做好两个，必须牺牲一个。

可以从这三个维度来解释下：

1. 精度，也就是召回率Recall，就是被ANN找回来的比例
2. 速度，也就是延迟，查询一次需要多长时间，这个当然是速度越快体验越好，越快的话就是机器的QPS也越高
3. 内存占用，索引需要将结构存储在内存中，这样才能够更快，这里有两个常用的索引结构，HNSW和IVF，

当想要又快又准，就需要使用HNSW这种图结构，当想要又快又省内存，就必须要牺牲精度了，可以使用IVF这种聚类结构。

当前RAG主流的索引就两种结构：

1. IVF索引

   倒排文件，给向量数据分桶，检索时只找到相关的桶，而不会去查询全部桶。大概流程就是，首先会做一个预处理，对全库所有的向量做K-Means聚类，生成`nlist`个聚类中心，将每个向量分配到距离最近的桶里，这样相似的向量就会在相同的桶或者相邻的桶里，不相似的向量彻底分开。

   在检索的时候，拿到查询向量，会先计算它和所有的聚类中心的距离，找最相似的桶，然后在这最相似的桶中做暴力检索，返回TopK。

   这种方法的缺点就是在数据量大了后，聚类就越难精准，很容易遗漏相关向量，对于召回率极高的场景就不太适合饿了。

2. HNSW索引

   这是目前工业界最主流的ANN索引，可以理解为给向量建多层高速公路网，高层快速导航，底层精准查找。

   在预处理阶段，会构建多层图结构，在底层是这样的场景：包含所有的向量，每个向量会和周围多个相似向量建立邻居连接；高层就是底层的缩略版，向量数量极少，拦截稀疏；最顶层只有一个入口向量，是整个图的导航起点

   在检索阶段，从顶层的入口向量开始，找到距离查询向量最近的邻居，然后下钻到下一层；每一层都重读找最近的邻居，然后下钻，直接到达底层；在底层精准遍历少量的邻居向量，计算距离后返回TopK

##### 三、主流数据库介绍

当前主流的向量数据库主要有这么几种：

1. Pinecone

    是一款完全托管的向量数据库服务，采用Serverless架构设计。它提供存储计算分离、自动扩展和负载均衡等企业级特性，并保证99.95%的SLA。Pinecone支持多种语言SDK，提供极高可用性和低延迟搜索（<100ms），特别适合企业级生产环境、高并发场景和大规模部署。 

2. Milvus

    是一款开源的分布式向量数据库，采用分布式架构设计，支持GPU加速和多种索引算法。它能够处理亿级向量检索，提供高性能GPU加速和完善的生态系统。Milvus特别适合大规模部署、高性能要求的场景，以及需要自定义开发的开源项目。 

3. Qdrant

    是一款高性能的开源向量数据库，采用Rust开发，支持二进制量化技术。它提供多种索引策略和向量混合搜索功能，能够实现极高的性能（RPS>4000）和低延迟搜索。Qdrant特别适合性能敏感应用、高并发场景以及中小规模部署。 

4. Weaviate

    是一款支持GraphQL的AI集成向量数据库，提供20+AI模块和多模态支持。它采用GraphQL API设计，支持RAG优化，特别适合AI开发、多模态处理和快速开发场景。Weaviate具有活跃的社区支持和易于集成的特点。 

5. Chroma

   是一款轻量级的开源向量数据库，采用本地优先设计，无依赖。它提供零配置安装、本地运行和低资源消耗等特性，特别适合原型开发、教育培训和小规模应用。Chroma的部署简单，适合快速原型开发。 

6. FAISS

    是一款高性能的开源向量相似度搜索库，专注于大规模向量的快速检索，支持多种 ANN 索引（如 HNSW、IVF），提供 CPU/GPU 加速能力，但本身不包含数据库功能，更适合作为底层引擎用于构建高性能向量检索系统或作为其他向量数据库的核心组件 

##### 四、实战环节

接下来我们通过开源的FAISS和商用的Milvus的小案例，加深我们对向量数据库的理解。

###### FAISS

这个向量数据库是由Meta开源的，以高效的TopK检索而著称，接下来就详细的了解下这个向量数据库。

首先安装下这个向量数据库，

```
pip install faiss-cpu
```

然后写一个增删改查的案例，来加深对数据库的理解

首先选用一个开源的嵌入模型`BAAI/bge-small-zh-v1.5`，来录入几个句子，然后输入一个问题来做相似度匹配，首先封装下这个开源的模型：

```python
class OpenSourceEmbedder:
    """封装开源嵌入模型。"""

    def __init__(self, model_name: str = "BAAI/bge-small-zh-v1.5"):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.dim = self.model.get_sentence_embedding_dimension()

    def encode(self, texts: list[str]) -> np.ndarray:
        """输出归一化后的向量，适配余弦相似度检索。"""
        vectors = self.model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        return vectors.astype("float32")
```

这个类就是封装了开源的嵌入模型，首先在`__init__`初始化时，定义了模型的名称，通过`SentenceTransformer`从` HuggingFace  `下载模型，后续直接从缓存获取，然后通过`self.model.get_sentence_embedding_dimension()`来获取该模型的维度，绑定到类的实例上，后续建索引的时候，会用到这个向量维度；

类中定义了一个方法`encode`输出向量，调用`self.model.encode`方法，将`texts`转换为向量，其中`normalize_embeddings`参数设置为true，就是将每条向量归一化，将长度设置为1，避免做内积的时候，向量的长度来影响结果，这样归一化后的内积就等价于余弦相似度，会更加符合语义相似度的直觉；convert_to_numpy直接返回numpy数组；show_progress_bar不现实进度条，这样控制台会干净很多。最后返回vectors.astype("float32")，返回32位浮点数的矩阵。

调用时是这样

```python
embedder = OpenSourceEmbedder("BAAI/bge-small-zh-v1.5")
```

这个`embedder`就是一个实例，实例上有该模型的维度，还有将文本转为向量的方法。

然后封装数据库

```python
class FaissSemanticSearcher:
    """封装 Faiss 检索。使用 IndexFlatIP + 归一化向量 = 余弦相似度。"""

    def __init__(self, embedder: OpenSourceEmbedder):
        self.embedder = embedder
        self.index = faiss.IndexFlatIP(embedder.dim)
        self.texts: list[str] = []

    def build(self, texts: list[str]) -> None:
        if not texts:
            raise ValueError("至少输入 1 条句子")

        clean_texts = [t.strip() for t in texts if t.strip()]
        if not clean_texts:
            raise ValueError("输入句子不能为空")

        vectors = self.embedder.encode(clean_texts)
        self.index.reset()
        self.index.add(vectors)
        self.texts = clean_texts

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        if not self.texts:
            return []

        q_vec = self.embedder.encode([query])
        k = min(top_k, len(self.texts))
        scores, ids = self.index.search(q_vec, k)

        results = []
        for score, idx in zip(scores[0], ids[0]):
            results.append(
                {
                    "rank": len(results) + 1,
                    "score": float(score),
                    "text": self.texts[int(idx)],
                }
            )
        return results

```

这个类是这样调用的

```python
searcher = FaissSemanticSearcher(embedder)
```

接受一个嵌入模型的实例，该实例上面也介绍过。这个类首先在初始化的时候，保存了下`embedder`，就是前面嵌入模型的实例；`faiss.IndexFlatIP(embedder.dim)`就是`Faiss`数据库的索引，texts是原始文本列表。这里保存原始文本的原因是，数据库只会返回命中的向量下标和相速度分数，并不会返回原始的文本块，这就需要我们去将文本块和向量来做一个关联，在build方法中是通过`self.index.add(vectors)`按顺序将向量入库，所以保存的self.texts[i]就是向量对应的原始文本。业界常规的做法就是给每一个向量添加一个业务id，将原始的文本块对应这个业务id存储到数据库中，比如常见的关系型数据库和非关系型数据库，可以通过这个业务id来将原始文本和向量数据库关联起来。

这个类还封装了一个`build`方法，这个方法就是将文本入库，首先做了非空判断，然后调用`embedder.encode`方法将文本转化为向量，然后将调用`index.add`入库。

类中的search方法，这个方法就是来寻找最相似的文本。首先将用户的提问转化为向量`self.embedder.encode([query])`，然后调用数据库的`index.search`方法去搜索，结果会返回两个数组，scores是相似度分数，ids是命中的向量下标，可以通过这个下标来匹配到对应的文本块。

完整的代码如下：

```python
from __future__ import annotations

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class OpenSourceEmbedder:
    """封装开源嵌入模型。"""

    def __init__(self, model_name: str = "BAAI/bge-small-zh-v1.5"):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.dim = self.model.get_sentence_embedding_dimension()

    def encode(self, texts: list[str]) -> np.ndarray:
        """输出归一化后的向量，适配余弦相似度检索。"""
        vectors = self.model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        return vectors.astype("float32")


class FaissSemanticSearcher:
    """封装 Faiss 检索。使用 IndexFlatIP + 归一化向量 = 余弦相似度。"""

    def __init__(self, embedder: OpenSourceEmbedder):
        self.embedder = embedder
        self.index = faiss.IndexFlatIP(embedder.dim)
        self.texts: list[str] = []

    def build(self, texts: list[str]) -> None:
        if not texts:
            raise ValueError("至少输入 1 条句子")

        clean_texts = [t.strip() for t in texts if t.strip()]
        if not clean_texts:
            raise ValueError("输入句子不能为空")

        vectors = self.embedder.encode(clean_texts)
        self.index.reset()
        self.index.add(vectors)
        self.texts = clean_texts

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        if not self.texts:
            return []

        q_vec = self.embedder.encode([query])
        k = min(top_k, len(self.texts))
        scores, ids = self.index.search(q_vec, k)

        results = []
        for score, idx in zip(scores[0], ids[0]):
            results.append(
                {
                    "rank": len(results) + 1,
                    "score": float(score),
                    "text": self.texts[int(idx)],
                }
            )
        return results




def interactive_search(searcher: FaissSemanticSearcher) -> None:
    print("\n开始检索。输入 q 退出。")
    while True:
        query = input("\n查询句子: ").strip()
        if query.lower() in {"q", "quit", "exit"}:
            print("已退出。")
            break
        if not query:
            print("查询不能为空。")
            continue

        results = searcher.search(query, top_k=3)
        print("Top-3 结果：")
        for item in results:
            print(f"#{item['rank']} score={item['score']:.4f} | {item['text']}")


def main() -> None:
    print("加载开源嵌入模型: BAAI/bge-small-zh-v1.5")
    embedder = OpenSourceEmbedder("BAAI/bge-small-zh-v1.5")
    searcher = FaissSemanticSearcher(embedder)

    # 你提供的句子（直接向量化并入库）
    texts = [
        "我很喜欢吃苹果的，它膳食纤维、果胶、钾、抗氧化多酚，温和养胃、饱腹感好。",
        "我爱吃红富士这个品牌的苹果，它非常甜，产自山东烟台等地",
        "我红牛苹果也非常喜欢吃，也很甜",
        "苹果是一家非常伟大的公司，乔布斯是他的创始人，我很尊重他",
        "我很喜欢苹果手机，苹果手表，还有苹果电脑",
        "我不喜欢华为手机，它的爱国营销我很反感，它是一家没有底线的公司",
    ]

    searcher.build(texts)
    print(f"\n已入库 {len(searcher.texts)} 条句子，向量维度={embedder.dim}")

    # 你的提问
    query = "我要买苹果公司的股票，你觉得如何"
    print(f"\n查询: {query}")
    results = searcher.search(query, top_k=3)
    print("Top-3 结果：")
    for item in results:
        print(f"#{item['rank']} score={item['score']:.4f} | {item['text']}")


if __name__ == "__main__":
    main()

```

输出结果：

```
已入库 6 条句子，向量维度=512

查询: 我要买苹果公司的股票，你觉得如何
Top-3 结果：
#1 score=0.6664 | 苹果是一家非常伟大的公司，乔布斯是他的创始人，我很尊重他
#2 score=0.6111 | 我很喜欢苹果手机，苹果手表，还有苹果电脑
#3 score=0.5851 | 我很喜欢吃苹果的，它膳食纤维、果胶、钾、抗氧化多酚，温和养胃、饱腹感好。
```

前面介绍过一些索引结构，IVF索引和HNSW索引，这个案例采用的是`faiss.IndexFlatIP`，就是不做任何加速结构，直接暴力算相速度，而且使用内积来计算相似度。

Faiss有很多索引家族，比如

1. Flat，精准检索，IndexFlatIP和IndexFlatL2，在小数据集上做baseline和验证比较好
2. ID映射，给索引加自定义的id，IndexIdMap，对于一些文本较大的，将文本存储业务数据库，通过这个id来将向量和文本做映射
3. IVF，倒排文件分桶加速，IndexIVFFlat向量不压缩，只分桶，IndexIVFPQ这个索引会分桶+PQ压缩，这种支持大规模数据集，而且速度非常快
4. HNSW，图索引，IndexHNSWFlat，效果和速度折中很好，就是内存过大



###### Milvus

Milvus 是一个开源的、专为大规模向量相似性搜索和分析而设计的向量数据库。它诞生于 Zilliz 公司，并已成为 LF AI & Data 基金会的顶级项目，在AI领域拥有广泛的应用。

与 FAISS、ChromaDB 等轻量级本地存储方案不同，Milvus 从设计之初就瞄准了生产环境。其采用云原生架构，具备高可用、高性能、易扩展的特性，能够处理十亿、百亿甚至更大规模的向量数据。

 Milvus 有多种安装方式，这里选择最简单的单机嵌入

```
pip install pymilvus
```

它比faiss稍微复杂点，这里先简答的介绍下Milvus的一些核心组件

1. Collection

    Collection是 Milvus 中最基本的数据组织单位，类似于关系型数据库中的一张表 (Table)。是我们存储、管理和查询向量及相关元数据的容器。所有的数据操作，如插入、删除、查询等，都是围绕 Collection 展开的 

2. Schema

   在创建Collection之前，必须先定义它的Schema，Schema规定了Collection的数据结构，定义了其中包含的所有字段及其属性，一个良好的Schema能够保证数据一致性并提升查询性能。

   Schema主要包含以下字段：

   1. 主键，用于唯一标识数据的实体
   2. 向量，就是我们存储的向量数据
   3. 标量，用于存储向量之外的元数据，用于过滤查询，实现更加精确的检索

3. Partition

   Partition是Collection内部的一个逻辑划分，在查询的时候，可以指定在一个活几个分区内进行搜索，从而大幅减少需要扫描的数量

4. Alias

   Alias是为Collection提供更多一个昵称，主要是为了安全考虑，避免在原有的Collection操作

5. 索引

   同Faiss一样，支持Flat精准查找，IVF分桶查找和HNSW基于图的索引。

这里开始安装下Milvus，安装Milvus 比Faiss复杂多了，需要安装docker，本地安装docker很复杂，刚好我有一台云服务器，采用的简单方案就是在云服务器上安装Milvus，然后通过公网暴露端口，这样虽然不安全，但是学习，而且也没啥重要的数据。

本地验证下

```
powershell -NoProfile -Command "Test-NetConnection 118.31.222.50 -Port 19530"
http://118.xxx.50:9091/healthz 
```

说明我们的安装是成功了

然后使用Milvus来改写下前面的案例：

```python
from __future__ import annotations

import os
import time

import numpy as np
from pymilvus import Collection, CollectionSchema, DataType, FieldSchema, connections, utility
from sentence_transformers import SentenceTransformer


DEFAULT_MILVUS_HOST = "118.xxx.50"
DEFAULT_MILVUS_PORT = "19530"


class OpenSourceEmbedder:
	"""封装开源嵌入模型。"""

	def __init__(self, model_name: str = "BAAI/bge-small-zh-v1.5"):
		self.model_name = model_name
		self.model = SentenceTransformer(model_name)
		self.dim = self.model.get_sentence_embedding_dimension()

	def encode(self, texts: list[str]) -> np.ndarray:
		"""输出归一化后的向量，适配余弦相似度检索（Milvus 用 IP + 归一化 = cosine）。"""
		vectors = self.model.encode(
			texts,
			normalize_embeddings=True,
			convert_to_numpy=True,
			show_progress_bar=False,
		)
		return vectors.astype("float32")


class MilvusSemanticSearcher:
	"""封装 Milvus 检索：建表/写入/建索引/检索。"""

	def __init__(self, embedder: OpenSourceEmbedder, collection_name: str = "demo_text_vectors"):
		self.embedder = embedder
		self.collection_name = collection_name
		self.collection: Collection | None = None

	def connect(self) -> None:
		uri = os.getenv("MILVUS_URI", "").strip() or None
		token = os.getenv("MILVUS_TOKEN", "").strip() or None
		host = os.getenv("MILVUS_HOST", DEFAULT_MILVUS_HOST).strip()
		port = os.getenv("MILVUS_PORT", DEFAULT_MILVUS_PORT).strip()

		if uri:
			connections.connect(alias="default", uri=uri, token=token)
		else:
			connections.connect(alias="default", host=host, port=port)

	def _create_collection(self, drop_if_exists: bool = True) -> Collection:
		if utility.has_collection(self.collection_name):
			if drop_if_exists:
				utility.drop_collection(self.collection_name)
			else:
				return Collection(self.collection_name)

		fields = [
			FieldSchema(
				name="id",
				dtype=DataType.INT64,
				is_primary=True,
				auto_id=True,
			),
			FieldSchema(
				name="text",
				dtype=DataType.VARCHAR,
				max_length=512,
			),
			FieldSchema(
				name="embedding",
				dtype=DataType.FLOAT_VECTOR,
				dim=self.embedder.dim,
			),
		]
		schema = CollectionSchema(fields=fields, description="demo: text + embedding")
		return Collection(name=self.collection_name, schema=schema)

	def build(self, texts: list[str]) -> None:
		if not texts:
			raise ValueError("至少输入 1 条句子")

		clean_texts = [t.strip() for t in texts if t.strip()]
		if not clean_texts:
			raise ValueError("输入句子不能为空")

		vectors = self.embedder.encode(clean_texts)

		self.collection = self._create_collection(drop_if_exists=True)
		self.collection.insert(
			[
				clean_texts,
				vectors.tolist(),
			]
		)
		self.collection.flush()

		index_params = {
			"index_type": "IVF_FLAT",
			"metric_type": "IP",
			"params": {"nlist": 32},
		}
		self.collection.create_index(field_name="embedding", index_params=index_params)
		self.collection.load()

	def search(self, query: str, top_k: int = 3) -> list[dict]:
		if not self.collection:
			return []

		q_vec = self.embedder.encode([query]).tolist()
		k = max(1, int(top_k))
		search_params = {
			"metric_type": "IP",
			"params": {"nprobe": 10},
		}

		results = self.collection.search(
			data=q_vec,
			anns_field="embedding",
			param=search_params,
			limit=k,
			output_fields=["text"],
		)

		items: list[dict] = []
		for hit in results[0]:
			text = None
			if getattr(hit, "entity", None) is not None:
				text = hit.entity.get("text")
			if text is None and hasattr(hit, "get"):
				text = hit.get("text")

			items.append(
				{
					"rank": len(items) + 1,
					"score": float(hit.score),
					"text": text,
					"id": int(hit.id),
				}
			)
		return items


def interactive_search(searcher: MilvusSemanticSearcher) -> None:
	print("\n开始检索。输入 q 退出。")
	while True:
		query = input("\n查询句子: ").strip()
		if query.lower() in {"q", "quit", "exit"}:
			print("已退出。")
			break
		if not query:
			print("查询不能为空。")
			continue

		results = searcher.search(query, top_k=3)
		print("Top-3 结果：")
		for item in results:
			print(f"#{item['rank']} score={item['score']:.4f} | {item['text']}")


def main() -> None:
	print("加载开源嵌入模型: BAAI/bge-small-zh-v1.5")
	embedder = OpenSourceEmbedder("BAAI/bge-small-zh-v1.5")
	searcher = MilvusSemanticSearcher(embedder, collection_name=f"demo_text_vectors_{int(time.time())}")

	try:
		searcher.connect()
	except Exception as exc:  # noqa: BLE001
		print("连接 Milvus 失败：")
		print(str(exc))
		print("\n排查建议：")
		print("1) 确认 Milvus 服务已启动并监听 19530")
		print("2) 或设置环境变量 MILVUS_URI / MILVUS_TOKEN")
		print("3) 本地模式可设置：MILVUS_HOST=127.0.0.1, MILVUS_PORT=19530")
		return

	texts = [
		"我很喜欢吃苹果的，它膳食纤维、果胶、钾、抗氧化多酚，温和养胃、饱腹感好。",
		"我爱吃红富士这个品牌的苹果，它非常甜，产自山东烟台等地",
		"我红牛苹果也非常喜欢吃，也很甜",
		"苹果是一家非常伟大的公司，乔布斯是他的创始人，我很尊重他",
		"我很喜欢苹果手机，苹果手表，还有苹果电脑",
		"我不喜欢华为手机，它的爱国营销我很反感，它是一家没有底线的公司",
	]

	searcher.build(texts)
	print(f"\n已入库 {len(texts)} 条句子，向量维度={embedder.dim}")
	print(f"Collection: {searcher.collection_name}")

	query = "我要买苹果公司的股票，你觉得如何"
	print(f"\n查询: {query}")
	results = searcher.search(query, top_k=3)
	print("Top-3 结果：")
	for item in results:
		print(f"#{item['rank']} score={item['score']:.4f} | {item['text']}")

	# 需要交互的话，取消下一行注释
	# interactive_search(searcher)


if __name__ == "__main__":
	main()


```

输出：

```
BertModel LOAD REPORT from: BAAI/bge-small-zh-v1.5
Key                     | Status     |  |
------------------------+------------+--+-
embeddings.position_ids | UNEXPECTED |  |

Notes:
- UNEXPECTED:   can be ignored when loading from different task/architecture; not ok if you expect identical arch.
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.

已入库 6 条句子，向量维度=512
Collection: demo_text_vectors_1774774665

查询: 我要买苹果公司的股票，你觉得如何
Top-3 结果：
#1 score=0.6664 | 苹果是一家非常伟大的公司，乔布斯是他的创始人，我很尊重他
#2 score=0.6111 | 我很喜欢苹果手机，苹果手表，还有苹果电脑
#3 score=0.5851 | 我很喜欢吃苹果的，它膳食纤维、果胶、钾、抗氧化多酚，温和养胃、饱腹感好。
```



 