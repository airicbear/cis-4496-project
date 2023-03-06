import os

from ..consts import PHOTO2PAINTING_FILENAME, PAINTING2PHOTO_FILENAME, BUILD_DIR, EPOCHS
from ..modeling.create_model import create_cyclegan_model
from ..modeling.model import CycleGan


def load_cyclegan_model(
        photo2painting_generator_weights_path: str = f'{BUILD_DIR}/epoch{EPOCHS}/{PHOTO2PAINTING_FILENAME}',
        painting2photo_generator_weights_path: str = f'{BUILD_DIR}/epoch{EPOCHS}/{PAINTING2PHOTO_FILENAME}') -> CycleGan:
    """Reconstruct a pretrained CycleGAN model given the path to each of its generator's saved build.

    Args:
        photo2painting_generator_weights_path: Path to the CycleGAN's painting generator build.
        painting2photo_generator_weights_path: Path to the CycleGAN's photo generator build.

    Returns:
        The reconstructed CycleGAN model.
    """

    if not os.path.isfile(photo2painting_generator_weights_path):
        raise FileNotFoundError(f'Could not find {photo2painting_generator_weights_path}.')

    if not os.path.isfile(painting2photo_generator_weights_path):
        raise FileNotFoundError(f'Could not find {painting2photo_generator_weights_path}.')

    cyclegan_model = create_cyclegan_model()

    cyclegan_model.painting_generator.load_weights(photo2painting_generator_weights_path)
    cyclegan_model.photo_generator.load_weights(painting2photo_generator_weights_path)

    return cyclegan_model
