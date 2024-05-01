from PyQt6.QtCore import (
    QObject,
    pyqtSlot, 
    pyqtSignal
)

from audioPlayer import Player

class Backend(QObject):

    showExportAudioFolderDialog = pyqtSignal()
    setNewSong = pyqtSignal(str, float, arguments=['title', 'sample_count'])
    setPlayerProgressBarValue = pyqtSignal(float)
    showImportAudioFileDialog = pyqtSignal()
    showOpenAudioFileDialog = pyqtSignal()
    songStateChange = pyqtSignal(int)

    def __init__(self, engine, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engine = engine
        self.player = Player(
            self,
            songProgressCallback=self.setPlayerProgressBarValue.emit,
            stateChangeCallback=lambda x: self.songStateChange.emit(x.value)
        )

    @pyqtSlot()
    def onExportClicked(self):
        if self.player.state != Player.State.NO_TRACK:
            self.showExportAudioFolderDialog.emit()

    @pyqtSlot(str)
    def onExportFolderAccept(self, path):
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
        self.player.startPlayOrPausePlayback()

    @pyqtSlot(float)
    def onSongProgressBarChanged(self, value):
        self.player.userSetProgress(value)

    @pyqtSlot()
    def onStopClicked(self):
        self.player.setPlaybackState(Player.State.STOPPED)  

    @pyqtSlot(int, float)
    def onVolumeSliderChanged(self, enum, value):
        self.player.userSetVolume(self.getTrackFromEnumValue(enum), value)

    def getTrackFromEnumValue(self, value):
        for t in Player.Track:
            if t.value == value:
                return t
