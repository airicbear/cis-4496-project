from argparse import ArgumentParser

from ..consts import PHOTO_TFREC_DIR, BUILD_DIR, EPOCHS, PHOTO2PAINTING_WEIGHTS, PAINTING2PHOTO_WEIGHTS
from ..deployment.generate_images import generate_image, generate_images
from ..deployment.load_model import load_cyclegan_model
from ..utils import configure_logger, log_args


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument('--input', type=str, default=PHOTO_TFREC_DIR)
    parser.add_argument('--output', '-o', type=str, default=None)
    parser.add_argument('--artist', type=str, default='monet')
    parser.add_argument('--file', '-f', type=str)
    parser.add_argument('--ext', type=str, default='tfrec')
    parser.add_argument('--num', '-n', type=int, default=None)
    parser.add_argument('--epochs', type=int, default=EPOCHS)
    parser.add_argument('--build-dir', type=str, default=BUILD_DIR)
    parser.add_argument('--photo2painting', type=str, default=None)
    parser.add_argument('--painting2photo', type=str, default=None)
    parser.add_argument('--shuffle', action='store_true')
    parser.add_argument('--no-shuffle', dest='shuffle', action='store_false')
    parser.set_defaults(shuffle=False)
    parser.add_argument('--with-original', action='store_true')
    parser.add_argument('--without-original', dest='with-original', action='store_false')
    parser.set_defaults(with_original=False)
    parser.add_argument('--overwrite', action='store_true')
    parser.add_argument('--no-overwrite', dest='overwrite', action='store_false')
    parser.set_defaults(overwrite=False)
    parser.add_argument('--log-dir', type=str, default=None)
    args = parser.parse_args()

    epoch_dir = f'{args.build_dir}/{args.artist}/epoch{args.epochs}'
    weights_dir = f'{epoch_dir}/weights'
    saved_model_weights_dir = f'{weights_dir}/SavedModel'

    if args.log_dir:
        log_dir = args.log_dir
    else:
        log_dir = f'{epoch_dir}/logs/generate_images'

    configure_logger(log_dir=log_dir)
    log_args(args=args)

    if args.photo2painting:
        photo2painting_path = args.photo2painting
    else:
        photo2painting_path = f'{saved_model_weights_dir}/{PHOTO2PAINTING_WEIGHTS}'

    if args.painting2photo:
        painting2photo_path = args.painting2photo
    else:
        painting2photo_path = f'{saved_model_weights_dir}/{PAINTING2PHOTO_WEIGHTS}'

    model = load_cyclegan_model(
        photo2painting_generator_weights_path=photo2painting_path,
        painting2photo_generator_weights_path=painting2photo_path)

    if args.output:
        output_dir = args.output
    else:
        output_dir = f'{epoch_dir}/images'

    if args.file:
        generate_image(cyclegan_model=model,
                       input_path=args.file,
                       output_dir=output_dir)
    else:
        generate_images(cyclegan_model=model,
                        input_dir=args.input,
                        input_ext=args.ext,
                        output_dir=output_dir,
                        sample_size=args.num,
                        shuffle=args.shuffle,
                        with_original=args.with_original,
                        overwrite=args.overwrite)

    print(f"Images saved to '{output_dir}'.")


if __name__ == '__main__':
    main()
