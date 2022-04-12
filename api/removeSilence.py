import base64
from io import BytesIO, StringIO
from pydub import AudioSegment
from pydub.silence import detect_leading_silence

def trim_mp3_bytes(mp3_bytes: bytes) -> bytes:
    input = AudioSegment.from_mp3(BytesIO(mp3_bytes))
    trim_leading_silence: AudioSegment = lambda x: x[detect_leading_silence(x) :]
    trim_trailing_silence: AudioSegment = lambda x: trim_leading_silence(x.reverse()).reverse()
    strip_silence: AudioSegment = lambda x: trim_trailing_silence(trim_leading_silence(x))
    buf = BytesIO()
    trimmed_sound = strip_silence(input)
    trimmed_sound.export(buf, format="mp3")
    return buf.getvalue()

def trim_mp3_b64(mp3_b64: str) -> str:
    with open("output.mp3", "wb") as f:
        f.write(base64.standard_b64decode(mp3_b64))
    return base64.standard_b64encode(
        trim_mp3_bytes(base64.standard_b64decode(mp3_b64))
    ).decode("utf-8")