import argparse

from ..utils import configure_logger, log_args
from ..consts import PHOTO_TFREC_DIR, BUILD_DIR
from ..data_acquisition.augment import save_augmented_image, save_augmented_images


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default=PHOTO_TFREC_DIR)
    parser.add_argument('--output', '-o', type=str, default='./augmented-images')
    parser.add_argument('--file', '-f', type=str)
    parser.add_argument('--ext', type=str, default='tfrec')
    parser.add_argument('--num', '-n', type=int, default=None)
    parser.add_argument('--randomize', action='store_true')
    parser.add_argument('--no-randomize', dest='randomize', action='store_false')
    parser.set_defaults(randomize=False)
    parser.add_argument('--with-original', action='store_true')
    parser.add_argument('--without-original', dest='with-original', action='store_false')
    parser.set_defaults(with_original=False)
    parser.add_argument('--build-dir', type=str, default=BUILD_DIR)
    args = parser.parse_args()

    log_dir = f'{args.build_dir}/logs/augment_images'

    configure_logger(log_dir=log_dir)
    log_args(args=args)

    if args.file:
        save_augmented_image(input_path=args.file,
                             output_dir='.')
    else:
        save_augmented_images(input_dir=args.input,
                              input_ext=args.ext,
                              output_dir=args.output,
                              sample_size=args.num,
                              randomize=args.randomize,
                              with_original=args.with_original)


if __name__ == '__main__':
    main()
