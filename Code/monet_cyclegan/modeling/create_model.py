import logging

from .discriminator import discriminator
from .generator import generator
from .model import CycleGan

logger = logging.getLogger(__name__)


def create_cyclegan_model() -> CycleGan:
    """Create a CycleGAN model.

    Returns:
        A new CycleGAN model.
    """

    logger.info('Creating CycleGAN model.')

    painting_generator = generator()
    photo_generator = generator()
    painting_discriminator = discriminator()
    photo_discriminator = discriminator()

    return CycleGan(painting_generator=painting_generator,
                    photo_generator=photo_generator,
                    painting_discriminator=painting_discriminator,
                    photo_discriminator=photo_discriminator)
