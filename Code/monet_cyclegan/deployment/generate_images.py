"""
Generates images from the trained model.
"""

import os
import sys
from argparse import ArgumentParser

from .load_model import load_cyclegan_model
from .utils import translate_image, save_image, make_directory
from ..consts import IMAGE_SIZE, CHANNELS, PHOTO_TFREC_DIR
from ..data_acquisition.datasets import photo_tfrecorddataset
from ..data_acquisition.utils import read_image
from ..modeling.model import CycleGan


def generate_image(cyclegan_model: CycleGan, input_path: str, output_dir: str) -> None:
    """Use a CycleGAN model to translate an image to a Monet painting and save it.

    Args:
        cyclegan_model: The CycleGAN model to be used for image generation.
        input_path: Path of the image to be translated.
        output_dir: Directory where the generated image will be saved.
    """

    image = read_image(path=input_path,
                       width=IMAGE_SIZE[0],
                       height=IMAGE_SIZE[1],
                       channels=CHANNELS)

    generated_image = translate_image(cyclegan_model=cyclegan_model,
                                      image=image)

    filename = os.path.basename(input_path)

    save_image(image=generated_image,
               output_path=f'{output_dir}/monet-{filename}')


def generate_images(cyclegan_model: CycleGan, input_dir: str, output_dir: str) -> None:
    """Use a CycleGAN model to translate images to Monet paintings and save them.

    Args:
        cyclegan_model: The CycleGAN model to be used for image generation.
        input_dir: Directory of images to be translated.
        output_dir: Directory where the generated images will be saved.
    """

    photos = photo_tfrecorddataset(image_dir=input_dir).batch(1)
    make_directory(output_dir)
    for i, image in enumerate(photos):
        generated_image = translate_image(cyclegan_model=cyclegan_model, image=image)
        save_image(image=generated_image, output_path=f'{output_dir}/{i}.jpg')


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument('--dir', type=str, default=PHOTO_TFREC_DIR)
    parser.add_argument('--file', '-f', type=str)
    args = parser.parse_args()

    if not os.path.isdir(args.dir):
        print(f"ERROR: Can't find {args.dir}")
        sys.exit(1)

    model = load_cyclegan_model()

    if args.file:
        generate_image(cyclegan_model=model,
                       input_path=args.file,
                       output_dir='.')
    else:
        generate_images(cyclegan_model=model,
                        input_dir=args.dir,
                        output_dir='../submission_images')


if __name__ == '__main__':
    main()
