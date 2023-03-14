from argparse import ArgumentParser
from pathlib import Path

import tensorflowjs as tfjs


def main():
    parser = ArgumentParser()
    parser.add_argument('--photo2painting', type=str, required=True,
                        help='Path to photo2painting weights in SavedModel format.')
    parser.add_argument('--painting2photo', type=str, required=True,
                        help='Path to painting2photo weights in SavedModel format.')
    parser.add_argument('--output', '-o', type=str, required=True, help='Path to output directory.')
    args = parser.parse_args()

    photo2painting_path = f'{args.output.strip("/")}/{Path(args.photo2painting).stem}'
    painting2photo_path = f'{args.output.strip("/")}/{Path(args.painting2photo).stem}'

    tfjs.converters.convert_tf_saved_model(args.photo2painting, f'{photo2painting_path}')
    tfjs.converters.convert_tf_saved_model(args.painting2photo, f'{painting2photo_path}')


if __name__ == '__main__':
    main()
