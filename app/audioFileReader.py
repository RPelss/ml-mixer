import librosa
import import_ipynb
from .. import model_viewer

def getAudio(path):
    audio, sample_rate = librosa.load(path, sr=None)

    _, audio_tracks = model_viewer.predict(audio, sample_rate)

    print(audio_tracks)
    return audio_tracks

