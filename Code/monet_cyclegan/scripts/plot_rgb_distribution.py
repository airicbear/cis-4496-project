from argparse import ArgumentParser

from ..utils import configure_logger, log_args
from ..consts import BUILD_DIR
from ..data_acquisition.rgb_distribution import plot_rgb_distribution


def main():
    parser = ArgumentParser()
    parser.add_argument('--input', type=str, required=True)
    parser.add_argument('--ext', type=str, default='tfrec')
    parser.add_argument('--num', '-n', type=int, default=-1)
    parser.add_argument('--title', type=str, default=None)
    parser.add_argument('--xlabel', type=str, default=None)
    parser.add_argument('--ylabel', type=str, default=None)
    parser.add_argument('--exclude-zeros', action='store_true')
    parser.add_argument('--include-zeros', dest='exclude_zeros', action='store_false')
    parser.set_defaults(exclude_zeros=True)
    parser.add_argument('--build-dir', type=str, default=BUILD_DIR)
    args = parser.parse_args()

    log_dir = f'{args.build_dir}/logs/plot_rgb_distribution'

    configure_logger(log_dir=log_dir)
    log_args(args=args)

    if args.title:
        title = args.title
    else:
        title = f'RGB Distribution of "{args.input}"'

    plot_rgb_distribution(input_path=args.input,
                          ext=args.ext,
                          num=args.num,
                          title=title,
                          xlabel=args.xlabel,
                          ylabel=args.ylabel,
                          exclude_zeros=args.exclude_zeros)


if __name__ == '__main__':
    main()
