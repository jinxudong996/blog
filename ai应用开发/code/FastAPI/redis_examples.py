from typing import Any, Dict, List, Optional

import asyncio
from redis.asyncio import from_url, Redis


REDIS_URL = "redis://:jxd123321@118.31.222.50:6379"


def get_redis() -> Redis:
    return from_url(REDIS_URL, decode_responses=True)


async def example_string_set_get(key: str, value: str, expire_seconds: Optional[int] = None) -> str:
    r = get_redis()
    try:
        if expire_seconds:
            await r.set(key, value, ex=expire_seconds)
        else:
            await r.set(key, value)
        got = await r.get(key)
        return got or ""
    finally:
        await r.close()


async def example_hash_set_get(hash_key: str, data: Dict[str, Any]) -> Dict[str, Any]:
    r = get_redis()
    try:
        if data:
            await r.hset(hash_key, mapping=data)
        got = await r.hgetall(hash_key)
        return got
    finally:
        await r.close()


async def example_list_push_pop(list_key: str, values: List[str]) -> List[str]:
    r = get_redis()
    try:
        if values:
            await r.rpush(list_key, *values)
        # 读取全部元素
        length = await r.llen(list_key)
        items: List[str] = []
        for _ in range(length):
            item = await r.lpop(list_key)
            if item is not None:
                items.append(item)
        return items
    finally:
        await r.close()


async def example_pub_sub(channel: str, messages: List[str], timeout_seconds: int = 5) -> List[str]:
    r = get_redis()
    try:
        pubsub = r.pubsub()
        await pubsub.subscribe(channel)

        # 发布消息
        for msg in messages:
            await r.publish(channel, msg)

        received: List[str] = []

        async def reader():
            nonlocal received
            end_time = asyncio.get_event_loop().time() + timeout_seconds
            while asyncio.get_event_loop().time() < end_time:
                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                if message and isinstance(message.get("data"), str):
                    received.append(message["data"]) 
                await asyncio.sleep(0)

        await reader()
        await pubsub.unsubscribe(channel)
        await pubsub.close()
        return received
    finally:
        await r.close()


async def example_keys_scan(pattern: str = "*") -> List[str]:
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
    finally:
        await r.close()


async def main():
    print("String set/get:", await example_string_set_get("demo:key", "hello", 30))
    print("Hash set/get:", await example_hash_set_get("demo:hash", {"name": "Alice", "age": 20}))
    print("List push/pop:", await example_list_push_pop("demo:list", ["a", "b", "c"]))
    print("Pub/Sub:", await example_pub_sub("demo:chan", ["one", "two", "three"]))
    print("Scan keys:", await example_keys_scan("demo:*"))


if __name__ == "__main__":
    asyncio.run(main())
