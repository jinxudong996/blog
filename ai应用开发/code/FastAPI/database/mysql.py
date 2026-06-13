'''
Author: jinxudong 18751241086@163.com
Date: 2025-12-04 15:44:44
LastEditors: jinxudong 18751241086@163.com
LastEditTime: 2025-12-04 17:04:34
FilePath: \code\FastAPI\database\mysql.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from typing import Optional, Dict, Any, List

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text

DATABASE_URL = "mysql+aiomysql://root:my-mysql@118.31.222.50:3307/text"

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
            text("SELECT * FROM student_info WHERE number = :sid"),
            {"sid": student_id},
        )
        row = result.mappings().first()
        return dict(row) if row else None