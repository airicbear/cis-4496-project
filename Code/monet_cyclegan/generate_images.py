import tensorflow as tf
import sys
from pathlib import Path
from numpy import uint8
from PIL import Image

from .datasets import photo_dataset
from .create_model import create_model


if __name__ == '__main__':
    USING_KAGGLE = False
    EPOCHS = 1

    photos = photo_dataset(USING_KAGGLE)
    try:
        model = create_model()
        model.monet_generator.load_weights(f'photo2monet_epoch{EPOCHS}.h5')
        model.photo_generator.load_weights(f'monet2photo_epoch{EPOCHS}.h5')
    except:
        sys.exit('Model not trained yet.')

    Path('../submission_images').mkdir(parents=True, exist_ok=True)

    i = 1
    for img in photos:
        prediction = model.monet_generator(img, training=False)[0].numpy()
        prediction = (prediction * 127.5 + 127.5).astype(uint8)
        im = Image.fromarray(prediction)
        im.save(f'../submission_images/{i}.jpg')
        i += 1
