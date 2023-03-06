"""
Generates images from the trained model.
"""
import logging
import os
import shutil
import sys

from ..consts import IMAGE_SIZE, CHANNELS
from ..modeling.model import CycleGan
from ..modeling.predict import translate_image
from ..utils import read_image, read_tfrecorddataset, get_filenames, save_image, tensor_to_image

logger = logging.getLogger(__name__)


def generate_image(cyclegan_model: CycleGan, input_path: str, output_dir: str) -> None:
    """Use a CycleGAN model to translate an image to a painting and save it.

    Args:
        cyclegan_model: The CycleGAN model to be used for image generation.
        input_path: Path of the image to be translated.
        output_dir: Directory where the generated image will be saved.
    """

    logger.info(f"Generating painting style version of '{input_path}'.")

    if not os.path.isfile(input_path):
        raise FileNotFoundError(f'Could not find file "{input_path}".')

    image = read_image(path=input_path,
                       width=IMAGE_SIZE[0],
                       height=IMAGE_SIZE[1],
                       channels=CHANNELS)

    generated_image = translate_image(cyclegan_model=cyclegan_model,
                                      image=image)

    filename = os.path.basename(input_path)

    output_path = f'{output_dir}/{filename}'
    save_image(image=generated_image,
               output_path=output_path)

    logger.info(f"Saved painting style version of '{input_path}' to '{output_path}'.")


def generate_images(cyclegan_model: CycleGan,
                    input_dir: str,
                    input_ext: str,
                    output_dir: str,
                    sample_size: int,
                    shuffle: bool,
                    with_original: bool,
                    overwrite: bool) -> None:
    """Use a CycleGAN model to translate images to paintings and save them.

    Args:
        cyclegan_model: The CycleGAN model to be used for image generation.
        input_dir: Directory of images to be translated.
        input_ext: File extension of the input image format.
        output_dir: Directory where the generated images will be saved.
        sample_size: Sample size of photos to generate.
        shuffle: Shuffle the first 2048 images before sampling if True.
        with_original: Save the original images in a separate folder by setting this to True.
        overwrite: Overwrite any existing files in the output directory if True.
    """

    logger.info(f"Generating painting style version of each image in '{input_dir}'.")

    if not os.path.isdir(input_dir):
        raise FileNotFoundError(f'Could not find directory "{input_dir}".')

    if not overwrite and os.path.isdir(output_dir) and len(os.listdir(output_dir)) > 0:
        prompt = input(f'Overwrite the images in "{output_dir}"? (y/n): ')

        if prompt == 'n':
            sys.exit(1)

    original_dir = f'{output_dir}-original'

    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)

    if os.path.isdir(original_dir):
        shutil.rmtree(original_dir)

    if input_ext == 'tfrec':
        photos = read_tfrecorddataset(filenames=get_filenames(image_dir=input_dir, ext=input_ext))

        if shuffle:
            logger.info('Shuffling the images.')
            photos = photos.shuffle(2048)

        if sample_size:
            logger.info(f'Sampling {sample_size} images.')
            photos = photos.take(sample_size)

        photos = photos.batch(1)

        logger.info('Generating and saving images.')

        for i, image in enumerate(photos):
            generated_image = translate_image(cyclegan_model=cyclegan_model,
                                              image=image)

            save_image(image=generated_image,
                       output_path=f'{output_dir}/{i}.jpg')

            if with_original:
                original_image = tensor_to_image(image)
                save_image(image=original_image[0],
                           output_path=f'{original_dir}/{i}.jpg')

    else:
        for i, filename in enumerate(get_filenames(image_dir=input_dir, ext=input_ext)):
            generate_image(cyclegan_model=cyclegan_model,
                           input_path=filename,
                           output_dir=output_dir)

    logger.info('Finished generating and saving all photo-to-painting images.')
