'''
Author: jinxudong 18751241086@163.com
Date: 2025-12-01 17:27:44
LastEditors: jinxudong 18751241086@163.com
LastEditTime: 2025-12-04 16:02:09
FilePath: \code\FastAPI\main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from fastapi import FastAPI
# 兼容包内外运行：优先相对导入，失败时回退到绝对导入
try:
	from .user import router as students_router
except ImportError:
	from user import router as students_router
try:
	from .redis_api import router as redis_router
except ImportError:
	from redis_api import router as redis_router

app = FastAPI(
	title="Hello World API",
	description="Basic demo of FastAPI: app instance, path operation, automatic docs.",
	version="0.1.0",
)
app.include_router(students_router)
app.include_router(redis_router)

@app.get("/", summary="Root Hello")
def read_root():
	return {"message": "Hello World"}


@app.get("/hello/{name}", summary="Personalized Hello")
def read_hello(name: str):
	return {"message": f"Hello {name}"}


@app.get("/health", summary="Health Check")
def health():
	return {"status": "ok"}


@app.get("/items")
def get_items():
    return {"message": "GET 请求"}

@app.post("/items")
def create_item(item: dict):
    return {"message": "POST 请求", "item": item}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: dict):
    return {"message": "PUT 请求", "id": item_id, "item": item}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"message": "DELETE 请求", "id": item_id}
