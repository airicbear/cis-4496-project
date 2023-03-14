import tensorflow as tf
from tensorflow_addons.layers import InstanceNormalization

from .layers import downsample


def discriminator() -> tf.keras.Model:
    """
    This is the function to create the Discriminator model for our CycleGAN model.
    First, the input images are down-sampled three times and zero-padded.
    Then, a 2D Convolutional Neural Network with stride 1 is applied to the inputs.
    From there, we apply Instance Normalization with a gamma initializer on the convolution.
    Leaky ReLU is applied to the normalization, and another zero-padding is performed.
    Next, the outputs are created from this with another 2D Convolutional Neural Network with stride 1.
    Finally, the Discriminator model is created and returned with the input and outputs as parameters.

    :return: Discriminator model with the inputs and outputs as parameters
    """

    initializer = tf.random_normal_initializer(0., 0.02)
    gamma_init = tf.keras.initializers.RandomNormal(mean=0.0, stddev=0.02)

    inputs = tf.keras.layers.Input(shape=[256, 256, 3], name='input_image')

    x = inputs
    down1 = downsample(name='downsample_1', filters=64, size=4, apply_instancenorm=False)(x)
    down2 = downsample(name='downsample_2', filters=128, size=4)(down1)
    down3 = downsample(name='downsample_3', filters=256, size=4)(down2)
    zero_pad1 = tf.keras.layers.ZeroPadding2D()(down3)
    conv = tf.keras.layers.Conv2D(512, 4, strides=1, kernel_initializer=initializer, use_bias=False)(zero_pad1)
    norm1 = InstanceNormalization(gamma_initializer=gamma_init)(conv)
    leaky_relu = tf.keras.layers.LeakyReLU()(norm1)
    zero_pad2 = tf.keras.layers.ZeroPadding2D()(leaky_relu)
    outputs = tf.keras.layers.Conv2D(1, 4, strides=1, kernel_initializer=initializer)(zero_pad2)

    return tf.keras.Model(inputs=inputs, outputs=outputs)
