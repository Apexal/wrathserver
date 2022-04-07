import json
from fastapi import FastAPI, HTTPException, Path, status
from fastapi.middleware.cors import CORSMiddleware
from api.db import fetch_character, initialize_redis_pool, store_character
from api.removeBackground import remove_bg_and_resize_b64
from api.normalizeAudio import normalize_mp3_b64
from api.models import *

app = FastAPI(
    title="Wrathserver",
    description="REST API to store, create, and serve characters from Wrathspriter to Wrathskeller.",
    version="0.0.3",
    contact={
        "name": "Frank Matranga",
        "url": "https://github.com/Apexal",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """On app startup, connect to the Redis server."""
    app.state.redis = await initialize_redis_pool()


@app.on_event("shutdown")
async def shutdown_event():
    """On app shutdown, close the connectiong to Redis so it doesn't hang."""
    await app.state.redis.close()


@app.post("/characters/", tags=["characters"], status_code=status.HTTP_201_CREATED)
async def save_character(character: Character):
    return await store_character(app.state.redis, "ABCD", character)


@app.patch("/characters/{character_id}", tags=["characters"])
async def update_character(
    character_id: str = Path(..., title="The unique character code.")
):
    return {"character_id": character_id}


@app.get("/characters/{character_id}", tags=["characters"], response_model=Character)
async def get_character(
    character_id: str = Path(..., title="The unique character code.")
):
    character = await fetch_character(app.state.redis, character_id)

    if character:
        return character
    else:
        raise HTTPException(status_code=404, detail="Character not found")


@app.post("/audio", tags=["process"])
async def process_audio(body: AudioBody):
    normalized_mp3_b64 = normalize_mp3_b64(body.base64EncodedAudio)
    return AudioBody(base64EncodedAudio=normalized_mp3_b64)


@app.post("/image", tags=["process"])
async def process_image(body: ImageBody):
    b64_image = body.base64EncodedImage
    # b64_pose_image = body.base64EncodedPoseImage

    png_image_bg_removed_b64 = remove_bg_and_resize_b64(b64_image)  # type: ignore

    return ImageBody(base64EncodedImage=png_image_bg_removed_b64)
