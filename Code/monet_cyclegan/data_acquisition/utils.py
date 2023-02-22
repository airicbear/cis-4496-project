import io
import zipfile
from typing import List

import requests
import tensorflow as tf

from ..consts import IMAGE_SIZE, CHANNELS


def decode_image(image: tf.Tensor,
                 width: int,
                 height: int,
                 channels: int) -> tf.Tensor:
    """Decode a JPEG encoded image to an uint8 `Tensor`.

    Args:
        image: The JPEG encoded image.
        width: The width of the decoded image.
        height: The height of the decoded image.
        channels: Number of color channels for the decoded image.

    Returns:
        The JPEG image decoded as an uint8 `Tensor`.
    """

    image = tf.image.decode_jpeg(image, channels=channels)
    image = (tf.cast(image, tf.float32) / 127.5) - 1
    image = tf.reshape(image, [width, height, channels])
    return image


def read_image(path: str,
               width: int,
               height: int,
               channels: int) -> tf.Tensor:
    """Read and decode a JPEG image file to an uint8 `Tensor`

    Args:
        path: Path of the JPEG image.
        width: The width of the decoded image.
        height: The height of the decoded image.
        channels: Number of color channels for the decoded image.

    Returns:
        The JPEG image decoded as an uint8 `Tensor`.
    """

    image = tf.io.read_file(path)
    image = decode_image(image, width, height, channels)
    image = tf.expand_dims(image, axis=0)
    return image


def read_tfrecord(example: tf.Tensor,
                  width: int,
                  height: int,
                  channels: int) -> tf.Tensor:
    """Decode a TFREC encoded image to an uint8 `Tensor`.

    Args:
        example: The TFREC encoded image.
        width: The width of the decoded image.
        height: The height of the decoded image.
        channels: Number of color channels for the decoded image.

    Returns:
        The TFREC image decoded as an uint8 `Tensor`.
    """

    tfrecord_format = {
        'image_name': tf.io.FixedLenFeature([], tf.string),
        'image': tf.io.FixedLenFeature([], tf.string),
        'target': tf.io.FixedLenFeature([], tf.string)
    }
    example = tf.io.parse_single_example(example, tfrecord_format)
    image = decode_image(image=example['image'],
                         width=width,
                         height=height,
                         channels=channels)
    return image


def read_tfrecorddataset(filenames: List[str],
                         image_width: int = IMAGE_SIZE[0],
                         image_height: int = IMAGE_SIZE[1],
                         channels: int = CHANNELS,
                         num_parallel_calls: int = tf.data.experimental.AUTOTUNE) -> tf.data.TFRecordDataset:
    """Construct a `TFRecordDataset` from a set of TFREC encoded images.

    Args:
        filenames: The list of filenames of each TFREC encoded image.
        image_width: The width of the images.
        image_height: The height of the images.
        channels: The number of color channels of the images.
        num_parallel_calls: Number TFREC images to process asynchronously in parallel.
                            If not specified, images will be processed sequentially.
                            By default, this is set to `AUTOTUNE` which sets this
                            parameter dynamically based on available CPU.

    Returns:
        A `TFRecordDataset` of the TFREC encoded images.
    """

    dataset = tf.data.TFRecordDataset(filenames)
    dataset = dataset.map(lambda x: read_tfrecord(example=x,
                                                  width=image_width,
                                                  height=image_height,
                                                  channels=channels),
                          num_parallel_calls=num_parallel_calls)
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


def get_filenames(image_dir: str, ext: str) -> List[str]:
    """Get the list of filenames in an image directory.

    Args:
        image_dir: Directory with images.
        ext: File extension for image format.

    Returns:
        List of filenames in the image directory.
    """

    return tf.io.gfile.glob(f'{image_dir}/*.{ext}')
