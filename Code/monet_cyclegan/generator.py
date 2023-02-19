import tensorflow as tf

from .layers import downsample, upsample


def Generator(output_channels: int = 3) -> tf.keras.Model:
    """
    The Generator applies an encoder-decoder architecture that down-samples the image and then decodes the image
    through various transpose convolutions. It is inspired by a "U-Net" architecture for image generation,
    which down-samples an image and then applies up-sampling.
    However, it keeps the information from the old images through the residual blocks (the Concatenate function).
    :param output_channels: default of 3 output channels
    :return: Generator model with the inputs (inputs) and outputs (x) as parameters
    """
    down_stack = [
        downsample(64, 4, apply_instancenorm=False),
        downsample(128, 4),
        downsample(256, 4),
        downsample(512, 4),
        downsample(512, 4),
        downsample(512, 4),
        downsample(512, 4),
        downsample(512, 4),
    ]

    up_stack = [
        upsample(512, 4, apply_dropout=True),
        upsample(512, 4, apply_dropout=True),
        upsample(512, 4, apply_dropout=True),
        upsample(512, 4),
        upsample(256, 4),
        upsample(128, 4),
        upsample(64, 4),
    ]

    initializer = tf.random_normal_initializer(0., 0.02)

    inputs = tf.keras.layers.Input(shape=[256, 256, 3])
    x = inputs

    skips: list[tf.keras.Sequential] = []
    for down in down_stack:
        x = down(x)
        skips.append(x)

    skips = reversed(skips[:-1])

    for up, skip in zip(up_stack, skips):
        x = up(x)
        x = tf.keras.layers.Concatenate()([x, skip])

    x = tf.keras.layers.Conv2DTranspose(output_channels, 4, strides=2, padding='same', kernel_initializer=initializer,
                                        activation='tanh')(x)

    return tf.keras.Model(inputs=inputs, outputs=x)
