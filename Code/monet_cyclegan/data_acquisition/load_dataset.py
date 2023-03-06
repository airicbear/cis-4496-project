import logging
import os
from typing import Callable

import tensorflow as tf

from .preprocess import preprocess_dataset
from ..consts import MONET_TFREC_DIR, PHOTO_TFREC_DIR, BATCH_SIZE
from ..utils import read_tfrecorddataset, get_filenames

logger = logging.getLogger(__name__)


def load_dataset(painting_dir: str = MONET_TFREC_DIR,
                 photo_dir: str = PHOTO_TFREC_DIR,
                 image_ext: str = 'tfrec',
                 augment: Callable[[tf.Tensor], tf.Tensor] = None,
                 repeat: bool = True,
                 shuffle: bool = False,
                 batch_size: int = BATCH_SIZE,
                 painting_sample_size: int = -1,
                 photo_sample_size: int = -1) -> tf.data.Dataset:
    """Load the dataset to be used for training the CycleGAN.

    Args:
        painting_dir: Directory of painting images.
        photo_dir: Directory of photo images.
        image_ext: File extension of the images.
        batch_size: Batch size of each dataset.
        painting_sample_size: The sample size of the paintings to train on.
                              If this value is -1 or greater than the size of the painting dataset,
                              then the entire dataset will be used.
        photo_sample_size: The sample size of the photos to train on.
                           If this value is -1 or greater than the size of the photo dataset,
                           then the entire dataset will be used.
        augment: Augment the images if True.
        repeat: Duplicate each element in the dataset if True.
        shuffle: Shuffle the first 2048 elements of the dataset if True.
        batch_size: The size of the batch size.

    Returns:
        The paintings and photos zipped into one dataset.
    """

    logger.info(f"Loading dataset (painting_dir='{painting_dir}', photo_dir='{photo_dir}', image_ext='{image_ext}', "
                f'batch_size={batch_size}, painting_sample_size={painting_sample_size}, '
                f'photo_sample_size={photo_sample_size}, repeat={repeat}, '
                f'shuffle={shuffle}, batch_size={batch_size})')

    if not os.path.isdir(painting_dir):
        raise OSError(f'Can\'t find directory "{painting_dir}".')

    if not os.path.isdir(photo_dir):
        raise OSError(f'Can\'t find directory "{photo_dir}".')

    if image_ext == 'tfrec':
        painting_filenames = get_filenames(image_dir=painting_dir, ext=image_ext)
        photo_filenames = get_filenames(image_dir=photo_dir, ext=image_ext)

        painting_dataset = read_tfrecorddataset(filenames=painting_filenames)
        photo_dataset = read_tfrecorddataset(filenames=photo_filenames)

        painting_dataset = preprocess_dataset(painting_dataset,
                                              augment=augment,
                                              repeat=repeat,
                                              shuffle=shuffle,
                                              batch_size=batch_size,
                                              sample_size=painting_sample_size)

        photo_dataset = preprocess_dataset(photo_dataset,
                                           augment=augment,
                                           repeat=repeat,
                                           shuffle=shuffle,
                                           batch_size=batch_size,
                                           sample_size=photo_sample_size)
    else:
        raise ValueError(f'Invalid file extension {image_ext}.')

    return tf.data.Dataset.zip((painting_dataset, photo_dataset))
