from argparse import ArgumentParser

from ..consts import IMAGE_SIZE
from ..data_acquisition.rgb_distribution import plot_rgb_distribution


def main():
    parser = ArgumentParser()
    parser.add_argument('--input', type=str, required=True)
    parser.add_argument('--bins', type=int, default=IMAGE_SIZE[0])
    parser.add_argument('--ext', type=str, default='tfrec')
    args = parser.parse_args()

    plot_rgb_distribution(input_path=args.input, bins=args.bins, ext=args.ext)


if __name__ == '__main__':
    main()
