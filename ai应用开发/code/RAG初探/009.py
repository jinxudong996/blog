import os
from pathlib import Path
from typing import List, Optional

from dotenv import load_dotenv
from llama_index.core import (
    Document,
    Settings,
    VectorStoreIndex,
)
from llama_index.core.node_parser import HierarchicalNodeParser
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import AutoMergingRetriever, VectorIndexRetriever
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.deepseek import DeepSeek


BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data" / "企业知识库建设方案.txt"


def _get_deepseek_key() -> str:
    """从 .env 或环境变量中读取 DeepSeek API Key。"""

    load_dotenv()
    key = os.getenv("DEEPSEEK_API_KEY")
    if not key:
        raise ValueError("未在环境变量中找到 DEEPSEEK_API_KEY")
    return key


DEEPSEEK_KEY = _get_deepseek_key()


def load_document() -> List[Document]:
    """读取虚构公司年度报告，构造成单个 Document。"""

    if not DATA_FILE.exists():
        raise FileNotFoundError(f"找不到文本文件: {DATA_FILE}")

    text = DATA_FILE.read_text(encoding="utf-8")
    return [Document(text=text, metadata={"source": str(DATA_FILE.name)})]


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


def demo_hierarchical_retrieval(
    query: str,
    chunk_sizes: Optional[List[int]] = None,
    top_k: int = 3,
) -> None:
    """演示在父子层级分块设置下，对同一问题的检索效果。"""

    documents = load_document()
    index = build_index_with_hierarchical_chunks(
        documents,
        chunk_sizes=chunk_sizes,
    )

    # 先用细粒度向量检索命中子节点，再用 AutoMergingRetriever
    # 将多个子节点自动“合并”成对应的父节点返回
    base_retriever = VectorIndexRetriever(index=index, similarity_top_k=top_k)
    retriever = AutoMergingRetriever(base_retriever, index.storage_context)
    results = retriever.retrieve(query)

    print("=" * 80)
    print(
        "父子层级分块检索结果："
        f"chunk_sizes={chunk_sizes}, top_k={top_k}"
    )
    print("-" * 80)

    for i, node_with_score in enumerate(results, start=1):
        node = node_with_score.node
        score = node_with_score.score
        preview = node.get_content()[:200].replace("\n", " ")

        print(f"[结果 {i}] 相似度得分: {score:.4f}")
        print(f"内容片段预览: {preview}...")
        print()


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

    print("=" * 80)
    print(
        "使用 DeepSeek + 父子层级分块的 RAG 回答："
        f"chunk_sizes={chunk_sizes}, top_k={top_k}"
    )
    print("-" * 80)
    print(str(response))

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
    """初始化嵌入模型和 DeepSeek LLM。"""

    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-zh-v1.5"
    )
    Settings.llm = DeepSeek(
        model="deepseek-chat",
        api_key=DEEPSEEK_KEY,
    )


if __name__ == "__main__":
    init_settings()

    user_query = "一周都要随时在线支持的是啥发布流程"

    default_chunk_sizes = [2048, 512, 128]

    # 1. 只看父子层级分块下的检索效果
    demo_hierarchical_retrieval(
        user_query,
        chunk_sizes=default_chunk_sizes,
        top_k=3,
    )

    # 2. 在父子层级分块基础上，使用 DeepSeek 做 RAG 回答
    print("\n" + "#" * 80)
    print("下面使用 DeepSeek + 父子层级分块给出一个完整回答")
    print("#" * 80)
    demo_hierarchical_rag_with_deepseek(
        user_query,
        chunk_sizes=default_chunk_sizes,
        top_k=3,
    )
