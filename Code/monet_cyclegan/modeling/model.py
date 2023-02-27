from abc import ABC
from typing import Callable, Tuple

import tensorflow as tf


class CycleGan(tf.keras.Model, ABC):
    """The CycleGAN model that initializes and compiles the generators and discriminators."""

    def __init__(self,
                 monet_generator: tf.keras.Model,
                 photo_generator: tf.keras.Model,
                 monet_discriminator: tf.keras.Model,
                 photo_discriminator: tf.keras.Model,
                 lambda_cycle: int = 10):
        """Initialization function for the generators, discriminators, and the lambda cycle.

        Args:
            monet_generator: the monet painting generator model
            photo_generator: the photo generator model
            monet_discriminator: the monet painting discriminator
            photo_discriminator: the photo discriminator
            lambda_cycle: the lambda cycle
        """

        super(CycleGan, self).__init__()
        self.monet_generator = monet_generator
        self.photo_generator = photo_generator
        self.monet_discriminator = monet_discriminator
        self.photo_discriminator = photo_discriminator
        self.lambda_cycle = lambda_cycle
        self.monet_generator_optimizer = None
        self.photo_generator_optimizer = None
        self.monet_discriminator_optimizer = None
        self.photo_discriminator_optimizer = None
        self.generator_loss_fn = None
        self.discriminator_loss_fn = None
        self.cycle_loss_fn = None
        self.identity_loss_fn = None

    def compile(self,
                monet_generator_optimizer: tf.keras.optimizers.Optimizer,
                photo_generator_optimizer: tf.keras.optimizers.Optimizer,
                monet_discriminator_optimizer: tf.keras.optimizers.Optimizer,
                photo_discriminator_optimizer: tf.keras.optimizers.Optimizer,
                generator_loss_fn: Callable[[tf.keras.Model], tf.Tensor],
                discriminator_loss_fn: Callable[[tf.keras.Model, tf.keras.Model], tf.Tensor],
                cycle_loss_fn: Callable[[tf.Tensor, tf.Tensor, float], float],
                identity_loss_fn: Callable[[tf.Tensor, tf.Tensor, float], float]):
        """Compiler function that sets the optimizers and the loss functions of the CycleGAN.

        Args:
            monet_generator_optimizer: optimizer for monet painting generator model
            photo_generator_optimizer: optimizer for photo generator model
            monet_discriminator_optimizer: optimizer for monet painting discriminator model
            photo_discriminator_optimizer: optimizer for photo discriminator model
            generator_loss_fn: loss function for the generator models
            discriminator_loss_fn: loss function for the discriminator models
            cycle_loss_fn: cycleGAN loss function
            identity_loss_fn: identity loss function
        """

        super(CycleGan, self).compile()
        self.monet_generator_optimizer = monet_generator_optimizer
        self.photo_generator_optimizer = photo_generator_optimizer
        self.monet_discriminator_optimizer = monet_discriminator_optimizer
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

        real_monet, real_photo = batch_data

        with tf.GradientTape(persistent=True) as tape:
            fake_monet = self.monet_generator(real_photo, training=True)
            cycled_photo = self.photo_generator(fake_monet, training=True)

            fake_photo = self.photo_generator(real_monet, training=True)
            cycled_monet = self.monet_generator(fake_photo, training=True)

            same_monet = self.monet_generator(real_monet, training=True)
            same_photo = self.photo_generator(real_photo, training=True)

            discriminator_real_monet = self.monet_discriminator(real_monet, training=True)
            discriminator_real_photo = self.photo_discriminator(real_photo, training=True)

            discriminator_fake_monet = self.monet_discriminator(fake_monet, training=True)
            discriminator_fake_photo = self.photo_discriminator(fake_photo, training=True)

            monet_generator_loss = self.generator_loss_fn(discriminator_fake_monet)
            photo_generator_loss = self.generator_loss_fn(discriminator_fake_photo)

            monet_cycle_loss = self.cycle_loss_fn(real_monet, cycled_monet, self.lambda_cycle)
            photo_cycle_loss = self.cycle_loss_fn(real_photo, cycled_photo, self.lambda_cycle)
            total_cycle_loss = monet_cycle_loss + photo_cycle_loss

            monet_identity_loss = self.identity_loss_fn(real_monet, same_monet, self.lambda_cycle)
            photo_identity_loss = self.identity_loss_fn(real_photo, same_photo, self.lambda_cycle)

            total_monet_generator_loss = monet_generator_loss + total_cycle_loss + monet_identity_loss
            total_photo_generator_loss = photo_generator_loss + total_cycle_loss + photo_identity_loss

            monet_discriminator_loss = self.discriminator_loss_fn(discriminator_real_monet, discriminator_fake_monet)
            photo_discriminator_loss = self.discriminator_loss_fn(discriminator_real_photo, discriminator_fake_photo)

        monet_generator_gradients = tape.gradient(total_monet_generator_loss, self.monet_generator.trainable_variables)
        photo_generator_gradients = tape.gradient(total_photo_generator_loss, self.photo_generator.trainable_variables)

        monet_discriminator_gradients = tape.gradient(monet_discriminator_loss,
                                                      self.monet_discriminator.trainable_variables)
        photo_discriminator_gradients = tape.gradient(photo_discriminator_loss,
                                                      self.photo_discriminator.trainable_variables)

        self.monet_generator_optimizer.apply_gradients(zip(monet_generator_gradients,
                                                           self.monet_generator.trainable_variables))
        self.photo_generator_optimizer.apply_gradients(zip(photo_generator_gradients,
                                                           self.photo_generator.trainable_variables))

        self.monet_discriminator_optimizer.apply_gradients(zip(monet_discriminator_gradients,
                                                               self.monet_discriminator.trainable_variables))
        self.photo_discriminator_optimizer.apply_gradients(zip(photo_discriminator_gradients,
                                                               self.photo_discriminator.trainable_variables))

        return {
            'monet_generator_loss': total_monet_generator_loss,
            'photo_generator_loss': total_photo_generator_loss,
            'monet_discriminator_loss': monet_discriminator_loss,
            'photo_discriminator_loss': photo_discriminator_loss
        }
