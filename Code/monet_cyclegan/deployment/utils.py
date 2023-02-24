from pathlib import Path

import tensorflow as tf
from PIL import Image
from numpy import uint8, ndarray

from ..modeling.model import CycleGan


def save_image(image: ndarray, output_path: str) -> None:
    """Save an image.

    Args:
        image: The image to be saved as a NumPy array.
        output_path: Path of the generated image.
    """

    make_directory(output_path, make_parent=True)

    image_array = Image.fromarray(image)
    image_array.save(output_path)


def translate_image(cyclegan_model: CycleGan, image: tf.Tensor) -> ndarray:
    """Translate an image to a Monet painting.

    Args:
        cyclegan_model: The CycleGAN model to be used for image generation.
        image: The image to be transformed.

    Returns:
        The image as a Monet painting in NumPy array format.
    """

    prediction = cyclegan_model.monet_generator(image, training=False)[0]
    prediction = tensor_to_image(prediction)
    return prediction


def tensor_to_image(image: tf.Tensor) -> ndarray:
    """Convert a tensor image to a NumPy array readable as a Pillow Image.

    Args:
        image: The image as a tensor.

    Returns:
        The image as a Pillow Image-compatible NumPy array.
    """

    result = image.numpy()
    result = result * 127.5 + 127.5
    result = result.astype(uint8)
    return result


def make_directory(path: str, make_parent: bool = False) -> None:
    """Make a directory.

    Args:
        path: Path of the directory to be created.
        make_parent: Make the path's parent directory instead of the path itself.
    """

    dir_path = Path(path)

    if make_parent:
        dir_path = dir_path.parent

    dir_path.mkdir(parents=True, exist_ok=True)
