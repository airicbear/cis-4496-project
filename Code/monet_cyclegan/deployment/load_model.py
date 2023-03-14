import os

import tensorflow as tf

from ..modeling.create_model import create_cyclegan_model
from ..modeling.model import CycleGan


def load_cyclegan_model(
        photo2painting_generator_weights_path: str,
        painting2photo_generator_weights_path: str) -> CycleGan:
    """Reconstruct a pretrained CycleGAN model given the path to each of its generator's saved build.

    Args:
        photo2painting_generator_weights_path: Path to the CycleGAN's painting generator build.
        painting2photo_generator_weights_path: Path to the CycleGAN's photo generator build.

    Returns:
        The reconstructed CycleGAN model.
    """

    if not os.path.isdir(photo2painting_generator_weights_path):
        raise FileNotFoundError(f'Could not find {photo2painting_generator_weights_path}.')

    if not os.path.isdir(painting2photo_generator_weights_path):
        raise FileNotFoundError(f'Could not find {painting2photo_generator_weights_path}.')

    cyclegan_model = create_cyclegan_model()

    cyclegan_model.painting_generator = tf.keras.models.load_model(photo2painting_generator_weights_path)
    cyclegan_model.photo_generator = tf.keras.models.load_model(painting2photo_generator_weights_path)

    return cyclegan_model
