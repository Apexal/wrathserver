import json
from typing import Any
from aioredis import from_url, Redis

from api.models import Character


async def initialize_redis_pool() -> Redis:
    return from_url("redis://localhost", encoding="utf-8", decode_responses=True)


async def store_character(redis: Redis, key: str, character: Character):
    return await redis.hset("characters", key, json.dumps(character.dict()))


async def fetch_character(redis: Redis, key: str) -> Character:
    return Character(**await redis.hget("characters", key))
