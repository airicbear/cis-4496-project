import tensorflow as tf

from .create_model import create_model
from .datasets import monet_dataset, photo_dataset


if __name__ == '__main__':
    USING_KAGGLE = False
    EPOCHS = 1

    monets = monet_dataset(USING_KAGGLE)
    photos = photo_dataset(USING_KAGGLE)
    model = create_model()
    model.fit(tf.data.Dataset.zip((monets, photos)), epochs=EPOCHS)
    model.monet_generator.save_weights(f'photo2monet_epoch{EPOCHS}.h5')
    model.photo_generator.save_weights(f'monet2photo_epoch{EPOCHS}.h5')
