from os import path
from enum import Enum

from PyQt6.QtCore import QObject, QThread, pyqtSignal, pyqtEnum
from PyQt6.QtQml import qmlRegisterType

from utils import getFullPath

class Model(QObject):

    @pyqtEnum
    class State(Enum):
        (
            INITIALISING, 
            PRE_PROCESSING, 
            WAITING_FROM_MODEL, 
            POST_PROCESSING, 
            IDLING
         ) = range(5)

    model = None
    pre_process = None
    post_process = None

    def __init__(self, stateChangeCallback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stateChangeCallback = stateChangeCallback
        self.setState(self.State.INITIALISING)

        def onModelInitialised(result):
            model, pre_process, post_process = result
            self.model = model
            self.pre_process = pre_process
            self.post_process = post_process
            self.setState(self.State.IDLING)

        self.modelInitThread = ModelInitThread()
        self.modelInitThread.modelInitialised.connect(onModelInitialised)
        self.modelInitThread.start()

    def predict(self, audio, sample_rate, resultCallback):

        def startThread():
            self.modelCallThread = ModelCallThread(self, audio, sample_rate)
            self.modelCallThread.modelReturnedResult.connect(resultCallback)
            self.modelCallThread.start()

        if self.modelInitThread.isFinished():
            startThread()
        else:
            self.modelInitThread.finished.connect(startThread)

    def setState(self, newState):
        self.state = newState
        self.stateChangeCallback(newState)

qmlRegisterType(Model, "MLModel", 1, 0, "Model")

class ModelInitThread(QThread):
    modelInitialised = pyqtSignal(tuple)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        from model.model_data_pipelines import tf, pre_process, post_process

        model = tf.keras.models.load_model(getFullPath('model/model_800'))

        self.modelInitialised.emit((model, pre_process, post_process))

class ModelCallThread(QThread):
    modelReturnedResult = pyqtSignal(list)

    def __init__(
            self, 
            model, 
            audio, 
            sample_rate, 
            *args, 
            **kwargs
        ):
        super().__init__(*args, **kwargs)
        self.model = model.model
        self.pre_process = model.pre_process
        self.post_process = model.post_process
        self.stateChangeCallback = model.setState
        self.audio = audio
        self.sample_rate = sample_rate

    def run(self):
        self.stateChangeCallback(Model.State.PRE_PROCESSING)
        stft, angles = self.pre_process(
            self.audio, 
            return_angle=True,
            source_sample_rate=self.sample_rate,
            is_audio_mono=True
        )

        self.stateChangeCallback(Model.State.WAITING_FROM_MODEL)
        model_result = self.model(stft, training=False)

        self.stateChangeCallback(Model.State.POST_PROCESSING)
        self.modelReturnedResult.emit(
            self.post_process(
                model_result, angles
            )
        )
        self.stateChangeCallback(Model.State.IDLING)
