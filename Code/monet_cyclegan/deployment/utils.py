from pathlib import Path

import tensorflow as tf
from PIL import Image
from numpy import uint8

from ..modeling.model import CycleGan


def save_image(image: tf.Tensor, output_path: str) -> None:
    """Save an image.

    Args:
        image: The image to be saved.
        output_path: Directory where the generated image will be stored.
    """

    Image.fromarray(image).save(output_path)


def translate_image(cyclegan_model: CycleGan, image: tf.Tensor) -> tf.Tensor:
    """Translate an image to a Monet painting.

    Args:
        cyclegan_model: The CycleGAN model to be used for image generation.
        image: The image to be transformed.

    Returns:
        The image as a Monet painting.
    """

    prediction = cyclegan_model.monet_generator(image, training=False)[0].numpy()
    prediction = (prediction * 127.5 + 127.5).astype(uint8)
    return prediction


def make_directory(path: str) -> None:
    """Make a directory.

    Args:
        path: Path of the directory to be created.
    """

    Path(path).mkdir(parents=True, exist_ok=True)
