from pydub import AudioSegment

# To use this library, you need pydub for the audio functions and ffmpeg
# for file formats.
# --> pip install pydub
# --> sudo apt-get install ffmpeg
# NOTE: You have to use .wav audio formats 

def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

#sound = AudioSegment.from_file("SFXLoud.wav", "wav")
sound = AudioSegment.from_file("SFXQuiet.wav", "wav")
normalized_sound = match_target_amplitude(sound, -20.0)
#normalized_sound.export("SFXNormalizedLoud.wav", format="wav")
normalized_sound.export("SFXNormalizedQuiet.wav", format="wav")
