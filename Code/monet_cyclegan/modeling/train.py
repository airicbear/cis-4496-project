"""
Compile and train the CycleGAN model.
"""
import logging

import tensorflow as tf

from .compile import cyclegan_compile_with_loss_rate
from .model import CycleGan
from ..consts import PHOTO2PAINTING_WEIGHTS, PAINTING2PHOTO_WEIGHTS

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


def save_hdf5_weights(cyclegan_model: CycleGan,
                      weights_dir: str) -> None:
    """Save the weights of a CycleGAN model in HDF5 format.

    Args:
        cyclegan_model: The CycleGAN model to have its build saved.
        weights_dir: The directory where the model's generator and discriminator weights will be stored.
    """

    painting_generator_hdf5_path = f'{weights_dir}/HDF5/{PHOTO2PAINTING_WEIGHTS}.h5'
    photo_generator_hdf5_path = f'{weights_dir}/HDF5/{PAINTING2PHOTO_WEIGHTS}.h5'

    logger.info(f"Saving painting generator HDF5 weights to '{painting_generator_hdf5_path}'.")
    logger.info(f"Saving photo generator HDF5 weights to '{photo_generator_hdf5_path}'.")

    cyclegan_model.painting_generator.save(painting_generator_hdf5_path)
    cyclegan_model.photo_generator.save(photo_generator_hdf5_path)

    logger.info(f"Saved painting generator HDF5 weights to '{painting_generator_hdf5_path}'.")
    logger.info(f"Saved photo generator HDF5 weights to '{photo_generator_hdf5_path}'.")


def save_saved_model_weights(cyclegan_model: CycleGan,
                             weights_dir: str) -> None:
    """Save the build of a CycleGAN model.

    Args:
        cyclegan_model: The CycleGAN model to have its build saved.
        weights_dir: The directory where the model's generator and discriminator weights will be stored.
    """

    painting_generator_saved_model_path = f'{weights_dir}/SavedModel/{PHOTO2PAINTING_WEIGHTS}'
    photo_generator_saved_model_path = f'{weights_dir}/SavedModel/{PAINTING2PHOTO_WEIGHTS}'

    logger.info(f"Saving painting generator SavedModel weights to '{painting_generator_saved_model_path}'.")
    logger.info(f"Saving photo generator SavedModel weights to '{photo_generator_saved_model_path}'.")

    cyclegan_model.painting_generator.save(painting_generator_saved_model_path)
    cyclegan_model.photo_generator.save(photo_generator_saved_model_path)

    logger.info(f"Saved painting generator SavedModel weights to '{painting_generator_saved_model_path}'.")
    logger.info(f"Saved photo generator SavedModel weights to '{photo_generator_saved_model_path}'.")


def save_weights(cyclegan_model: CycleGan,
                 weights_dir: str) -> None:
    """Save the build of a CycleGAN model.

    Args:
        cyclegan_model: The CycleGAN model to have its build saved.
        weights_dir: The directory where the model's generator and discriminator weights will be stored.
    """

    save_hdf5_weights(cyclegan_model=cyclegan_model, weights_dir=weights_dir)
    save_saved_model_weights(cyclegan_model=cyclegan_model, weights_dir=weights_dir)
