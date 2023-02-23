"""
Compile and train the CycleGAN model.
"""

from argparse import ArgumentParser

import tensorflow as tf

from .compile import cyclegan_compile_with_loss_rate
from .create_model import create_cyclegan_model
from .model import CycleGan
from ..consts import BATCH_SIZE, MONET_TFREC_DIR, PHOTO_TFREC_DIR
from ..data_acquisition.datasets import load_dataset


def train_model(cyclegan_model: CycleGan,
                loss_rate: float,
                train_dataset: tf.data.Dataset) -> None:
    """Train a given CycleGAN model.

    Args:
        cyclegan_model: The CycleGAN model to be trained.
        loss_rate: The loss rate at which the model should be trained.
        train_dataset: The data to be used for training.
    """

    cyclegan_compile_with_loss_rate(cyclegan_model=cyclegan_model, loss_rate=loss_rate)
    cyclegan_model.fit(train_dataset, epochs=1)


def save_weights(cyclegan_model: CycleGan,
                 monet_generator_path: str = 'photo2monet.h5',
                 photo_generator_path: str = 'monet2photo.h5') -> None:
    """Save the weights of a CycleGAN model.

    Args:
        cyclegan_model: The CycleGAN model to have its weights saved.
        monet_generator_path: The path where the Monet generator's weights will be stored.
        photo_generator_path: The path where the photo generator's weights will be stored.
    """

    cyclegan_model.monet_generator.save_weights(monet_generator_path)
    cyclegan_model.photo_generator.save_weights(photo_generator_path)


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument('--monet_dir', type=str, default=MONET_TFREC_DIR)
    parser.add_argument('--photo_dir', type=str, default=PHOTO_TFREC_DIR)
    args = parser.parse_args()

    dataset = load_dataset(monet_dir=args.monet_dir, photo_dir=args.photo_dir, batch_size=BATCH_SIZE)

    model = create_cyclegan_model()

    train_model(cyclegan_model=model,
                loss_rate=2e-4,
                train_dataset=dataset)

    save_weights(cyclegan_model=model)


if __name__ == '__main__':
    main()
