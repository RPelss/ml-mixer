from enum import Enum

import librosa
import pyaudio
import numpy

from PyQt6.QtCore import QTimer

from model import predict

class Player(object):

    class State(Enum):
        PLAYING = "PLAYING"
        PAUSED = "PAUSED"
        STOPPED = "STOPPED"
        WAITING = "WAITING"
        NO_TRACK = "NO TRACK"

    class Track(Enum):
        MIX = "MIX"
        DRUMS = "DRUMS"
        BASS = "BASS"
        OTHER = "OTHER"
        VOCALS = "VOCALS"

    progress = 0
    state = State.NO_TRACK
    tracks = None
    volumes = {
        Track.MIX: 1.0,
        Track.DRUMS: 1.0,
        Track.BASS: 1.0,
        Track.OTHER: 1.0,
        Track.VOCALS: 1.0
    }

    def __init__(self, backend, songProgressCallback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.backend = backend
        self.songProgressCallback = songProgressCallback

    def getAudioFromModel(self, path):
        self.state = self.State.NO_TRACK

        audio, sampleRate = librosa.load(path, sr=None)

        modelResult = predict(audio, sampleRate)

        self.tracks = {
            self.Track.DRUMS: modelResult[0],
            self.Track.BASS: modelResult[1],
            self.Track.OTHER: modelResult[2],
            self.Track.VOCALS: modelResult[3]
        }

        self.state = self.State.STOPPED
        return path, len(self.tracks[self.Track.DRUMS])
    
    def startPlayback(self):
        if self.state == self.State.NO_TRACK:
            return

        self.state = self.State.PLAYING
        self.progress = 0

        def createMixture(fromFrame, toFrame):
            getTrackData = lambda track: self.tracks[track][fromFrame : toFrame] * self.volumes[track]

            tracks = [
                getTrackData(self.Track.DRUMS),
                getTrackData(self.Track.BASS),
                getTrackData(self.Track.OTHER),
                getTrackData(self.Track.VOCALS) 
            ]

            return numpy.mean(tracks, axis=0) * self.volumes[self.Track.MIX]

        def callback(_, frame_count, __, ___):
            match self.state:
                case self.State.PLAYING:
                    data = createMixture(self.progress, self.progress + frame_count)

                    self.progress += len(data)
                    self.songProgressCallback(self.progress)

                    if len(data) != frame_count:
                        stream.close()
                        p.terminate()

                    return (data, pyaudio.paContinue)
                
                case self.State.PAUSED | self.State.WAITING:
                    return (
                        numpy.zeros(frame_count, dtype=numpy.float32), 
                        pyaudio.paContinue
                    )
                
                case self.State.STOPPED | self.State.NO_TRACK:
                    self.songProgressCallback(0)
                    stream.close()
                    p.terminate()
                    return (
                        numpy.zeros(1, dtype=numpy.float32), 
                        pyaudio.paComplete
                    )
        
        p = pyaudio.PyAudio()

        stream = p.open(
            format=1,
            channels=1,
            rate=22050,
            output=True,
            stream_callback=callback
        )

    def userSetVolume(self, track, value):
        self.volumes[track] = value

    def userSetProgress(self, value):
        self.progress = int(value)

        self.originalState = (
            self.state 
            if self.state != self.State.WAITING 
            else self.originalState
        )
        self.state = self.State.WAITING

        def endWait():
            self.state = self.originalState

        self.waitTimer = QTimer()
        self.waitTimer.setInterval(500)
        self.waitTimer.setSingleShot(True)
        self.waitTimer.timeout.connect(endWait)
        self.waitTimer.start()

    def startPlayOrPausePlayback(self):
        match self.state:
            case self.State.PLAYING:
                self.state = self.State.PAUSED
            case self.State.PAUSED:
                self.state = self.State.PLAYING
            case self.State.STOPPED:
                self.startPlayback()
            case self.State.NO_TRACK:
                return

    def setPlaybackState(self, state):
        if self.state != self.State.NO_TRACK:
            self.state = state
