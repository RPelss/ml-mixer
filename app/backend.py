from PyQt6.QtCore import (
    QObject, 
    pyqtSlot, 
    pyqtSignal
)

from audioPlayer import Player, PlayerState

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
    def onFileOpenClicked(self):
        self.showOpenAudioFileDialog.emit()

    @pyqtSlot(float)
    def onSongProgressBarChanged(self, value):
        self.player.userSetProgress(value)

    @pyqtSlot(str)
    def onFileDialogAccept(self, value):
        name, sample_count = self.player.getAudioFromModel(value)
        self.setNewSong.emit(name, sample_count)

    @pyqtSlot()
    def onPlayPauseClicked(self):
        self.player.startPlayOrPausePlayback()

    @pyqtSlot()
    def onStopClicked(self):
        self.player.setPlaybackState(PlayerState.STOPPED)  