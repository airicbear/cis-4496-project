import tensorflow as tf
from numpy import ndarray

from .model import CycleGan
from ..utils import tensor_to_image


def translate_image(cyclegan_model: CycleGan, image: tf.Tensor) -> ndarray:
    """Translate an image to a painting.

    Args:
        cyclegan_model: The CycleGAN model to be used for image generation.
        image: The image to be transformed.

    Returns:
        The image as a painting in NumPy array format.
    """

    prediction = cyclegan_model.painting_generator(image, training=False)[0]
    prediction = tensor_to_image(prediction)
    return prediction
