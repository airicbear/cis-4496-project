import tensorflow as tf

from .consts import strategy
from .discriminator import discriminator
from .generator import Generator
from .losses import generator_loss, discriminator_loss, calc_cycle_loss, identity_loss
from .model import CycleGan

monet_generator = Generator()
photo_generator = Generator()
monet_discriminator = discriminator()
photo_discriminator = discriminator()

cycle_gan_model = CycleGan(monet_generator=monet_generator,
                           photo_generator=photo_generator,
                           monet_discriminator=monet_discriminator,
                           photo_discriminator=photo_discriminator)


def cycle_gan_compile(monet_generator_optimizer: tf.keras.optimizers.Optimizer,
                      photo_generator_optimizer: tf.keras.optimizers.Optimizer,
                      monet_discriminator_optimizer: tf.keras.optimizers.Optimizer,
                      photo_discriminator_optimizer: tf.keras.optimizers.Optimizer) -> None:
    cycle_gan_model.compile(
        monet_generator_optimizer=monet_generator_optimizer,
        photo_generator_optimizer=photo_generator_optimizer,
        monet_discriminator_optimizer=monet_discriminator_optimizer,
        photo_discriminator_optimizer=photo_discriminator_optimizer,
        generator_loss_fn=generator_loss,
        discriminator_loss_fn=discriminator_loss,
        cycle_loss_fn=calc_cycle_loss,
        identity_loss_fn=identity_loss,
    )


def cycle_gan_compile_with_loss_rate(loss_rate: float) -> None:
    with strategy.scope():
        monet_generator_optimizer = tf.keras.optimizers.Adam(loss_rate, beta_1=0.5)
        photo_generator_optimizer = tf.keras.optimizers.Adam(loss_rate, beta_1=0.5)
        monet_discriminator_optimizer = tf.keras.optimizers.Adam(loss_rate, beta_1=0.5)
        photo_discriminator_optimizer = tf.keras.optimizers.Adam(loss_rate, beta_1=0.5)

        cycle_gan_compile(monet_generator_optimizer,
                          photo_generator_optimizer,
                          monet_discriminator_optimizer,
                          photo_discriminator_optimizer)
