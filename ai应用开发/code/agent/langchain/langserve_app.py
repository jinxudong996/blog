"""A minimal LangServe API that exposes a LangChain Runnable to the web."""

import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langserve import add_routes


load_dotenv(Path(__file__).resolve().parent.parent / ".ENV")


def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


model = ChatOpenAI(
    model=required_env("LLM_MODEL_ID"),
    base_url=required_env("LLM_BASE_URL"),
    api_key=required_env("LLM_API_KEY"),
    temperature=0.2,
    timeout=int(os.getenv("LLM_TIMEOUT", "60")),
    streaming=True,
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a concise and helpful assistant. Reply in Chinese."),
        ("human", "{message}"),
    ]
)

# StrOutputParser forwards model chunks, so /chat/stream returns text incrementally.
chat_chain = prompt | model | StrOutputParser()

app = FastAPI(title="LangServe Runnable Demo", version="1.0.0")

# Adjust allow_origins in production to contain only the web application's origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


add_routes(app, chat_chain, path="/chat")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("langserve_app:app", host="127.0.0.1", port=8000, reload=True)
