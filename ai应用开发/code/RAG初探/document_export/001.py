'''
Author: jinxudong 18751241086@163.com
Date: 2025-11-26 22:25:28
LastEditors: jinxudong 18751241086@163.com
LastEditTime: 2025-11-27 20:57:55
FilePath: \code\RAG初探\document_export\001.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from langchain_community.document_loaders import TextLoader
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.normpath(os.path.join(base_dir, "..", "..", "data", "黑神话悟空设定.txt"))
if not os.path.exists(data_path):
	raise FileNotFoundError(f"目标文件不存在: {data_path} 请确认名称是否为 '黑神话悟空设定.txt'")

loader = TextLoader(data_path, encoding="utf-8")
documents = loader.load()
print(documents)