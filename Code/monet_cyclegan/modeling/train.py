"""
Compile and train the CycleGAN model.
"""

from argparse import ArgumentParser

import tensorflow as tf

from .compile import cyclegan_compile_with_loss_rate
from .create_model import create_cyclegan_model
from .model import CycleGan
from ..consts import BATCH_SIZE, MONET_TFREC_DIR, PHOTO_TFREC_DIR, MONET_GENERATOR_WEIGHT_PATH, \
    PHOTO_GENERATOR_WEIGHT_PATH, EPOCHS, LOSS_RATE, WEIGHT_OUTPUT_DIR
from ..data_acquisition.datasets import load_dataset
from ..deployment.utils import make_directory


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


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument('--monet_dir', type=str, default=MONET_TFREC_DIR)
    parser.add_argument('--photo_dir', type=str, default=PHOTO_TFREC_DIR)
    parser.add_argument('--loss_rate', '-lr', type=float, default=LOSS_RATE)
    parser.add_argument('--epochs', type=int, default=EPOCHS)
    parser.add_argument('--output', '-o', type=str, default=WEIGHT_OUTPUT_DIR)
    parser.add_argument('--num_monet', type=int, default=None)
    parser.add_argument('--num_photo', type=int, default=None)
    args = parser.parse_args()

    dataset = load_dataset(monet_dir=args.monet_dir, photo_dir=args.photo_dir, batch_size=BATCH_SIZE)

    model = create_cyclegan_model()

    train_model(cyclegan_model=model,
                loss_rate=args.loss_rate,
                train_dataset=dataset,
                epochs=args.epochs)

    save_weights(cyclegan_model=model,
                 monet_generator_path=f'{args.output}/epoch{args.epochs}/{MONET_GENERATOR_WEIGHT_PATH}',
                 photo_generator_path=f'{args.output}/epoch{args.epochs}/{PHOTO_GENERATOR_WEIGHT_PATH}')


if __name__ == '__main__':
    main()
