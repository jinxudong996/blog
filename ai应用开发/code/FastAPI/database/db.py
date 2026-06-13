'''
Author: jinxudong 18751241086@163.com
Date: 2025-12-04 15:45:49
LastEditors: jinxudong 18751241086@163.com
LastEditTime: 2025-12-04 15:46:02
FilePath: \code\FastAPI\database\db.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from database.mysql import async_session

async def get_db():
    async with async_session() as session:
        yield session