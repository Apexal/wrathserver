import base64
from io import BytesIO
from pydub import AudioSegment


def match_target_amplitude(sound, target_dBFS: float):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


def normalize_mp3_bytes(mp3_bytes: bytes) -> bytes:
    input = AudioSegment.from_raw(mp3_bytes)
    normalized_sound = match_target_amplitude(input, -20.0)
    buf = BytesIO()
    normalized_sound.export(buf, format="mp3")
    return buf.getvalue()


def normalize_mp3_b64(mp3_b64: str) -> str:
    return base64.standard_b64encode(
        normalize_mp3_bytes(base64.standard_b64decode(mp3_b64))
    ).decode("utf-8")
