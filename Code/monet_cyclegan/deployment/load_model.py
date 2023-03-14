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

    cyclegan_model = create_cyclegan_model()

    photo_generator_path_tokens = os.path.splitext(painting2photo_generator_weights_path)
    painting_generator_path_tokens = os.path.splitext(photo2painting_generator_weights_path)

    if len(photo_generator_path_tokens) == 2:
        if not os.path.isfile(painting2photo_generator_weights_path):
            raise FileNotFoundError(f'Could not find {painting2photo_generator_weights_path}.')

        cyclegan_model.photo_generator.load_weights(painting2photo_generator_weights_path)

    elif len(photo_generator_path_tokens) == 1:
        if not os.path.isdir(painting2photo_generator_weights_path):
            raise FileNotFoundError(f'Could not find {painting2photo_generator_weights_path}.')

        cyclegan_model.photo_generator = tf.keras.models.load_model(painting2photo_generator_weights_path)

    else:
        raise IOError(f'Invalid photo generator path: "{painting2photo_generator_weights_path}"')

    if len(painting_generator_path_tokens) == 2:
        if not os.path.isfile(photo2painting_generator_weights_path):
            raise FileNotFoundError(f'Could not find {photo2painting_generator_weights_path}.')

        cyclegan_model.painting_generator.load_weights(photo2painting_generator_weights_path)

    elif len(painting_generator_path_tokens) == 1:
        if not os.path.isdir(photo2painting_generator_weights_path):
            raise FileNotFoundError(f'Could not find {photo2painting_generator_weights_path}.')

        cyclegan_model.painting_generator = tf.keras.models.load_model(photo2painting_generator_weights_path)

    else:
        raise IOError(f'Invalid painting generator path: "{photo2painting_generator_weights_path}"')

    return cyclegan_model
