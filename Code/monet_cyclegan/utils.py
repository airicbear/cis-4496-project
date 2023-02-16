import tensorflow as tf

def decode_image(image: tf.io.FixedLenFeature, image_size: 'list[int]' = [256, 256]) -> tf.Tensor:
    image = tf.image.decode_jpeg(image, channels=3)
    image = (tf.cast(image, tf.float32) / 127.5) - 1
    image = tf.reshape(image, [*image_size, 3])
    return image

def read_tfrecord(example: tf.Tensor) -> tf.Tensor:
    tfrecord_format = {
        'image_name': tf.io.FixedLenFeature([], tf.string),
        'image': tf.io.FixedLenFeature([], tf.string),
        'target': tf.io.FixedLenFeature([], tf.string)
    }
    example = tf.io.parse_single_example(example, tfrecord_format)
    image = decode_image(example['image'])
    return image

def read_tfrecords(filenames: 'list[str]') -> tf.data.TFRecordDataset:
    dataset = tf.data.TFRecordDataset(filenames)
    dataset = dataset.map(read_tfrecord, num_parallel_calls=tf.data.experimental.AUTOTUNE)
    return dataset
