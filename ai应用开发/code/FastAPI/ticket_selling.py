import threading
import time
from typing import Dict, List

TOTAL_TICKETS = 100
SALE_DELAY_SEC = 0.01  # 每次卖票的模拟耗时

class TicketCounter:
    def __init__(self, total: int):
        self.total = total
        self.sold = 0
        self.lock = threading.Lock()

    def try_sell_one(self) -> bool:
        """尝试卖一张票，保证不超卖。成功返回 True，失败返回 False。"""
        with self.lock:
            if self.sold < self.total:
                self.sold += 1
                return True
            return False


def window_worker(name: str, counter: TicketCounter, stats: Dict[str, Dict[str, float]]):
    start = time.perf_counter()
    sold_count = 0
    while True:
        if not counter.try_sell_one():
            break
        sold_count += 1
        time.sleep(SALE_DELAY_SEC)
    end = time.perf_counter()
    stats[name] = {
        "sold": sold_count,
        "seconds": round(end - start, 4),
    }


def main():
    counter = TicketCounter(TOTAL_TICKETS)
    stats: Dict[str, Dict[str, float]] = {}

    windows = [f"窗口-{i}" for i in range(1, 4)]
    threads: List[threading.Thread] = []

    for w in windows:
        t = threading.Thread(target=window_worker, args=(w, counter, stats), name=w)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    # 汇总
    total_sold = sum(s["sold"] for s in stats.values())
    print(f"总票数: {TOTAL_TICKETS}, 实际售出: {total_sold}")
    print("是否超卖:", "是" if total_sold > TOTAL_TICKETS else "否")
    print("各窗口统计:")
    for w in windows:
        s = stats[w]
        print(f"- {w}: 卖出 {s['sold']} 张, 用时 {s['seconds']} 秒")


if __name__ == "__main__":
    main()
