from argparse import ArgumentParser

from ..utils import configure_logger, log_args

from ..consts import BUILD_DIR
from ..data_acquisition.download_dataset import download_kaggle_dataset


def main():
    parser = ArgumentParser()
    parser.add_argument('--build-dir', type=str, default=BUILD_DIR)
    args = parser.parse_args()

    log_dir = f'{args.build_dir}/logs/download_dataset'

    configure_logger(log_dir=log_dir)
    log_args(args=args)

    download_kaggle_dataset()


if __name__ == '__main__':
    main()
