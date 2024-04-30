from os import path

from PyQt6.QtCore import QThread, pyqtSignal
    
class ModelInitThread(QThread):
    modelInitialised = pyqtSignal(tuple)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        from model.model_data_pipelines import tf, pre_process, post_process

        model = tf.keras.models.load_model(
            path.abspath(path.join(path.dirname(__file__), 'model_800'))
        )

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
        self.audio = audio
        self.sample_rate = sample_rate

    def run(self):
        stft, angles = self.pre_process(
            self.audio, 
            return_angle=True,
            source_sample_rate=self.sample_rate,
            is_audio_mono=True
        )
        self.modelReturnedResult.emit(
            self.post_process(
                self.model(stft, training=False), angles
            )
        )