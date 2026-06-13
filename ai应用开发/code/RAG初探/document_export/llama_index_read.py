from llama_index.core import SimpleDirectoryReader
import os

# 构建规范路径：当前脚本 -> 上级(code) -> data -> 文件名
base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.normpath(os.path.join(base_dir, "..", "..", "data", "黑神话悟空设定.txt"))

if not os.path.exists(data_path):
    raise FileNotFoundError(f"目标文件不存在: {data_path} 请确认名称是否为 '黑神话悟空设定.txt'")

# 使用 LlamaIndex 的文件读取器加载文档
reader = SimpleDirectoryReader(input_files=[data_path])
docs = reader.load_data()

print(f"读取到 {len(docs)} 个文档")
print("第一段内容预览:\n")
print(docs[0].text[:300])
