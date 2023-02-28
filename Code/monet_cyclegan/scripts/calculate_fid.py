import argparse
import logging

from ..consts import PHOTO_TFREC_DIR, MONET_TFREC_DIR, BUILD_DIR, MONET_GENERATOR_WEIGHT_FILENAME, \
    PHOTO_GENERATOR_WEIGHT_FILENAME, EPOCHS
from ..deployment.fid import calculate_frechet_inception_distance
from ..deployment.load_model import load_cyclegan_model
from ..utils import read_tfrecorddataset, get_filenames


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--monet_dir', type=str, default=MONET_TFREC_DIR)
    parser.add_argument('--photo_dir', type=str, default=PHOTO_TFREC_DIR)
    parser.add_argument('--epochs', type=int, default=EPOCHS)
    parser.add_argument('--output', '-o', type=str, default=BUILD_DIR)
    parser.add_argument('--ext', type=str, default='tfrec')
    parser.add_argument('--filename-weight-monet', type=str, default=MONET_GENERATOR_WEIGHT_FILENAME)
    parser.add_argument('--filename-weight-photo', type=str, default=PHOTO_GENERATOR_WEIGHT_FILENAME)
    parser.add_argument('--save-logs', action='store_true')
    parser.add_argument('--no-logs', dest='save_logs', action='store_false')
    parser.set_defaults(save_logs=True)
    args = parser.parse_args()

    if args.save_logs:
        logging.basicConfig(filename=f'{args.output}/epoch{args.epochs}/calculate_fid.log',
                            filemode='w',
                            format='%(asctime)s.%(msecs)03d %(name)s.%(funcName)s %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            level=logging.DEBUG)

    for arg, value in sorted(vars(args).items()):
        logging.info(f'{arg}: {value}')

    photo_filenames = get_filenames(image_dir=args.photo_dir, ext=args.ext)
    monet_filenames = get_filenames(image_dir=args.monet_dir, ext=args.ext)

    photo_dataset = read_tfrecorddataset(filenames=photo_filenames).batch(1)
    monet_dataset = read_tfrecorddataset(filenames=monet_filenames).batch(1)

    cyclegan_model = load_cyclegan_model(
        monet_generator_weights_path=f'{args.output}/epoch{args.epochs}/{args.filename_weight_monet}',
        photo_generator_weights_path=f'{args.output}/epoch{args.epochs}/{args.filename_weight_photo}')

    fid = calculate_frechet_inception_distance(photo_dataset=photo_dataset,
                                               monet_dataset=monet_dataset,
                                               monet_generator=cyclegan_model.monet_generator)
    print(fid)


if __name__ == '__main__':
    main()
