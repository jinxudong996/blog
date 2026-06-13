"""Milvus + 开源嵌入模型：把句子向量写入 Milvus，再做相似度检索。

前置：你已安装 pymilvus
运行：python Milvus.PY

默认连接：118.31.222.50:19530（可用环境变量覆盖）
- MILVUS_URI：优先使用（例如 Zilliz Cloud / 反代地址）
- MILVUS_TOKEN：配合 MILVUS_URI 使用（形如 "user:password" 或云 token）
- MILVUS_HOST / MILVUS_PORT：未设置 URI 时使用

如果你本机还没启动 Milvus（推荐直接用本目录的 compose）：
1) 安装 Docker Desktop
2) 在本目录运行：docker compose -f docker-compose.milvus.yml up -d
3) 等待容器健康后再运行本脚本
"""

from __future__ import annotations

import os
import time

import numpy as np
from pymilvus import Collection, CollectionSchema, DataType, FieldSchema, connections, utility
from sentence_transformers import SentenceTransformer


DEFAULT_MILVUS_HOST = "118.31.222.50"
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

