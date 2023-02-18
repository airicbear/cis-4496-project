from typing import Callable, Dict, List

import tensorflow as tf

from .consts import strategy

with strategy.scope():
    def diff_augment(x: tf.Tensor,
                     policy: str = '',
                     channels_first: bool = False) -> tf.Tensor:
        if policy:
            if channels_first:
                x = tf.transpose(x, [0, 2, 3, 1])
            for p in policy.split(','):
                for fn in AUGMENT_FNS[p]:
                    x = fn(x)
            if channels_first:
                x = tf.transpose(x, [0, 3, 1, 2])
        return x


    def rand_brightness(x: tf.Tensor) -> tf.Tensor:
        magnitude: tf.Tensor

        magnitude = tf.random.uniform([tf.shape(x)[0], 1, 1, 1]) - 0.5
        x = x + magnitude

        return x


    def rand_saturation(x: tf.Tensor) -> tf.Tensor:
        magnitude: tf.Tensor
        x_mean: tf.Tensor

        magnitude = tf.random.uniform([tf.shape(x)[0], 1, 1, 1]) * 2
        x_mean = tf.reduce_mean(x, axis=3, keepdims=True) * 0.3333333333333333333
        x = (x - x_mean) * magnitude + x_mean

        return x


    def rand_contrast(x: tf.Tensor) -> tf.Tensor:
        magnitude: tf.Tensor
        x_mean: tf.Tensor

        magnitude = tf.random.uniform([tf.shape(x)[0], 1, 1, 1]) + 0.5
        x_mean = tf.reduce_mean(x, axis=[1, 2, 3], keepdims=True) * 5.086e-6
        x = (x - x_mean) * magnitude + x_mean

        return x


    def rand_translation(x: tf.Tensor,
                         ratio: float = 0.125) -> tf.Tensor:
        batch_size: tf.Tensor
        image_size: tf.Tensor
        shift: tf.Tensor
        translation_x: tf.Tensor
        translation_y: tf.Tensor
        grid_x: tf.Tensor
        grid_y: tf.Tensor

        batch_size = tf.shape(x)[0]
        image_size = tf.shape(x)[1:3]
        shift = tf.cast(tf.cast(image_size, tf.float32) * ratio + 0.5, tf.int32)
        translation_x = tf.random.uniform([batch_size, 1], -shift[0], shift[0] + 1, dtype=tf.int32)
        translation_y = tf.random.uniform([batch_size, 1], -shift[1], shift[1] + 1, dtype=tf.int32)
        grid_x = tf.clip_by_value(tf.expand_dims(tf.range(image_size[0], dtype=tf.int32), 0) + translation_x + 1,
                                  0,
                                  image_size[0] + 1)
        grid_y = tf.clip_by_value(tf.expand_dims(tf.range(image_size[1], dtype=tf.int32), 0) + translation_y + 1,
                                  0,
                                  image_size[1] + 1)
        x = tf.gather_nd(tf.pad(x, [[0, 0], [1, 1], [0, 0], [0, 0]]), tf.expand_dims(grid_x, -1), batch_dims=1)
        x = tf.transpose(tf.gather_nd(tf.pad(tf.transpose(x, [0, 2, 1, 3]), [[0, 0], [1, 1], [0, 0], [0, 0]]),
                                      tf.expand_dims(grid_y, -1),
                                      batch_dims=1),
                         [0, 2, 1, 3])

        return x


    def rand_cutout(x: tf.Tensor,
                    ratio: float = 0.5) -> tf.Tensor:
        batch_size: tf.Tensor
        image_size: tf.Tensor
        cutout_size: tf.Tensor
        offset_x: tf.Tensor
        offset_y: tf.Tensor
        grid_batch: tf.Tensor
        grid_x: tf.Tensor
        grid_y: tf.Tensor
        cutout_grid: tf.Tensor
        mask: tf.Tensor

        batch_size = tf.shape(x)[0]
        image_size = tf.shape(x)[1:3]
        cutout_size = tf.cast(tf.cast(image_size, tf.float32) * ratio + 0.5, tf.int32)
        offset_x = tf.random.uniform([tf.shape(x)[0], 1, 1],
                                     maxval=image_size[0] + (1 - cutout_size[0] % 2),
                                     dtype=tf.int32)
        offset_y = tf.random.uniform([tf.shape(x)[0], 1, 1],
                                     maxval=image_size[1] + (1 - cutout_size[1] % 2),
                                     dtype=tf.int32)
        grid_batch, grid_x, grid_y = tf.meshgrid(tf.range(batch_size, dtype=tf.int32),
                                                 tf.range(cutout_size[0], dtype=tf.int32),
                                                 tf.range(cutout_size[1], dtype=tf.int32),
                                                 indexing='ij')
        cutout_grid = tf.stack([grid_batch,
                                grid_x + offset_x - cutout_size[0] // 2,
                                grid_y + offset_y - cutout_size[1] // 2],
                               axis=-1)
        mask_shape = tf.stack([batch_size, image_size[0], image_size[1]])
        cutout_grid = tf.maximum(cutout_grid, 0)
        cutout_grid = tf.minimum(cutout_grid, tf.reshape(mask_shape - 1, [1, 1, 1, 3]))
        mask = tf.maximum(1 - tf.scatter_nd(cutout_grid,
                                            tf.ones([batch_size, cutout_size[0], cutout_size[1]], dtype=tf.float32),
                                            mask_shape),
                          0)
        x = x * tf.expand_dims(mask, axis=3)

        return x


    AUGMENT_FNS: Dict[str, List[Callable[[tf.Tensor], tf.Tensor]]] = {
        'color': [rand_brightness, rand_saturation, rand_contrast],
        'translation': [rand_translation],
        'cutout': [rand_cutout],
    }


    def aug_fn(image: tf.Tensor) -> tf.Tensor:
        return diff_augment(image,
                            "color,translation,cutout")


def data_augment_flip(image: tf.Tensor) -> tf.Tensor:
    print(f'Calling data_augment_flip on {image}')
    image = tf.image.random_flip_left_right(image)
    return image
