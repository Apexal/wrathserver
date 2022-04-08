import logging
import json
import random
import string
import os
from typing import Optional
from aioredis import from_url, Redis

from api.models import CharacterBase, CharacterOut

logger = logging.getLogger(__name__)

REDIS_URL = os.environ["REDIS_URL"]


async def initialize_redis_pool() -> Redis:
    logger.info(f"Connecting to Redis...")
    return from_url(
        REDIS_URL,
        encoding="utf-8",
        decode_responses=True,
    )


def generate_character_id():
    return "".join(random.choice(string.ascii_uppercase) for _ in range(5))


async def generate_new_character_id(redis: Redis):
    existing_character_ids = await redis.hkeys("characters")

    id = generate_character_id()
    while id in existing_character_ids:
        id = generate_character_id()

    return id


async def store_character(
    redis: Redis, key: str, character: CharacterBase
) -> CharacterOut:
    stored_character = CharacterOut(id=key, **character.dict())
    await redis.set("character:" + key, json.dumps(stored_character.dict()))
    await redis.expire("character:" + key, 60 * 5)  # Remove after 5 minutes
    return stored_character


async def fetch_character(redis: Redis, key: str) -> Optional[CharacterOut]:
    character_json = await redis.get("character:" + key)
    if not character_json:
        return None
    return CharacterOut(**json.loads(character_json))
