import tensorflow as tf
from scrinet.analysis import frequencyseries_batch as frequencyseries
from scrinet.analysis import timeseries_batch as timeseries


def fft(y):
    """ Fourier transform of y.
    This is fixed to assume:
        1. y is a real TimeSeries
        2. we use a real fft i.e. rfft
    Parameters
    ----------
    y : TimeSeries
        The input vector.
    Returns
    -------
    FrequencySeries:
        The (real) fourier transform of this (real) time series.
    """
    # need to assert either timeseries.TimeSeries timeseries_batch.TimeSeries
    # assert isinstance(y, timeseries.TimeSeries)
    y_data = tf.cast(y.data, tf.float32)
    f = tf.signal.rfft(y_data)
    # print(f)
    dt = tf.cast(y.delta_t, f.dtype)
    f = f * dt
    delta_f = 1.0/(tf.cast(y.delta_t, tf.float32) * tf.cast(tf.shape(y.data)[1], tf.float32))
    fs = frequencyseries.FrequencySeries(
        f, delta_f=delta_f, epoch=y.start_time)
    return fs


def ifft(ytilde, normalise=True):
    """ Inverse fourier transform of ytilde.
    This is fixed to assume:
        1. ytilde is a complex FrequencySeries
        2. we use a complex ifft i.e. ifft
    Parameters
    ----------
    ytilde : FrequencySeries
        The input vector.
    normalise : {bool, True}
        The output is always multiplied by the length of the ytilde data.
        If true then the output is also multiplied by delta_f * 2
    Returns
    -------
    TimeSeries:
        The inverse fourier transform of this frequency series.
    """
    # assert isinstance(ytilde, frequencyseries.FrequencySeries)
    # print(ytilde.data)
    t = tf.signal.ifft(ytilde.data)

    norm = tf.cast(tf.shape(ytilde.data)[1], tf.complex64)
    df = tf.cast(ytilde.delta_f, t.dtype)
    if normalise:
        norm *= df * 2

    norm = tf.cast(norm, tf.complex64)
    t = tf.cast(t, tf.complex64)
    t = t * norm

    delta_t = 1.0/(tf.cast(ytilde.delta_f, tf.float32) * tf.cast(tf.shape(ytilde.data)[1], tf.float32))
    return timeseries.TimeSeries(t, delta_t=delta_t, epoch=ytilde._epoch)
