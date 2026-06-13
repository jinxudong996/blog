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
DATA_FILE = BASE_DIR / "data" / "虚构公司年度报告.txt"

def _get_deepseek_key() -> str:
	"""从 .env 或环境变量中读取 DeepSeek API Key。"""

	load_dotenv()  # 允许在当前目录读取 .env
	key = os.getenv("DEEPSEEK_API_KEY")
	if not key:
		raise ValueError("未在环境变量中找到 DEEPSEEK_API_KEY")
	return key


DEEPSEEK_KEY = _get_deepseek_key()

def load_document() -> List[Document]:

	if not DATA_FILE.exists():
		raise FileNotFoundError(f"找不到文本文件: {DATA_FILE}")

	text = DATA_FILE.read_text(encoding="utf-8")
	return [Document(text=text, metadata={"source": str(DATA_FILE.name)})]

def build_index_with_chunk_size(documents: List[Document], chunk_size: int) -> VectorStoreIndex:

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
	sizes = [64, 128]

	# 3. 定义一个你关心的问题，用来观察检索片段的区别
	user_query = "公司2024 年 Q4 营业收入是多少" 

	# 4. 运行仅检索的对比实验
	# demo_retrieval_for_chunk_sizes(user_query, sizes, top_k=3)
    
	# # 4.1 使用简单的关键词规则，粗略评估不同 chunk_size 的召回率
	# test_cases = [
	# 	{
	# 		"query": "阿Q为什么会被处决？",
	# 		# 这里放你认为“正确答案”里一定会出现的几个关键词，示例仅供参考
	# 		"keywords": ["处决"],
	# 	},
	# ]
	# # 5. 使用 DeepSeek 在其中一个 chunk_size 上生成最终回答
	# print("\n" + "#" * 80)
	# print("下面使用 DeepSeek 给出一个完整回答")
	# print("#" * 80)
	demo_rag_with_deepseek(user_query, chunk_size=128, top_k=3)