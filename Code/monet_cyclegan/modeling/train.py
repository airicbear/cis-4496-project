"""
Compile and train the CycleGAN model.
"""

import tensorflow as tf

from .compile import cyclegan_compile_with_loss_rate
from .create_model import create_cyclegan_model
from .model import CycleGan
from ..consts import BATCH_SIZE
from ..data_acquisition.datasets import load_dataset


def train_model(cyclegan_model: CycleGan, train_dataset: tf.data.Dataset) -> None:
    """Train a given CycleGAN model.

    Args:
        cyclegan_model: The CycleGAN model to be trained.
        train_dataset: The data to be used for training.
    """

    cyclegan_compile_with_loss_rate(cyclegan_model=cyclegan_model, loss_rate=2e-4)
    cyclegan_model.fit(train_dataset, epochs=1)

    cyclegan_model.monet_generator.save_weights('photo2monet.h5')
    cyclegan_model.photo_generator.save_weights('monet2photo.h5')


def main() -> None:
    dataset = load_dataset(batch_size=BATCH_SIZE)
    model = create_cyclegan_model()
    train_model(cyclegan_model=model, train_dataset=dataset)


if __name__ == '__main__':
    main()
