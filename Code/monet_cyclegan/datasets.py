import tensorflow as tf

from .utils import read_tfrecords


def dataset_path(using_kaggle: bool = False, path: str = '../Sample_Data/Raw') -> str:
    """
    This function loads the Monet and photo images in `TFRecordDataset` format.
    :param using_kaggle: True if wanting to use Kaggle Datasets. False otherwise (default)
    :param path: default portion of path
    :return: path of dataset as string
    """
    if using_kaggle:
        from kaggle_datasets import KaggleDatasets
        return KaggleDatasets().get_gcs_path()
    else:
        return path


def monet_filenames(using_kaggle: bool = False):
    """
    :param using_kaggle: True if wanting to use Kaggle Datasets. False otherwise (default)
    :return: filenames for the monet painting.
    """
    return tf.io.gfile.glob(f'{dataset_path(using_kaggle)}/monet_tfrec/*.tfrec')


def photo_filenames(using_kaggle: bool = False):
    """
    :param using_kaggle: True if wanting to use Kaggle Datasets. False otherwise (default)
    :return: filenames for the photos
    """
    return tf.io.gfile.glob(f'{dataset_path(using_kaggle)}/photo_tfrec/*.tfrec')


def monet_dataset(using_kaggle: bool = False):
    """
    :param using_kaggle: True if wanting to use Kaggle Datasets. False otherwise (default)
    :return: the loaded Monet paintings in `TFRecordDataset` format.
    """
    return read_tfrecords(monet_filenames(using_kaggle)).batch(1)


def photo_dataset(using_kaggle: bool = False):
    """
    :param using_kaggle: True if wanting to use Kaggle Datasets. False otherwise (default)
    :return: the loaded photos in `TFRecordDataset` format.
    """
    return read_tfrecords(photo_filenames(using_kaggle)).batch(1)
