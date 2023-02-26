import argparse

from ..consts import PHOTO_TFREC_DIR, MONET_TFREC_DIR, WEIGHT_OUTPUT_DIR, MONET_GENERATOR_WEIGHT_PATH, \
    PHOTO_GENERATOR_WEIGHT_PATH, EPOCHS
from ..deployment.fid import calculate_frechet_inception_distance
from ..deployment.load_model import load_cyclegan_model
from ..utils import read_tfrecorddataset, get_filenames


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--epochs', type=int, default=EPOCHS)
    args = parser.parse_args()

    photo_dataset = read_tfrecorddataset(filenames=get_filenames(image_dir=PHOTO_TFREC_DIR, ext='tfrec')).batch(1)
    monet_dataset = read_tfrecorddataset(filenames=get_filenames(image_dir=MONET_TFREC_DIR, ext='tfrec')).batch(1)
    cyclegan_model = load_cyclegan_model(
        monet_generator_weights_path=f'{WEIGHT_OUTPUT_DIR}/epoch{args.epochs}/{MONET_GENERATOR_WEIGHT_PATH}',
        photo_generator_weights_path=f'{WEIGHT_OUTPUT_DIR}/epoch{args.epochs}/{PHOTO_GENERATOR_WEIGHT_PATH}')
    fid = calculate_frechet_inception_distance(photo_dataset=photo_dataset,
                                               monet_dataset=monet_dataset,
                                               monet_generator=cyclegan_model.monet_generator)
    print(fid)


if __name__ == '__main__':
    main()
