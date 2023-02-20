import sys
from pathlib import Path

from PIL import Image
from numpy import uint8

from .create_model import create_model
from .datasets import photo_dataset

if __name__ == '__main__':
    """
    Generates images from the trained model
    """

    USING_KAGGLE = False
    EPOCHS = 1

    # Get photo data from datasets.py:
    photos = photo_dataset(USING_KAGGLE)

    # Try to create generator models using create_model.py
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
