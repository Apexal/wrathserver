from pydub import AudioSegment
from pydub.effects import normalize, strip_silence


def trim_audio_silence(audio: AudioSegment) -> AudioSegment:
    return strip_silence(audio, silence_thresh=-24)


def normalize_audio(audio: AudioSegment) -> AudioSegment:
    return normalize(audio)
