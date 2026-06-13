from typing import Optional, Dict, Any, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from redis.asyncio import from_url, Redis


REDIS_URL = "redis://:jxd123321@118.31.222.50:6379"


def get_redis() -> Redis:
    return from_url(REDIS_URL, decode_responses=True)


router = APIRouter(prefix="/redis", tags=["redis"])


class SetRequest(BaseModel):
    key: str
    value: str
    expire_seconds: Optional[int] = None


@router.post("/set", summary="设置字符串键值，可选过期")
async def redis_set(req: SetRequest):
    r = get_redis()
    try:
        if req.expire_seconds:
            ok = await r.set(req.key, req.value, ex=req.expire_seconds)
        else:
            ok = await r.set(req.key, req.value)
        return {"ok": bool(ok)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis set 失败: {e}")
    finally:
        await r.close()


@router.get("/get", summary="读取字符串键值")
async def redis_get(key: str):
    r = get_redis()
    try:
        # 仅用于字符串类型的键；其他类型将报错提示
        val = await r.get(key)
        return {"key": key, "type": "string", "value": val}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis get 失败: {e}")
    finally:
        await r.close()


class HashSetRequest(BaseModel):
    fields: Dict[str, Any]


@router.post("/hash/{name}", summary="写入哈希字段")
async def redis_hset(name: str, req: HashSetRequest):
    r = get_redis()
    try:
        await r.hset(name, mapping=req.fields)
        got = await r.hgetall(name)
        return got
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis hset 失败: {e}")
    finally:
        await r.close()


@router.get("/hash/{name}", summary="读取哈希全部字段")
async def redis_hgetall(name: str):
    r = get_redis()
    try:
        got = await r.hgetall(name)
        return got
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis hgetall 失败: {e}")
    finally:
        await r.close()


@router.get("/keys", summary="扫描匹配的键")
async def redis_keys(pattern: str = "*") -> List[str]:
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis scan 失败: {e}")
    finally:
        await r.close()


@router.get("/type", summary="获取键的类型")
async def redis_type(key: str):
    r = get_redis()
    try:
        t = await r.type(key)
        # redis 返回 bytes 或 str，decode_responses=True 已处理
        return {"key": key, "type": t}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis type 查询失败: {e}")
    finally:
        await r.close()


@router.get("/get_any", summary="按键类型读取值")
async def redis_get_any(key: str):
    r = get_redis()
    try:
        t = await r.type(key)
        if t == "string":
            val = await r.get(key)
            return {"key": key, "type": t, "value": val}
        elif t == "hash":
            val = await r.hgetall(key)
            return {"key": key, "type": t, "value": val}
        elif t == "list":
            length = await r.llen(key)
            val = await r.lrange(key, 0, length)
            return {"key": key, "type": t, "value": val}
        elif t == "set":
            members = await r.smembers(key)
            return {"key": key, "type": t, "value": list(members) if isinstance(members, set) else members}
        elif t == "zset":
            val = await r.zrange(key, 0, -1, withscores=True)
            return {"key": key, "type": t, "value": val}
        elif t in (None, "none"):
            return {"key": key, "type": "none", "value": None}
        else:
            raise HTTPException(status_code=400, detail=f"不支持的键类型: {t}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"读取失败: {e}")
    finally:
        await r.close()
