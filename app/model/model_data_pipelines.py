import tensorflow as tf
import tensorflow_io as tfio

sliding_window_step = 5

stft_fft_length = 1024
stft_fft_unique_bins = stft_fft_length // 2 + 1
stft_window = 512
stft_step = int(stft_window / 4)

model_sample_rate = 22050
db_sample_rate = 44100

# https://stackoverflow.com/questions/62558696/how-do-i-re-batch-a-tensor-in-tensorflow
def sliding_window(x, axis=0):
    window_size = sliding_window_step
    stride = sliding_window_step
    n_in = tf.shape(x)[axis]
    n_out = (n_in - window_size) // stride + 1
    # Just in case n_in < window_size
    n_out = tf.math.maximum(n_out, 0)
    r = tf.expand_dims(tf.range(n_out), 1)
    idx = r * stride + tf.range(window_size)
    return tf.gather(x, idx, axis=axis)

def downsample(audio, source_sample_rate=db_sample_rate):
    return tfio.audio.resample(
        audio, 
        source_sample_rate,
        model_sample_rate
    )

def separate_imaginary(stft, return_angle=False):
    abs = tf.math.abs(stft)
    if return_angle:
        return abs, tf.math.angle(stft)
    else:
        return abs, abs

def pre_process(audio, return_angle=False, source_sample_rate=db_sample_rate, is_audio_mono=False):
    audio = audio if is_audio_mono else audio[0,:]
    abs, angle = separate_imaginary(
        get_stft(
            downsample(
                tf.convert_to_tensor(audio, dtype=tf.float32), 
                source_sample_rate=tf.convert_to_tensor(source_sample_rate, dtype=tf.int64)
            )
        ), 
        return_angle=return_angle
    )

    if return_angle:
        return sliding_window(abs), sliding_window(angle)
    else:
        return sliding_window(abs)
    
def post_process_func(magnitudes, angles):
    return tf.reshape(
        tf.complex(
            tf.math.multiply(magnitudes, tf.math.cos(angles)),
            tf.math.multiply(magnitudes, tf.math.sin(angles))
        ), 
        [-1, stft_fft_unique_bins]
    )

def post_process(stfts, angles):
    return list(map(
        lambda x: get_inverse_stft(
            post_process_func(x, angles)
        ),
        stfts
    ))

def get_stft(audio):
    return tf.signal.stft(
        audio,
        stft_window,
        stft_step,
        fft_length=stft_fft_length
    )

def get_inverse_stft(stft):
    return tf.signal.inverse_stft(
        stft,
        stft_window,
        stft_step,
        fft_length=stft_fft_length
    ).numpy()