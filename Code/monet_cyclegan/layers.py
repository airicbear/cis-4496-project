import tensorflow as tf
from tensorflow_addons.layers import InstanceNormalization

def downsample(filters: int, size: int, apply_instancenorm: bool = True) -> tf.keras.Sequential:
    """
    Down-sampling layer function that gets used in the models
    :param filters: the number of filters
    :param size: the input size
    :param apply_instancenorm: True if it should apply InstanceNormalization to result. False, otherwise. Default, True
    :return: the down-sampled result
    """
    initializer = tf.random_normal_initializer(0., 0.02)
    gamma_init = tf.keras.initializers.RandomNormal(mean=0.0, stddev=0.02)
    
    result = tf.keras.Sequential()
    result.add(tf.keras.layers.Conv2D(filters, size, strides=2, padding='same', kernel_initializer=initializer,
                                      use_bias=False))
    if apply_instancenorm:
        result.add(InstanceNormalization(gamma_initializer=gamma_init))
    result.add(tf.keras.layers.ReLU())

    return result

def upsample(filters: int, size: int, apply_dropout: bool = False) -> tf.keras.Sequential:
    """
    Up-sampling layer function that gets used in the models
    :param filters: the number of filters
    :param size: the input size
    :param apply_dropout: True if it should apply dropout to result
    :return: the up-sampled result
    """
    initializer = tf.random_normal_initializer(0., 0.02)
    gamma_init = tf.keras.initializers.RandomNormal(mean=0.0, stddev=0.02)

    result = tf.keras.Sequential()
    result.add(tf.keras.layers.Conv2DTranspose(filters, size, strides=2, padding='same',
                                               kernel_initializer=initializer, use_bias=False))
    result.add(InstanceNormalization(gamma_initializer=gamma_init))
    if apply_dropout:
        result.add(tf.keras.layers.Dropout(0.5))
    result.add(tf.keras.layers.ReLU())

    return result
