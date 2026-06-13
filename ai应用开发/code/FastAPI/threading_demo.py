from concurrent.futures import ThreadPoolExecutor, as_completed
import time


def worker(name):
    print(f"{name} start")
    time.sleep(1)
    print(f"{name} end")
    return name

if __name__ == "__main__":
    names = ["Thread-1", "Thread-2", "Thread-3"]
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(worker, n) for n in names]
        for future in as_completed(futures):
            _ = future.result()
    print("All threads done")
