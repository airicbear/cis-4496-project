import logging
from typing import Tuple

import tensorflow as tf
from scipy.linalg import sqrtm

logger = logging.getLogger(__name__)


def create_inception_model() -> tf.keras.Model:
    """Create an Inception model.

    The inception model is primarily used to create the FID model.
    The output of the Inception model is replaced by its last pooling layer.
    For Inception v3, this is a global average pooling layer.

    Returns:
        An Inception v3 model with its output layer replaced by its last pooling layer.
    """

    inception_model = tf.keras.applications.InceptionV3(input_shape=(256, 256, 3), pooling='avg', include_top=False)

    # Get the last pooling layer
    mix3 = inception_model.get_layer('mixed9').output
    f0 = tf.keras.layers.GlobalAveragePooling2D()(mix3)

    inception_model = tf.keras.Model(inputs=inception_model.input, outputs=f0)
    inception_model.trainable = False

    return inception_model


def create_fid_model(monet_generator: tf.keras.Model,
                     inception_model: tf.keras.Model) -> tf.keras.Model:
    """Create an FID model.

    Args:
        monet_generator: The Monet painting generator from a CycleGAN.
        inception_model: An inception model.

    Returns:
        The FID model for the Monet painting CycleGAN.
    """

    input_layer = tf.keras.layers.Input(shape=[256, 256, 3], name='input_image')
    x = monet_generator(input_layer)
    x = inception_model(x)
    fid_model = tf.keras.Model(inputs=input_layer, outputs=x)
    return fid_model


def calculate_activations(image_dataset: tf.data.TFRecordDataset,
                          model: tf.keras.Model) -> tf.Tensor:
    """Calculate activations.

    Args:
        image_dataset: The image dataset.
        model: The model used to calculate the activations.

    Returns:
        The activations.
    """

    activations = model.predict(image_dataset)
    activations = tf.cast(activations, tf.float32)
    return activations


def calculate_mean(activations: tf.Tensor):
    """Calculate the mean of a collection of activations.

    Args:
        activations: The activations to be summarized.

    Returns:
        The mean of the activations.
    """

    mean = tf.reduce_mean(activations, axis=0)
    return mean


def calculate_covariance(activations: tf.Tensor):
    """Calculate the covariance of a collection of activations.

    Args:
        activations: The activations to be summarized.

    Returns:
        The covariance of the activations.
    """

    mean_x = tf.reduce_mean(activations, axis=0, keepdims=True)
    mx = tf.matmul(tf.transpose(mean_x), mean_x)
    vx = tf.matmul(tf.transpose(activations), activations) / tf.cast(tf.shape(activations)[0], tf.float32)
    covariance = vx - mx
    return covariance


def calculate_trace_covariance_mean(sigma_real: tf.Tensor, sigma_generated: tf.Tensor):
    """Calculates the trace covariance mean.

    Args:
        sigma_real: The covariance matrix of the real image distribution.
        sigma_generated: The covariance matrix of the generated image distribution.

    Returns:
        The trace of the mean of the covariance matrix
    """

    covariance_mean = tf.cast(tf.matmul(sigma_real, sigma_generated), tf.complex64)
    covariance_mean = sqrtm(covariance_mean)
    covariance_mean = tf.cast(tf.math.real(covariance_mean), tf.float32)

    trace_covariance_mean = tf.linalg.trace(covariance_mean)

    return trace_covariance_mean


def calculate_activation_summary(image_dataset: tf.data.TFRecordDataset,
                                 model: tf.keras.Model) -> Tuple[tf.Tensor, tf.Tensor]:
    """Calculate the mean and covariance of the model's activations.

    Args:
        image_dataset: The image dataset used to input to the model.
        model: The model whose activations will be summarized.

    Returns:
        A tuple of the mean and covariance of the model's activations.
    """

    activations = calculate_activations(image_dataset=image_dataset, model=model)

    mean = calculate_mean(activations=activations)
    covariance = calculate_covariance(activations=activations)

    return mean, covariance


def calculate_frechet_distance(mu_real: tf.Tensor,
                               sigma_real: tf.Tensor,
                               mu_generated: tf.Tensor,
                               sigma_generated: tf.Tensor) -> tf.Tensor:
    """Calculate the Fréchet distance between the real and generated image distributions given their mean and variance.

    Given the means μ_r and μ_g of the real and generated image distributions and their
    covariance matrices Σ_r and Σ_g, the Fréchet distance between these two distributions is calculated as::

        d^2 = |μ_r - μ_g|^2 + Tr(Σ_r + Σ_g + 2 * sqrt(Σ_r * Σ_g))

    Args:
        mu_real: The mean of the real image distribution.
        sigma_real: The covariance of the real image distribution.
        mu_generated: The mean of the generated image distribution.
        sigma_generated: The covariance of the generated image distribution.

    Returns:
        The Fréchet distance between the two distributions.
    """

    mean_difference = mu_real - mu_generated
    mean_difference_squared = tf.matmul(tf.expand_dims(mean_difference, axis=0),
                                        tf.expand_dims(mean_difference, axis=1))
    trace_covariance_real = tf.linalg.trace(sigma_real)
    trace_covariance_generated = tf.linalg.trace(sigma_generated)
    trace_covariance_mean = calculate_trace_covariance_mean(sigma_real=sigma_real, sigma_generated=sigma_generated)

    return mean_difference_squared + trace_covariance_real + trace_covariance_generated - 2 * trace_covariance_mean


def calculate_frechet_inception_distance(photo_dataset: tf.data.TFRecordDataset,
                                         monet_dataset: tf.data.TFRecordDataset,
                                         monet_generator: tf.keras.Model,
                                         inception_model: tf.keras.Model = create_inception_model()) -> tf.Tensor:
    """Calculate the Fréchet inception distance (FID) of a Monet painting generator.

    Args:
        photo_dataset: The photo dataset used to calculate the FID.
        monet_dataset: The Monet painting dataset used to calculate the FID.
        monet_generator: The Monet painting generator to be evaluated.
        inception_model: The inception model to be used to calculate the FID.

    Returns:
        The FID score of the Monet painting generator.
    """

    logger.info('Calculating FID.')

    fid_model = create_fid_model(monet_generator=monet_generator, inception_model=inception_model)

    logger.info('Calculating mean mu1 and covariance sigma1 of activations from FID model applied to photo dataset.')
    mu1, sigma1 = calculate_activation_summary(image_dataset=photo_dataset, model=fid_model)
    logger.info(f'mu1={mu1}, sigma1={sigma1}.')

    logger.info('Calculating mean mu2 and covariance sigma2 of activations from Inception model applied to Monet dataset.')
    mu2, sigma2 = calculate_activation_summary(image_dataset=monet_dataset, model=inception_model)
    logger.info(f'mu2={mu2}, sigma2={sigma2}.')

    logger.info('Calculate the Frechet distance based on mu1, sigma1, mu2, and sigma2.')
    fid_value = calculate_frechet_distance(mu1, sigma1, mu2, sigma2)

    logger.info(f'FID score is {fid_value}.')

    return fid_value
