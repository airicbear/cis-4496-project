import argparse

from ..consts import PHOTO_TFREC_DIR
from ..data_acquisition.preprocess import save_preprocessed_image, save_preprocessed_images


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default=PHOTO_TFREC_DIR)
    parser.add_argument('--output', '-o', type=str, default='./preprocessed-images')
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

    if args.file:
        save_preprocessed_image(input_path=args.file,
                                output_dir='.')
    else:
        save_preprocessed_images(input_dir=args.input,
                                 input_ext=args.ext,
                                 output_dir=args.output,
                                 sample_size=args.num,
                                 randomize=args.randomize,
                                 with_original=args.with_original)


if __name__ == '__main__':
    main()
