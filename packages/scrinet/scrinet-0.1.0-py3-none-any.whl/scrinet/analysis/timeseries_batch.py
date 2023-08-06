import tensorflow as tf
import numpy as np
import scrinet.analysis.tf_fft_batch


class TimeSeries(object):
    """Models a time series consisting of uniformly sampled scalar values.
    The time series can be complex but the FFTs only support real time
    series.

    Parameters
    ----------
    initial_array : array-like
        Array containing sampled data.
    delta_t : float
        Time between consecutive samples in seconds.
    epoch : {None, float}, optional
        Time of the first sample in seconds.
    dtype : {None, tensorflow or numpy data-type}, optional
        Sample data type.
    Attributes
    ----------
    data (tf.Tensor)
    delta_t
    duration
    start_time
    end_time
    sample_times
    sample_rate
    """

    def __init__(self, initial_array, delta_t, epoch=None, dtype=None, cast=tf.float64):
        self._name = "TimeSeries"

        if isinstance(initial_array, list):
            initial_array = self._resize_list_of_waveforms_to_constant_length(initial_array)

        if dtype is None:
            dtype = initial_array.dtype
        self._dtype = tf.dtypes.as_dtype(dtype)

        if self._dtype == tf.complex64:
            dt_dtype = tf.float32
        elif self._dtype == tf.complex128:
            dt_dtype = tf.float64
        else:
            # not sure about this catch
            dt_dtype = self._dtype

        self.delta_t = tf.cast(delta_t, dt_dtype)
        if epoch is None:
            epoch = tf.zeros(initial_array.shape[0])
        self._epoch = tf.reshape(tf.cast(epoch, dt_dtype), shape=(tf.shape(initial_array)[0], 1))
        self.data = tf.convert_to_tensor(initial_array, self._dtype)


        self.sample_times = self.get_sample_times()
        self.duration = self.get_duration()
        self.sample_rate = self.get_sample_rate()
        self.start_time = self.get_start_time()
        self.end_time = self.get_end_time()

    def _resize_list_of_waveforms_to_constant_length(self, list_of_waveforms):
        """
        Resizes a list of possible different length waveforms into an array object where each
        waveform is the same length as the longest waveform in the list. Resizing is done by appending zeros
        :param list_of_waveforms: List of waveform arrays
        :return:
        Resized array of waveforms

        """
        ### need to tf this function
        resize_len = np.max([len(wvf) for wvf in list_of_waveforms])
        resized_wvfs = np.zeros((len(list_of_waveforms), resize_len))
        for idx, wvf in enumerate(list_of_waveforms):
            zeros_to_append = np.zeros(resize_len - len(wvf))
            resized_wvfs[idx, :] = np.append(wvf, zeros_to_append)
        return resized_wvfs

    def get_sample_times(self):
        wvf_len = tf.shape(self.data)

        wvf_len_float = tf.cast(wvf_len, tf.float32)
        delta_t = tf.cast(self.delta_t, tf.float32)
        time_vals = tf.linspace(0., wvf_len_float[1] * delta_t - delta_t, wvf_len[1])
        zero_start_sample_times = tf.ones((wvf_len[0],
                                           wvf_len[1])) * time_vals
        if self._epoch is None:
            return zero_start_sample_times
        else:
            return zero_start_sample_times + self._epoch

    def get_duration(self):
        return tf.cast(tf.shape(self.data)[1], tf.float32) * tf.cast(self.delta_t, tf.float32)

    def get_sample_rate(self):
        """Return the sample rate of the time series.
        """
        return tf.cast(tf.math.round(1.0 / self.delta_t), tf.int64)

    def get_start_time(self):
        """Return time series start time.
        """
        return self._epoch

    def get_end_time(self):
        """Return time series end time
        """
        return tf.cast(self._epoch, tf.float32) + self.get_duration()

    def to_frequencyseries(self, delta_f=None):
        """ Return the Fourier transform of this time series
        Parameters
        ----------
        delta_f : {None, float}, optional
            The frequency resolution of the returned frequency series. By
        default the resolution is determined by the duration of the timeseries.
        Returns
        -------
        FrequencySeries:
            The fourier transform of this time series.
        """
        if self._dtype in [tf.complex64, tf.complex128]:
            raise NotImplementedError("only FFT of real time series supported")

        if not delta_f:
            delta_f = 1.0 / self.duration
        else:
            raise NotImplementedError("custom delta_f not supported")
            delta_f = tf.cast(delta_f, self.duration.dtype)
        delta_f = tf.cast(delta_f, tf.float64)
        # add 0.5 to round integer
        tlen = tf.cast(1.0 / delta_f / tf.cast(self.delta_t, tf.float64) + 0.5, tf.int64)
        # flen = tf.cast(tlen / 2 + 1, tf.int64)

        # not sure how to assert this with symbolic tensor??
        # if tlen < self.data.shape[0]:
        #     raise ValueError("The value of delta_f (%s) would be "
        #                      "undersampled. Maximum delta_f "
        #                      "is %s." % (delta_f, 1.0 / self.duration))

        # zero pad the end of the data to the required length
        # to get desired delta_f
        # tmp_t = np.zeros(tlen)
        # tmp_t[:self.data.shape[0]] = self.data.numpy()[:]
        # tmp_t = tf.convert_to_tensor(tmp_t, self._dtype)

        # wvf_shape = tf.shape(self.data)
        # new_len = tf.math.abs(tlen - tf.cast(wvf_shape[1], tf.int64))
        # #TODO this line is problematic, not sure its necessary though?
        # # arr_to_append = tf.zeros(
        # #     shape=(tf.cast(wvf_shape[0], tf.int64), new_len), dtype=self.data.dtype)
        #
        # arr_to_append = tf.zeros(
        #     shape=(3, 0), dtype=self.data.dtype)
        #
        # tmp_t = tf.concat([self.data, arr_to_append], axis=1)
        tmp_t = self.data
        tmp = TimeSeries(tmp_t,
                         delta_t=self.delta_t,
                         epoch=self.start_time)
        fs = scrinet.analysis.tf_fft_batch.fft(tmp)
        return fs
