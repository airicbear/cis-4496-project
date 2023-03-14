from argparse import ArgumentParser

import tensorflow as tf

from ..deployment.load_model import load_cyclegan_model


def main():
    parser = ArgumentParser()
    parser.add_argument('--photo2painting', type=str, required=True, help='Path of photo2painting.h5 file.')
    parser.add_argument('--painting2photo', type=str, required=True, help='Path of painting2photo.h5 file.')
    parser.add_argument('--output', '-o', type=str, required=True, help='Path of output directory.')
    args = parser.parse_args()

    model = load_cyclegan_model(photo2painting_generator_weights_path=args.photo2painting,
                                painting2photo_generator_weights_path=args.painting2photo)

    painting_generator_path = f'{args.output}/photo2painting'
    photo_generator_path = f'{args.output}/painting2photo'

    tf.saved_model.save(obj=model.painting_generator, export_dir=painting_generator_path)
    tf.saved_model.save(obj=model.photo_generator, export_dir=photo_generator_path)


if __name__ == '__main__':
    main()