import tensorflow as tf
from tensorflow_addons.layers import InstanceNormalization


def downsample(name: str, filters: int, size: int, apply_instancenorm: bool = True) -> tf.keras.Sequential:
    """Down-sampling layer to be included in the models.

    Args:
        name: The name of the layer.
        filters: The number of filters.
        size: The input size.
        apply_instancenorm: True if the model should include an `InstanceNormalization` layer before activation.

    Returns:
        The down-sampling layer.
    """

    initializer = tf.random_normal_initializer(mean=0., stddev=0.02)
    gamma_init = tf.keras.initializers.RandomNormal(mean=0.0, stddev=0.02)

    result = tf.keras.Sequential(name=name)
    result.add(tf.keras.layers.Conv2D(filters=filters,
                                      kernel_size=size,
                                      strides=2,
                                      padding='same',
                                      kernel_initializer=initializer,
                                      use_bias=False))
    if apply_instancenorm:
        result.add(InstanceNormalization(gamma_initializer=gamma_init))
    result.add(tf.keras.layers.ReLU())

    return result


def upsample(name: str, filters: int, size: int, apply_dropout: bool = False) -> tf.keras.Sequential:
    """Up-sampling layer to be included in the models.

    Args:
        name: The name of the layer.
        filters: The number of filters.
        size: The input size.
        apply_dropout: True if the model should include a Dropout layer before activation.

    Returns:
        The up-sampling layer.
    """

    initializer = tf.random_normal_initializer(mean=0., stddev=0.02)
    gamma_init = tf.keras.initializers.RandomNormal(mean=0.0, stddev=0.02)

    result = tf.keras.Sequential(name=name)
    result.add(tf.keras.layers.Conv2DTranspose(filters=filters,
                                               kernel_size=size,
                                               strides=2,
                                               padding='same',
                                               kernel_initializer=initializer,
                                               use_bias=False))
    result.add(InstanceNormalization(gamma_initializer=gamma_init))
    if apply_dropout:
        result.add(tf.keras.layers.Dropout(rate=0.5))
    result.add(tf.keras.layers.ReLU())

    return result
