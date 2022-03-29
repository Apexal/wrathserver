from fastapi import FastAPI, Path, WebSocket, status
from fastapi.middleware.cors import CORSMiddleware
from api.normalizeAudio import normalize_mp3_b64
from api.removeBackground import remove_background_b64
from pydantic import BaseModel


app = FastAPI(
    title="Wrathserver",
    description="REST API and WebSocket server to store, create, and serve characters from Wrathspriter to Wrathskeller.",
    version="0.0.2",
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


@app.post("/characters/", tags=["characters"], status_code=status.HTTP_201_CREATED)
async def save_character():
    return {"message": "Hello World"}


@app.patch("/characters/{character_id}", tags=["characters"])
async def update_character(
    character_id: str = Path(..., title="The unique character code.")
):
    return {"character_id": character_id}


@app.get("/characters/{character_id}", tags=["characters"])
async def get_character(
    character_id: str = Path(..., title="The unique character code.")
):
    return {"character_id": character_id}


class AudioBody(BaseModel):
    base64EncodedAudio: str


@app.post("/audio", tags=["audio"])
async def process_audio(body: AudioBody):
    normalized_mp3_b64 = normalize_mp3_b64(body.base64EncodedAudio)
    return AudioBody(base64EncodedAudio=normalized_mp3_b64)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            message = await websocket.receive_json()

            if not "type" in message or not "data" in message:
                await websocket.send_json({"error": "Invalid message format"})

            mtype, data = message["type"], message["data"]

            # Check type
            if mtype == "image-with-pose":
                b64_png_image = message["data"]["base64EncodedImage"]
                b64_png_pose_image = message["data"]["base64EncodedPoseImage"]

                image_bg_removed = remove_background_b64(b64_png_image)  # type: ignore

                await websocket.send_json(
                    {"poseMatchPercentage": 1, "base64EncodedImage": image_bg_removed}
                )
        except Exception as e:
            print("websocket error", e)
            break
