from typing import Callable

import tensorflow as tf

from ..consts import BATCH_SIZE, AUTOTUNE


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

    if augment:
        dataset = dataset.map(augment, num_parallel_calls=AUTOTUNE)

    if repeat:
        dataset = dataset.repeat()

    if shuffle:
        dataset = dataset.shuffle(2048)

    if sample_size >= 0:
        dataset = dataset.take(sample_size)

    dataset = dataset.batch(batch_size, drop_remainder=True)
    dataset = dataset.cache()
    dataset = dataset.prefetch(AUTOTUNE)

    return dataset
