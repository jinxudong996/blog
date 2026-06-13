##### 一、前言

准备朝着ai应用开发学习下，python完善的生态就注定必须学习的，相关的web框架有很多， Flask 与 Django 一直是最常见的选择，Django 功能完善、内置 ORM 和管理后台，适合快速构建大型、结构化的项目；Flask 则以极简著称，灵活自由，但需要开发者自行选择和组合扩展。随着项目对性能与类型安全要求的提高，一种更“现代化”的框架需求开始凸显。 

 FastAPI 正是在这样的背景下受到关注。它基于 Python 类型提示构建，自动生成清晰的 API 文档；内置高性能异步特性，速度可媲美 Node.js 和 Go；搭配 Pydantic 做数据校验，让开发、调试、联调都更高效。相比 Flask 的轻量但需要自己拼装生态、Django 的重量级但偏传统，FastAPI 更适合构建现代、快速迭代的 API 服务。 

##### 二、环境准备

python常见的开发方式就是通过venv创建一个虚拟环境，这个虚拟环境就是一个独立的mini-python系统，包含一个独立的python解释器，独立的pip和独立的site-package，这样我们可以再不通的项目中使用不通的python版本。和node_modules不一样的是，python env隔离的是整个python环境，而node_modules隔离的只是依赖文件。

接下来就通过venv来创建虚拟环境，前提是已经安装好了python版本，不建议安装最新的，之前`llama_index`的例子，就出现过不兼容的现象，3.11即可。

首先激活虚拟环境

```
# 1. 创建虚拟环境（venv 是目录名，可自行修改）
python3 -m venv venv

# 2. 激活虚拟环境
# Windows
venv\Scripts\activate
```

然后安装框架和服务器

```
pip install fastapi uvicorn[standard]
```

其中fastapi就是这个博客要学习的东西，`uvicorn` 是一款轻量级、超高性能的 **ASGI 服务器（Asynchronous Server Gateway Interface）**。

FastAPI 基于 ASGI 协议构建，因此需要一个 ASGI 服务器来运行它。

##### 三、FastAPI最小实例

接下来就开始代码实操

```python
from fastapi import FastAPI

app = FastAPI(
	title="Hello World API",
	description="Basic demo of FastAPI: app instance, path operation, automatic docs.",
	version="0.1.0",
)


@app.get("/", summary="Root Hello")
def read_root():
	return {"message": "Hello World"}


@app.get("/hello/{name}", summary="Personalized Hello")
def read_hello(name: str):
	return {"message": f"Hello {name}"}


@app.get("/health", summary="Health Check")
def health():
	return {"status": "ok"}

```

代码也是比较简单的， `FastAPI` 是一个为API 提供了所有功能的 Python 类，变量 `app` 会是 `FastAPI` 类的一个实例，这个实例将是创建所有 API 的主要交互对象。

运行命令

```
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- 基础根路径: [http://localhost:8000/](vscode-file://vscode-app/d:/job/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html)
- 个性问候: [http://localhost:8000/hello/张三](vscode-file://vscode-app/d:/job/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html)
- 健康检查: [http://localhost:8000/health](vscode-file://vscode-app/d:/job/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html)
- 自动文档 (Swagger UI): [http://localhost:8000/docs](vscode-file://vscode-app/d:/job/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html)
- ReDoc: [http://localhost:8000/redoc](vscode-file://vscode-app/d:/job/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html)

##### 四、路径操作

在 FastAPI 中，所谓“路径操作”指的就是我们常说的 API 接口（如 GET、POST 等）。每个路径操作由一个 URL 路径和一个 HTTP 方法组成。FastAPI 为每一种方法都提供了对应的装饰器，使用非常直观。

 FastAPI 支持常见的 RESTful 风格接口，示例：  

```python
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
```

1. ###### 路径参数

    路径参数指 URL 中的一部分，例如 `/users/123` 中的 `123` 

   ```python
   @app.get("/users/{user_id}")
   def read_user(user_id: int):
       return {"user_id": user_id}
   ```

   FastAPI 会根据类型自动校验：访问 `/users/abc` 会报 422 错误。 

   还可以添加约束，例如：

   ```python
   from fastapi import Path
   
   @app.get("/orders/{order_id}")
   def read_order(order_id: int = Path(gt=0, description="订单 ID 必须大于 0")):
       return {"order_id": order_id}
   ```

   

2. ###### 查询参数

    查询参数是 `?key=value` 的部分，例如：`/search?q=fastapi&page=1` 

   ```python
   @app.get("/search")
   def search(q: str, page: int = 1):
       return {"q": q, "page": page}
   ```

   可以添加校验：

   ```python
   from fastapi import Query
   
   @app.get("/products")
   def get_products(limit: int = Query(10, le=100), keyword: str = Query(None, min_length=2)):
       return {"limit": limit, "keyword": keyword}
   ```

   

3. ###### 参数校验

   FastAPI 的校验通过 `Query()`、`Path()` 等完成，常用校验包括：

   - **最小值/最大值**：`ge`（>=）、`le`（<=）、`gt`（>）、`lt`（<）
   - **字符串长度**：`min_length` / `max_length`
   - **正则校验**：`regex`

   示例：

   ```python
   @app.get("/validate")
   def validate(
       username: str = Query(..., min_length=3, max_length=20, regex="^[a-zA-Z0-9_]+$"),
       age: int = Query(..., ge=1, le=120)
   ):
       return {"username": username, "age": age}
   ```

​      

##### 五、使用Pydantic模型

FastAPI 在数据校验和数据转换方面非常强大，这要归功于 **Pydantic**。在接收 JSON 请求体时，我们可以通过 Pydantic 模型来定义结构、类型、默认值以及校验规则，让 API 更健壮、更易维护。 

1. ###### 定义请求模型

   一个典型的请求体（Request Body）使用 Pydantic 的 `BaseModel` 来定义字段和类型：

   ```python
   from pydantic import BaseModel
   
   class Item(BaseModel):
       name: str
       description: str | None = None
       price: float
       in_stock: bool = True
   ```

   FastAPI 会根据这些类型自动验证请求体，并在 Swagger 文档中展示字段结构。

2. ###### 使用模型

   直接将模型作为参数即可：

   ```python
   from fastapi import FastAPI
   
   app = FastAPI()
   
   @app.post("/items")
   def create_item(item: Item):
       return {"message": "商品已创建", "item": item}
   ```

   ```python
   {
     "name": "iPhone 16",
     "description": "最新型号",
     "price": 6999.99,
     "in_stock": true
   }
   
   ```

    FastAPI 会自动把它转换为 `Item` 实例。如果字段缺失、类型不匹配，会返回 422 错误。 

3. ###### 字段校验

   这里需要使用Pydantic 的 `Field()` ，来添加更精确的校验规则和描述 

   ```python
   from pydantic import BaseModel, Field
   
   class User(BaseModel):
       username: str = Field(..., min_length=3, max_length=20, description="用户名必须为 3~20 个字符")
       age: int = Field(..., ge=1, le=120, description="年龄必须在 1~120 之间")
   ```

   这里就在`Field`中定义了`username`和`age`两个字段，`...`表明是必传字段，其中`username`的长度要在3-20之间，`age`要在1-120之间

4. ###### 嵌套模型

   当遇到一些复杂的模型时，就需要用到嵌套了

   ```python
   class Address(BaseModel):
       city: str
       street: str
   
   class Customer(BaseModel):
       name: str
       address: Address
   ```

   对应的请求体就需要这样写了

   ```json
   {
     "name": "Tom",
     "address": {
       "city": "Shanghai",
       "street": "Nanjing Road"
     }
   }
   ```

   

5. ###### 相应模型

   上面的是入参的限制，同样也可以限制响应值的类型

   ```python
   class UserPublic(BaseModel):
       username: str
   
   @app.post("/users", response_model=UserPublic)
   def create_user(user: User):
       # 假装保存数据库...
       return user
   ```

   



##### 六、高级请求参数和路由模块化

除了常见的get、post这种`JSON`请求体，还会处理表单、Cookies、Headers等输入

1. ###### 表单请求

   就是前端常见的form表单来提交数据

   ```python
   from fastapi import Form
   
   @app.post("/login")
   def login(username: str = Form(...), password: str = Form(...)):
       return {"username": username}
   ```

2. ###### 文件上传

   文件上传也是一个很常见的功能

   ```python
   async function upload() {
       const fileInput = document.getElementById("fileInput");
       const file = fileInput.files[0];
   
       const formData = new FormData();
       formData.append("file", file);
   
       const res = await fetch("http://127.0.0.1:8000/upload", {
           method: "POST",
           body: formData
       });
   
       const data = await res.json();
       console.log("上传结果:", data);
    }
   ```

   对应的后端

   ```python
   from fastapi import File, UploadFile
   
   @app.post("/upload")
   def upload(file: UploadFile = File(...)):
       return {"filename": file.filename}
   ```

   

3. ###### Cookies和headers

   ```python
   from fastapi import Cookie
   
   @app.get("/read-cookie")
   def read_cookie(session_id: str | None = Cookie(None)):
       return {"session_id": session_id}
   ```

   ```python
   from fastapi import Header
   
   @app.get("/agent")
   def get_agent(user_agent: str = Header(...)):
       return {"User-Agent": user_agent}
   ```

4. ###### 路由模块化

   随着项目的变大，所有的路由都写在`main.py`中就会变得很难维护，可以使用`APIRouter`将路由拆分成多个模块

   定义子路由

   ```python
   from fastapi import APIRouter
   
   router = APIRouter()
   
   @router.get("/users")
   def get_users():
       return [{"name": "tom"}]
   
   ```

   在`main.py`中使用

   ```python
   from fastapi import FastAPI
   from routers import user_router
   
   app = FastAPI()
   app.include_router(user_router, prefix="/api", tags=["Users"])
   ```

   这里的`prefix`就是给所有的路由加前缀，`tags`就是给文档分组显示

   

##### 七、依赖注入

FastAPI 的依赖注入（Dependency Injection, DI）是其最强大的特性之一，主要用来处理权限、数据库连接、配置加载、复用逻辑 。

举一个例子就知道具体的用法了

```python
def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()

def get_current_user(db = Depends(get_db)):
    token = ...  # 从请求头拿 token
    user = db.query(User).filter(...).first()
    if not user:
        raise HTTPException(401)
    return user

@app.get("/profile")
def profile(user = Depends(get_current_user)):
    return {"username": user.name}
```

这里定义了两个，get_db是获取数据库实例，get_current_user是获取当前用户的，在get_current_user方法中通过Depends() 将 get_db方法注入到db参数，这样在get_current_user方法内部就可以直接使用db来做数据路的查询了。

这里将get_current_user方法的执行流程描述下，就可以更加清晰的知道依赖注入的用法了

1. 在调用get_current_user方法时，看到db = Depends(get_db)
2. 开始调用get_db方法获取实例，复制给db
3. 执行get_db内部方法，db = DBSession()，遇到yield db，就将yield值传递给db = Depends(get_db)的db
4. 方法执行完成后，会执行finally中的方法关闭连接

后续在请求`"/profile"`中，也是一样的流程，值得一提的是，依赖注入不管请求调用多少次，同一个请求中的依赖注入只会调用一次，这样也是为了避免连接数据库的庞大开销。

开始我以为这里的依赖注入是`@app.get("/profile")`，后来了解了下才发现是`def profile(user = Depends(get_current_user)):`中的`Depends`关键字，`@app.get("/profile")`这个实际上是装饰器模式，他就是一个语法糖，这两行代码没有本质区别

```
@app.get("/users")
def list_users(): ...
```

```
list_users = app.get("/users")(list_users)
```

##### 八、中间件

中间件就是处理请求和相应的管道函数，位于客户端请求和路由函数之间，可以在请求到达路由前执行，也可以在相应返回客户端前处理，同样也可以在路由和其他中间件之间传递控制权

 FastAPI 中的中间件遵循 **ASGI 规范**，比如下面这个例子

```python
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

@app.middleware("http")
async def simple_middleware(request: Request, call_next):
    print("请求到来：", request.url.path)
    response = await call_next(request)  # 调用下一个中间件或路由
    print("响应返回")
    return response
```

中间件是通过关键字`middleware`来修饰，中间件的作用于就是全局的，会作用与所有注册的路由，上面代码的执行顺序就是这样的

```
【请求进来】
1. print("请求到来")

2. 调用下一个中间件 或 最终的路由函数
   response = await call_next(request)

3. print("响应返回")

【响应返回给客户端】
```

然后如果注册了多个中间件，他们的注册顺序呢，比如下面这样

```python
@app.middleware("http")
async def M1(request, call_next): ...

@app.middleware("http")
async def M2(request, call_next): ...
```

这就和koa中的中间件执行顺序一样，就是一个洋葱模型

```
请求进来 →
  M1.before
    M2.before
      ROUTE()（路由函数执行）
    M2.after
  M1.after
响应返回
```

常见的中间件可以处理token鉴权

```python
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    token = request.headers.get("Authorization")
    if token != "mysecrettoken":
        from fastapi.responses import JSONResponse
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    return await call_next(request)
```

还可以设置`CORS`跨域

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

上面提到了`ASGI`，接下来介绍下这个协议：

 ASGI （Asynchronous Server Gateway Interface），异步服务器网关接口， Python Web 服务器与 Web 框架之间的 **通信协议标准** ，支持异步和同步的，转为高并发、WebSocket、长连接设计的。

在`ASGI`出现之前，比如`Django`、`Flask`他们都是`ASGI`， 而`ASGI`只能处理同步任务，一次只能处理一个请求，也不支持`WebSocket`，不适合做高并发和长连接，

##### 九、数据库集成

接口的实际应用，还是得和数据库做交互，接下来分别介绍下mysql和redis的使用

1. ###### mysql使用

   FastAPI 推荐异步方式，需要额外安装两个库 

```
pip install sqlalchemy[asyncio] aiomysql
```

 创建数据库引擎

```python
'''
Author: jinxudong 18751241086@163.com
Date: 2025-12-04 15:44:44
LastEditors: jinxudong 18751241086@163.com
LastEditTime: 2025-12-04 16:44:58
FilePath: \code\FastAPI\database\mysql.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from typing import Optional, Dict, Any, List

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text

DATABASE_URL = "mysql+aiomysql://xxx"

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


def get_session() -> AsyncSession:
    return async_session()


async def fetch_all_students() -> List[Dict[str, Any]]:
    async with get_session() as session:
        # 直接使用原生 SQL 查询 student_info 全部数据
        result = await session.execute(text("SELECT * FROM student_info"))
        rows = result.mappings().all()
        return [dict(row) for row in rows]


async def fetch_student_by_id(student_id: str) -> Optional[Dict[str, Any]]:
    async with get_session() as session:
        result = await session.execute(
            text("SELECT * FROM student_info WHERE student_id = :sid"),
            {"sid": student_id},
        )
        row = result.mappings().first()
        return dict(row) if row else None
```

这里定义了两个查询数据库的方法，`fetch_all_students`是查询所有的`student_info`表，`fetch_student_by_id`去根据id查询学生信息，

定义user类型的api

```python
#user.py
from fastapi import APIRouter, HTTPException

# 兼容包内外运行：优先相对导入，失败时回退到绝对导入

from database.mysql import fetch_all_students, fetch_student_by_id

router = APIRouter(prefix="/students", tags=["students"])


@router.get("", summary="查询所有学生信息")
async def list_students():
    try:
        rows = await fetch_all_students()
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {e}")


@router.get("/{student_id}", summary="根据学号查询学生信息")
async def get_student(student_id: str):
    try:
        row = await fetch_student_by_id(student_id)
        if not row:
            raise HTTPException(status_code=404, detail="未找到该学生")
        return row
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {e}")
```

然后在`main.py`中使用`user.py`

```python
from user import router as students_router 
...
app.include_router(students_router)
```

然后通过浏览器`http://localhost:8000/students`和`http://localhost:8000/students/20180102`就可以进行查询了。

1. ###### redis使用

 MySQL 是关系型数据库，擅长存储结构化数据，支持复杂的 SQL 查询、事务和持久化，适合存储业务核心数据，如用户信息、订单记录等。而 Redis 则是内存数据库，提供极高的读写性能，支持多种数据结构（字符串、哈希、列表、集合、有序集合等），适合做缓存、排行榜、会话存储或消息队列等场景。简单来说，MySQL 保证数据的可靠性和完整性，而 Redis 提供高速的数据访问能力，两者结合可以在保证数据安全的同时，显著提升系统的响应速度和并发处理能力。

接下来写一个redis查询的小例子

```python
from typing import Optional, Dict, Any, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from redis.asyncio import from_url, Redis


REDIS_URL = "redis://:xxx"


def get_redis() -> Redis:
    return from_url(REDIS_URL, decode_responses=True)


router = APIRouter(prefix="/redis", tags=["redis"])


class SetRequest(BaseModel):
    key: str
    value: str
    expire_seconds: Optional[int] = None

@router.get("/keys", summary="扫描匹配的键")
async def redis_keys(pattern: str = "*") -> List[str]:
    r = get_redis()
    try:
        keys: List[str] = []
        cursor = 0
        while True:
            cursor, batch = await r.scan(cursor=cursor, match=pattern, count=100)
            keys.extend(batch)
            if cursor == 0:
                break
        return keys
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis scan 失败: {e}")
    finally:
        await r.close()
```

然后在`main.py`中导入路由

```python
from redis_api import router as redis_router
...
app.include_router(redis_router)
```

然后再`http://localhost:8000/docs`文档中通过swagger直接调用我们写的接口，就可以正常看到返回值了。

上面也只是一些基本知识的梳理，距离企业开发还差的很远，尤其是这个框架以高性能、适合高迸发著称，后续打算做一个网关项目，一个聊天室项目，最后再做一个uniapp+fastapi的即时通讯软件，这一套下来，对于fastapi就应该更加熟练了。