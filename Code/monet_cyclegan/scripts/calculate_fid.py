from ..consts import PHOTO_TFREC_DIR, MONET_TFREC_DIR
from ..deployment.fid import calculate_frechet_inception_distance
from ..deployment.load_model import load_cyclegan_model
from ..utils import read_tfrecorddataset, get_filenames


def main():
    photo_dataset = read_tfrecorddataset(filenames=get_filenames(image_dir=PHOTO_TFREC_DIR, ext='tfrec')).batch(1)
    monet_dataset = read_tfrecorddataset(filenames=get_filenames(image_dir=MONET_TFREC_DIR, ext='tfrec')).batch(1)
    cyclegan_model = load_cyclegan_model()
    fid = calculate_frechet_inception_distance(photo_dataset=photo_dataset,
                                               monet_dataset=monet_dataset,
                                               monet_generator=cyclegan_model.monet_generator)
    print(fid)


if __name__ == '__main__':
    main()
