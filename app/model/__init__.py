from os import path

from model.return_value_threading import ReturnValueThread

model = None
pre_process = None
post_process = None

def init():
    from model.model_data_pipelines import tf, pre_process, post_process

    model = tf.keras.models.load_model(
        path.abspath(path.join(path.dirname(__file__), 'model_800'))
    )

    return model, pre_process, post_process

thread = ReturnValueThread(target=init)
thread.start()

def predict(audio, sample_rate):
    global model, pre_process, post_process

    if model is None:
        model, pre_process, post_process = thread.join()

    stft, angles = pre_process(
        audio, 
        return_angle=True,
        source_sample_rate=sample_rate,
        is_audio_mono=True
    )
    return post_process(model(stft, training=False), angles)