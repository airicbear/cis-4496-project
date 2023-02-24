from argparse import ArgumentParser

from ..consts import PHOTO_TFREC_DIR, OUTPUT_DIR, WEIGHT_OUTPUT_DIR, EPOCHS, \
    MONET_GENERATOR_WEIGHT_PATH, PHOTO_GENERATOR_WEIGHT_PATH
from ..deployment.generate_images import generate_image, generate_images
from ..deployment.load_model import load_cyclegan_model


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
