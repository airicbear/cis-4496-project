import argparse
import logging
import os

from ..utils import configure_logger, log_args


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--painting_dir', type=str, required=True)
    parser.add_argument('--transformed-photos-dir', type=str, required=True)
    parser.add_argument('--output', '-o', type=str, required=True)
    args = parser.parse_args()

    log_dir = f'{args.output}/logs/calculate_fid'

    configure_logger(log_dir=log_dir)
    log_args(args=args)

    fid_output = os.popen('python -m pytorch_fid ' + args.painting_dir + ' ' + args.transformed_photos_dir).read()

    logger = logging.getLogger()
    logger.info(fid_output)

    print(fid_output)


if __name__ == '__main__':
    main()
