from enum import Enum

from PyQt6.QtCore import (
    QObject,
    pyqtSlot, 
    pyqtSignal
)

from audioPlayer import Player

class Backend(QObject):

    setNewSong = pyqtSignal(str, float, arguments=['title', 'sample_count'])
    setPlayerProgressBarValue = pyqtSignal(int)
    showOpenAudioFileDialog = pyqtSignal()

    def __init__(self, engine, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engine = engine
        self.player = Player(
            self,
            songProgressCallback=lambda x: self.setPlayerProgressBarValue.emit(x)
        )

    @pyqtSlot(str)
    def onFileDialogAccept(self, value):
        name, sample_count = self.player.getAudioFromModel(value)
        self.setNewSong.emit(name, sample_count)

    @pyqtSlot()
    def onFileOpenClicked(self):
        self.showOpenAudioFileDialog.emit()

    @pyqtSlot()
    def onPlayPauseClicked(self):
        self.player.startPlayOrPausePlayback()

    @pyqtSlot(float)
    def onSongProgressBarChanged(self, value):
        self.player.userSetProgress(value)

    @pyqtSlot()
    def onStopClicked(self):
        self.player.setPlaybackState(Player.State.STOPPED)  

    @pyqtSlot(str, float)
    def onVolumeSliderChanged(self, trackName, value):
        self.player.userSetVolume(self.getTrackFromName(trackName), value)

    def getTrackFromName(self, name):
        for t in Player.Track:
            if t.value == name:
                return t
