import tensorflow as tf

from .consts import strategy

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
        return tf.keras.losses.BinaryCrossentropy(from_logits=True,
                                                  reduction=tf.keras.losses.Reduction.NONE)(tf.ones_like(generated),
                                                                                            generated)


    def calc_cycle_loss(real_image: tf.Tensor, cycled_image: tf.Tensor, alpha: float) -> float:
        """
        sub-function to calculate the cycle loss.
        This helps to verify whether the result is close to the original input.
        :param real_image: the real image
        :param cycled_image: the image after being cycled
        :param LAMBDA: the lambda value to be multiplied by the loss value
        :return: the calculated cycle loss
        """
        loss1: tf.Tensor = tf.reduce_mean(tf.abs(real_image - cycled_image))
        return loss1 * alpha


    def identity_loss(real_image: tf.Tensor, same_image: tf.Tensor, alpha: float) -> float:
        """
        sub-function to calculate the identity loss, which says that, if you feed the image to the generator,
         it should yield the real image or something close to the image.
        :param real_image: the real image
        :param same_image: the image tht should be close to the real image
        :param LAMBDA: the lambda value to be multiplied by the loss value
        :return:the calculated identity loss
        """
        loss: tf.Tensor = tf.reduce_mean(tf.abs(real_image - same_image))
        return alpha * 0.5 * loss
