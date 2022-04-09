import base64
from io import BytesIO
from pydub import AudioSegment


def match_target_amplitude(sound, target_dBFS: float):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


def normalize_audio_segment_to_mp3(segment: AudioSegment) -> bytes:
    """Given an audio segment, normalize its volume and then return its bytes in MP3 format."""
    normalized_sound = match_target_amplitude(segment, -20.0)
    buf = BytesIO()
    normalized_sound.export(buf, format="mp3")
    return buf.getvalue()


def normalize_bytes(audio_bytes: bytes, mimetype: str) -> bytes:
    """Given arbitrary bytes of audio and a mimetype of either MP3 or OGG, normalize the audio and return the bytes in MP3 format."""
    if mimetype == "audio/mpeg":
        input = AudioSegment.from_mp3(BytesIO(audio_bytes))
    elif mimetype == "audio/ogg":
        input = AudioSegment.from_file(BytesIO(audio_bytes), codec="opus")
    else:
        raise Exception("Unknown mimetype")

    return normalize_audio_segment_to_mp3(input)


def normalize_to_b64(b64: str, mimetype: str) -> str:
    return base64.standard_b64encode(
        normalize_bytes(base64.standard_b64decode(b64), mimetype)
    ).decode("utf-8")
