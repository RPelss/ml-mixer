from PyQt6.QtCore import (
    QObject, 
    pyqtSlot, 
    pyqtSignal
)

from audioFileReader import getAudio

class Backend(QObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    setNewSong = pyqtSignal(str, float, arguments=['title, sample_count'])
    showOpenAudioFileDialog = pyqtSignal()

    @pyqtSlot(str)
    def onClicked(self, message):
        self.showOpenAudioFileDialog.emit()
        self.setNewSong.emit(message, 0)
        print("Button clicked :) by " + message)

    @pyqtSlot(float)
    def onSongProgressBarChanged(self, value):
        print(f"Progess bar set to {value}")

    @pyqtSlot(str)
    def onFileDialogAccept(self, value):
        getAudio(value)