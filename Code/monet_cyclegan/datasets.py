import tensorflow as tf

from .consts import USING_KAGGLE
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


def load_dataset(batch_size: int = 1) -> tf.data.Dataset:
    monets = monet_dataset().batch(batch_size, drop_remainder=True)
    photos = photo_dataset().batch(batch_size, drop_remainder=True)
    return tf.data.Dataset.zip((monets, photos))
