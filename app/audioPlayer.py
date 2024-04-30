import os
from enum import Enum

import pyaudio
import numpy
import soundfile as sf
import stempeg
from PyQt6.QtCore import QTimer

from model import Model

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

    modelSampleRate = 22050

    def __init__(self, backend, songProgressCallback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = Model()
        self.backend = backend
        self.songProgressCallback = songProgressCallback

    def getAudioFromModel(self, path, resultCallback):
        audio, sampleRate = sf.read(path)
        audio = numpy.transpose(audio)[0]

        def processModelResult(modelResult):
            self.state = self.State.NO_TRACK

            self.tracks = {
                self.Track.DRUMS: modelResult[0],
                self.Track.BASS: modelResult[1],
                self.Track.OTHER: modelResult[2],
                self.Track.VOCALS: modelResult[3]
            }

            self.modelSampleRate = 22050
            self.name = os.path.basename(path).split('.')[0]
            self.state = self.State.STOPPED

            resultCallback(self.name, len(self.tracks[self.Track.DRUMS]))  

        self.model.predict(audio, sampleRate, processModelResult)
    
    def exportTracks(self, path):
        data = {}
        for key, value in self.tracks.items():
            data[key] = numpy.transpose([value])

        stempeg.write_stems(
            path=os.path.join(path, f'{self.name}.mm-mikseris.m4a'),
            data=data,
            sample_rate=self.modelSampleRate,
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

        self.modelSampleRate = rate
        self.tracks = {
            self.Track.DRUMS: stems[0],
            self.Track.BASS: stems[1],
            self.Track.OTHER: stems[2],
            self.Track.VOCALS: stems[3]
        }
        self.state = self.State.STOPPED
        self.name = os.path.basename(path).split('.')[0]

        return self.name, len(self.tracks[self.Track.DRUMS])

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
                self.songProgressCallback(self.progress)

                if len(data) != frame_count:
                    self.stream.close()
                    self.p.terminate()

                return (data, pyaudio.paContinue)
            
            case self.State.PAUSED | self.State.WAITING:
                return (
                    numpy.zeros(frame_count, dtype=numpy.float32), 
                    pyaudio.paContinue
                )
            
            case self.State.STOPPED | self.State.NO_TRACK:
                self.songProgressCallback(0)
                self.stream.close()
                self.p.terminate()
                return (
                    numpy.zeros(1, dtype=numpy.float32), 
                    pyaudio.paComplete
                )

    def startPlayback(self):
        if self.state == self.State.NO_TRACK:
            return

        self.state = self.State.PLAYING
        self.progress = 0
        
        self.p = pyaudio.PyAudio()

        self.stream = self.p.open(
            format=1,
            channels=1,
            rate=self.modelSampleRate,
            output=True,
            stream_callback=self.__playbackCallback
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
