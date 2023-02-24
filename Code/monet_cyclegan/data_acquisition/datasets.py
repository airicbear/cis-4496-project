import os

import tensorflow as tf

from .utils import read_tfrecorddataset, get_filenames
from ..consts import MONET_TFREC_DIR, PHOTO_TFREC_DIR


def load_dataset(monet_dir: str = MONET_TFREC_DIR,
                 photo_dir: str = PHOTO_TFREC_DIR,
                 image_ext: str = 'tfrec',
                 batch_size: int = 1,
                 monet_sample_size: int = -1,
                 photo_sample_size: int = -1,
                 random_sample: bool = False) -> tf.data.Dataset:
    """Load the dataset to be used for training the CycleGAN.

    Args:
        monet_dir: Directory of Monet painting images.
        photo_dir: Directory of photo images.
        image_ext: File extension of the images.
        batch_size: Batch size of each dataset.
        monet_sample_size: The sample size of the Monet paintings to train on.
                           If this value is -1 or greater than the size of the Monet painting dataset,
                           then the entire dataset will be used.
        photo_sample_size: The sample size of the photos to train on.
                           If this value is -1 or greater than the size of the photo dataset,
                           then the entire dataset will be used.

    Returns:
        The Monet paintings and photos zipped into one dataset.
    """

    if not os.path.isdir(monet_dir):
        raise OSError(f'Can\'t find directory "{monet_dir}".')

    if not os.path.isdir(photo_dir):
        raise OSError(f'Can\'t find directory "{photo_dir}".')

    if image_ext == 'tfrec':
        monet_dataset = read_tfrecorddataset(filenames=get_filenames(image_dir=monet_dir, ext=image_ext))
        photo_dataset = read_tfrecorddataset(filenames=get_filenames(image_dir=photo_dir, ext=image_ext))
    else:
        raise ValueError(f'Invalid file extension {image_ext}.')

    monet_dataset = monet_dataset.take(monet_sample_size)
    photo_dataset = photo_dataset.take(photo_sample_size)

    if random_sample:
        monet_dataset = monet_dataset.shuffle(monet_sample_size)
        photo_dataset = photo_dataset.shuffle(photo_sample_size)

    monet_dataset = monet_dataset.batch(batch_size, drop_remainder=True)
    photo_dataset = photo_dataset.batch(batch_size, drop_remainder=True)

    return tf.data.Dataset.zip((monet_dataset, photo_dataset))
