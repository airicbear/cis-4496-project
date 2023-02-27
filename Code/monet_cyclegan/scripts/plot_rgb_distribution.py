from argparse import ArgumentParser

from ..consts import IMAGE_SIZE
from ..data_acquisition.rgb_distribution import plot_rgb_distribution


def main():
    parser = ArgumentParser()
    parser.add_argument('--input', type=str, required=True)
    parser.add_argument('--bins', type=int, default=IMAGE_SIZE[0])
    parser.add_argument('--ext', type=str, default='tfrec')
    parser.add_argument('--num', '-n', type=int, default=-1)
    parser.add_argument('--title', type=str, default=None)
    parser.add_argument('--exclude-zeros', action='store_true')
    parser.add_argument('--include-zeros', dest='exclude_zeros', action='store_false')
    parser.set_defaults(exclude_zeros=True)
    args = parser.parse_args()

    if args.title:
        title = args.title
    else:
        title = f'RGB Distribution of "{args.input}"'

    plot_rgb_distribution(input_path=args.input,
                          bins=args.bins,
                          ext=args.ext,
                          num=args.num,
                          title=title,
                          exclude_zeros=args.exclude_zeros)


if __name__ == '__main__':
    main()
