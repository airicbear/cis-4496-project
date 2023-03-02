import argparse
import os

from ..consts import PHOTO_TFREC_DIR, MONET_TFREC_DIR, BUILD_DIR, MONET_GENERATOR_WEIGHT_FILENAME, \
    PHOTO_GENERATOR_WEIGHT_FILENAME, EPOCHS
from ..deployment.load_model import load_cyclegan_model
from ..utils import configure_logger, log_args, read_tfrecorddataset, get_filenames


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

    fid = os.system('python -m pytorch_fid '+args.painting_dir+' '+args.transformed_photos_dir)
    print(fid)


if __name__ == '__main__':
    main()
