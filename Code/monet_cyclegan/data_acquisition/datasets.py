from typing import List

import tensorflow as tf

from .utils import read_tfrecorddataset, get_filenames
from ..consts import MONET_TFREC_DIR, PHOTO_TFREC_DIR


def monet_tfrec_filenames(image_dir: str = MONET_TFREC_DIR) -> List[str]:
    """Get the list of filenames for each Monet painting.

    Returns:
        List of filenames for each Monet painting.
    """

    return get_filenames(image_dir=image_dir, ext='tfrec')


def photo_tfrec_filenames(image_dir: str = PHOTO_TFREC_DIR) -> List[str]:
    """Get the list of filenames for each photo.

    Returns:
        List of filenames for each photo.
    """

    return get_filenames(image_dir=image_dir, ext='tfrec')


def monet_tfrecorddataset(image_dir: str = MONET_TFREC_DIR) -> tf.data.TFRecordDataset:
    """The set of Monet paintings as a `TFRecordDataset`.

    Returns:
        The Monet painting dataset in `TFRecordDataset` format.
    """

    return read_tfrecorddataset(filenames=monet_tfrec_filenames(image_dir=image_dir))


def photo_tfrecorddataset(image_dir: str = PHOTO_TFREC_DIR) -> tf.data.TFRecordDataset:
    """The set of photos as a `TFRecordDataset`.

    Returns:
        The photo dataset in `TFRecordDataset` format.
    """

    return read_tfrecorddataset(filenames=photo_tfrec_filenames(image_dir=image_dir))


def load_dataset(monet_dir: str, photo_dir: str, batch_size: int = 1) -> tf.data.Dataset:
    """Load the dataset to be used for training the CycleGAN.

    Args:
        batch_size: Batch size of the dataset.
        monet_dir: Directory of Monet painting images.
        photo_dir: Directory of photo images.

    Returns:
        The Monet paintings and photos zipped into one dataset.
    """

    monets = monet_tfrecorddataset(image_dir=monet_dir).batch(batch_size, drop_remainder=True)
    photos = photo_tfrecorddataset(image_dir=photo_dir).batch(batch_size, drop_remainder=True)
    return tf.data.Dataset.zip((monets, photos))
