import asyncio
import time
from typing import Dict, List
from redis.asyncio import from_url, Redis

# Redis 连接地址（复用现有环境）
REDIS_URL = "redis://:jxd123321@118.31.222.50:6379"

# 业务常量与键名
TOTAL_TICKETS = 100
QUEUE_KEY = "queue:tickets"          # 队列键，存放每张票的任务
STATS_HASH = "stats:tickets"         # 可选：统计哈希（本脚本内部统计即可，不强依赖Redis）
SALE_DELAY_SEC = 0.01                 # 模拟售票耗时


def get_redis() -> Redis:
    return from_url(REDIS_URL, decode_responses=True)


async def init_queue(r: Redis) -> None:
    # 清空旧队列，重新放入 TOTAL_TICKETS 个任务（每个任务代表一张票）
    await r.delete(QUEUE_KEY)
    if TOTAL_TICKETS > 0:
        # 用LPUSH批量插入，提高初始化速度
        values = [str(i) for i in range(1, TOTAL_TICKETS + 1)]
        # Redis 允许 LPUSH 多值：LPUSH key v1 v2 ...
        await r.lpush(QUEUE_KEY, *values)


async def window_worker(name: str) -> Dict[str, float]:
    r = get_redis()
    start = time.perf_counter()
    sold_count = 0
    try:
        while True:
            # BRPOP 从队列右侧阻塞弹出1秒，若超时返回None，视为可能售罄
            try:
                item = await r.brpop(QUEUE_KEY, timeout=1)
            except Exception:
                item = None
            if not item:
                # 再次检查队列长度，0则退出
                length = await r.llen(QUEUE_KEY)
                if length == 0:
                    break
                await asyncio.sleep(0.002)
                continue

            # 成功弹出一张票
            sold_count += 1
            # 模拟售票耗时（不占用队列操作）
            await asyncio.sleep(SALE_DELAY_SEC)
    finally:
        await r.aclose()
    seconds = round(time.perf_counter() - start, 4)
    return {"window": name, "sold": sold_count, "seconds": seconds}


async def main():
    # 初始化队列
    r = get_redis()
    try:
        await init_queue(r)
        length = await r.llen(QUEUE_KEY)
        print(f"队列初始化完成: 票数={length}")
    finally:
        await r.aclose()

    # 三个窗口并发消费队列
    windows = ["窗口-1", "窗口-2", "窗口-3"]
    stats: List[Dict[str, float]] = await asyncio.gather(
        *[window_worker(w) for w in windows]
    )

    # 汇总与校验
    total_sold_by_windows = sum(int(s["sold"]) for s in stats)
    r2 = get_redis()
    try:
        remaining = await r2.llen(QUEUE_KEY)
    finally:
        await r2.aclose()

    print(f"消息队列卖票: 总票数={TOTAL_TICKETS}, 剩余={remaining}, 已售={TOTAL_TICKETS - remaining}")
    print(f"窗口统计: 实际售出={total_sold_by_windows}")
    print("是否超卖:", "是" if (TOTAL_TICKETS - remaining) > TOTAL_TICKETS else "否")
    for s in stats:
        print(f"- {s['window']}: 卖出 {int(s['sold'])} 张, 用时 {s['seconds']} 秒")


if __name__ == "__main__":
    asyncio.run(main())
