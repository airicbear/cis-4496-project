from argparse import ArgumentParser

from ..data_acquisition.rgb_distribution import plot_rgb_distribution

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--file', '-f', type=str, required=True)
    args = parser.parse_args()

    plot_rgb_distribution(input_path=args.file)
