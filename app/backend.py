from PyQt6.QtCore import (
    QObject,
    pyqtSlot, 
    pyqtSignal,
    pyqtProperty
)

from audioPlayer import Player
from utils import getVersion

class Backend(QObject):

    modelStateChanged = pyqtSignal(int)
    showExportAudioFileDialog = pyqtSignal(str)
    setNewSong = pyqtSignal(str, float, arguments=['title', 'sample_count'])
    setPlayerProgressBarValue = pyqtSignal(float)
    showImportAudioFileDialog = pyqtSignal()
    showOpenAudioFileDialog = pyqtSignal()
    songStateChanged = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player = Player(
            self,
            songProgressCallback=self.setPlayerProgressBarValue.emit,
            stateChangeCallback=lambda x: self.songStateChanged.emit(x.value),
            modelStateChangeCallback=lambda x: self.modelStateChanged.emit(x.value)
        )

    @pyqtSlot()
    def onExportClicked(self):
        if self.player.state != Player.State.NO_TRACK:
            self.showExportAudioFileDialog.emit(
                f'{self.player.name}.mp4'
            )

    @pyqtSlot(str)
    def onExportFileAccept(self, path):
        self.player.exportTracks(path)

    @pyqtSlot(str)
    def onFileDialogAccept(self, path):
        self.player.getAudioFromModel(path, self.setNewSong.emit)
        
    @pyqtSlot(str)
    def onImportFileAccept(self, path):
        name, durationSeconds = self.player.importTracks(path)
        self.setNewSong.emit(name, durationSeconds)

    @pyqtSlot()
    def onFileOpenClicked(self):
        self.showOpenAudioFileDialog.emit()

    @pyqtSlot()
    def onImportClicked(self):
        self.showImportAudioFileDialog.emit()

    @pyqtSlot()
    def onPlayPauseClicked(self):
        match self.player.state:
            case Player.State.PLAYING:
                self.player.setPlaybackState(Player.State.PAUSED)
            case Player.State.PAUSED:
                self.player.setPlaybackState(Player.State.PLAYING)
            case Player.State.STOPPED:
                self.player.startPlayback()

    @pyqtSlot(float)
    def onSongProgressBarChanged(self, value):
        self.player.userSetProgress(value)

    @pyqtSlot()
    def onStopClicked(self):
        self.player.setPlaybackState(Player.State.STOPPED)  

    @pyqtSlot(int, float)
    def onVolumeSliderChanged(self, enum, value):
        self.player.userSetVolume(self.__getTrackFromEnumValue(enum), value)

    @pyqtProperty(str)
    def version(self):
        return getVersion()

    def __getTrackFromEnumValue(self, value):
        for t in Player.Track:
            if t.value == value:
                return t
