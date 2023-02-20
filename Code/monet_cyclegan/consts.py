import tensorflow as tf

USING_KAGGLE = False
AUTOTUNE = tf.data.experimental.AUTOTUNE
BATCH_SIZE = 1
IMAGE_SIZE = [256, 256]

try:
    tpu = tf.distribute.cluster_resolver.TPUClusterResolver()
    tf.config.experimental_connect_to_cluster(tpu)
    tf.tpu.experimental.initialize_tpu_system(tpu)
    strategy = tf.distribute.experimental.TPUStrategy(tpu)
except:
    strategy = tf.distribute.get_strategy()
