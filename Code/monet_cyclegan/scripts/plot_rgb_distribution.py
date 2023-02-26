from argparse import ArgumentParser

from ..data_acquisition.rgb_distribution import plot_rgb_distribution


def main():
    parser = ArgumentParser()
    parser.add_argument('--file', '-f', type=str, required=True)
    parser.add_argument('--bins', type=int, default=None)
    args = parser.parse_args()

    plot_rgb_distribution(input_path=args.file, bins=args.bins)


if __name__ == '__main__':
    main()
