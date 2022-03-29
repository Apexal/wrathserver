from fastapi.testclient import TestClient
from ..main import app

# test_client = TestClient(app)


# def test_websocket_response_format():
#     test_client = TestClient(app)
#     with test_client.websocket_connect("/ws") as websocket:
#         websocket.send_json({"type": "audio", "data": {"base64EncodedAudio": ""}})
#         data = websocket.receive_json()
#         assert "base64EncodedAudio" in data
