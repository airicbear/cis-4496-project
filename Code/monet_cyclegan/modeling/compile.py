import logging

import tensorflow as tf

from .losses import generator_loss, discriminator_loss, calc_cycle_loss, identity_loss
from .model import CycleGan
from ..consts import strategy

logger = logging.getLogger(__name__)


def cyclegan_compile(cyclegan_model: CycleGan,
                     monet_generator_optimizer: tf.keras.optimizers.Optimizer,
                     photo_generator_optimizer: tf.keras.optimizers.Optimizer,
                     monet_discriminator_optimizer: tf.keras.optimizers.Optimizer,
                     photo_discriminator_optimizer: tf.keras.optimizers.Optimizer) -> None:
    """Compile a CycleGAN with generator optimizers and discriminator optimizers.

    Args:
        cyclegan_model: The CycleGAN model to be compiled.
        monet_generator_optimizer: The optimizer for the Monet painting generator.
        photo_generator_optimizer: The optimizer for the photo generator.
        monet_discriminator_optimizer: The optimizer for the Monet painting discriminator.
        photo_discriminator_optimizer: The optimizer for the photo discriminator.
    """

    cyclegan_model.compile(
        monet_generator_optimizer=monet_generator_optimizer,
        photo_generator_optimizer=photo_generator_optimizer,
        monet_discriminator_optimizer=monet_discriminator_optimizer,
        photo_discriminator_optimizer=photo_discriminator_optimizer,
        generator_loss_fn=generator_loss,
        discriminator_loss_fn=discriminator_loss,
        cycle_loss_fn=calc_cycle_loss,
        identity_loss_fn=identity_loss,
    )


def cyclegan_compile_with_loss_rate(cyclegan_model: CycleGan,
                                    loss_rate: float) -> None:
    """Compile a CycleGAN with a given loss rate.

    Args:
        cyclegan_model: The CycleGAN to be compiled.
        loss_rate: The loss rate to be used by the CycleGAN optimizers.
    """

    logger.info(f'Compiling model using a loss rate of {loss_rate}.')

    with strategy.scope():
        monet_generator_optimizer = tf.keras.optimizers.Adam(loss_rate, beta_1=0.5)
        photo_generator_optimizer = tf.keras.optimizers.Adam(loss_rate, beta_1=0.5)
        monet_discriminator_optimizer = tf.keras.optimizers.Adam(loss_rate, beta_1=0.5)
        photo_discriminator_optimizer = tf.keras.optimizers.Adam(loss_rate, beta_1=0.5)

        cyclegan_compile(cyclegan_model,
                         monet_generator_optimizer,
                         photo_generator_optimizer,
                         monet_discriminator_optimizer,
                         photo_discriminator_optimizer)
