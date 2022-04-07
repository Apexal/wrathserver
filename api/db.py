from typing import Any
from aioredis import from_url, Redis


async def initialize_redis_pool() -> Redis:
    return from_url("redis://localhost", encoding="utf-8", decode_responses=True)


async def store_character(redis: Redis, key: str, character: Any):
    return await redis.hset("characters", key, character)


async def fetch_character(redis: Redis, key: str):
    return await redis.hget("characters", key)
