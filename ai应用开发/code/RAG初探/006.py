import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredFileLoader
from llama_index.core import (
    Document,
    Settings,
    VectorStoreIndex,
)
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
    """读取企业知识库建设方案，构造成单个 Document（备用）。"""

    if not DATA_FILE.exists():
        raise FileNotFoundError(f"找不到文本文件: {DATA_FILE}")

    text = DATA_FILE.read_text(encoding="utf-8")
    return [Document(text=text, metadata={"source": str(DATA_FILE.name)})]


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


def demo_unstructured_retrieval(
    query: str,
    top_k: int = 3,
) -> None:
    """演示在 Unstructured by_title 分块设置下，对同一问题的检索效果。"""

    index = build_index_with_unstructured_by_title()

    retriever = VectorIndexRetriever(index=index, similarity_top_k=top_k)
    results = retriever.retrieve(query)

    print("=" * 80)
    print(f"Unstructured by_title 分块下的检索结果（top_k={top_k}）")
    print("-" * 80)

    for i, node_with_score in enumerate(results, start=1):
        node = node_with_score.node
        score = node_with_score.score
        preview = node.get_content()[:200].replace("\n", " ")

        print(f"[结果 {i}] 相似度得分: {score:.4f}")
        print(f"内容片段预览: {preview}...")
        print()


def demo_unstructured_rag_with_deepseek(
    query: str,
    top_k: int = 3,
) -> None:
    """在 Unstructured by_title 分块的基础上，调用 DeepSeek 做 RAG 回答。"""

    index = build_index_with_unstructured_by_title()

    query_engine = index.as_query_engine(similarity_top_k=top_k)
    response = query_engine.query(query)

    print("=" * 80)
    print(f"使用 DeepSeek + Unstructured by_title 分块的 RAG 回答（top_k={top_k}）")
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

    # 1. 只看 Unstructured by_title 分块下的检索效果
    # demo_unstructured_retrieval(
    #     user_query,
    #     top_k=3,
    # )

    # 2. 在 Unstructured by_title 分块基础上，使用 DeepSeek 做 RAG 回答
    print("\n" + "#" * 80)
    print("下面使用 DeepSeek + Unstructured by_title 分块给出一个完整回答")
    print("#" * 80)
    demo_unstructured_rag_with_deepseek(
        user_query,
        top_k=3,
    )
