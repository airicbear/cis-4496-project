import os

from ..modeling.create_model import create_cyclegan_model
from ..modeling.model import CycleGan


def load_cyclegan_model(monet_generator_weights_path: str = 'photo2monet.h5',
                        photo_generator_weights_path: str = 'monet2photo.h5') -> CycleGan:
    """Reconstruct a pretrained CycleGAN model given the path to each of its generator's saved weights.

    Args:
        monet_generator_weights_path: Path to the CycleGAN's Monet generator weights.
        photo_generator_weights_path: Path to the CycleGAN's photo generator weights.

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
