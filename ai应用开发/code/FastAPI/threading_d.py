'''
Author: jinxudong 18751241086@163.com
Date: 2025-12-06 21:15:49
LastEditors: jinxudong 18751241086@163.com
LastEditTime: 2025-12-06 21:16:00
FilePath: \code\FastAPI\threading.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import threading
import time


def worker(name):
    print(f"{name} start")
    time.sleep(1)
    print(f"{name} end")


t1 = threading.Thread(target=worker, args=("Thread-1",))
t2 = threading.Thread(target=worker, args=("Thread-2",))

t1.start()
t2.start()

t1.join()
t2.join()

print("All threads done")
