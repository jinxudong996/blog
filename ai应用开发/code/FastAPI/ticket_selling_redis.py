import asyncio
import time
from typing import Dict, List
from redis.asyncio import from_url, Redis

# Redis 连接地址
REDIS_URL = "redis://:jxd123321@118.31.222.50:6379"

# 业务常量
TOTAL_TICKETS = 100
TICKET_KEY = "tickets:remaining"  # 剩余票数的键
LOCK_KEY = "lock:tickets"         # 分布式锁键
SALE_DELAY_SEC = 0.01              # 每次卖票的模拟耗时


def get_redis() -> Redis:
    return from_url(REDIS_URL, decode_responses=True)


async def init_stock(r: Redis) -> None:
    # 如果不存在则初始化为 TOTAL_TICKETS；存在则保留当前值（便于多次运行观察）
    exists = await r.exists(TICKET_KEY)
    if not exists:
        await r.set(TICKET_KEY, TOTAL_TICKETS)


async def sell_one_with_lock(r: Redis, window_name: str) -> bool:
    """使用 Redis 分布式锁保护“检查+扣减”关键区，成功卖出返回 True，售罄或失败返回 False。"""
    lock = r.lock(LOCK_KEY, timeout=5, blocking_timeout=1)  # 超时时间与获取等待时间可调
    acquired = await lock.acquire(blocking=True)
    if not acquired:
        # 未拿到锁，视为本次卖票失败（可重试）
        return False
    try:
        # 关键区：读取剩余、判定、扣减
        remaining_str = await r.get(TICKET_KEY)
        remaining = int(remaining_str) if remaining_str is not None else 0
        if remaining <= 0:
            return False
        # 扣减一张（原子自减命令）
        await r.decr(TICKET_KEY)
        return True
    finally:
        try:
            await lock.release()
        except Exception:
            # 若锁已过期或其他异常，忽略释放错误
            pass


async def window_worker(name: str) -> Dict[str, float]:
    r = get_redis()
    start = time.perf_counter()
    sold_count = 0
    try:
        while True:
            ok = await sell_one_with_lock(r, name)
            if not ok:
                # 售罄或未拿到锁（可以继续尝试），策略：若剩余为0则退出；否则短暂休眠后重试
                remaining_str = await r.get(TICKET_KEY)
                remaining = int(remaining_str) if remaining_str is not None else 0
                if remaining <= 0:
                    break
                await asyncio.sleep(0.002)
                continue
            sold_count += 1
            # 模拟售票耗时（不占用锁，避免长时间持锁）
            await asyncio.sleep(SALE_DELAY_SEC)
    finally:
        await r.aclose()
    seconds = round(time.perf_counter() - start, 4)
    return {"window": name, "sold": sold_count, "seconds": seconds}


async def main():
    r = get_redis()
    try:
        await init_stock(r)
        remaining_str = await r.get(TICKET_KEY)
        remaining = int(remaining_str) if remaining_str is not None else 0
        print(f"初始剩余票数: {remaining}")
    finally:
        await r.aclose()

    # 三个窗口并发卖票
    windows = ["窗口-1", "窗口-2", "窗口-3"]
    stats: List[Dict[str, float]] = await asyncio.gather(
        *[window_worker(w) for w in windows]
    )

    # 汇总
    r2 = get_redis()
    try:
        remaining_str = await r2.get(TICKET_KEY)
        remaining = int(remaining_str) if remaining_str is not None else 0
    finally:
        await r2.aclose()

    total_sold_by_windows = sum(int(s["sold"]) for s in stats)
    print(f"数据库(Redis)记录: 总票数={TOTAL_TICKETS}, 剩余={remaining}, 已售={TOTAL_TICKETS - remaining}")
    print(f"窗口统计: 实际售出={total_sold_by_windows}")
    print("是否超卖:", "是" if (TOTAL_TICKETS - remaining) > TOTAL_TICKETS else "否")
    for s in stats:
        print(f"- {s['window']}: 卖出 {int(s['sold'])} 张, 用时 {s['seconds']} 秒")


if __name__ == "__main__":
    asyncio.run(main())
