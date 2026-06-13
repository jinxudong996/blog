import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
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
DATA_FILE = BASE_DIR / "data" / "虚构公司年度报告.txt"


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


def demo_recursive_retrieval(
    query: str,
    chunk_size: int = 200,
    chunk_overlap: int = 10,
    top_k: int = 3,
) -> None:
    """演示在递归分块设置下，对同一问题的检索与 RAG 效果。"""

    documents = load_document()
    index = build_index_with_recursive_splitter(documents, chunk_size, chunk_overlap)

    retriever = VectorIndexRetriever(index=index, similarity_top_k=top_k)
    results = retriever.retrieve(query)

    print("=" * 80)
    print(
        f"递归分块检索结果：chunk_size={chunk_size}, "
        f"chunk_overlap={chunk_overlap}, top_k={top_k}"
    )
    print("-" * 80)

    for i, node_with_score in enumerate(results, start=1):
        node = node_with_score.node
        score = node_with_score.score
        preview = node.get_content()[:200].replace("\n", " ")

        print(f"[结果 {i}] 相似度得分: {score:.4f}")
        print(f"内容片段预览: {preview}...")
        print()


def demo_recursive_rag_with_deepseek(
    query: str,
    chunk_size: int = 200,
    chunk_overlap: int = 10,
    top_k: int = 3,
) -> None:
    """在递归分块的基础上，调用 DeepSeek 做 RAG 回答。"""

    documents = load_document()
    index = build_index_with_recursive_splitter(documents, chunk_size, chunk_overlap)

    query_engine = index.as_query_engine(similarity_top_k=top_k)
    response = query_engine.query(query)

    print("=" * 80)
    print(
        f"使用 DeepSeek + 递归分块的 RAG 回答：chunk_size={chunk_size}, "
        f"chunk_overlap={chunk_overlap}, top_k={top_k}"
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

    user_query = "公司 2024 年 Q4 营业收入是多少？"

    # 1. 只看递归分块下的检索效果
    demo_recursive_retrieval(
        user_query,
        chunk_size=200,
        chunk_overlap=10,
        top_k=3,
    )

    # 2. 在递归分块基础上，使用 DeepSeek 做 RAG 回答
    # print("\n" + "#" * 80)
    # print("下面使用 DeepSeek + 递归分块给出一个完整回答")
    # print("#" * 80)
    # demo_recursive_rag_with_deepseek(
    #     user_query,
    #     chunk_size=200,
    #     chunk_overlap=10,
    #     top_k=3,
    # )
