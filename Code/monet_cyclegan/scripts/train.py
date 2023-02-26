from argparse import ArgumentParser

from ..consts import MONET_TFREC_DIR, PHOTO_TFREC_DIR, LOSS_RATE, EPOCHS, WEIGHT_OUTPUT_DIR, \
    BATCH_SIZE, MONET_GENERATOR_WEIGHT_PATH, PHOTO_GENERATOR_WEIGHT_PATH
from ..data_acquisition.augment import augment_image
from ..data_acquisition.load_dataset import load_dataset
from ..modeling.create_model import create_cyclegan_model
from ..modeling.train import train_model, save_weights
from ..utils import get_filenames, count_tfrec_items


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument('--monet_dir', type=str, default=MONET_TFREC_DIR)
    parser.add_argument('--photo_dir', type=str, default=PHOTO_TFREC_DIR)
    parser.add_argument('--output', '-o', type=str, default=WEIGHT_OUTPUT_DIR)
    parser.add_argument('--loss_rate', '-lr', type=float, default=LOSS_RATE)
    parser.add_argument('--augment', action='store_true')
    parser.add_argument('--no-augment', dest='augment', action='store_false')
    parser.set_defaults(augment=True)
    parser.add_argument('--shuffle', action='store_true')
    parser.add_argument('--no-shuffle', dest='shuffle', action='store_false')
    parser.set_defaults(shuffle=True)
    parser.add_argument('--repeat', action='store_true')
    parser.add_argument('--no-repeat', dest='repeat', action='store_false')
    parser.set_defaults(repeat=True)
    parser.add_argument('--epochs', type=int, default=EPOCHS)
    parser.add_argument('--batch-size', type=int, default=BATCH_SIZE)
    parser.add_argument('--num_monet', type=int, default=-1)
    parser.add_argument('--num_photo', type=int, default=-1)
    parser.add_argument('--steps-per-epoch', type=int, default=None)
    parser.add_argument('--filename-weight-monet', type=str, default=MONET_GENERATOR_WEIGHT_PATH)
    parser.add_argument('--filename-weight-photo', type=str, default=PHOTO_GENERATOR_WEIGHT_PATH)
    parser.add_argument('--ext', type=str, default='tfrec')
    args = parser.parse_args()

    monet_filenames = get_filenames(image_dir=args.monet_dir, ext=args.ext)
    photo_filenames = get_filenames(image_dir=args.photo_dir, ext=args.ext)

    count_monet_samples = count_tfrec_items(tfrec_filenames=monet_filenames)
    count_photo_samples = count_tfrec_items(tfrec_filenames=photo_filenames)

    if args.num_monet >= 0:
        count_monet_samples = args.num_monet

    if args.num_photo >= 0:
        count_photo_samples = args.num_photo

    if not args.steps_per_epoch:
        steps_per_epoch = max(count_monet_samples, count_photo_samples) // args.batch_size
    else:
        steps_per_epoch = args.steps_per_epoch

    dataset = load_dataset(monet_dir=args.monet_dir,
                           photo_dir=args.photo_dir,
                           augment=(augment_image if args.augment else None),
                           repeat=args.repeat,
                           shuffle=args.shuffle,
                           batch_size=args.batch_size,
                           monet_sample_size=args.num_monet,
                           photo_sample_size=args.num_photo)

    model = create_cyclegan_model()

    train_model(cyclegan_model=model,
                loss_rate=args.loss_rate,
                train_dataset=dataset,
                epochs=args.epochs,
                steps_per_epoch=steps_per_epoch)

    save_weights(cyclegan_model=model,
                 monet_generator_path=f'{args.output}/epoch{args.epochs}/{args.filename_weight_monet}',
                 photo_generator_path=f'{args.output}/epoch{args.epochs}/{args.filename_weight_photo}')


if __name__ == '__main__':
    main()
