"""
Compile and train the CycleGAN model.
"""

import tensorflow as tf

from .compile import cyclegan_compile_with_loss_rate
from .model import CycleGan
from ..consts import MONET_GENERATOR_WEIGHT_PATH, PHOTO_GENERATOR_WEIGHT_PATH
from ..utils import make_directory


def train_model(cyclegan_model: CycleGan,
                loss_rate: float,
                train_dataset: tf.data.Dataset,
                epochs: int) -> None:
    """Train a given CycleGAN model.

    Args:
        cyclegan_model: The CycleGAN model to be trained.
        loss_rate: The loss rate at which the model should be trained.
        train_dataset: The data to be used for training.
        epochs: The number of epochs to train the model for.
    """

    cyclegan_compile_with_loss_rate(cyclegan_model=cyclegan_model, loss_rate=loss_rate)
    cyclegan_model.fit(train_dataset, epochs=epochs)


def save_weights(cyclegan_model: CycleGan,
                 monet_generator_path: str = MONET_GENERATOR_WEIGHT_PATH,
                 photo_generator_path: str = PHOTO_GENERATOR_WEIGHT_PATH) -> None:
    """Save the weights of a CycleGAN model.

    Args:
        cyclegan_model: The CycleGAN model to have its weights saved.
        monet_generator_path: The path where the Monet generator's weights will be stored.
        photo_generator_path: The path where the photo generator's weights will be stored.
    """

    make_directory(monet_generator_path, make_parent=True)

    cyclegan_model.monet_generator.save_weights(monet_generator_path)
    cyclegan_model.photo_generator.save_weights(photo_generator_path)
