import tensorflow as tf

from .discriminator import Discriminator
from .generator import Generator
from .model import CycleGan


def create_model() -> CycleGan:
    """
    The configured model. This is where the loss functions and optimizers are defined.
    :return: the CycleGAN model
    """
    try:
        tpu = tf.distribute.cluster_resolver.TPUClusterResolver()
        tf.config.experimental_connect_to_cluster(tpu)
        tf.tpu.experimental.initialize_tpu_system(tpu)
        strategy = tf.distribute.experimental.TPUStrategy(tpu)
    except:
        strategy = tf.distribute.get_strategy()

    with strategy.scope():
        def discriminator_loss(real: tf.keras.Model, generated: tf.keras.Model) -> tf.Tensor:
            """
            sub-function for the discriminator loss, which is the loss metric for the discriminator models
            :param real: the real/actual item
            :param generated: the generated/fake item
            :return: the discriminator loss
            """
            real_loss = tf.keras.losses.BinaryCrossentropy(from_logits=True,
                                                           reduction=tf.keras.losses.Reduction.NONE)(tf.ones_like(real),
                                                                                                     real)
            generated_loss = tf.keras.losses.BinaryCrossentropy(from_logits=True,
                                                                reduction=tf.keras.losses.Reduction.NONE)(
                tf.zeros_like(generated), generated)
            total_discriminator_loss = real_loss + generated_loss
            return total_discriminator_loss * 0.5

        def generator_loss(generated: tf.keras.Model) -> tf.Tensor:
            """
            sub-function for the generator loss, which is the loss metric for the generator models
            :param generated: the generated/fake item
            :return: the generator loss (binary cross entropy)
            """
            return tf.keras.losses.BinaryCrossentropy(from_logits=True, reduction=tf.keras.losses.Reduction.NONE)(
                tf.ones_like(generated), generated)

        def calc_cycle_loss(real_image: tf.Tensor, cycled_image: tf.Tensor, LAMBDA: float) -> tf.Tensor:
            """
            sub-function to calculate the cycle loss.
            This helps to verify whether the result is close to the original input.
            :param real_image: the real image
            :param cycled_image: the image after being cycled
            :param LAMBDA: the lambda value to be multiplied by the loss value
            :return: the calculated cycle loss
            """
            loss1 = tf.reduce_mean(tf.abs(real_image - cycled_image))
            return LAMBDA * loss1

        def identity_loss(real_image: tf.Tensor, same_image: tf.Tensor, LAMBDA: float) -> tf.Tensor:
            """
            sub-function to calculate the identity loss, which says that, if you feed the image to the generator,
             it should yield the real image or something close to the image.
            :param real_image: the real image
            :param same_image: the image tht should be close to the real image
            :param LAMBDA: the lambda value to be multiplied by the loss value
            :return:the calculated identity loss
            """
            loss = tf.reduce_mean(tf.abs(real_image - same_image))
            return LAMBDA * 0.5 * loss

        photo_generator_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)
        monet_generator_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)
        monet_discriminator_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)
        photo_discriminator_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)

        monet_generator = Generator()
        photo_generator = Generator()
        monet_discriminator = Discriminator()
        photo_discriminator = Discriminator()

        cycle_gan_model = CycleGan(monet_generator, photo_generator, monet_discriminator, photo_discriminator)
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

        return cycle_gan_model
