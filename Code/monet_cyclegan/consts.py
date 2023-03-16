import tensorflow as tf

USING_KAGGLE = False
AUTOTUNE = tf.data.experimental.AUTOTUNE
SEED = 42
BATCH_SIZE = 1
IMAGE_SIZE = [256, 256]
SIZE = 60
CHANNELS = 3
DATA_PATH = '../Sample_Data/Raw/Small_Dataset'
MONET_TFREC_DIR = f'{DATA_PATH}/monet_tfrec'
PHOTO_TFREC_DIR = f'{DATA_PATH}/photo_tfrec'
KAGGLE_DATASET_URL = 'https://github.com/airicbear/cis-4496-project/releases/download/kaggle-dataset/kaggle-dataset.zip'
KAGGLE_DATASET_PATH = '../Sample_Data/Raw/Kaggle_Dataset'
PHOTO2PAINTING_WEIGHTS = 'photo2painting'
PAINTING2PHOTO_WEIGHTS = 'painting2photo'
LOSS_RATE = 2e-4
EPOCHS = 1
BUILD_DIR = './build'

# Set global seed
tf.random.set_seed(SEED)

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
