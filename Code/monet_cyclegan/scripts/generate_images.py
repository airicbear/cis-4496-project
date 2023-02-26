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
    parser.add_argument('--epochs', type=int, default=EPOCHS)
    parser.add_argument('--weight-dir', type=str, default=WEIGHT_OUTPUT_DIR)
    parser.add_argument('--filename-weight-monet', type=str, default=MONET_GENERATOR_WEIGHT_PATH)
    parser.add_argument('--filename-weight-photo', type=str, default=PHOTO_GENERATOR_WEIGHT_PATH)
    parser.add_argument('--shuffle', action='store_true')
    parser.add_argument('--no-shuffle', dest='shuffle', action='store_false')
    parser.set_defaults(shuffle=False)
    parser.add_argument('--with-original', action='store_true')
    parser.add_argument('--without-original', dest='with-original', action='store_false')
    parser.set_defaults(with_original=False)
    args = parser.parse_args()

    model = load_cyclegan_model(
        monet_generator_weights_path=f'{args.weight_dir}/epoch{args.epochs}/{args.filename_weight_monet}',
        photo_generator_weights_path=f'{args.weight_dir}/epoch{args.epochs}/{args.filename_weight_photo}')

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
                        shuffle=args.shuffle,
                        with_original=args.with_original)


if __name__ == '__main__':
    main()
