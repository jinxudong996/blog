# 第一行代码：导入相关的库
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.deepseek import DeepSeek
from dotenv import load_dotenv
import os


def _get_deepseek_key() -> str:
    load_dotenv()  # 允许在当前目录读取 .env
    key = os.getenv("DEEPSEEK_API_KEY")
    return key

DEEPSEEK_KEY = _get_deepseek_key()

# 加载本地嵌入模型
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-zh")

# 创建 DeepSeek LLM (不在代码中硬编码密钥)
llm = DeepSeek(model="deepseek-chat", api_key=DEEPSEEK_KEY)

# 第二行代码：加载数据（使用规范路径，避免相对路径错误）
base_dir = os.path.dirname(os.path.abspath(__file__))  # 当前脚本所在目录
doc_path = os.path.normpath(os.path.join(base_dir, "..", "data", "黑神话悟空设定.txt"))
if not os.path.exists(doc_path):
    raise FileNotFoundError(f"文档未找到: {doc_path} 请确认文件存在并名称匹配。")
documents = SimpleDirectoryReader(input_files=[doc_path]).load_data()

# 第三行代码：构建索引
index = VectorStoreIndex.from_documents(
    documents,
    embed_model=embed_model
)

# 第四行代码：创建问答引擎
query_engine = index.as_query_engine(
    llm=llm
)

# 第五行代码: 开始问答
# print(query_engine.query("黑神话悟空中有哪些战斗工具?"))
print(query_engine.query("帮我介绍下黑神话悟空?"))
