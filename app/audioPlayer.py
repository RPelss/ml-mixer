from enum import Enum

import librosa
import pyaudio
import numpy

from PyQt6.QtCore import QTimer

from model import predict

class PlayerState(Enum):
    PLAYING = "PLAYING"
    PAUSED = "PAUSED"
    STOPPED = "STOPPED"
    WAITING = "WAITING"
    NO_TRACK = "NO TRACK"

class Player(object):

    currentTracks = None
    currentProgress = 0

    currentState = PlayerState.NO_TRACK

    def __init__(self, backend, songProgressCallback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.backend = backend
        self.songProgressCallback = songProgressCallback

    def getAudioFromModel(self, path):
        self.currentState = PlayerState.NO_TRACK

        audio, sample_rate = librosa.load(path, sr=None)

        self.currentTracks = predict(audio, sample_rate)

        self.currentState = PlayerState.STOPPED
        return path, len(self.currentTracks[0])
    
    def startPlayback(self):
        if self.currentState == PlayerState.NO_TRACK:
            return

        self.currentState = PlayerState.PLAYING
        self.currentProgress = 0

        # Define callback for playback (1)
        def callback(in_data, frame_count, time_info, status):
            match self.currentState:
                case PlayerState.PLAYING:
                    data = self.currentTracks[0][
                        self.currentProgress 
                        : self.currentProgress + frame_count
                    ]

                    self.currentProgress += len(data)
                    self.songProgressCallback(self.currentProgress)

                    if len(data) != frame_count:
                        stream.close()
                        p.terminate()

                    return (data, pyaudio.paContinue)
                
                case PlayerState.PAUSED | PlayerState.WAITING:
                    return (
                        numpy.zeros(frame_count, dtype=numpy.float32), 
                        pyaudio.paContinue
                    )
                
                case PlayerState.STOPPED | PlayerState.NO_TRACK:
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

    def userSetProgress(self, value):
        self.currentProgress = int(value)

        self.originalState = (
            self.currentState 
            if self.currentState != PlayerState.WAITING 
            else self.originalState
        )
        self.currentState = PlayerState.WAITING

        def endWait():
            self.currentState = self.originalState

        self.waitTimer = QTimer()
        self.waitTimer.setInterval(500)
        self.waitTimer.setSingleShot(True)
        self.waitTimer.timeout.connect(endWait)
        self.waitTimer.start()

    def startPlayOrPausePlayback(self):
        match self.currentState:
            case PlayerState.PLAYING:
                self.currentState = PlayerState.PAUSED
            case PlayerState.PAUSED:
                self.currentState = PlayerState.PLAYING
            case PlayerState.STOPPED:
                self.startPlayback()
            case PlayerState.NO_TRACK:
                return

    def setPlaybackState(self, state):
        if self.currentState == PlayerState.NO_TRACK:
            return
        self.currentState = state
