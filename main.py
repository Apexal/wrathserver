from fastapi import FastAPI, Path, WebSocket, WebSocketDisconnect, status
from fastapi.testclient import TestClient

app = FastAPI(
    title="Wrathserver",
    description="REST API and WebSocket server to store, create, and serve characters from Wrathspriter to Wrathskeller.",
    version="0.0.1",
    contact={
        "name": "Frank Matranga",
        "url": "https://github.com/Apexal",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            message = await websocket.receive_json()

            if not "type" in message or not "payload" in message:
                await websocket.send_json({"error": "Invalid message format"})

            mtype, data = message["type"], message["data"]

            # Check type
            if mtype == "audio":
                b64_mp3 = message["data"]["base64EncodedAudio"]

                await websocket.send_json({"base64EncodedAudio": b64_mp3})
            elif mtype == "image-with-pose":
                b64_png_image = message["data"]["base64EncodedImage"]
                b64_png_pose_image = message["data"]["base64EncodedPoseImage"]

                await websocket.send_json(
                    {"poseMatchPercentage": 1, "base64EncodedImage": b64_png_image}
                )
        except Exception as e:
            print("websocket error", e)
            break


# TESTS

test_client = TestClient(app)


def test_websocket():
    test_client = TestClient(app)
    with test_client.websocket_connect("/ws") as websocket:
        websocket.send_json({"type": "audio", "data": {"base64EncodedAudio": ""}})
        data = websocket.receive_json()
        print(data)
