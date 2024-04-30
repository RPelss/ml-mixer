from os import path

from PyQt6.QtCore import QObject

from model.return_value_threading import ModelCallThread, ModelInitThread

class Model(QObject):

    model = None
    pre_process = None
    post_process = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def onModelInitialised(result):
            model, pre_process, post_process = result
            self.model = model
            self.pre_process = pre_process
            self.post_process = post_process

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