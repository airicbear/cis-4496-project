from typing import Callable

import tensorflow as tf
import numpy as np
import re

from .consts import USING_KAGGLE, AUTOTUNE
from .utils import read_tfrecords


def dataset_path(path: str = '../Sample_Data/Raw') -> str:
    """
    This function loads the Monet and photo images in `TFRecordDataset` format.
    :param path: default portion of path
    :return: path of dataset as string
    """
    if USING_KAGGLE:
        from kaggle_datasets import KaggleDatasets
        return KaggleDatasets().get_gcs_path()
    else:
        return path


def monet_filenames():
    """
    :return: filenames for the monet painting.
    """
    return tf.io.gfile.glob(f'{dataset_path()}/monet_tfrec/*.tfrec')


def photo_filenames():
    """
    :return: filenames for the photos
    """
    return tf.io.gfile.glob(f'{dataset_path()}/photo_tfrec/*.tfrec')


def monet_dataset():
    """
    :return: the loaded Monet paintings in `TFRecordDataset` format.
    """
    return read_tfrecords(monet_filenames())


def photo_dataset():
    """
    :return: the loaded photos in `TFRecordDataset` format.
    """
    return read_tfrecords(photo_filenames())


def count_data_items(filenames) -> np.array:
    n: list

    n = [int(re.compile(r"-([0-9]*)\.").search(filename).group(1)) for filename in filenames]

    return np.sum(n)


def count_monet_samples():
    return count_data_items(monet_filenames())


def count_photo_samples():
    return count_data_items(photo_filenames())


def get_gan_dataset(augment: Callable[[tf.Tensor], tf.Tensor] = None,
                    repeat: bool = True,
                    shuffle: bool = True,
                    batch_size: int = 1):
    monets = monet_dataset()
    photos = photo_dataset()

    if repeat:
        monets = monets.repeat()
        photos = photos.repeat()

    if shuffle:
        monets = monets.shuffle(2048)
        photos = photos.shuffle(2048)

    monets = monets.batch(batch_size, drop_remainder=True)
    photos = photos.batch(batch_size, drop_remainder=True)

    if augment:
        monets = monets.map(augment, num_parallel_calls=AUTOTUNE)
        photos = photos.map(augment, num_parallel_calls=AUTOTUNE)

    monets = monets.prefetch(AUTOTUNE)
    photos = photos.prefetch(AUTOTUNE)

    gan_dataset = tf.data.Dataset.zip((monets, photos))

    return gan_dataset
