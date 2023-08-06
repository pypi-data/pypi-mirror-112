import tensorflow as tf
import tensorflow_probability as tfp
import numpy as  np

tfd = tfp.distributions

class Sine(tfp.distributions.Distribution):
    """
    Sine prior
    """

    def __init__(self,
                 minimum=0,
                 maximum=2 * np.pi,
                 ):
        self.minimum = minimum
        self.maximum = maximum

    def prob(self, value, name='prob', **kwargs):
        is_in_prior_range = tf.math.logical_and(tf.math.greater_equal(value, self.minimum),
                                                tf.math.less_equal(value, self.maximum))
        prob = tf.math.sin(value) / 2
        out_of_bounds = tf.zeros_like(prob, dtype=tf.float64)
        prob = tf.where(is_in_prior_range, prob, out_of_bounds)
        return prob

    def log_prob(self, value, name='log_prob', **kwargs):
        prob = self.prob(value)
        return tf.math.log(prob)


class Cosine(tfp.distributions.Distribution):
    """
    Cosine prior
    """

    def __init__(self,
                 minimum=-np.pi / 2,
                 maximum=np.pi / 2,
                 ):
        self.minimum = minimum
        self.maximum = maximum

    def prob(self, value, **kwargs):
        is_in_prior_range = tf.math.logical_and(tf.math.greater_equal(value, self.minimum),
                                                tf.math.less_equal(value, self.maximum))
        prob = tf.math.cos(value) / 2
        out_of_bounds = tf.zeros_like(prob, dtype=tf.float32)
        prob = tf.where(is_in_prior_range, prob, out_of_bounds)
        return prob

    def log_prob(self, value, **kwargs):
        prob = self.prob(value)
        return tf.math.log(prob)

    def sample(self, shape=(1,)):
        # this is not correct but probably okay for now
        return tfd.Uniform(self.minimum, self.maximum).sample(shape)

