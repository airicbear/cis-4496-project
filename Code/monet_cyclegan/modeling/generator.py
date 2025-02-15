from typing import List, Tuple

import tensorflow as tf

from .layers import downsample, upsample


def generator(output_channels: int = 3) -> tf.keras.Model:
    """
    The Generator applies an encoder-decoder architecture that down-samples the image and then decodes the image
    through various transpose convolutions. It is inspired by a "U-Net" architecture for image generation,
    which down-samples an image and then applies up-sampling.
    However, it keeps the information from the old images through the residual blocks (the Concatenate layer).

    Args:
        output_channels: Number of output channels (default: 3).

    Returns:
        A generator for the CycleGAN.
    """

    down_stack = [
        downsample(name='downsample_1', filters=64, size=4, apply_instancenorm=False),
        downsample(name='downsample_2', filters=128, size=4),
        downsample(name='downsample_3', filters=256, size=4),
        downsample(name='downsample_4', filters=512, size=4),
        downsample(name='downsample_5', filters=512, size=4),
        downsample(name='downsample_6', filters=512, size=4),
        downsample(name='downsample_7', filters=512, size=4),
        downsample(name='downsample_8', filters=512, size=4),
    ]

    up_stack = [
        upsample(name='upsample_1', filters=512, size=4, apply_dropout=True),
        upsample(name='upsample_2', filters=512, size=4, apply_dropout=True),
        upsample(name='upsample_3', filters=512, size=4, apply_dropout=True),
        upsample(name='upsample_4', filters=512, size=4),
        upsample(name='upsample_5', filters=256, size=4),
        upsample(name='upsample_6', filters=128, size=4),
        upsample(name='upsample_7', filters=64, size=4),
    ]

    initializer = tf.random_normal_initializer(0., 0.02)

    inputs = tf.keras.layers.Input(shape=[256, 256, 3])
    x = inputs

    skips: List[tf.keras.Sequential] = []
    for down in down_stack:
        x = down(x)
        skips.append(x)

    skips = list(reversed(skips[:-1]))

    for up, skip in zip(up_stack, skips):
        x = up(x)
        x = tf.keras.layers.Concatenate()([x, skip])

    x = tf.keras.layers.Conv2DTranspose(output_channels,
                                        4,
                                        strides=2,
                                        padding='same',
                                        kernel_initializer=initializer,
                                        activation='tanh')(x)

    return tf.keras.Model(inputs=inputs, outputs=x)
