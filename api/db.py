import logging
import json
import random
import string
from typing import Any, Optional
from aioredis import from_url, Redis

from api.models import Character

logger = logging.getLogger(__name__)


async def initialize_redis_pool() -> Redis:
    logger.info(f"Connecting to Redis...")
    return from_url("redis://localhost", encoding="utf-8", decode_responses=True)


def generate_character_id():
    return "".join(random.choice(string.ascii_uppercase) for _ in range(5))


async def generate_new_character_id(redis: Redis):
    existing_character_ids = await redis.hkeys("characters")

    id = generate_character_id()
    while id in existing_character_ids:
        id = generate_character_id()

    return id


async def store_character(redis: Redis, key: str, character: Character):
    await redis.hset("characters", key, json.dumps(character.dict()))
    return character


async def fetch_character(redis: Redis, key: str) -> Optional[Character]:
    character_json = await redis.hget("characters", key)
    if character_json:
        return None
    return Character(**character_json)
