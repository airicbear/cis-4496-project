"""
Generates images from the trained model.
"""

import argparse
import os
import sys
from pathlib import Path

from PIL import Image
from numpy import uint8

from .load_model import load_cyclegan_model
from ..consts import DATA_PATH
from ..data_acquisition.datasets import photo_dataset
from ..modeling.model import CycleGan


def generate_images(cyclegan_model: CycleGan,
                    data_path: str = DATA_PATH,
                    output_dir: str = '../submission_images') -> None:
    """Generate images from a CycleGAN model.

    Args:
        cyclegan_model: The CycleGAN model to be used for image generation.
        data_path: Path of the data folder.
        output_dir: Directory where the generated images will be stored.
    """

    photos = photo_dataset(data_path=data_path).batch(1)

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    i = 1
    for img in photos:
        prediction = cyclegan_model.monet_generator(img, training=False)[0].numpy()
        prediction = (prediction * 127.5 + 127.5).astype(uint8)
        im = Image.fromarray(prediction)
        im.save(f'{output_dir}/{i}.jpg')
        i += 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', type=str, default=DATA_PATH)
    args = parser.parse_args()

    if not os.path.isdir(args.data_path):
        print(f"ERROR: Can't find {args.data_path}")
        sys.exit(1)

    model = load_cyclegan_model()
    generate_images(cyclegan_model=model, data_path=args.data_path)


if __name__ == '__main__':
    main()
