"""Faiss + 开源嵌入模型：手动输入句子做相似度匹配。

模型：BAAI/bge-small-zh-v1.5（开源中文嵌入模型）
运行：python first.py
"""

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
