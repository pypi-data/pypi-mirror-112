import tensorflow as tf
import tensorflow_probability as tfp
from scrinet.analysis.frequencyseries_batch import FrequencySeries

from scrinet.analysis.timeseries_batch import TimeSeries
from scrinet.analysis import matchedfilter_batch as matchedfilter
import numpy as np
from scrinet.sample.sample_helpers import WaveformParams, DetectorParams, tf_generate_surrogate_at_detector
from typing import NamedTuple, Any
from scrinet.sample.priors import Cosine

tfd = tfp.distributions
tfb = tfp.bijectors


class GwPriors(NamedTuple):
    """
    Object for passing waveform params to functions

    Attributes:
        distance: distance in metre - shape = N,1
        m_tot: total mass in Msun - shape = N,1
        mass_ratio: mass ratio (defined as q>1) - shape = N,1
        chi1: dimensionless spin for bh1  (defined over (-1, 1) - shape = N,1
        chi2: dimensionless spin for bh2 (defined over (-1, 1) - shape = N,1
        theta: sphharm polar - shape = N,1
        phi: sphharm azimuth - shape = N,1
        phase_shift: phase shift - shape = N,1
        ra: right ascension in radians - shape = N,1
        dec: declination in radians - shape = N,1
        psi: polarisation angle in radians - shape = N,1
        time: time (geocentrc maybe!?) - shape = N,1

    """
    # TODO Defaults are very bad defaults atm
    # TODO not sure of distribution type?

    distance: Any = tfd.Uniform(0.125, 1.0)
    m_tot: Any = tfd.Uniform(0.6, 1.)
    mass_ratio: Any = tfd.Uniform(0.125, 1.)
    chi_1: Any = tfd.Uniform(-1., 1.)
    chi_2: Any = tfd.Uniform(-1, 1.)
    theta: Any = tfd.Uniform(0, 1.)
    phi: Any = tfd.Uniform(0, 1.)
    phase_shift: Any = tfd.Uniform(0, 1.)
    ra: Any = tfd.Uniform(0, 1.)
    dec: Any = Cosine(minimum=-1, maximum=1)
    psi: Any = tfd.Uniform(0, 1.)
    time: Any = tfd.Uniform(0.99, 1.01)  # can make this very restrictive


def log_likelihood(
        signal,
        waveform_params,
        detector_params,
        n_batch,
        f_lower,
        delta_f,
        seglen,
        sample_rate,
        delta_t,
        amp_model,
        amp_basis,
        phase_model,
        phase_basis,
        psd,
        detector,
):
    template = tf_generate_surrogate_at_detector(
        waveform_params=waveform_params,
        detector_params=detector_params,
        n_batch=n_batch,
        f_lower=f_lower,
        seglen=seglen,
        sample_rate=sample_rate,
        amp_model=amp_model,
        amp_basis=amp_basis,
        phase_model=phase_model,
        phase_basis=phase_basis,
        detector=detector,
    )

    template = TimeSeries(template, delta_t=delta_t)

    template = FrequencySeries(template.to_frequencyseries().data, delta_f=delta_f)

    log_like = gw_log_like_of_template(
        signal, template, psd=psd, delta_f=delta_f, flow=f_lower, fhigh=3000
    )
    return log_like


# @tf.function(experimental_compile=True)
def gw_log_like_of_template(signal, template, delta_f=1., psd=None, flow=None, fhigh=None):
    """

    :param signal:
    :param template:
    :param delta_f:
    :param psd:
    :return:
    """

    duration = 1. / delta_f

    _, qtilde_fs_sig_temp, _ = matchedfilter.matched_filter_core(
        template, signal, psd=psd, low_frequency_cutoff=flow, high_frequency_cutoff=fhigh)
    # if time marginalised

    # d_inner_h = 4 / duration * \
    #             tf.math.reduce_sum(qtilde_fs_sig_temp.data, axis=1)

    d_inner_h = 4 / duration * \
                tf.signal.fft(qtilde_fs_sig_temp.data)

    _, qtilde_sig_sig, _ = matchedfilter.matched_filter_core(
        template, template, psd=psd, low_frequency_cutoff=flow, high_frequency_cutoff=fhigh)

    optimal_snr_squared = 4 / duration * \
                          tf.math.reduce_sum(qtilde_sig_sig.data, axis=1)

    # log_l = d_inner_h - optimal_snr_squared / 2
    # return tf.math.real(log_l)
    # MAY NEED TO CHECK WHETHER NOT MULTIPLYING BY PRIOR/DT MATTERS
    #also need to check when to add in opt_snr
    log_l = abs(d_inner_h) + tf.math.log(tf.math.bessel_i0e(abs(d_inner_h))) - \
     tf.reshape(tf.math.real(optimal_snr_squared / 2), (d_inner_h.shape[0], 1))
    # if time-marginalised
    log_l = tf.math.reduce_logsumexp(log_l, axis=1)
    return log_l


# @tf.function(experimental_compile=True, autograph=False, experimental_relax_shapes=True)
def simple_gw_prior(waveform_params: WaveformParams, detector_params: DetectorParams):
    prior_val = tf.zeros_like(waveform_params.mass_ratio,
                              dtype=tf.float32)

    prior_dict = GwPriors()._asdict()
    wvf_param_dict = waveform_params._asdict()
    detector_params_dict = detector_params._asdict()

    for param in waveform_params._fields:
        prior_val += prior_dict[param].log_prob(tf.cast(wvf_param_dict[param], tf.float32))

    for param in detector_params._fields:
        prior_val += prior_dict[param].log_prob(tf.cast(detector_params_dict[param], tf.float32))

    return tf.squeeze(prior_val)
