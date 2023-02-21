from typing import List

import tensorflow as tf

from .utils import read_tfrecorddataset
from ..consts import DATA_PATH


def monet_filenames(ext: str = 'tfrec') -> List[str]:
    """Get the list of filenames for each Monet painting.

    Args:
        ext: File extension of the Monet paintings.

    Returns:
        List of filenames for each Monet painting.
    """

    return tf.io.gfile.glob(f'{DATA_PATH}/monet_{ext}/*.{ext}')


def photo_filenames(ext: str = 'tfrec') -> List[str]:
    """Get the list of filenames for each photo.

    Args:
        ext: File extension of the photos.

    Returns:
        List of filenames for each photo.
    """

    return tf.io.gfile.glob(f'{DATA_PATH}/photo_{ext}/*.{ext}')


def monet_dataset(ext: str = 'tfrec') -> tf.data.TFRecordDataset:
    """The set of Monet paintings as a `TFRecordDataset`.

    Args:
        ext: File extension of the Monet paintings.

    Returns:
        The Monet painting dataset in `TFRecordDataset` format.
    """

    return read_tfrecorddataset(monet_filenames(ext=ext))


def photo_dataset(ext: str = 'tfrec') -> tf.data.TFRecordDataset:
    """The set of photos as a `TFRecordDataset`.

    Args:
        ext: File extension of the photos.

    Returns:
        The photo dataset in `TFRecordDataset` format.
    """

    return read_tfrecorddataset(photo_filenames(ext=ext))


def load_dataset(ext: str = 'tfrec', batch_size: int = 1) -> tf.data.Dataset:
    """Load the dataset to be used for training the CycleGAN.

    Args:
        ext: File extension of images.
        batch_size: Batch size of the dataset.

    Returns:
        The Monet paintings and photos zipped into one dataset.
    """

    monets = monet_dataset(ext).batch(batch_size, drop_remainder=True)
    photos = photo_dataset(ext).batch(batch_size, drop_remainder=True)
    return tf.data.Dataset.zip((monets, photos))
