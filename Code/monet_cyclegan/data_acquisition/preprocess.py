import logging
from typing import Callable

import tensorflow as tf

from ..consts import BATCH_SIZE, AUTOTUNE

logger = logging.getLogger(__name__)


def preprocess_dataset(dataset: tf.data.TFRecordDataset,
                       augment: Callable[[tf.Tensor], tf.Tensor] = None,
                       repeat: bool = True,
                       shuffle: bool = True,
                       batch_size: int = BATCH_SIZE,
                       sample_size: int = -1) -> tf.data.TFRecordDataset:
    """Preprocess a dataset.

    Args:
        dataset: The dataset to be preprocessed.
        augment: Augment the images if True.
        repeat: Duplicate each element in the dataset if True.
        shuffle: Shuffle the first 2048 elements of the dataset if True.
        batch_size: The size of the batch size.
        sample_size: The size of the sample.

    Returns:
        The preprocessed dataset.
    """

    logger.info(f'Preprocessing dataset.')

    if repeat:
        logger.info('Duplicating images in dataset.')
        dataset = dataset.repeat()

    if shuffle:
        logger.info('Shuffling the first 2048 images in the dataset.')
        dataset = dataset.shuffle(2048)

    if sample_size >= 0:
        logger.info(f'Sampling {sample_size} images from the dataset.')
        dataset = dataset.take(sample_size)

    if augment:
        logger.info('Augmenting images in dataset.')
        dataset = dataset.map(augment, num_parallel_calls=AUTOTUNE)

    logger.info(f'Applying a batch size of {batch_size} to the dataset.')
    dataset = dataset.batch(batch_size, drop_remainder=True)
    dataset = dataset.cache()
    dataset = dataset.prefetch(AUTOTUNE)

    return dataset
