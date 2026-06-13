'''
Author: jinxudong 18751241086@163.com
Date: 2026-02-24 16:52:54
LastEditors: jinxudong 18751241086@163.com
LastEditTime: 2026-02-24 19:27:57
FilePath: \code\RAG初探\002.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from llama_index.core import (
	Document,
	Settings,
	VectorStoreIndex,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.deepseek import DeepSeek


BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data" / "阿Q正传.txt"


def _get_deepseek_key() -> str:
	"""从 .env 或环境变量中读取 DeepSeek API Key。"""

	load_dotenv()  # 允许在当前目录读取 .env
	key = os.getenv("DEEPSEEK_API_KEY")
	if not key:
		raise ValueError("未在环境变量中找到 DEEPSEEK_API_KEY")
	return key


DEEPSEEK_KEY = _get_deepseek_key()


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


def evaluate_recall_with_keywords(
	test_cases: List[dict],
	chunk_sizes: List[int],
	top_k: int = 3,
) -> None:
	documents = load_document()

	for size in chunk_sizes:
		index = build_index_with_chunk_size(documents, size)
		retriever = VectorIndexRetriever(index=index, similarity_top_k=top_k)

		hit_count = 0

		print("=" * 80)
		print(f"基于关键词的召回评估：chunk_size={size}, top_k={top_k}")
		print("-" * 80)

		for case in test_cases:
			query = case["query"]
			keywords = case["keywords"]

			results = retriever.retrieve(query)
			is_hit = False

			for node_with_score in results:
				content = node_with_score.node.get_content()
				if any(kw in content for kw in keywords):
					is_hit = True
					break

			status = "命中" if is_hit else "未命中"
			print(f"问题: {query} -> {status}")

			if is_hit:
				hit_count += 1

		recall = hit_count / len(test_cases) if test_cases else 0.0
		print(f"chunk_size={size} 的近似召回率: {hit_count}/{len(test_cases)} = {recall:.2f}")
		print()


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

	# 同时打印本次回答实际用到的检索 chunk，便于分析召回情况
	if hasattr(response, "source_nodes") and response.source_nodes:
		print("\n[本次回答使用到的检索 chunk 列表]")
		for i, node_with_score in enumerate(response.source_nodes, start=1):
			node = node_with_score.node
			score = getattr(node_with_score, "score", None)
			preview = node.get_content()[:200].replace("\n", " ")

			if score is not None:
				print(f"[chunk {i}] 相似度得分: {score:.4f}")
			else:
				print(f"[chunk {i}]")
			print(f"内容片段预览: {preview}...")
			print()


def init_settings() -> None:
	"""初始化 LlamaIndex 的全局配置。

	这里使用本地 HuggingFace 中文向量模型（会自动下载）。
	如果你已经在别处设置过 Settings，可以根据需要删掉或修改。
	"""

	# 设置向量模型，用于检索阶段
	Settings.embed_model = HuggingFaceEmbedding(
		model_name="BAAI/bge-small-zh-v1.5"
	)

	# 设置 DeepSeek 作为大语言模型，用于生成回答
	Settings.llm = DeepSeek(
		model="deepseek-chat",
		api_key=DEEPSEEK_KEY,
	)


if __name__ == "__main__":
	# 1. 初始化向量模型等设置
	init_settings()

	# 2. 定义要比较的 chunk_size 列表（可根据需要增删）
	sizes = [512, 1024, 2048, 4096]

	# 3. 定义一个你关心的问题，用来观察检索片段的区别
	user_query = "阿Q为什么会被处决？" 

	# 4. 运行仅检索的对比实验
	# demo_retrieval_for_chunk_sizes(user_query, sizes, top_k=3)

	# 4.1 使用简单的关键词规则，粗略评估不同 chunk_size 的召回率
	test_cases = [
		{
			"query": "阿Q为什么会被处决？",
			# 这里放你认为“正确答案”里一定会出现的几个关键词，示例仅供参考
			"keywords": ["处决"],
		},
	]
	evaluate_recall_with_keywords(test_cases, sizes, top_k=3)

	# 5. 使用 DeepSeek 在其中一个 chunk_size 上生成最终回答
	print("\n" + "#" * 80)
	print("下面使用 DeepSeek 给出一个完整回答")
	print("#" * 80)
	demo_rag_with_deepseek(user_query, chunk_size=512, top_k=3)

