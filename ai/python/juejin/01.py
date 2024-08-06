import os
from langchain_openai import OpenAI
from fastapi import FastAPI
from langserve import add_routes

os.environ["OPENAI_KEY"] = "sk-I23bFbiP6pUIX4Fo2934BfAb93814745883eB82a5f994bD1"
os.environ["OPENAI_API_BASE"] = "https://ai-yyds.com/v1"

# os.environ['OPENAI_API_KEY'] = '你的openai key'
# os.environ['OPENAI_API_BASE'] = '你的代理url'
llm = OpenAI()
app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple API server using LangChain's Runnable interfaces",
)
# 3. Adding chain route
add_routes(
    app,
    llm,
    path="/first_llm",
)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)