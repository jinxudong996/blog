'''
Author: jinxudong 18751241086@163.com
Date: 2026-01-16 09:56:48
LastEditors: jinxudong 18751241086@163.com
LastEditTime: 2026-01-17 11:49:38
FilePath: \code\RAG初探\word.py
Description: RAG 示例，使用 HuggingFace 向量模型 + DeepSeek LLM
'''
from dotenv import load_dotenv
from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.deepseek import DeepSeek


# 读取 .env 中的环境变量（例如 DEEPSEEK_API_KEY）
load_dotenv()

# 显式指定 LLM 和 Embedding，避免使用默认的 OpenAI
Settings.llm = DeepSeek(
    model="deepseek-chat",  # 如有需要可改成其它 DeepSeek 模型
)

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-zh-v1.5"  # 适合中文的向量模型
)

documents = [
    Document(
        text="LlamaIndex 是一个用于构建 RAG 应用的数据框架。",
        metadata={"source": "intro"},
    ),
    Document(
        text="RAG 的核心思想是通过检索外部知识来增强 LLM 的回答能力。",
        metadata={"source": "rag"},
    ),
]


index = VectorStoreIndex.from_documents(documents)
# print(type(index))  # 看看类名
print(index.index_struct)  # 索引的元信息

storage = index.storage_context
print(storage.docstore)      # 文本/节点存储
print(storage.vector_store)  # 向量存储（不同后端表现不同）
query_engine = index.as_query_engine()

response = query_engine.query("什么是 RAG？")

print(response)