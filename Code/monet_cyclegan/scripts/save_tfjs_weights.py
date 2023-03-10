import os
from argparse import ArgumentParser
from pathlib import Path

import tensorflowjs as tfjs

from ..deployment.load_model import load_cyclegan_model


def main():
    parser = ArgumentParser()
    parser.add_argument('--photo2painting', type=str, required=True, help='Path to photo2painting.h5 file.')
    parser.add_argument('--painting2photo', type=str, required=True, help='Path to painting2photo.h5 file.')
    parser.add_argument('--output', '-o', type=str, required=True, help='Path to output directory.')
    args = parser.parse_args()

    model = load_cyclegan_model(
        photo2painting_generator_weights_path=args.photo2painting,
        painting2photo_generator_weights_path=args.painting2photo)

    tfjs.converters.save_keras_model(model=model.painting_generator,
                                     artifacts_dir=f'{args.output.strip("/")}/{Path(args.photo2painting).stem}')
    tfjs.converters.save_keras_model(model=model.photo_generator,
                                     artifacts_dir=f'{args.output.strip("/")}/{Path(args.painting2photo).stem}')


if __name__ == '__main__':
    main()
