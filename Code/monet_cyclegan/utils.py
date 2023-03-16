import io
import logging
import os
import re
import zipfile
from argparse import Namespace
from datetime import datetime
from pathlib import Path
from typing import List

import cv2
import numpy as np
import requests
import tensorflow as tf
from PIL import Image
from numpy import uint8, ndarray

from .consts import IMAGE_SIZE, CHANNELS, SIZE

logger = logging.getLogger(__name__)


def decode_image(image: tf.Tensor,
                 width: int,
                 height: int,
                 channels: int) -> tf.Tensor:
    """Decode a JPEG encoded image to a float32 `Tensor`.

    Args:
        image: The JPEG encoded image.
        width: The width of the decoded image.
        height: The height of the decoded image.
        channels: Number of color channels for the decoded image.

    Returns:
        The JPEG image decoded as a float32 `Tensor`.
    """

    image = tf.image.decode_jpeg(image, channels=channels)
    image = (tf.cast(image, tf.float32) / 127.5) - 1
    image = tf.reshape(image, [width, height, channels])
    return image


def read_image(path: str,
               width: int,
               height: int,
               channels: int) -> tf.Tensor:
    """Read and decode an image file to an float32 `Tensor`

    Args:
        path: Path of the image.
        width: The width of the decoded image.
        height: The height of the decoded image.
        channels: Number of color channels for the decoded image.

    Returns:
        The image decoded as an float32 `Tensor`.
    """

    image = tf.io.read_file(path)
    image = decode_image(image, width, height, channels)
    image = tf.expand_dims(image, axis=0)
    return image


def read_tfrecord(example: tf.Tensor,
                  width: int,
                  height: int,
                  channels: int) -> tf.Tensor:
    """Decode a TFREC encoded image to an float32 `Tensor`.

    Args:
        example: The TFREC encoded image.
        width: The width of the decoded image.
        height: The height of the decoded image.
        channels: Number of color channels for the decoded image.

    Returns:
        The TFREC image decoded as an float32 `Tensor`.
    """

    tfrecord_format = {
        'image': tf.io.FixedLenFeature([], tf.string),
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

    logger.info(
        f'Reading TFRecordDataset (image_width={image_width}, image_height={image_height}, channels={channels}, num_parallel_calls={num_parallel_calls}, filenames={filenames}).')

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

    logger.info(f'Downloading file from "{url}".')

    r = requests.get(url, stream=True)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(output_dir)

    logger.info(f"Extracted file(s) to '{output_dir}'.")


def get_filenames(image_dir: str, ext: str) -> List[str]:
    """Get the list of filenames in an image directory.

    Args:
        image_dir: Directory with images.
        ext: File extension for image format.

    Returns:
        List of filenames in the image directory.
    """

    image_dir = image_dir.strip('/')

    logger.info(f"Getting filenames from '{image_dir}'.")

    filenames = tf.io.gfile.glob(f'{image_dir}/*.{ext}')

    if len(filenames) == 0:
        logger.warning(f"Could not find any '{ext}' files in '{image_dir}'.")
    else:
        logger.info(f'Found {filenames}.')

    return filenames


def save_image(image: ndarray, output_path: str) -> None:
    """Save an image.

    Args:
        image: The image to be saved as a NumPy array.
        output_path: Path of the generated image.
    """

    logger.info(f"Saving image to '{output_path}'.")

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

    if not os.path.isdir(dir_path):
        dir_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Made a directory at '{dir_path}'.")


def random_number(minval: float, maxval: float, dtype: tf.dtypes.DType = tf.float32) -> float:
    """Generate a random number in an interval.

    The number is randomly sampled from a uniform distribution.

    Args:
        minval: The lower bound of the interval.
        maxval: The upper bound of the interval.
        dtype: The data type of the random number.

    Returns:
        A random number in the specified interval.
    """

    result = tf.random.uniform([], minval=minval, maxval=maxval, dtype=dtype)
    result = float(result)

    return result


def count_tfrec_items(tfrec_filenames: List[str]) -> int:
    """Count the total number of images in a set of TFREC files.

    Args:
        tfrec_filenames: List of TFREC filenames.

    Returns:
        The total number of images in the TFREC filenames.
    """

    logger.info(f'Counting number of images in {tfrec_filenames}.')

    regexp = re.compile(r"-([0-9]*)\.")
    n = [int(regexp.search(filename).group(1)) for filename in tfrec_filenames]
    result = int(np.sum(n))

    logger.info(f'Found {result} images.')

    return result


def configure_logger(log_dir: str) -> None:
    """Configure the logging system to output log files to the given directory.

    Args:
        log_dir: Directory where log files will be stored.
    """

    make_directory(log_dir)

    log_file = f"{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}.log"

    logging.basicConfig(filename=f'{log_dir}/{log_file}',
                        filemode='w',
                        format='%(asctime)s.%(msecs)03d %(name)s.%(funcName)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.DEBUG)


def log_args(args: Namespace) -> None:
    """Log all arguments from a given `Namespace` object.

    Args:
        args: The `Namespace` object.
    """

    for arg, value in sorted(vars(args).items()):
        logging.info(f'{arg}: {value}')


def _bytes_feature(value: bytes) -> tf.train.Feature:
    """Returns a bytes_list from a string / byte

      Args:
          value - A string/byte.
      """

    if isinstance(value, type(tf.constant(0))):
        value = value.numpy()  # BytesList won't unpack a string from an EagerTensor.
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def serialize_example(image: str) -> any:
    """This function works to serialize an image path and returns a binary string

    Args:
      image: An image path to a JPG file.
    """

    feature = {
        'image': _bytes_feature(image),
    }
    example_proto = tf.train.Example(features=tf.train.Features(feature=feature))
    return example_proto.SerializeToString()


def generate_tfrec_records(input_dir: str,
                           output_dir: str,
                           artist: str,
                           ext: str) -> None:
    """This function takes a path to a list of jpg files and generates TFREC records

    This code and the two above functions were gotten from this link
    https://www.kaggle.com/code/dimitreoliveira/monet-paintings-berkeley-tfrecords-256x256

    Args:
        input_dir: A path to a directory that holds JPG files.
        output_dir: Path to the output directory.
        artist: Name of the artist.
        ext: File extension of the images.
    """

    imgs = tf.io.gfile.glob(f'{input_dir}/*.{ext}')

    CT = len(imgs) // SIZE + int(len(imgs) % SIZE != 0)

    make_directory(output_dir)

    for j in range(CT):
        print()
        print('Writing TFRecord %i of %i...' % (j, CT))
        CT2 = min(SIZE, len(imgs) - j * SIZE)
        with tf.io.TFRecordWriter(f'{output_dir}/{artist}{j:02d}-{CT2}.tfrec') as writer:
            for k in range(CT2):
                img = cv2.imread(f'{imgs[SIZE * j + k]}')
                print(f"cv2.imread({imgs[SIZE * j + k]})")
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                img = cv2.imencode('.jpg', img, (cv2.IMWRITE_JPEG_QUALITY, 94))[1].tostring()
                example = serialize_example(img)
                writer.write(example)
