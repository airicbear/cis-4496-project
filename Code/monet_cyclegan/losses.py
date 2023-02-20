import tensorflow as tf

from .consts import strategy

with strategy.scope():
    def discriminator_loss(real: tf.keras.Model, generated: tf.keras.Model) -> tf.Tensor:
        real_loss = tf.keras.losses.BinaryCrossentropy(from_logits=True,
                                                       reduction=tf.keras.losses.Reduction.NONE)(tf.ones_like(real),
                                                                                                 real)
        generated_loss = tf.keras.losses.BinaryCrossentropy(from_logits=True,
                                                            reduction=tf.keras.losses.Reduction.NONE)(
            tf.zeros_like(generated), generated)
        total_discriminator_loss = real_loss + generated_loss
        return total_discriminator_loss * 0.5


    def generator_loss(generated: tf.keras.Model) -> tf.Tensor:
        return tf.keras.losses.BinaryCrossentropy(from_logits=True,
                                                  reduction=tf.keras.losses.Reduction.NONE)(tf.ones_like(generated),
                                                                                            generated)


    def calc_cycle_loss(real_image: tf.Tensor, cycled_image: tf.Tensor, alpha: float) -> tf.Tensor:
        loss1 = tf.reduce_mean(tf.abs(real_image - cycled_image))
        return alpha * loss1


    def identity_loss(real_image: tf.Tensor, same_image: tf.Tensor, alpha: float) -> tf.Tensor:
        loss = tf.reduce_mean(tf.abs(real_image - same_image))
        return alpha * 0.5 * loss
