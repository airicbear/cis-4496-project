from typing import List

import tensorflow as tf

from .utils import read_tfrecorddataset


def monet_filenames(data_path: str, ext: str = 'tfrec') -> List[str]:
    """Get the list of filenames for each Monet painting.

    Args:
        data_path: Path of the data folder.
        ext: File extension of the Monet paintings.

    Returns:
        List of filenames for each Monet painting.
    """

    return tf.io.gfile.glob(f'{data_path}/monet_{ext}/*.{ext}')


def photo_filenames(data_path: str, ext: str = 'tfrec') -> List[str]:
    """Get the list of filenames for each photo.

    Args:
        data_path: Path of the data folder.
        ext: File extension of the photos.

    Returns:
        List of filenames for each photo.
    """

    return tf.io.gfile.glob(f'{data_path}/photo_{ext}/*.{ext}')


def monet_dataset(data_path: str, ext: str = 'tfrec') -> tf.data.TFRecordDataset:
    """The set of Monet paintings as a `TFRecordDataset`.

    Args:
        data_path: Path of the data folder.
        ext: File extension of the Monet paintings.

    Returns:
        The Monet painting dataset in `TFRecordDataset` format.
    """

    return read_tfrecorddataset(monet_filenames(data_path=data_path, ext=ext))


def photo_dataset(data_path: str, ext: str = 'tfrec') -> tf.data.TFRecordDataset:
    """The set of photos as a `TFRecordDataset`.

    Args:
        data_path: Path of the data folder.
        ext: File extension of the photos.

    Returns:
        The photo dataset in `TFRecordDataset` format.
    """

    return read_tfrecorddataset(photo_filenames(data_path=data_path, ext=ext))


def load_dataset(data_path: str, ext: str = 'tfrec', batch_size: int = 1) -> tf.data.Dataset:
    """Load the dataset to be used for training the CycleGAN.

    Args:
        data_path: Path of the data folder.
        ext: File extension of images.
        batch_size: Batch size of the dataset.

    Returns:
        The Monet paintings and photos zipped into one dataset.
    """

    monets = monet_dataset(data_path=data_path, ext=ext).batch(batch_size, drop_remainder=True)
    photos = photo_dataset(data_path=data_path, ext=ext).batch(batch_size, drop_remainder=True)
    return tf.data.Dataset.zip((monets, photos))
