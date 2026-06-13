

#### 一、技术栈与环境准备



##### uv包管理工具

首先介绍下最常用的python包管理工具

- pip

  这是python自带的标准包安装工具，只要安装了python，就会自带pip

  ```
  #安装
  pip install requests
  #卸载
  pip uninstall requests
  #导出依赖
  pip freeze > requirements.txt
  ```

  这是非常原始的包管理工具了，也非常简单，缺点就是安装速度慢，没有环境管理的功能，依赖解析很容易冲突

- venv

  venv是官方虚拟环境工具，python3.3以后就会内置的工具，无需额外安装。核心作用就是隔离不同项目的依赖

  ```
  # 创建环境
  python -m venv .venv
  
  # 激活环境（Windows）
  .venv\Scripts\activate
  # 激活环境（Mac/Linux）
  source .venv/bin/activate
  ```

  这个工具只是隔离环境，不管包的安装，要安装包必须要配合pip来使用

- uv

  uv是使用rust写的极速全能工具，可以同时替代pip+venv，核心优势就是速度极快，比pip快乐10-100倍，技能创建虚拟环境，又可以安装包、管理依赖。

  ```
  # 一行安装
  pip install uv
  # 1. 创建虚拟环境（替代 venv）
  uv venv
  
  # 2. 安装包（替代 pip，超快）
  uv pip install requests
  
  # 3. 激活环境（和 venv 完全一样）
  ```

  

常见的pip、venv的缺陷



#### 二、项目初始化

##### 代码结构

一般复杂点的后端项目，都是采用的MVC(模型-视图-控制器)一种聚焦UI于业务分离的经典架构模式，其中分为了三个核心的组件：

- Model，模型层，负责数据结构，业务状态于业务规则，直接于数据库做交互，处理数据的持久化，这里经常与数据库打交道
- View层，视图层，这里负责数据可视化于用户交互呈现，没有业务规则，接受用户输入
- Controller，控制器，接受用户请求，调用Model处理，选择View响应，处理请求参数，流程控制、结果封装，不承载核心的业务逻辑处理

然而在实际的项目中，实际上用的是这样的三层：Controller、Service和Dao/Model层

- Controller，API入口，参数校验，响应封装
- Service，业务逻辑层，事务、流程的编排
- Dao/Model，数据实体、数据库操作

这种变体结构简单，易上手，开发效率非常高，前后端分离，UI与逻辑解耦，便于并发开发，适合快速迭代的中小型系统。

当然结构简单也会带来另一个问题：业务逻辑容易堆积在Service层，导致数据与行为分离，业务语义弱，于是DDD( Domain-Driven Design，领域驱动设计 )被提了出来，以业务领域为核心，通过领域建模让代码精准映射现实业务，专门适应于复杂业务系统。





#### 三、通用模块开发

##### 环境变量配置

一般项目都是将系统环境变量写入到`.env`文件中，然后通过`dotenv.load_dotenv()`去加载环境变量，这个项目使用`pydantic-setting`实现对.env环境变量的读取

看下相关代码:

```python
class Settings(BaseSettings):
    """Manus后端中控配置信息，从.env或者环境变量中加载数据"""

    # 项目基础配置
    env: str = "development"
    log_level: str = "INFO"
    app_config_filepath: str = "config.yaml"

    # 数据库相关配置
    sqlalchemy_database_uri: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/manus"

    # Redis缓存配置
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str | None = None

    # 使用pydantic v2的写法来完成环境变量信息的告知
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
@lru_cache()
def get_settings() -> Settings:
    """获取Manus项目的配置信息，并对内容进行缓存，避免重复读取"""
    settings = Settings()
    return settings
```

先在`Settings`类中申明默认值和类型，然后读取本地的`.env`文件，最后通过`get_settings`方法将变量返回出去，同时通过标准库中的`@lru_cache()`装饰器来给函数的返回值增加一个缓存，

##### 日志系统

```python
import logging
import sys

from core.config import get_settings


def setup_logging():
    """配置Manus项目的日志系统，涵盖日志等级、输出格式、输出渠道等"""
    # 1.获取项目配置
    settings = get_settings()

    # 2.获取根日志处理器
    root_logger = logging.getLogger()

    # 3.清除已有的handlers，避免uvicorn的dictConfig重配置后产生冲突或重复
    root_logger.handlers.clear()

    # 4.设置根日志处理器等级
    log_level = getattr(logging, settings.log_level)
    root_logger.setLevel(log_level)

    # 5.日志输出格式定义
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 6.创建控制台日志输出处理器(使用stderr，stderr在Python中始终无缓冲，Docker中更可靠)
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)

    # 7.将控制台日志处理器添加到根日志处理器中
    root_logger.addHandler(console_handler)

    root_logger.info("日志系统初始化完成")


#初始化日志
setup_logging()
logger = logging.getLogger(__name__)
```





##### 路由设计

项目入口

```
app.include_router(router, prefix="/api")
```

主路由文件 `route.py`

```python
from fastapi import APIRouter

from . import status_route
# , app_config_routes, file_routes, session_routes


def create_api_routes() -> APIRouter:
    """创建API路由，涵盖整个项目的所有路由管理"""
    # 1.创建APIRouter实例
    api_router = APIRouter()

    # 2.将各个模块添加到api_router中
    api_router.include_router(status_route.router)

    # 3.返回api路由实例
    return api_router


router = create_api_routes()
```

后续所有的路由功能模块，都可以写到主路由`route.py`同目录下

比如：

```python
# 在 status_route.py 中
router = APIRouter()

@router.get("/health")
def check_health():
    return {"status": "ok"}
```

##### 异常处理

这里看不太懂 待定





##### 数据源连接

- redis设置

     

  ```python
  class RedisClient:
      """Redis客户端，用于完成redis缓存连接&使用"""
  
      def __init__(self):
          """构造函数，完成redis客户端的创建"""
          self._client: Redis | None = None
          self._settings: Settings = get_settings()
  
      async def init(self) -> None:
          """完成redis客户端的初始化"""
          # 1.判断客户端是否存在，如果存在则表示已连接上，无需重复连接
          if self._client:
              logger.warning("Redis客户端已初始化，无需重复操作")
              return
  
          try:
              # 2.创建Redis客户端并连接
              self._client = Redis(
                  host=self._settings.redis_host,
                  port=self._settings.redis_port,
                  db=self._settings.redis_db,
                  password=self._settings.redis_password,
                  decode_responses=True,
              )
  
              # 3.测试连接redis缓存
              await self._client.ping()
              logger.info("Redis客户端初始化成功")
          except Exception as e:
              logger.error(f"初始化Redis客户端失败: {str(e)}")
              raise
  
      async def shutdown(self) -> None:
          """关闭Redis时执行的操作"""
          # 1.客户端存在则关闭客户端并提示
          if self._client is not None:
              await self._client.aclose()
              self._client = None
              logger.info("Redis客户端成功关闭")
  
          # 2.清除缓存
          get_redis.cache_clear()
  
      @property
      def client(self) -> Redis:
          """只读属性，返回redis客户端"""
          if self._client is None:
              raise RuntimeError("Redis客户端未初始化，获取客户端失败")
          return self._client
  
  
  @lru_cache()
  def get_redis() -> RedisClient:
      """获取redis实例"""
      return RedisClient()
  ```

  封装了一个`RedisClient`类，在初始化时会从配置文件中获取redis连接的相关设置，比如主机、端口、数据库和密码，类中定义了两个方法`init`和`shutdown`，其中`shutdown`就是redis关闭的方法，`init`是连接redis的方法，然后在封装一个`get_redis`单利方法，返回一个`RedisClient`类的实例，这个类是单利的，避免重复创建连接。

- pg连接

  安装库`uv add asyncpg sqlalchemy`

  ```python
  class Postgres:
      """Postgres数据库基础类，用于完成数据库连接等配置操作"""
  
      def __init__(self):
          """构造函数，完成postgres数据库引擎、会话工厂的创建"""
          self._engine: Optional[AsyncEngine] = None
          self._session_factory: Optional[async_sessionmaker] = None
          self._settings = get_settings()
  
      async def init(self) -> None:
          """初始化postgres连接"""
          # 1.判断是否已经创建好引擎，如果连上了则中断程序
          if self._engine is not None:
              logger.warning(f"Postgres引擎已初始化，无需重复操作")
              return
  
          try:
              # 2.创建异步引擎
              logger.info("正在初始化Postgres连接...")
              self._engine = create_async_engine(
                  self._settings.sqlalchemy_database_uri,
                  echo=True if self._settings.env == "development" else False,
                  pool_pre_ping=True,  # 每次从连接池获取连接前先检测连接是否有效，防止使用已关闭的连接
              )
  
              # 3.创建会话工厂
              self._session_factory = async_sessionmaker(
                  autocommit=False,
                  autoflush=False,
                  bind=self._engine,
              )
              logger.info("Postgres会话工厂创建完毕")
  
              # 4.连接Postgres并执行预操作
              async with self._engine.begin() as async_conn:
                  # 5.检查是否安装了uuid扩展，如果没有的话则安装
                  await async_conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))
                  logger.info("成功连接Postgres并安装uuid-ossp扩展")
          except Exception as e:
              logger.error(f"连接Postgres失败: {str(e)}")
              raise
  
      async def shutdown(self) -> None:
          """关闭Postgres连接"""
          if self._engine:
              await self._engine.dispose()
              self._engine = None
              self._session_factory = None
              logger.info("成功关闭Postgres连接")
  
          # 2.清除缓存
          get_postgres.cache_clear()
  
      @property
      def session_factory(self) -> async_sessionmaker[AsyncSession]:
          """只读属性，返回已初始化的会话工厂"""
          if self._session_factory is None:
              raise RuntimeError("Postgres未初始化，请先调用init()函数初始化")
          return self._session_factory
  
  
  @lru_cache()
  def get_postgres() -> Postgres:
      """获取Postgres实例"""
      return Postgres()
  ```

  

##### 跨域设置

配置跨域就比较简单了

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

##### ORM



#### 四、LLM模块开发



#### 五、Agent模块开发





#### 六、工具模块开发



#### 七、沙箱模块开发



#### 八、A2A模块开发



#### 九、上下文工程



#### 十、前端开发时





#### 十一、部署