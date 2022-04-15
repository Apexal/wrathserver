import logging
from fastapi import FastAPI, HTTPException, Path, Query, status
from fastapi.middleware.cors import CORSMiddleware
from api.db import (
    fetch_character,
    generate_new_character_id,
    initialize_redis_pool,
    store_character,
)
from api.removeBackground import remove_background
from api.normalizeAudio import normalize_to_b64
from api.models import *
from api.utils.converting import b64_to_image, image_to_b64
from api.utils.images import (
    crop_to_content,
    crop_to_pose,
    expand_img_to_square,
    resize,
    scale_img,
)
from api.utils.posing import determine_pose_from_image, pose_height

FORMAT = "%(levelname)s:\t%(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Wrathserver",
    description="REST API to store, create, and serve characters from Wrathspriter to Wrathskeller.",
    version="0.0.5",
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
    logger.info(f"Starting up and connecting Redis...")
    app.state.redis = await initialize_redis_pool()


@app.on_event("shutdown")
async def shutdown_event():
    """On app shutdown, close the connectiong to Redis so it doesn't hang."""
    logger.info("Shutting down and disconnecting Redis...")
    await app.state.redis.close()


@app.post(
    "/characters/",
    tags=["characters"],
    status_code=status.HTTP_201_CREATED,
    response_model=CharacterOut,
)
async def save_character(
    character: CharacterBase, character_id: Optional[str] = Query(None, max_length=5)
):
    new_character_id = (
        character_id
        if character_id
        else await generate_new_character_id(app.state.redis)
    )
    logger.info(f"Generated new character id '{new_character_id}'")
    saved_character = await store_character(
        app.state.redis, new_character_id, character
    )

    return saved_character


@app.get("/characters/{character_id}", tags=["characters"], response_model=CharacterOut)
async def get_character(
    character_id: str = Path(..., title="The unique character code.")
):
    character = await fetch_character(app.state.redis, character_id)

    if character:
        return character
    else:
        raise HTTPException(status_code=404, detail="Character not found")


@app.post("/audio", tags=["process"])
async def process_audio(mimetype: str, body: AudioBody):
    try:
        normalized_mp3_b64 = normalize_to_b64(body.base64EncodedAudio, mimetype)
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)

    return AudioBody(base64EncodedAudio=normalized_mp3_b64)


@app.post("/image", tags=["process"], response_model=ImageBodyOut)
async def process_image(body: ImageBodyIn):
    b64_image = body.base64EncodedImage

    normalized_pose_landmarks = body.normalizedPoseLandmarks
    if normalized_pose_landmarks is None:
        pose_results = determine_pose_from_image(b64_to_image(b64_image))
        if not pose_results.pose_landmarks:  # type: ignore
            # TODO: error message
            raise HTTPException(status_code=400, detail="Pose not detected in image")

        normalized_pose_landmarks = pose_results.pose_landmarks.landmark  # type: ignore

    img = b64_to_image(b64_image)
    img = scale_img(img, scale_factor=250 / pose_height(img, normalized_pose_landmarks))
    img = crop_to_pose(img, normalized_pose_landmarks)
    img = expand_img_to_square(img)
    img = remove_background(img)

    return ImageBodyOut(base64EncodedImage=image_to_b64(img))
