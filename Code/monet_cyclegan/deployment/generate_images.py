"""
Generates images from the trained model.
"""
import os
from argparse import ArgumentParser

from numpy import uint8

from .load_model import load_cyclegan_model
from .utils import translate_image, save_image, make_directory, tensor_to_image
from ..consts import IMAGE_SIZE, CHANNELS, PHOTO_TFREC_DIR, MONET_GENERATOR_WEIGHT_PATH, WEIGHT_OUTPUT_DIR, OUTPUT_DIR, \
    PHOTO_GENERATOR_WEIGHT_PATH, EPOCHS
from ..data_acquisition.utils import read_image, read_tfrecorddataset, get_filenames
from ..modeling.model import CycleGan


def generate_image(cyclegan_model: CycleGan, input_path: str, output_dir: str) -> None:
    """Use a CycleGAN model to translate an image to a Monet painting and save it.

    Args:
        cyclegan_model: The CycleGAN model to be used for image generation.
        input_path: Path of the image to be translated.
        output_dir: Directory where the generated image will be saved.
    """

    if not os.path.isfile(input_path):
        raise FileNotFoundError(f'Could not find file "{input_path}".')

    image = read_image(path=input_path,
                       width=IMAGE_SIZE[0],
                       height=IMAGE_SIZE[1],
                       channels=CHANNELS)

    generated_image = translate_image(cyclegan_model=cyclegan_model,
                                      image=image)

    filename = os.path.basename(input_path)

    save_image(image=generated_image,
               output_path=f'{output_dir}/generated-{filename}')


def generate_images(cyclegan_model: CycleGan,
                    input_dir: str,
                    input_ext: str,
                    output_dir: str,
                    sample_size: int,
                    randomize: bool,
                    with_original: bool) -> None:
    """Use a CycleGAN model to translate images to Monet paintings and save them.

    Args:
        cyclegan_model: The CycleGAN model to be used for image generation.
        input_dir: Directory of images to be translated.
        input_ext: File extension of the input image format.
        output_dir: Directory where the generated images will be saved.
        sample_size: Sample size of photos to generate.
        randomize: Use random sampling.
        with_original: Save the original images in a separate folder by setting this to True.
    """

    if not os.path.isdir(input_dir):
        raise FileNotFoundError(f'Could not find directory "{input_dir}".')

    if input_ext == 'tfrec':
        photos = read_tfrecorddataset(filenames=get_filenames(image_dir=input_dir, ext=input_ext))

        if sample_size:
            photos = photos.take(sample_size)

        if randomize:
            photos = photos.shuffle(sample_size)

        photos = photos.batch(1)

        make_directory(output_dir)

        for i, image in enumerate(photos):
            generated_image = translate_image(cyclegan_model=cyclegan_model,
                                              image=image)

            save_image(image=generated_image,
                       output_path=f'{output_dir}-generated/generated-{i}.jpg')

            if with_original:
                original_image = tensor_to_image(image)
                save_image(image=original_image[0],
                           output_path=f'{output_dir}-original/original-{i}.jpg')
    else:
        make_directory(output_dir)

        for i, filename in enumerate(get_filenames(image_dir=input_dir, ext=input_ext)):
            generate_image(cyclegan_model=cyclegan_model,
                           input_path=filename,
                           output_dir=output_dir)


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument('--input', type=str, default=PHOTO_TFREC_DIR)
    parser.add_argument('--output', '-o', type=str, default=OUTPUT_DIR)
    parser.add_argument('--file', '-f', type=str)
    parser.add_argument('--ext', type=str, default='tfrec')
    parser.add_argument('--num', '-n', type=int, default=None)
    parser.add_argument('--randomize', action='store_true')
    parser.add_argument('--no-randomize', dest='randomize', action='store_false')
    parser.set_defaults(randomize=False)
    parser.add_argument('--with-original', action='store_true')
    parser.add_argument('--without-original', dest='with-original', action='store_false')
    parser.set_defaults(with_original=False)
    args = parser.parse_args()

    model = load_cyclegan_model(
        monet_generator_weights_path=f'{WEIGHT_OUTPUT_DIR}/epoch{EPOCHS}/{MONET_GENERATOR_WEIGHT_PATH}',
        photo_generator_weights_path=f'{WEIGHT_OUTPUT_DIR}/epoch{EPOCHS}/{PHOTO_GENERATOR_WEIGHT_PATH}')

    if args.file:
        generate_image(cyclegan_model=model,
                       input_path=args.file,
                       output_dir='.')
    else:
        generate_images(cyclegan_model=model,
                        input_dir=args.input,
                        input_ext=args.ext,
                        output_dir=args.output,
                        sample_size=args.num,
                        randomize=args.randomize,
                        with_original=args.with_original)


if __name__ == '__main__':
    main()
