import tensorflow as tf

from ..consts import strategy

with strategy.scope():
    def discriminator_loss(real: tf.keras.Model,
                           generated: tf.keras.Model,
                           label_smoothing: float = 0.3) -> tf.Tensor:
        """
        Sub-function for the discriminator loss, which is the loss metric for the discriminator models.

        Args:
            real: The real/actual item.
            generated: The generated/fake item.
            label_smoothing: Regularization float number from 0 to 1 to prevent overfitting.

        Returns:
            The discriminator loss.
        """

        real_loss = tf.keras.losses.BinaryCrossentropy(from_logits=True,
                                                       reduction=tf.keras.losses.Reduction.NONE,
                                                       label_smoothing=label_smoothing)(tf.ones_like(real),
                                                                                        real)
        generated_loss = tf.keras.losses.BinaryCrossentropy(from_logits=True,
                                                            reduction=tf.keras.losses.Reduction.NONE,
                                                            label_smoothing=label_smoothing)(tf.zeros_like(generated),
                                                                                             generated)
        total_discriminator_loss = real_loss + generated_loss
        return total_discriminator_loss * 0.5


    def generator_loss(generated: tf.keras.Model) -> tf.Tensor:
        """
        Sub-function for the generator loss, which is the loss metric for the generator models.

        Args:
            generated: The generated/fake item.

        Returns:
            The generator loss (binary cross entropy).
        """

        return tf.keras.losses.BinaryCrossentropy(from_logits=True,
                                                  reduction=tf.keras.losses.Reduction.NONE)(tf.ones_like(generated),
                                                                                            generated)


    def calc_cycle_loss(real_image: tf.Tensor, cycled_image: tf.Tensor, alpha: tf.Tensor) -> tf.Tensor:
        """
        Calculate the cycle loss given a real image and the image after being cycled.
        This helps to verify whether the result is close to the original input.

        Args:
            real_image: The real image.
            cycled_image: The image after being cycled.
            alpha: The alpha value to be multiplied by the loss value.

        Returns:
            The calculated cycle loss.
        """

        loss = tf.reduce_mean(tf.abs(real_image - cycled_image))
        return loss * alpha


    def identity_loss(real_image: tf.Tensor, same_image: tf.Tensor, alpha: tf.Tensor) -> tf.Tensor:
        """
        Sub-function to calculate the identity loss, which says that, if you feed the image to the generator,
        it should yield the real image or something close to the image.

        Args:
            real_image: The real image.
            same_image: The image that should be close to the real image.
            alpha: The alpha value to be multiplied by the loss value.

        Returns:
            The calculated identity loss.
        """

        loss = tf.reduce_mean(tf.abs(real_image - same_image))
        return tf.math.scalar_mul(0.5, alpha * loss)
