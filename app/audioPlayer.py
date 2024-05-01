import os
from enum import Enum

import pyaudio
import numpy
import soundfile as sf
import stempeg
from PyQt6.QtCore import QTimer, QObject, pyqtEnum
from PyQt6.QtQml import qmlRegisterType

from model import Model

class Player(QObject):

    @pyqtEnum
    class State(Enum):
        (
            PLAYING, 
            PAUSED, 
            STOPPED, 
            WAITING, 
            NO_TRACK
         ) = range(5)

    @pyqtEnum
    class Track(Enum):
        (
            MIX,
            DRUMS,
            BASS,
            OTHER,
            VOCALS
        ) = range(5)

    progress = 0
    tracks = None
    trackSampleRate = 22050
    waitingDurationMs = 250
    volumes = {
        Track.MIX: 1.0,
        Track.DRUMS: 1.0,
        Track.BASS: 1.0,
        Track.OTHER: 1.0,
        Track.VOCALS: 1.0
    }

    def __init__(
            self, 
            backend, 
            songProgressCallback, 
            stateChangeCallback, 
            *args, 
            **kwargs
        ):
        super().__init__(*args, **kwargs)
        self.model = Model()
        self.backend = backend
        self.songProgressCallback = songProgressCallback
        self.stateChangeCallback = stateChangeCallback
        self.__setState(self.State.NO_TRACK)

    def getAudioFromModel(self, path, resultCallback):
        audio, sampleRate = sf.read(path)
        audio = numpy.transpose(audio)[0]

        def processModelResult(modelResult):
            self.__setState(self.State.NO_TRACK)

            self.tracks = {
                self.Track.DRUMS: modelResult[0],
                self.Track.BASS: modelResult[1],
                self.Track.OTHER: modelResult[2],
                self.Track.VOCALS: modelResult[3]
            }

            self.trackSampleRate = 22050
            self.progress = 0
            self.name = os.path.basename(path).split('.')[0]
            self.__setState(self.State.STOPPED)

            resultCallback(
                self.name, 
                len(self.tracks[self.Track.DRUMS]) / self.trackSampleRate
            )  

        self.model.predict(audio, sampleRate, processModelResult)
    
    def exportTracks(self, path):
        data = {}
        for key, value in self.tracks.items():
            data[key] = numpy.transpose([value])

        stempeg.write_stems(
            path=os.path.join(path, f'{self.name}.mm-mikseris.m4a'),
            data=data,
            sample_rate=self.trackSampleRate,
            writer=stempeg.ChannelsWriter()
        )
    
    def importTracks(self, path):
        stems, rate = stempeg.read_stems(
            path, 
            dtype=numpy.float32,
            reader=stempeg.ChannelsReader(nb_channels=1)
        )

        if numpy.shape(stems)[0] != 4:
            return
        
        self.__setState(self.State.NO_TRACK)

        self.trackSampleRate = rate
        self.tracks = {
            self.Track.DRUMS: stems[0],
            self.Track.BASS: stems[1],
            self.Track.OTHER: stems[2],
            self.Track.VOCALS: stems[3]
        }
        self.progress = 0
        self.name = os.path.basename(path).split('.')[0]
        self.__setState(self.State.STOPPED)

        return (
            self.name, 
            len(self.tracks[self.Track.DRUMS]) / self.trackSampleRate
        )

    def startPlayback(self):
        if self.state == self.State.NO_TRACK:
            return

        self.__setState(self.State.PLAYING)
        
        self.p = pyaudio.PyAudio()

        self.stream = self.p.open(
            format=1,
            channels=1,
            rate=self.trackSampleRate,
            output=True,
            stream_callback=self.__playbackCallback
        )

    def userSetVolume(self, track, value):
        self.volumes[track] = value

    def userSetProgress(self, value):
        self.progress = int(value * self.trackSampleRate)

        self.originalState = (
            self.state 
            if self.state != self.State.WAITING 
            else self.originalState
        )
        self.__setState(self.State.WAITING)

        def endWait():
            self.__setState(self.originalState)

        self.waitTimer = QTimer()
        self.waitTimer.setInterval(self.waitingDurationMs)
        self.waitTimer.setSingleShot(True)
        self.waitTimer.timeout.connect(endWait)
        self.waitTimer.start()

    def startPlayOrPausePlayback(self):
        match self.state:
            case self.State.PLAYING:
                self.__setState(self.State.PAUSED)
            case self.State.PAUSED:
                self.__setState(self.State.PLAYING)
            case self.State.STOPPED:
                self.startPlayback()

    def setPlaybackState(self, state):
        if self.state != self.State.NO_TRACK:
            self.__setState(state)

    def __setState(self, newState):
        self.state = newState
        if newState != self.State.WAITING:
            self.stateChangeCallback(newState)

    def __createMixture(self, fromFrame, toFrame):
        getTrackData = lambda track: self.tracks[track][fromFrame : toFrame] * self.volumes[track]

        tracks = [
            getTrackData(self.Track.DRUMS),
            getTrackData(self.Track.BASS),
            getTrackData(self.Track.OTHER),
            getTrackData(self.Track.VOCALS) 
        ]

        return numpy.clip(numpy.sum(tracks, axis=0), -1, 1) * self.volumes[self.Track.MIX]
    
    def __playbackCallback(self, _, frame_count, __, ___):
        match self.state:
            case self.State.PLAYING:
                data = self.__createMixture(self.progress, self.progress + frame_count)

                self.progress += len(data)
                self.songProgressCallback(self.progress / self.trackSampleRate)

                if len(data) != frame_count:
                    self.stream.close()

                return (data, pyaudio.paContinue)
            
            case self.State.PAUSED | self.State.WAITING:
                return (
                    numpy.zeros(frame_count, dtype=numpy.float32), 
                    pyaudio.paContinue
                )
            
            case self.State.STOPPED | self.State.NO_TRACK:
                self.progress = 0
                self.songProgressCallback(0)
                self.stream.close()
                return (
                    numpy.zeros(1, dtype=numpy.float32), 
                    pyaudio.paComplete
                )
        

qmlRegisterType(Player, "AudioPlayer", 1, 0, "Player")
