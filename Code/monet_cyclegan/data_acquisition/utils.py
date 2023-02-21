import io
import zipfile
from typing import List

import requests
import tensorflow as tf

from ..consts import IMAGE_SIZE


def decode_image(image: tf.io.FixedLenFeature) -> tf.Tensor:
    """Decode a JPEG encoded image to an uint8 `Tensor`.

    Args:
        image: The JPEG encoded image.

    Returns:
        The JPEG image decoded as an uint8 `Tensor`.
    """

    image = tf.image.decode_jpeg(image, channels=3)
    image = (tf.cast(image, tf.float32) / 127.5) - 1
    image = tf.reshape(image, [*IMAGE_SIZE, 3])
    return image


def read_tfrecord(example: tf.Tensor) -> tf.Tensor:
    """Decode a TFREC encoded image to an uint8 `Tensor`.

    Args:
        example: The TFREC encoded image.

    Returns:
        The TFREC image decoded as an uint8 `Tensor`.
    """

    tfrecord_format = {
        'image_name': tf.io.FixedLenFeature([], tf.string),
        'image': tf.io.FixedLenFeature([], tf.string),
        'target': tf.io.FixedLenFeature([], tf.string)
    }
    example = tf.io.parse_single_example(example, tfrecord_format)
    image = decode_image(example['image'])
    return image


def read_tfrecorddataset(filenames: List[str]) -> tf.data.TFRecordDataset:
    """Construct a `TFRecordDataset` from a set of TFREC encoded images.

    Args:
        filenames: The list of filenames of each TFREC encoded image.

    Returns:
        A `TFRecordDataset` of the TFREC encoded images.
    """

    dataset = tf.data.TFRecordDataset(filenames)
    dataset = dataset.map(read_tfrecord, num_parallel_calls=tf.data.experimental.AUTOTUNE)
    return dataset


def download_extract_zip(url: str, output_dir: str) -> None:
    """Download and extract a zip file from a URL.

    Args:
        url: The URL of the zip file.
        output_dir: The directory where the zip file will be extracted to.
    """

    r = requests.get(url, stream=True)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(output_dir)
