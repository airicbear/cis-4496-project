import tensorflow as tf

USING_KAGGLE = False
AUTOTUNE = tf.data.experimental.AUTOTUNE
BATCH_SIZE = 1
IMAGE_SIZE = [256, 256]
CHANNELS = 3
DATA_PATH = '../Sample_Data/Raw/Small_Dataset'
MONET_TFREC_DIR = f'{DATA_PATH}/monet_tfrec'
PHOTO_TFREC_DIR = f'{DATA_PATH}/photo_tfrec'
KAGGLE_DATASET_URL = 'https://github.com/airicbear/cis-4496-project/releases/download/kaggle-dataset/kaggle-dataset.zip'
KAGGLE_DATASET_PATH = '../Sample_Data/Raw/Kaggle_Dataset'
MONET_GENERATOR_WEIGHT_PATH = 'photo2monet.h5'
PHOTO_GENERATOR_WEIGHT_PATH = 'monet2photo.h5'

if USING_KAGGLE:
    from kaggle_datasets import KaggleDatasets

    DATA_PATH = KaggleDatasets().get_gcs_path()

try:
    tpu = tf.distribute.cluster_resolver.TPUClusterResolver()
    tf.config.experimental_connect_to_cluster(tpu)
    tf.tpu.experimental.initialize_tpu_system(tpu)
    strategy = tf.distribute.experimental.TPUStrategy(tpu)
except:
    strategy = tf.distribute.get_strategy()
