import base64
from io import BytesIO
from PIL import Image, ImageOps
from pydub import AudioSegment


def b64_to_bytes(b64: str) -> bytes:
    return base64.standard_b64decode(b64)


def bytes_to_b64(b: bytes) -> str:
    return base64.standard_b64encode(b).decode("utf-8")


def b64_to_image(b64_png: str) -> Image.Image:
    img = Image.open(BytesIO(b64_to_bytes(b64_png)))
    img = ImageOps.exif_transpose(img)
    return img


def image_to_b64(img: Image.Image) -> str:
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return bytes_to_b64(buffered.getvalue())


def b64_to_audio(b64: str, mimetype: str) -> AudioSegment:
    audio_bytes = b64_to_bytes(b64)
    if mimetype == "audio/mpeg":
        input = AudioSegment.from_mp3(BytesIO(audio_bytes))
    elif mimetype == "audio/ogg":
        input = AudioSegment.from_file(BytesIO(audio_bytes), codec="opus")
    else:
        raise Exception("Unknown mimetype")

    return input


def audio_to_mp3_b64(audio: AudioSegment) -> str:
    buf = BytesIO()
    audio.export(buf, format="mp3")
    return bytes_to_b64(buf.getvalue())
