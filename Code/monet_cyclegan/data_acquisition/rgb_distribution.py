import os

import matplotlib.pyplot as plt
import tensorflow as tf

from ..consts import IMAGE_SIZE, CHANNELS
from ..utils import read_image, tensor_to_image


def plot_rgb_distribution(input_path: str, bins: int) -> None:
    """Plot the RGB distribution of a given image.

    Args:
        input_path: The path of the image.
        bins: Number of bins.
    """

    if not os.path.isfile(input_path):
        raise FileNotFoundError(f'Could not find file "{input_path}".')

    image = read_image(path=input_path,
                       width=IMAGE_SIZE[0],
                       height=IMAGE_SIZE[1],
                       channels=CHANNELS)[0]
    image = tensor_to_image(image=image)

    red_channel = tf.reshape(tensor=image[:, :, 0], shape=[-1]).numpy()
    green_channel = tf.reshape(tensor=image[:, :, 1], shape=[-1]).numpy()
    blue_channel = tf.reshape(tensor=image[:, :, 2], shape=[-1]).numpy()

    colors = ['red', 'green', 'blue']
    plt.title(f'RGB Distribution of "{input_path}"')
    plt.hist(x=[red_channel, blue_channel, green_channel], stacked=True, color=colors, bins=bins)
    plt.show(block=True)
