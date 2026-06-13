import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from llama_index.core import (
    Document,
    Settings,
    VectorStoreIndex,
)
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.schema import TextNode
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


def demo_semantic_retrieval(
    query: str,
    breakpoint_percentile_threshold: float = 95.0,
    buffer_size: int = 1,
    top_k: int = 3,
) -> None:
    """演示在语义分块设置下，对同一问题的检索效果。"""

    documents = load_document()
    index = build_index_with_semantic_splitter(
        documents,
        breakpoint_percentile_threshold=breakpoint_percentile_threshold,
        buffer_size=buffer_size,
    )

    retriever = VectorIndexRetriever(index=index, similarity_top_k=top_k)
    results = retriever.retrieve(query)

    print("=" * 80)
    print(
        "语义分块检索结果："
        f"breakpoint_percentile_threshold={breakpoint_percentile_threshold}, "
        f"buffer_size={buffer_size}, top_k={top_k}"
    )
    print("-" * 80)

    for i, node_with_score in enumerate(results, start=1):
        node = node_with_score.node
        score = node_with_score.score
        preview = node.get_content()

        print(f"[结果 {i}] 相似度得分: {score:.4f}")
        print(f"内容片段预览: {preview}...")
        print()


def demo_semantic_rag_with_deepseek(
    query: str,
    breakpoint_percentile_threshold: float = 95.0,
    buffer_size: int = 1,
    top_k: int = 3,
) -> None:
    """在语义分块的基础上，调用 DeepSeek 做 RAG 回答。"""

    documents = load_document()
    index = build_index_with_semantic_splitter(
        documents,
        breakpoint_percentile_threshold=breakpoint_percentile_threshold,
        buffer_size=buffer_size,
    )

    query_engine = index.as_query_engine(similarity_top_k=top_k)
    response = query_engine.query(query)

    print("=" * 80)
    print(
        "使用 DeepSeek + 语义分块的 RAG 回答："
        f"breakpoint_percentile_threshold={breakpoint_percentile_threshold}, "
        f"buffer_size={buffer_size}, top_k={top_k}"
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

    # 1. 只看语义分块下的检索效果
    demo_semantic_retrieval(
        user_query,
        breakpoint_percentile_threshold=95.0,
        buffer_size=1,
        top_k=3,
    )

    # 2. 在语义分块基础上，使用 DeepSeek 做 RAG 回答
    print("\n" + "#" * 80)
    print("下面使用 DeepSeek + 语义分块给出一个完整回答")
    print("#" * 80)
    demo_semantic_rag_with_deepseek(
        user_query,
        breakpoint_percentile_threshold=95.0,
        buffer_size=1,
        top_k=3,
    )
