import argparse
import logging
import os

from ..consts import BUILD_DIR, EPOCHS
from ..utils import configure_logger, log_args


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--painting_dir', type=str)
    parser.add_argument('--transformed_photos_dir', type=str)
    parser.add_argument('--epochs', type=int, default=EPOCHS)
    parser.add_argument('--output', '-o', type=str, default=BUILD_DIR)
    args = parser.parse_args()

    log_dir = f'{args.output}/epoch{args.epochs}/logs/calculate_fid'

    configure_logger(log_dir=log_dir)
    log_args(args=args)

    fid_output = os.popen('python -m pytorch_fid ' + args.painting_dir + ' ' + args.transformed_photos_dir).read()

    logger = logging.getLogger()
    logger.info(fid_output)

    print(fid_output)


if __name__ == '__main__':
    main()
