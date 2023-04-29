import tensorflow as tf
from numpy import ndarray

from ..utils import tensor_to_image


def translate_image(generator: tf.keras.models.Model, image: tf.Tensor) -> ndarray:
    """Translate an image to a painting.

    Args:
        generator: The generator model.
        image: The image to be transformed.

    Returns:
        The image as a painting in NumPy array format.
    """

    prediction = generator(image, training=False)[0]
    prediction = tensor_to_image(prediction)
    return prediction
