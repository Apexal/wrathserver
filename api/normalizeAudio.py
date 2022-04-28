from pydub import AudioSegment


def match_target_amplitude(sound, target_dBFS: float):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


def normalize_audio(audio: AudioSegment) -> AudioSegment:
    """Given an audio segment, normalize its volume and then return its bytes in MP3 format."""
    return match_target_amplitude(audio, -20.0)
