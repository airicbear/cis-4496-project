import logging
from abc import ABC
from typing import Callable, Tuple

import tensorflow as tf

logger = logging.getLogger(__name__)


class CycleGan(tf.keras.Model, ABC):
    """The CycleGAN model that initializes and compiles the generators and discriminators."""

    def __init__(self,
                 painting_generator: tf.keras.Model,
                 photo_generator: tf.keras.Model,
                 painting_discriminator: tf.keras.Model,
                 photo_discriminator: tf.keras.Model,
                 lambda_cycle: tf.Tensor = 10):
        """Initialization function for the generators, discriminators, and the lambda cycle.

        Args:
            painting_generator: The painting generator model.
            photo_generator: The photo generator model.
            painting_discriminator: The painting discriminator.
            photo_discriminator: The photo discriminator.
            lambda_cycle: The lambda cycle.
        """

        super(CycleGan, self).__init__()
        self.painting_generator = painting_generator
        self.photo_generator = photo_generator
        self.painting_discriminator = painting_discriminator
        self.photo_discriminator = photo_discriminator
        self.lambda_cycle = lambda_cycle
        self.painting_generator_optimizer: tf.keras.optimizers.Optimizer = None
        self.photo_generator_optimizer: tf.keras.optimizers.Optimizer = None
        self.painting_discriminator_optimizer: tf.keras.optimizers.Optimizer = None
        self.photo_discriminator_optimizer: tf.keras.optimizers.Optimizer = None
        self.generator_loss_fn: Callable[[tf.keras.Model], tf.Tensor] = None
        self.discriminator_loss_fn: Callable[[tf.keras.Model, tf.keras.Model], tf.Tensor] = None
        self.cycle_loss_fn: Callable[[tf.Tensor, tf.Tensor, tf.Tensor], tf.Tensor] = None
        self.identity_loss_fn: Callable[[tf.Tensor, tf.Tensor, tf.Tensor], tf.Tensor] = None

    def compile(self,
                painting_generator_optimizer: tf.keras.optimizers.Optimizer,
                photo_generator_optimizer: tf.keras.optimizers.Optimizer,
                painting_discriminator_optimizer: tf.keras.optimizers.Optimizer,
                photo_discriminator_optimizer: tf.keras.optimizers.Optimizer,
                generator_loss_fn: Callable[[tf.keras.Model], tf.Tensor],
                discriminator_loss_fn: Callable[[tf.keras.Model, tf.keras.Model], tf.Tensor],
                cycle_loss_fn: Callable[[tf.Tensor, tf.Tensor, tf.Tensor], tf.Tensor],
                identity_loss_fn: Callable[[tf.Tensor, tf.Tensor, tf.Tensor], tf.Tensor]):
        """Compiler function that sets the optimizers and the loss functions of the CycleGAN.

        Args:
            painting_generator_optimizer: Optimizer for painting generator model.
            photo_generator_optimizer: Optimizer for photo generator model.
            painting_discriminator_optimizer: Optimizer for painting discriminator model.
            photo_discriminator_optimizer: Optimizer for photo discriminator model.
            generator_loss_fn: Loss function for the generator models.
            discriminator_loss_fn: Loss function for the discriminator models.
            cycle_loss_fn: Cycle consistency loss function.
            identity_loss_fn: Identity loss function.
        """

        super(CycleGan, self).compile()
        self.painting_generator_optimizer = painting_generator_optimizer
        self.photo_generator_optimizer = photo_generator_optimizer
        self.painting_discriminator_optimizer = painting_discriminator_optimizer
        self.photo_discriminator_optimizer = photo_discriminator_optimizer
        self.generator_loss_fn = generator_loss_fn
        self.discriminator_loss_fn = discriminator_loss_fn
        self.cycle_loss_fn = cycle_loss_fn
        self.identity_loss_fn = identity_loss_fn

    @tf.function
    def train_step(self, batch_data: Tuple[tf.Tensor, tf.Tensor]):
        """Main function for training the generators and discriminators as well as determining the corresponding loss.

        Args:
            batch_data: the batch data_acquisition

        Returns:
            The loss metrics for all four models.
        """

        logger.info('Performing train step.')

        real_painting, real_photo = batch_data

        with tf.GradientTape(persistent=True) as tape:
            fake_painting = self.painting_generator(real_photo, training=True)
            cycled_photo = self.photo_generator(fake_painting, training=True)

            fake_photo = self.photo_generator(real_painting, training=True)
            cycled_painting = self.painting_generator(fake_photo, training=True)

            same_painting = self.painting_generator(real_painting, training=True)
            same_photo = self.photo_generator(real_photo, training=True)

            discriminator_real_painting = self.painting_discriminator(real_painting, training=True)
            discriminator_real_photo = self.photo_discriminator(real_photo, training=True)

            discriminator_fake_painting = self.painting_discriminator(fake_painting, training=True)
            discriminator_fake_photo = self.photo_discriminator(fake_photo, training=True)

            painting_generator_loss = self.generator_loss_fn(discriminator_fake_painting)
            photo_generator_loss = self.generator_loss_fn(discriminator_fake_photo)

            painting_cycle_loss = self.cycle_loss_fn(real_painting, cycled_painting, self.lambda_cycle)
            photo_cycle_loss = self.cycle_loss_fn(real_photo, cycled_photo, self.lambda_cycle)
            total_cycle_loss = painting_cycle_loss + photo_cycle_loss

            painting_identity_loss = self.identity_loss_fn(real_painting, same_painting, self.lambda_cycle)
            photo_identity_loss = self.identity_loss_fn(real_photo, same_photo, self.lambda_cycle)

            total_painting_generator_loss = painting_generator_loss + total_cycle_loss + painting_identity_loss
            total_photo_generator_loss = photo_generator_loss + total_cycle_loss + photo_identity_loss

            painting_discriminator_loss = self.discriminator_loss_fn(discriminator_real_painting,
                                                                     discriminator_fake_painting)
            photo_discriminator_loss = self.discriminator_loss_fn(discriminator_real_photo, discriminator_fake_photo)

        painting_generator_gradients = tape.gradient(total_painting_generator_loss,
                                                     self.painting_generator.trainable_variables)
        photo_generator_gradients = tape.gradient(total_photo_generator_loss, self.photo_generator.trainable_variables)

        painting_discriminator_gradients = tape.gradient(painting_discriminator_loss,
                                                         self.painting_discriminator.trainable_variables)
        photo_discriminator_gradients = tape.gradient(photo_discriminator_loss,
                                                      self.photo_discriminator.trainable_variables)

        self.painting_generator_optimizer.apply_gradients(zip(painting_generator_gradients,
                                                              self.painting_generator.trainable_variables))
        self.photo_generator_optimizer.apply_gradients(zip(photo_generator_gradients,
                                                           self.photo_generator.trainable_variables))

        self.painting_discriminator_optimizer.apply_gradients(zip(painting_discriminator_gradients,
                                                                  self.painting_discriminator.trainable_variables))
        self.photo_discriminator_optimizer.apply_gradients(zip(photo_discriminator_gradients,
                                                               self.photo_discriminator.trainable_variables))

        return {
            'painting_generator_loss': total_painting_generator_loss,
            'photo_generator_loss': total_photo_generator_loss,
            'painting_discriminator_loss': painting_discriminator_loss,
            'photo_discriminator_loss': photo_discriminator_loss
        }
