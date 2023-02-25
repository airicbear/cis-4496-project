import os

import tensorflow as tf

from ..consts import IMAGE_SIZE, CHANNELS
from ..utils import random_number, tensor_to_image, read_image, save_image, make_directory, get_filenames, \
    read_tfrecorddataset


def random_crop(image: tf.Tensor, width: int, height: int, channels: int) -> tf.Tensor:
    """Randomly crop an image.

    Args:
        image: The image to be randomly cropped.
        width: The width of the cropped image.
        height: The height of the cropped image.
        channels: The number of channels of the cropped image.

    Returns:
        The randomly cropped image.
    """

    probability = random_number(0, 1.0)

    if probability > 0.5:
        image = tf.image.resize(image, [width + 30, height + 30])
        image = tf.image.random_crop(image, size=[width, height, channels])

        if probability > 0.9:
            image = tf.image.resize(image, [width + 44, height + 44])
            image = tf.image.random_crop(image, size=[width, height, channels])

    return image


def random_rotate(image: tf.Tensor) -> tf.Tensor:
    """Randomly rotate an image by 90 degrees.

    Args:
        image: The image to be randomly rotated.

    Returns:
        The randomly rotated image.
    """

    probability = random_number(0, 1.0)

    if probability > 0.9:
        image = tf.image.rot90(image, k=3)
    elif probability > 0.7:
        image = tf.image.rot90(image, k=2)
    elif probability > 0.5:
        image = tf.image.rot90(image, k=1)

    return image


def random_flip(image: tf.Tensor) -> tf.Tensor:
    """Randomly flip an image.

    Args:
        image: The image to be randomly flipped.

    Returns:
        The randomly flipped image
    """

    probability = random_number(0, 1.0)

    if probability > 0.6:
        image = tf.image.random_flip_left_right(image)
        image = tf.image.random_flip_up_down(image)

        if probability > 0.9:
            image = tf.image.transpose(image)

    return image


def process_image(image: tf.Tensor) -> tf.Tensor:
    """Randomly crop, resize, rotate and/or flip an image.

    Args:
        image: The image to be processed.

    Returns:
        The processed image.
    """

    image = random_crop(image, width=IMAGE_SIZE[0], height=IMAGE_SIZE[1], channels=CHANNELS)
    image = random_rotate(image)
    image = random_flip(image)

    return image


def save_preprocessed_image(input_path: str, output_dir: str) -> None:
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f'Could not find file "{input_path}".')

    image = read_image(path=input_path,
                       width=IMAGE_SIZE[0],
                       height=IMAGE_SIZE[1],
                       channels=CHANNELS)[0]

    processed_image = process_image(image=image)
    processed_image = tensor_to_image(image=processed_image)

    filename = os.path.basename(input_path)

    save_image(image=processed_image,
               output_path=f'{output_dir}/preprocessed-{filename}')


def save_preprocessed_images(input_dir: str,
                             output_dir: str,
                             input_ext: str,
                             sample_size: int,
                             randomize: bool,
                             with_original: bool) -> None:
    if not os.path.isdir(input_dir):
        raise FileNotFoundError(f'Could not find directory "{input_dir}".')

    if input_ext == 'tfrec':
        images = read_tfrecorddataset(filenames=get_filenames(input_dir, ext=input_ext))

        if sample_size:
            images = images.take(sample_size)

        if randomize:
            images = images.shuffle(sample_size)

        images = images.batch(1)

        for i, image in enumerate(images):
            processed_image = process_image(image[0])
            processed_image = tensor_to_image(processed_image)

            save_image(image=processed_image,
                       output_path=f'{output_dir}-preprocessed/preprocessed-{i}.jpg')

            if with_original:
                original_image = tensor_to_image(image)
                save_image(image=original_image[0],
                           output_path=f'{output_dir}-preprocessed-original/original-preprocessed-{i}.jpg')

    else:
        make_directory(f'{input_dir}-preprocessed')

        for i, filename in enumerate(get_filenames(image_dir=input_dir, ext=input_ext)):
            image = read_image(path=filename,
                               width=IMAGE_SIZE[0],
                               height=IMAGE_SIZE[1],
                               channels=CHANNELS)[0]

            processed_image = process_image(image)
            processed_image = tensor_to_image(processed_image)

            filename = os.path.basename(filename)

            save_image(image=processed_image,
                       output_path=f'{input_dir}-preprocessed/preprocessed-{filename}')
