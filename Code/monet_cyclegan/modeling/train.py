"""
Compile and train the CycleGAN model.
"""
import logging

import tensorflow as tf

from .compile import cyclegan_compile_with_loss_rate
from .model import CycleGan
from ..consts import MONET_GENERATOR_WEIGHT_FILENAME, PHOTO_GENERATOR_WEIGHT_FILENAME
from ..utils import make_directory

logger = logging.getLogger(__name__)


def train_model(cyclegan_model: CycleGan,
                loss_rate: float,
                train_dataset: tf.data.Dataset,
                epochs: int,
                steps_per_epoch: int) -> None:
    """Train a given CycleGAN model.

    Args:
        cyclegan_model: The CycleGAN model to be trained.
        loss_rate: The loss rate at which the model should be trained.
        train_dataset: The data to be used for training.
        epochs: The number of epochs to train the model for.
        steps_per_epoch: The number of steps per epoch.
    """

    cyclegan_compile_with_loss_rate(cyclegan_model=cyclegan_model, loss_rate=loss_rate)

    logger.info(f'Fitting model using {epochs} epochs and {steps_per_epoch} steps per epoch.')
    cyclegan_model.fit(train_dataset, epochs=epochs, steps_per_epoch=steps_per_epoch)
    logger.info(f'Finished fitting model.')

def save_weights(cyclegan_model: CycleGan,
                 monet_generator_path: str = MONET_GENERATOR_WEIGHT_FILENAME,
                 photo_generator_path: str = PHOTO_GENERATOR_WEIGHT_FILENAME) -> None:
    """Save the build of a CycleGAN model.

    Args:
        cyclegan_model: The CycleGAN model to have its build saved.
        monet_generator_path: The path where the Monet generator's build will be stored.
        photo_generator_path: The path where the photo generator's build will be stored.
    """

    make_directory(monet_generator_path, make_parent=True)

    logger.info(f"Saving Monet generator build to '{monet_generator_path}'.")
    logger.info(f"Saving photo generator build to '{photo_generator_path}'.")

    cyclegan_model.monet_generator.save_weights(monet_generator_path)
    cyclegan_model.photo_generator.save_weights(photo_generator_path)

    logger.info(f"Saved Monet generator build to '{monet_generator_path}'.")
    logger.info(f"Saved photo generator build to '{photo_generator_path}'.")
