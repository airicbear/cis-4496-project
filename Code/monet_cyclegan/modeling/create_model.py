from .discriminator import discriminator
from .generator import generator
from .model import CycleGan


def create_cyclegan_model() -> CycleGan:
    """Create a CycleGAN model.

    Returns:
        A new CycleGAN model.
    """

    monet_generator = generator()
    photo_generator = generator()
    monet_discriminator = discriminator()
    photo_discriminator = discriminator()

    return CycleGan(monet_generator=monet_generator,
                    photo_generator=photo_generator,
                    monet_discriminator=monet_discriminator,
                    photo_discriminator=photo_discriminator)
