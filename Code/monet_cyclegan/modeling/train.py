"""
Compile and train the CycleGAN model.
"""

import argparse
import os
import sys

import tensorflow as tf

from .compile import cyclegan_compile_with_loss_rate
from .create_model import create_cyclegan_model
from .model import CycleGan
from ..consts import BATCH_SIZE, DATA_PATH
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
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', type=str, default=DATA_PATH)
    args = parser.parse_args()

    dataset = load_dataset(data_path=args.data_path, batch_size=BATCH_SIZE)

    if not os.path.isdir(args.data_path):
        print(f"ERROR: Can't find {args.data_path}")
        sys.exit(1)

    model = create_cyclegan_model()

    print(f'Training CycleGAN on {dataset}.')
    train_model(cyclegan_model=model, train_dataset=dataset)


if __name__ == '__main__':
    main()
