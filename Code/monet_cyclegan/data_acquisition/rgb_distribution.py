import os
from typing import Tuple, List

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import tensorflow as tf

from ..consts import IMAGE_SIZE, CHANNELS
from ..utils import read_image, tensor_to_image, read_tfrecorddataset, get_filenames, count_tfrec_items


def get_image_rgb_distribution(image: tf.Tensor) -> Tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
    """Get the RGB distribution of an image.

    Args:
        image: The image.

    Returns:
        Tuple of tensors for each channel.
    """

    image = tensor_to_image(image=image)

    red_channel = tf.reshape(tensor=image[:, :, 0], shape=[-1])
    green_channel = tf.reshape(tensor=image[:, :, 1], shape=[-1])
    blue_channel = tf.reshape(tensor=image[:, :, 2], shape=[-1])

    return red_channel, green_channel, blue_channel


def get_jpg_folder_rgb_distribution(filenames: List[str],
                                    width: int,
                                    height: int,
                                    num_images: int) -> Tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
    """Get JPG folder RGB distribution.

    Args:
        filenames: The list of JPG files.
        width: The width of the image.
        height: The height of the image.
        num_images: The number of JPG images in the folder.

    Returns:
        Tuple of tensors for each RGB channel.
    """

    red_channel = np.zeros(shape=(num_images * width * height,))
    green_channel = np.zeros(shape=(num_images * width * height,))
    blue_channel = np.zeros(shape=(num_images * width * height,))

    for i, filename in enumerate(filenames):
        image = read_image(path=filename,
                           width=IMAGE_SIZE[0],
                           height=IMAGE_SIZE[1],
                           channels=CHANNELS)[0]

        r, g, b = get_image_rgb_distribution(image)
        start_index = r.shape[0] * i
        end_index = r.shape[0] * (i + 1)
        red_channel[start_index:end_index] = r.numpy()
        green_channel[start_index:end_index] = g.numpy()
        blue_channel[start_index:end_index] = b.numpy()

    red_channel = tf.convert_to_tensor(red_channel)
    green_channel = tf.convert_to_tensor(green_channel)
    blue_channel = tf.convert_to_tensor(blue_channel)

    return red_channel, green_channel, blue_channel


def get_tfrecorddataset_rgb_distribution(images: tf.data.TFRecordDataset,
                                         width: int,
                                         height: int,
                                         num_images: int) -> Tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
    """Get the RGB distribution of an entire `TFRecordDataset`.

    Args:
        images: The `TFRecordDataset`.
        width: The width of the image.
        height: The height of the image.
        num_images: The number of images in the dataset.

    Returns:
        Tuple of tensors for each RGB channel.
    """

    red_channel = np.zeros(shape=(num_images * width * height,))
    green_channel = np.zeros(shape=(num_images * width * height,))
    blue_channel = np.zeros(shape=(num_images * width * height,))

    for i, image in enumerate(images):
        r, g, b = get_image_rgb_distribution(image)
        start_index = r.shape[0] * i
        end_index = r.shape[0] * (i + 1)
        red_channel[start_index:end_index] = r.numpy()
        green_channel[start_index:end_index] = g.numpy()
        blue_channel[start_index:end_index] = b.numpy()

    red_channel = tf.convert_to_tensor(red_channel)
    green_channel = tf.convert_to_tensor(green_channel)
    blue_channel = tf.convert_to_tensor(blue_channel)

    return red_channel, green_channel, blue_channel


def plot_rgb_density(red_channel: tf.Tensor,
                     green_channel: tf.Tensor,
                     blue_channel: tf.Tensor,
                     exclude_zeros: bool = True,
                     title: str = None,
                     xlabel: str = None,
                     ylabel: str = None) -> None:
    """Plot the RGB distribution as a density plot.

    Args:
        red_channel: The red channel values.
        green_channel: The green channel values.
        blue_channel: The blue channel values.
        exclude_zeros: Exclude zero RGB values if set to True.
        title: The title of the plot.
        xlabel: The label of the x-axis.
        ylabel: The label of the y-axis.
    """

    if exclude_zeros:
        red_channel = red_channel[red_channel != 0]
        green_channel = green_channel[green_channel != 0]
        blue_channel = blue_channel[blue_channel != 0]

    palette = ['red', 'green', 'blue']
    sns.displot(data=[red_channel, green_channel, blue_channel],
                palette=sns.color_palette(palette, 3),
                kind='kde',
                fill=True,
                legend=False)
    plt.legend(['blue', 'green', 'red'])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.show(block=True)


def plot_rgb_distribution(input_path: str,
                          ext: str,
                          num: int,
                          title: str,
                          xlabel: str,
                          ylabel: str,
                          exclude_zeros: bool) -> None:
    """Plot the RGB distribution of given image(s).

    Args:
        input_path: The path of the image(s).
        ext: The file extension of the image(s).
        bins: Number of bins.
        num: The number of images to use.
        title: The title of the plot.
        exclude_zeros: Exclude zeros if True.
    """

    if os.path.isdir(input_path) and ext == 'tfrec':
        filenames = get_filenames(image_dir=input_path, ext='tfrec')
        count_images = count_tfrec_items(tfrec_filenames=filenames)
        images = read_tfrecorddataset(filenames=filenames)
        if num >= 0:
            images = images.take(num)
        r, g, b = get_tfrecorddataset_rgb_distribution(images=images,
                                                       width=IMAGE_SIZE[0],
                                                       height=IMAGE_SIZE[1],
                                                       num_images=count_images)

        plot_rgb_density(r, g, b, xlabel=xlabel, ylabel=ylabel, title=title, exclude_zeros=exclude_zeros)


    elif os.path.isdir(input_path) and ext == 'jpg':
        filenames = get_filenames(image_dir=input_path, ext='jpg')
        if num >= 0:
            filenames = filenames[:num]
        count_images = len(filenames)
        r, g, b = get_jpg_folder_rgb_distribution(filenames=filenames,
                                                  width=IMAGE_SIZE[0],
                                                  height=IMAGE_SIZE[1],
                                                  num_images=count_images)

        plot_rgb_density(r, g, b, xlabel=xlabel, ylabel=ylabel, title=title, exclude_zeros=exclude_zeros)

    elif os.path.isfile(input_path):
        image = read_image(path=input_path,
                           width=IMAGE_SIZE[0],
                           height=IMAGE_SIZE[1],
                           channels=CHANNELS)[0]

        r, g, b = get_image_rgb_distribution(image)

        plot_rgb_density(r, g, b, xlabel=xlabel, ylabel=ylabel, title=title, exclude_zeros=exclude_zeros)
