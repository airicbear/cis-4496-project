import os

from ..consts import MONET_GENERATOR_WEIGHT_FILENAME, PHOTO_GENERATOR_WEIGHT_FILENAME, BUILD_DIR, EPOCHS
from ..modeling.create_model import create_cyclegan_model
from ..modeling.model import CycleGan


def load_cyclegan_model(
        monet_generator_weights_path: str = f'{BUILD_DIR}/epoch{EPOCHS}/{MONET_GENERATOR_WEIGHT_FILENAME}',
        photo_generator_weights_path: str = f'{BUILD_DIR}/epoch{EPOCHS}/{PHOTO_GENERATOR_WEIGHT_FILENAME}') -> CycleGan:
    """Reconstruct a pretrained CycleGAN model given the path to each of its generator's saved build.

    Args:
        monet_generator_weights_path: Path to the CycleGAN's Monet generator build.
        photo_generator_weights_path: Path to the CycleGAN's photo generator build.

    Returns:
        The reconstructed CycleGAN model.
    """

    if not os.path.isfile(monet_generator_weights_path):
        raise FileNotFoundError(f'Could not find {monet_generator_weights_path}.')

    if not os.path.isfile(photo_generator_weights_path):
        raise FileNotFoundError(f'Could not find {photo_generator_weights_path}.')

    cyclegan_model = create_cyclegan_model()

    cyclegan_model.monet_generator.load_weights(monet_generator_weights_path)
    cyclegan_model.photo_generator.load_weights(photo_generator_weights_path)

    return cyclegan_model
