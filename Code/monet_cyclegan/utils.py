import io
import re
import zipfile
from pathlib import Path
from typing import List

import numpy as np
import requests
import tensorflow as tf
from PIL import Image
from numpy import uint8, ndarray

from .consts import IMAGE_SIZE, CHANNELS


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
    """Read and decode an image file to an uint8 `Tensor`

    Args:
        path: Path of the image.
        width: The width of the decoded image.
        height: The height of the decoded image.
        channels: Number of color channels for the decoded image.

    Returns:
        The image decoded as an uint8 `Tensor`.
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


def save_image(image: ndarray, output_path: str) -> None:
    """Save an image.

    Args:
        image: The image to be saved as a NumPy array.
        output_path: Path of the generated image.
    """

    make_directory(output_path, make_parent=True)

    image_array = Image.fromarray(image)
    image_array.save(output_path)


def tensor_to_image(image: tf.Tensor) -> ndarray:
    """Convert a tensor image to a NumPy array readable as a Pillow Image.

    Args:
        image: The image as a tensor.

    Returns:
        The image as a Pillow Image-compatible NumPy array.
    """

    result = image.numpy()
    result = result * 127.5 + 127.5
    result = result.astype(uint8)
    return result


def make_directory(path: str, make_parent: bool = False) -> None:
    """Make a directory.

    Args:
        path: Path of the directory to be created.
        make_parent: Make the path's parent directory instead of the path itself.
    """

    dir_path = Path(path)

    if make_parent:
        dir_path = dir_path.parent

    dir_path.mkdir(parents=True, exist_ok=True)


def random_number(minval: float, maxval: float, dtype: tf.dtypes.DType = tf.float32):
    """Generate a random number in an interval.

    The number is randomly sampled from a uniform distribution.

    Args:
        minval: The lower bound of the interval.
        maxval: The upper bound of the interval.
        dtype: The data type of the random number.

    Returns:
        A random number in the specified interval.
    """

    return tf.random.uniform([], minval=minval, maxval=maxval, dtype=dtype)


def count_tfrec_items(tfrec_filenames: List[str]) -> int:
    """Count the total number of images in a set of TFREC files.

    Args:
        tfrec_filenames: List of TFREC filenames.

    Returns:
        The total number of images in the TFREC filenames.
    """
    regexp = re.compile(r"-([0-9]*)\.")
    n = [int(regexp.search(filename).group(1)) for filename in tfrec_filenames]
    return int(np.sum(n))
