import tensorflow as tf
from scrinet.analysis.utils import tf_get_antenna_response, detector_vertex
from tensorflow_probability.python.math import interpolation as tfp_interp

import numpy as np
import arviz as az
import scrinet.analysis.timeseries_batch as ts
import scrinet.analysis.utils as ut
import lal
import phenom
from typing import NamedTuple

from scrinet.interfaces import lalutils


# @tf.function(experimental_compile=True, autograph=True, experimental_relax_shapes=True)

class WaveformParams(NamedTuple):
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

    """

    distance: tf.Tensor
    m_tot: tf.Tensor
    mass_ratio: tf.Tensor
    chi_1: tf.Tensor
    chi_2: tf.Tensor
    theta: tf.Tensor
    phi: tf.Tensor
    phase_shift: tf.Tensor


class DetectorParams(NamedTuple):
    """
    Object for passing detector response params to functions

    Attributes:
         ra: right ascension in radians - shape = N,1
         dec: declination in radians - shape = N,1
         psi: polarisation angle in radians - shape = N,1
         time: time (geocentrc maybe!?) - shape = N,1

    """

    ra: tf.Tensor
    dec: tf.Tensor
    psi: tf.Tensor
    time: tf.Tensor


class GwParamScalers(NamedTuple):
    """
    Object for passing scalers from sample space into physical space
    basically a normalisation so that parameters are defined over the same
    (scale to order of magnitude)

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

    distance: float = 8. * 10 ** 3
    m_tot: float = 100.
    mass_ratio: float = 8.
    chi_1: float = 1.
    chi_2: float = 1.
    theta: float = 2 * np.pi
    phi: float = 2 * np.pi
    phase_shift: float = 1.
    ra: float = 2 * np.pi
    dec: float = np.pi / 2
    psi: float = 2 * np.pi
    time: float = 3.0


def amp_predict_hack(model, _input):
    """
    Function to re-create model.predict(input) but allows the graph to be built correctly
    (see https://github.com/tensorflow/tensorflow/issues/33997)

    :param model: A trained scrinet Neural Network
    :param _input: The point at which you want to make a prediction
    :return:
    """
    x = _input
    x = x_scale_hack(model, x)
    pred = tf.convert_to_tensor(x)
    net_layers = model.model.layers
    for layer in net_layers:
        pred = layer(pred)
    return pred


# @tf.function(experimental_compile=True, autograph=True, experimental_relax_shapes=True)
def phase_predict_hack(model, _input):
    """
    Function to re-create model.predict(input) but allows the graph to be built correctly
    (see https://github.com/tensorflow/tensorflow/issues/33997)

    :param model: A trained scrinet Neural Network
    :param _input: The point at which you want to make a prediction
    :return:
    """
    x = _input
    x = x_scale_hack(model, x)
    pred = tf.convert_to_tensor(x)
    net_layers = model.model.layers
    for layer in net_layers:
        pred = layer(pred)
    pred = y_inv_minmax_scale_hack(model, pred)
    return pred


# @tf.function(experimental_compile=True, experimental_relax_shapes=True)
def x_scale_hack(model, _input):
    """
    Function to re-create sklearn standard scaler for the input (as a tensorflow function)

    :param model: A trained scrinet Neural Network
    :param _input: The point at which you want to scale
    :return:
    """
    x = _input
    # can hardcode 3 because surrogate is q, chi1, chi2
    x_dim = 3
    means = tf.constant([model.X_scalers[i].mean_[0]
                         for i in range(x_dim)])
    stds = tf.constant([model.X_scalers[i].scale_[0]
                        for i in range(x_dim)])
    means = tf.cast(means, tf.float32)
    stds = tf.cast(stds, tf.float32)
    x_scaled = (x - means) / stds
    x_scaled = tf.cast(x_scaled, tf.float32)
    return x_scaled


# @tf.function(experimental_compile=True, experimental_relax_shapes=True)
def get_model_y_std_scalers(model, _input):
    """
    Re-casts the sklearn output std scalers for each output basis

    :param model: A trained scrinet Neural Network
    :param _input: The point at which you want to scale
    :return:
    """
    n_basis = 8
    std = [model.Y_scalers[i].scale_[0] for i in range(n_basis)]
    std = tf.stack(std, axis=0)
    std = tf.cast(std, tf.float32)
    return std


# @tf.function(experimental_compile=True, experimental_relax_shapes=True)
def get_model_y_mean_scalers(model, _input):
    """
    Re-casts the sklearn output mean scalers for each output basis

    :param model: A trained scrinet Neural Network
    :param _input: The point at which you want to scale
    :return:
    """
    n_basis = 8
    mean = [model.Y_scalers[i].mean_[0] for i in range(n_basis)]
    mean = tf.stack(mean, axis=0)
    mean = tf.cast(mean, tf.float32)
    return mean


# @tf.function(experimental_compile=True, experimental_relax_shapes=True)
def y_inv_scale_hack(model, _input):
    """
    Re-creates the sklearn inverse standard scaler as a tensorflow function,

    :param model: A trained scrinet Neural Network
    :param _input: The point at which you want to scale
    :return:
    """
    y_scaled = _input

    mean = get_model_y_mean_scalers(model, _input)

    std = get_model_y_std_scalers(model, _input)
    y = y_scaled * std + mean
    return y


# @tf.function(experimental_compile=True, experimental_relax_shapes=True)


def get_model_y_minmax_scale_scalers(model, _input):
    """
    Re-casts the sklearn output scale scalers for each output basis

    :param model: A trained scrinet Neural Network
    :param _input: The point at which you want to scale
    :return:
    """
    # I think this is always the same
    n_basis = 8
    scale = [model.Y_scalers[i].scale_[0] for i in range(n_basis)]
    scale = tf.stack(scale, axis=0)
    scale = tf.cast(scale, tf.float32)
    return scale


# @tf.function(experimental_compile=True, experimental_relax_shapes=True)
def get_model_y_minmax_min_scalers(model, _input):
    """
    Re-casts the sklearn output min scalers for each output basis

    :param model: A trained scrinet Neural Network
    :param _input: The point at which you want to scale
    :return:
    """
    # I think this is always the same
    n_basis = 8
    mins = [model.Y_scalers[i].min_[0] for i in range(n_basis)]
    mins = tf.stack(mins, axis=0)
    mins = tf.cast(mins, tf.float32)
    return mins


# @tf.function(experimental_compile=True, experimental_relax_shapes=True)
def y_inv_minmax_scale_hack(model, _input):
    """
    Re-creates the sklearn inverse standard scaler as a tensorflow function,

    :param model: A trained scrinet Neural Network
    :param _input: The point at which you want to scale
    :return:
    """
    y_scaled = _input
    mins = get_model_y_minmax_min_scalers(model, _input)
    scale = get_model_y_minmax_scale_scalers(model, _input)
    y = (y_scaled - mins) / scale
    return y


# we need a function to tell us the time before merger for a particular frequency
# we can estimate this using PN
# from https://github.com/gwastro/pycbc/blob/master/pycbc/waveform/spa_tmplt.py
# non-spinning only
# removed the 'porder' and hardcoding max-order
# @tf.function(experimental_relax_shapes=True)
# @tf.function()


def tf_findchirp_chirptime(m1, m2, fLower):
    # variables used to compute chirp time
    m = m1 + m2
    eta = m1 * m2 / m / m
    c0T = c2T = c3T = c4T = c5T = c6T = c6LogT = c7T = 0.

    c7T = lal.PI * (14809.0 * eta * eta / 378.0 - 75703.0 *
                    eta / 756.0 - 15419335.0 / 127008.0)

    c6T = lal.GAMMA * 6848.0 / 105.0 - 10052469856691.0 / 23471078400.0 + \
          lal.PI * lal.PI * 128.0 / 3.0 + \
          eta * (3147553127.0 / 3048192.0 - lal.PI * lal.PI * 451.0 / 12.0) - \
          eta * eta * 15211.0 / 1728.0 + eta * eta * eta * 25565.0 / 1296.0 + \
          eta * eta * eta * 25565.0 / 1296.0 + tf.math.log(4.0) * 6848.0 / 105.0
    c6LogT = 6848.0 / 105.0

    c5T = 13.0 * lal.PI * eta / 3.0 - 7729.0 * lal.PI / 252.0

    c4T = 3058673.0 / 508032.0 + eta * (5429.0 / 504.0 + eta * 617.0 / 72.0)
    c3T = -32.0 * lal.PI / 5.0
    c2T = 743.0 / 252.0 + eta * 11.0 / 3.0
    c0T = 5.0 * m * lal.MTSUN_SI / (256.0 * eta)

    # This is the PN parameter v evaluated at the lower freq. cutoff
    xT = tf.pow(lal.PI * m * lal.MTSUN_SI * fLower, 1.0 / 3.0)
    x2T = xT * xT
    x3T = xT * x2T
    x4T = x2T * x2T
    x5T = x2T * x3T
    x6T = x3T * x3T
    x7T = x3T * x4T
    x8T = x4T * x4T

    # Computes the chirp time as tC = t(v_low)
    # tC = t(v_low) - t(v_upper) would be more
    # correct, but the difference is negligble.

    # This formula works for any PN order, because
    # higher order coeffs will be set to zero.
    return c0T * (1 + c2T * x2T + c3T * x3T + c4T * x4T + c5T * x5T + (
            c6T + c6LogT * tf.math.log(xT)) * x6T + c7T * x7T) / x8T


# @tf.function(experimental_compile=True)
# @tf.function()


def tf_chieffective(m1, m2, s1z, s2z):
    """
    https://git.ligo.org/lscsoft/lalsuite/-/blob/master/lalsimulation/lib/LALSimInspiralTaylorF2ReducedSpin.c#L46
    /* sanity checks */
    if (m1 <= 0) XLAL_ERROR(XLAL_EDOM);
    if (m2 <= 0) XLAL_ERROR(XLAL_EDOM);
    if (fabs(s1z) > 1) XLAL_ERROR(XLAL_EDOM);
    if (fabs(s2z) > 1) XLAL_ERROR(XLAL_EDOM);
    """
    m = m1 + m2
    eta = m1 * m2 / (m * m)
    delta = (m1 - m2) / m
    chi_s = (s1z + s2z) / 2.
    chi_a = (s1z - s2z) / 2.

    return chi_s * (1. - 76. * eta / 113.) + delta * chi_a


# @tf.function(experimental_compile=True)
# @tf.function()


def tf_XLALSimInspiralTaylorF2ReducedSpinChirpTime(
        m1,  # /**< mass of companion 1 (Msun) */
        m2,  # /**< mass of companion 2 (Msun) */
        chi,  # /**< dimensionless aligned-spin param */
        fStart  # /**< start GW frequency (Hz) */
):
    """
    https://git.ligo.org/lscsoft/lalsuite/-/blob/master/lalsimulation/lib/LALSimInspiralTaylorF2ReducedSpin.c#L307
#     if (fStart <= 0) XLAL_ERROR(XLAL_EDOM);
#     if (m1_SI <= 0) XLAL_ERROR(XLAL_EDOM);
#     if (m2_SI <= 0) XLAL_ERROR(XLAL_EDOM);
#     if (fabs(chi) > 1) XLAL_ERROR(XLAL_EDOM);


    returns tau (chirp time in seconds)

    """
    m = m1 + m2
    eta = m1 * m2 / (m * m)
    eta2 = eta * eta
    chi2 = chi * chi
    sigma0 = (-12769 * (-81. + 4. * eta)) / (16. * (-113. + 76. * eta) * (-113. + 76. * eta))
    gamma0 = (565 * (-146597. + 135856. * eta + 17136. * eta2)) / \
             (2268. * (-113. + 76. * eta))

    #     https://git.ligo.org/lscsoft/lalsuite/-/blob/master/lalsimulation/lib/LALSimInspiralTaylorF2ReducedSpin.c#L31
    # # this is PI**2
    Pi_p2 = 9.8696044010893586188344909998761511

    v = tf.pow(lal.PI * m * lal.MTSUN_SI * fStart, 1. / 3.)
    vk = v  # /* v^k */
    #     REAL8 tk[8];  /* chirp time coefficients up to 3.5 PN */
    #     /* chirp time coefficients up to 3.5PN  */
    tk0 = (5. * m * lal.MTSUN_SI) / (256. * tf.pow(v, 8) * eta)
    tk1 = 0.
    tk2 = 2.9484126984126986 + (11 * eta) / 3.
    tk3 = (-32 * lal.PI) / 5. + (226. * chi) / 15.
    tk4 = 6.020630590199042 - 2 * sigma0 * chi2 + (5429 * eta) / 504. + (617 * eta2) / 72.
    tk5 = (3 * gamma0 * chi) / 5. - (7729 * lal.PI) / 252. + (13 * lal.PI * eta) / 3.
    tk6 = -428.291776175525 + (128 * Pi_p2) / 3. + (6848 * lal.GAMMA) / 105. + (3147553127 * eta) / 3.048192e6 - (
            451 * Pi_p2 * eta) / 12. - (15211 * eta2) / 1728. + (25565 * eta2 * eta) / 1296. + (
                  6848 * tf.math.log(4 * v)) / 105.
    tk7 = (-15419335 * lal.PI) / 127008. - (75703 * lal.PI * eta) / \
          756. + (14809 * lal.PI * eta2) / 378.

    vk2 = vk * v
    vk3 = vk2 * v
    vk4 = vk3 * v
    vk5 = vk4 * v
    vk6 = vk5 * v
    vk7 = vk6 * v

    tau = tk0 * (1 + tk2 * vk2 + tk3 * vk3 + tk4 * vk4 + tk5 * vk5 + tk6 * vk6 + tk7 * vk7)

    return tau


# @tf.function(experimental_compile=True)
# @tf.function()


def tf_get_surrogate_index_and_value_at_f_lower(m1, m2, s1z, s2z, flower):
    """
    returns the first index above the input flower
    and the value at that index
    """
    #     time_at_flower_sec = -tf_findchirp_chirptime(m1,m2,flower)
    chi = tf_chieffective(m1, m2, s1z, s2z)
    time_at_flower_sec = - \
        tf_XLALSimInspiralTaylorF2ReducedSpinChirpTime(m1, m2, chi, flower)
    time_at_flower_M = tf.cast(phenom.StoM(
        time_at_flower_sec, m1 + m2), tf.float64)
    # hardcoded to the final ann-sur model
    tstart_M = tf.cast(-20000., tf.float64)
    tend_M = 100.
    tnum = 40000

    # comment this out to support XLA compilation
    # tf.debugging.assert_greater_equal(
    #     time_at_flower_M,
    #     tstart_M,
    #     message=f"error: flower too low. flower = {flower}. time_at_flower_M = {time_at_flower_M}"
    # )

    surrogate_times = tf.linspace(tstart_M, tend_M, tnum)
    dt_M = surrogate_times[1] - surrogate_times[0]

    # Todo need to think about time, *0 below is bad
    target_indexs = tf.cast(
        tf.floor((20000. + time_at_flower_M) / dt_M), tf.int32)

    target_indexs = tf.clip_by_value(target_indexs,
                                     clip_value_max=tnum - 1,
                                     clip_value_min=0)
    vals = tf.gather(surrogate_times, target_indexs)

    return target_indexs, vals


# @tf.function


def y22_func(theta, phi):
    """
    https://lscsoft.docs.ligo.org/lalsuite/lal/_spherical_harmonics_8c_source.html#l00042
    """
    fac = tf.math.sqrt(5.0 / (64.0 * lal.PI)) * \
          (1.0 + tf.math.cos(theta)) * (1.0 + tf.math.cos(theta))

    m = tf.cast(2., tf.complex64)
    return tf.math.exp(1.j * m * tf.cast(phi, tf.complex64)) * tf.cast(fac, tf.complex64)


# @tf.function


def y2m2_func(theta, phi):
    """
    https://lscsoft.docs.ligo.org/lalsuite/lal/_spherical_harmonics_8c_source.html#l00042
    """
    fac = tf.math.sqrt(5.0 / (64.0 * lal.PI)) * \
          (1.0 - tf.math.cos(theta)) * (1.0 - tf.math.cos(theta))

    m = tf.cast(-2., tf.complex64)
    return tf.math.exp(1.j * m * tf.cast(phi, tf.complex64)) * tf.cast(fac, tf.complex64)


# @tf.function(experimental_compile=True)
# @tf.function()


def make_rect_window_tensor(M, start_end):
    B = []
    for se in start_end:
        B.append(tf.ones(se[1] - se[0]))

    C = [tf.pad(B[i], [[start_end[i][0], M - start_end[i][1]]])
         for i in range(len(start_end))]
    return tf.convert_to_tensor(C)


def apply_roll(tensor_in, shifts):
    """
    tensor_in: input tensor to roll - shape = N,M (N waveforms, M samples in time)
    shifts: tensor - shape = N,
        number of indicies to shift each row by

    returns: the rolled tensor

    """
    rolled = [tf.roll(tensor_in[i], shifts[i], axis=0)
              for i in range(tensor_in.shape[0])]
    return tf.convert_to_tensor(rolled)


# based on generate_surrogate in sample_helpers.py
# @tf.function(experimental_compile=True)
# @tf.function()


def generate_surrogate_hp_hc(
        waveform_params: WaveformParams,
        n_batch,
        f_lower,
        seglen,
        sample_rate,
        amp_model,
        amp_basis,
        phase_model,
        phase_basis
):
    """
    generate hplus and hcross. the shape is NxM
        N = number of waveforms
        M = seglen/samples_rate
    times start at 0s and extend for seglen seconds
    the returned data have the sample sample-rate and duration.
    they also start at the correct start frequency
    so waveforms with different parameters will have different lengths
    n_batch:
    f_lower, : shape = scalar
    seglen, : shape = scalar in seconds - duration of output times
    sample_rate, : shape = scalar in seconds

    :param theta: sphharm polar : shape = N,1
    :param phi: sphharm azimuth : shape = N,1

    :param x: The location in parameter space - currently (q, chi1, chi2) : shape = N,3
    :param amp_model: The pre-loaded amplitude nn generator
    :param amp_basis: The pre-loaded amplitude basis
    :param phase_model: The pre-loaded phase nn generator
    :param phase_basis: The pre-loaded phase basis
    :param phase_shift: phase shift (default: 0.) : shape = N,1

    :return:

    surr_times_sec: times in seconds: shape = (1,)
    hp_rolled: plus pol : shape = (N, M)
    hc_rolled: cross pol : shape = (N, M)
    -start_times: approximate time of merger : shape = (N, 1)


    """

    dt = 1. / sample_rate
    dt_M = phenom.StoM(dt, waveform_params.m_tot)

    # q = tf.transpose(tf.expand_dims(waveform_params.mass_ratio, 0))
    # s1z = tf.transpose(tf.expand_dims(waveform_params.chi_1, 0))
    # s2z = tf.transpose(tf.expand_dims(waveform_params.chi_2, 0))

    q = waveform_params.mass_ratio
    s1z = waveform_params.chi_1
    s2z = waveform_params.chi_2

    m1, m2 = phenom.m1_m2_M_q(waveform_params.m_tot, q)

    x = tf.concat([tf.math.log(waveform_params.mass_ratio),
                   waveform_params.chi_1,
                   waveform_params.chi_2], axis=1)

    x = tf.cast(x, tf.float32)

    amp_alpha = amp_predict_hack(amp_model, x)
    amp = tf.tensordot(amp_alpha, amp_basis, axes=1)
    phase_alpha = phase_predict_hack(phase_model, x)
    phase = tf.tensordot(phase_alpha, phase_basis, axes=1)
    phase_shift = waveform_params.phase_shift
    phase_shift = tf.cast(phase_shift, dtype=tf.float32)
    # phase = phase + phase_shift
    phase = phase
    amp_pre_fac = lalutils.td_amp_scale(waveform_params.m_tot,
                                        waveform_params.distance) * phenom.eta_from_q(q)

    amp_pre_fac = tf.cast(amp_pre_fac, tf.float32)

    amp = amp * amp_pre_fac

    idx, val = tf_get_surrogate_index_and_value_at_f_lower(
        m1, m2, s1z, s2z, f_lower - 5)

    original_idx = idx
    original_val = val  # i think this can be use to estimate the epoch
    val_idx = tf.argmin(idx)[0]
    # TODO is new_idx a constant? No this needs more thinkinf
    new_idx = tf.gather_nd(idx, [[val_idx, 0]])[0]
    # val = tf.cast(tf.gather_nd(val, [[val_idx, 0]])[0],
    #               dtype=tf.float32)
    # val = tf.cast(val[val_idx, 0], dtype=tf.float32)
    # these numbers are specific to the time axis of the surrogate
    x_ref_min = -20000.
    #    x_ref_min = val
    x_ref_max = 100.

    tfdt = tf.cast(dt_M, tf.float64)

    # TODO move all this time conversion stuff to its own function

    num_t_int = tf.cast(seglen / dt, tf.int32)
    num_T = tf.cast(num_t_int, tf.float64)

    times_M = tf.range(num_T) * tfdt - tf.abs(tf.cast(val, tf.float64))
    times_M_f32 = tf.cast(times_M, tf.float32)

    # x_ref_min = val * tf.ones(n_batch)
    x_ref_min = x_ref_min * tf.ones(n_batch)
    x_ref_max = x_ref_max * tf.ones(n_batch)

    # y_ref_gather =tf.stack(tf.gather_nd(amp, [:,new_idx:]))
    y_ref = tf.stack((amp, phase))
    # y_ref = tf.stack((amp[:, new_idx:], phase[:, new_idx:]))
    #
    # TODO Need to check if this actually produces the right waveform
    iy = tfp_interp.batch_interp_regular_1d_grid(
        x=times_M_f32,
        x_ref_min=x_ref_min,
        x_ref_max=x_ref_max,
        y_ref=y_ref,
        # y_ref=tf.stack((amp[:, new_idx:], phase[:, new_idx:])),
        #         fill_value=0 # comment this line out to work with tf.function.... not sure why....
    )

    new_amp = iy[0]
    new_phase = iy[1]

    phase = tf.cast(new_phase, tf.complex64)
    amp = tf.cast(new_amp, tf.complex64)

    theta = tf.cast(waveform_params.theta, tf.float32)
    phi = tf.cast(waveform_params.phi, tf.float32)

    h22 = amp * tf.math.exp(-1.j * phase)

    y22 = y22_func(theta, phi)
    y2m2 = y2m2_func(theta, phi)

    h = h22 * y22 + tf.math.conj(h22) * y2m2

    hplus = tf.math.real(h)
    hcross = tf.math.imag(h)

    surr_times_sec = phenom.MtoS(
        times_M,
        tf.cast(waveform_params.m_tot, tf.float64)
    )

    # negative becuase these times start at negative values
    epochs = -surr_times_sec[:, 0][:, tf.newaxis]
    surr_times_sec = surr_times_sec + epochs

    # finally here lets pad to the desired seglen
    # right now all waveforms have the same shape and sample-rate
    # so padding to desired seglen should be easy
    start_times = phenom.MtoS(original_val, tf.cast(waveform_params.m_tot,
                                                    tf.float64))
    epochs = tf.cast(epochs, tf.float64)
    dt = tf.cast(dt, tf.float64)

    extra_time = phenom.MtoS(150, tf.cast(waveform_params.m_tot, tf.float64))

    index_start_freq = tf.cast((epochs + start_times) / dt, tf.int32)

    index_peak_amp = tf.cast((epochs + extra_time) / dt, tf.int32)
    # need to work out a better way to estimate extra_time, should be related to hz
    # current implementation will be a problem for v high masses
    index_start_freq_buffer = tf.cast((epochs + start_times + 3 * extra_time) / dt, tf.int32)
    # ab = tf.transpose((index_start_freq_buffer, index_peak_amp))[0]
    ab = tf.transpose((index_start_freq, index_peak_amp))[0]
    # Can't XLA compile function below, only this one left
    window_zeros = tf.zeros((n_batch, num_t_int))
    # window = make_rect_window_tensor(num_t_int, [ab[0, i] for i in range(n_batch)])
    # window_ones = tf.ones((n_batch, num_t_int))

    ar = tf.range(num_t_int)
    cond = (ar >= ab[0][0]) & (ar < ab[0][1])
    window = tf.where(tf.math.logical_not(cond), window_zeros[0], 1.0)
    window = tf.reshape(window, (1, num_t_int))

    for i in range(1, n_batch):
        ar = tf.range(num_t_int)
        cond = (ar >= ab[i][0]) & (ar < ab[i][1])
        # cond = tf.math.logical_not(cond)
        window_next_bach = tf.where(tf.math.logical_not(cond), window_zeros[i], 1.0)
        window_next_bach = tf.reshape(window_next_bach, (1, num_t_int))

        window = tf.concat([window, window_next_bach], axis=0)

    cd = tf.transpose((index_start_freq,
                       index_start_freq_buffer))[0]
    cond_taper = (ar >= cd[0][0]) & (ar < cd[0][1])
    taper_ones = tf.ones((n_batch,
                           num_t_int))

    taper_len = tf.linspace(0., np.pi/2, num_t_int)
    P = tf.cast(num_t_int/index_start_freq_buffer[0][0], tf.float32)
    taper = tf.math.sin(P * taper_len) ** 2
    left_window = tf.where(tf.math.logical_not(cond_taper),
                           taper_ones[0],
                           taper)

    left_window = tf.reshape(left_window, (1, num_t_int))

    for i in range(1, n_batch):
        cond_taper = (ar >= cd[i][0]) & (ar < cd[i][1])
        P = tf.cast(num_t_int/index_start_freq_buffer[i][0], tf.float32)
        taper = tf.math.sin(P * taper_len) ** 2
        taper_next_batch = tf.where(tf.math.logical_not(cond_taper),
                               taper_ones[i],
                               taper)

        taper_next_batch = tf.reshape(taper_next_batch, (1, num_t_int))
        left_window = tf.concat([left_window, taper_next_batch], axis=0)

    # print(left_window)
    # test that window agrees with original implemtation
    # window = 1,
    # return amp
    # # uncomment this if you want to start the timeseries at 0
    # # otherwise below we roll such that the timeseries starts at the peak
    # #     hp_rolled = apply_roll(hplus*window, -tf.reshape(index_start_freq, (N,)))
    # #     hc_rolled = apply_roll(hcross*window, -tf.reshape(index_start_freq, (N,)))
    #
    index_peak_amp = tf.cast((epochs) / dt, tf.int32)

    hp_rolled = apply_roll(hplus * window * left_window, -tf.reshape(index_peak_amp, (n_batch,)))
    hc_rolled = apply_roll(hcross * window * left_window, -tf.reshape(index_peak_amp, (n_batch,)))

    # if we want to taper

    return surr_times_sec[0], hp_rolled, hc_rolled, -start_times


def make_detector_waveform_from_polarisations(detector,
                                              h_plus,
                                              h_cross,
                                              detector_params,
                                              n_batch,
                                              delta_t):
    """
    https://git.ligo.org/lscsoft/bilby/-/blob/master/bilby/gw/detector/interferometer.py
    get_detector_response

    :param detector:
    :param h_plus:
    :param h_cross:
    :param detector_params:
    :param delta_t
    :return:
    """
    ra = detector_params.ra
    dec = detector_params.dec
    psi = detector_params.psi
    time = detector_params.time

    num_waveforms = n_batch

    det_plus_response = tf.cast(tf_get_antenna_response(detector, ra, dec, time, psi, 'plus'), tf.float32)
    det_cross_response = tf.cast(tf_get_antenna_response(detector, ra, dec, time, psi, 'cross'), tf.float32)

    det_plus_response = tf.reshape(det_plus_response, (num_waveforms, 1))
    det_cross_response = tf.reshape(det_cross_response, (num_waveforms, 1))

    detector_h = h_plus * det_plus_response + h_cross * det_cross_response

    time_shift = ut.tf_time_delay_geocentric(detector_vertex[detector],
                                             tf.zeros((1,
                                                       3)),
                                             ra,
                                             dec,
                                             time)[0]

    # # Be careful to first subtract the two GPS times which are ~1e9 sec.
    # # And then add the time_shift which varies at ~1e-5 sec
    # # may be a hack below
    strain_data_start_time = 0.
    dt_geocent = time - strain_data_start_time
    dt = tf.cast(dt_geocent, tf.complex64) + tf.cast(time_shift, tf.complex64)

    detector_h_ts = ts.TimeSeries(detector_h,
                                  delta_t=delta_t)

    # TODO, need to check this is actually resolved
    detector_h_fs = detector_h_ts.to_frequencyseries()

    freqs = detector_h_fs.get_sample_frequencies()
    freqs = tf.cast(freqs, tf.complex64)
    fac = tf.math.exp(-1j * 2 * np.pi * dt * freqs)
    #
    detector_h_fs.data = detector_h_fs.data * fac

    #
    detector_h_ts = ts.TimeSeries(tf.math.real(detector_h_fs.to_timeseries().data), delta_t=delta_t)
    #
    return detector_h_ts.data


def tf_generate_surrogate_at_detector(waveform_params,
                                      detector_params,
                                      n_batch,
                                      f_lower,
                                      seglen,
                                      sample_rate,
                                      amp_model,
                                      amp_basis,
                                      phase_model,
                                      phase_basis,
                                      detector='H1'):
    """
    # Todo add docs
    :param params:
    :param amp_model:
    :param amp_basis:
    :param phase_model:
    :param phase_basis:
    :param detector:
    :return:
    """
    #         phase_shift=phase_shift)
    surr_times_sec, hplus, hcross, unrolled_peak_time = generate_surrogate_hp_hc(
        waveform_params=waveform_params,
        n_batch=n_batch,
        f_lower=f_lower,
        seglen=seglen,
        sample_rate=sample_rate,
        amp_model=amp_model,
        amp_basis=amp_basis,
        phase_model=phase_model,
        phase_basis=phase_basis
    )

    delta_t = surr_times_sec[1] - surr_times_sec[0]
    # return hplus, hcross
    hplus = ts.TimeSeries(hplus, delta_t=delta_t)
    hcross = ts.TimeSeries(hcross, delta_t=delta_t)
    # return hplus.data, hcross.data
    det_wvf = make_detector_waveform_from_polarisations(detector=detector,
                                                        h_plus=hplus.data,
                                                        h_cross=hcross.data,
                                                        detector_params=detector_params,
                                                        n_batch=n_batch,
                                                        delta_t=delta_t)
    #
    # # TODO returning a ts class and not a tensor may be problematic
    return det_wvf


def convert_tfp_chains_to_arviz_object(chains, param_names, varying_param_names=None):
    """
    Changes the output from sampling into an arviz object, this makes it easier to perform diagnostics
    and plots using arviz

    :param chains: The raw output from the tfp sampler
    :param param_names:

    :return:
    """
    if not varying_param_names:
        varying_param_names = param_names
    param_scalers = GwParamScalers()._asdict()

    samples_ar = np.array(chains.numpy())
    samples_right_shape = np.swapaxes(samples_ar, 0, 1)
    samples_dict = {key: param_scalers[key] * samples_right_shape[:, :, param_names.index(key)] for key in
                    varying_param_names}
    arv_samples = az.from_dict(samples_dict)
    return arv_samples


@tf.function()
def elbo_loss():
    q_samples = distribution.sample((256,))
    return -tf.reduce_mean(
        target_log_prob_fn(q_samples) - distribution.log_prob(q_samples)
    )


def make_mcmc_kernel_fn(target_log_prob_fn):
    return tfp.mcmc.RandomWalkMetropolis(
        target_log_prob_fn=target_log_prob_fn,
        new_state_fn=tfp.mcmc.random_walk_normal_fn(
            scale=step_size,
        ),
    )


def make_hmc_kernel_fn(target_log_prob_fn):
    return tfp.mcmc.HamiltonianMonteCarlo(
        target_log_prob_fn=target_log_prob_fn, step_size=step_size, num_leapfrog_steps=3
    )

# CODE TO TRAIN NEUTRA-LIKE BIJECTOR, MOVING HERE FOR NOW BUT NEED TO TURN INTO FUNCTION
# made = tfb.AutoregressiveNetwork(
#     params=2,
#     hidden_units=[
#         512,
#         512,
#         512,
#         512,
#     ],
#     activation="tanh",
#     dtype=tf.float64,
# )
#
# distribution = tfd.TransformedDistribution(
#     distribution=tfd.MultivariateNormalDiag(tf.zeros_like(p0[0]), tf.ones_like(p0[0])),
#     bijector=tfb.Chain([constraints, tfb.MaskedAutoregressiveFlow(made)]),
# )
#
# optimiser = tf.optimizers.Adam(lr=0.0001, amsgrad=True, clipnorm=0.0001)
#
# print("starting network training")
# starttime = datetime.datetime.now()
# n_training_steps = 5 * 10 ** 2
# losses = []
#
# for i in range(n_training_steps):
#     optimiser.minimise(elbo_loss, distribution.trainable_variables)
#     loss = elbo_loss()
#     losses.append(loss)
#     if i % 200 == 0:
#         print(f" finishing step {i}, loss = {np.mean(losses[-20:])}")
#     if np.isnan(loss):
#         raise ValueError
#
# endtime = datetime.datetime.now()
# duration = endtime - starttime
# print("Training complete")
# print(f"Training duration: {duration}")
#
# plt.figure(figsize=(14, 6))
# plt.plot(losses)
# # plt.yscale('log')
# plt.ylabel("loss")
# plt.xlabel("num training steps")
# plt.savefig(f"{image_dir}VI/bijector_loss.png")
# plt.close()
#
# smp = distribution.sample((5 * 10 ** 3, num_chains))
#
# vi_data = sample_helpers.convert_tfp_chains_to_arviz_object(
#     smp, param_names
# )
#
# print('VI summary')
# print(az.summary(vi_data))
# plt.figure()
# az.plot_pair(vi_data,
#              var_names=param_names,
#              kind='kde',
#              contour=True,
#              marginals=True)
#
# plt.savefig(f"{image_dir}VI/tmp_corner.png")
# plt.close()
#
# plt.figure()
# az.plot_posterior(vi_data,
#                   hdi_prob=0.9)
#
# plt.savefig(f"{image_dir}VI/post.png")
# plt.close()
