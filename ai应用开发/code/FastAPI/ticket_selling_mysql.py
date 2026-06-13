import asyncio
import time
from typing import Dict, List
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection
from sqlalchemy import text

# 你的数据库地址
DATABASE_URL = "mysql+aiomysql://root:my-mysql@118.31.222.50:3307/text"

TOTAL_TICKETS = 100  # 与数据库中的 total 一致即可，此处仅用于校验展示
SALE_DELAY_SEC = 0.01  # 每次卖票的模拟耗时
STOCK_ID = 1  # tickets_stock 表的主键 id

async def sell_one(conn: AsyncConnection, window_name: str) -> bool:
    """在一个事务中卖出一张票，使用 SELECT ... FOR UPDATE 防止超卖。"""
    try:
        async with conn.begin():
            result = await conn.execute(
                text("SELECT sold, total FROM tickets_stock WHERE id=:id FOR UPDATE"),
                {"id": STOCK_ID},
            )
            row = result.fetchone()
            if row is None:
                return False
            sold, total = row[0], row[1]
            if sold < total:
                await conn.execute(
                    text("UPDATE tickets_stock SET sold = sold + 1 WHERE id=:id"),
                    {"id": STOCK_ID},
                )
                await conn.execute(
                    text(
                        """
                        INSERT INTO sale_logs(`window`, `qty`, `sold_after`)
                        VALUES(:window, :qty, :sold_after)
                        """
                    ),
                    {"window": window_name, "qty": 1, "sold_after": sold + 1},
                )
                # 事务上下文退出时自动提交
                return True
            # 不可售时事务回滚（上下文自动处理）
            return False
    except Exception as e:
        print(f"[ERROR] sell_one 异常: {e}")
        return False

async def window_worker(conn: AsyncConnection, name: str) -> Dict[str, float]:
    start = time.perf_counter()
    sold_count = 0
    while True:
        ok = await sell_one(conn, name)
        if not ok:
            # 未能售出，可能是售罄、无行、或SQL错误
            break
        sold_count += 1
        await asyncio.sleep(SALE_DELAY_SEC)
    seconds = round(time.perf_counter() - start, 4)
    return {"window": name, "sold": sold_count, "seconds": seconds}

async def main():
    engine = create_async_engine(DATABASE_URL, pool_size=5, max_overflow=10, pool_pre_ping=True)
    try:
        # 初始化：创建 sale_logs 表；确保 tickets_stock 存在 id=1 记录
        async with engine.begin() as init_conn:
            await init_conn.execute(text(
                """
                CREATE TABLE IF NOT EXISTS sale_logs (
                  id BIGINT PRIMARY KEY AUTO_INCREMENT,
                  `window` VARCHAR(20) NOT NULL,
                  `qty` INT NOT NULL,
                  `sold_after` INT NOT NULL,
                  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                """
            ))
            # 确保库存行存在
            result = await init_conn.execute(text("SELECT COUNT(*) FROM tickets_stock WHERE id=:id"), {"id": STOCK_ID})
            count = result.scalar_one()
            if count == 0:
                await init_conn.execute(text("INSERT INTO tickets_stock (id, total, sold) VALUES (:id, :total, 0)"), {"id": STOCK_ID, "total": TOTAL_TICKETS})

        # 为每个窗口分别获取连接，确保在事件循环关闭前正确关闭
        async with engine.connect() as conn1:
            async with engine.connect() as conn2:
                async with engine.connect() as conn3:
                    windows = ["窗口-1", "窗口-2", "窗口-3"]
                    tasks = [
                        window_worker(conn1, windows[0]),
                        window_worker(conn2, windows[1]),
                        window_worker(conn3, windows[2]),
                    ]
                    stats: List[Dict[str, float]] = await asyncio.gather(*tasks)

                    # 读取最终库存用于校验
                    result = await conn1.execute(
                        text("SELECT sold, total FROM tickets_stock WHERE id=:id"),
                        {"id": STOCK_ID},
                    )
                    row = result.fetchone()
                    sold, total = (row[0], row[1]) if row else (0, TOTAL_TICKETS)
                    if row is None:
                        print("[WARN] tickets_stock 找不到 id=1 的行，请确认已插入初始库存记录。")

        # 输出统计
        total_sold_by_windows = sum(int(s["sold"]) for s in stats)
        print(f"数据库记录: 总票数={total}, 已售={sold}")
        print(f"窗口统计: 实际售出={total_sold_by_windows}")
        print("是否超卖:", "是" if sold > total else "否")
        for s in stats:
            print(f"- {s['window']}: 卖出 {int(s['sold'])} 张, 用时 {s['seconds']} 秒")
    finally:
        # 显式释放引擎与连接池，避免事件循环关闭后清理触发异常
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())
