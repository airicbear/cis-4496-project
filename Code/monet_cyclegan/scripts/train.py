import logging
from argparse import ArgumentParser
from datetime import datetime

import tensorflow as tf

from ..consts import MONET_TFREC_DIR, PHOTO_TFREC_DIR, LOSS_RATE, EPOCHS, BUILD_DIR, \
    BATCH_SIZE
from ..data_acquisition.augment import augment_image
from ..data_acquisition.load_dataset import load_dataset
from ..modeling.create_model import create_cyclegan_model
from ..modeling.train import train_model, save_weights
from ..utils import get_filenames, count_tfrec_items, configure_logger, log_args

logger = logging.getLogger()


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument('--painting-dir', type=str, default=MONET_TFREC_DIR)
    parser.add_argument('--photo-dir', type=str, default=PHOTO_TFREC_DIR)
    parser.add_argument('--output', '-o', type=str, default=BUILD_DIR)
    parser.add_argument('--artist', type=str, default='monet')
    parser.add_argument('--loss-rate', '-lr', type=float, default=LOSS_RATE)
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
    parser.add_argument('--num-painting', type=int, default=-1)
    parser.add_argument('--num-photo', type=int, default=-1)
    parser.add_argument('--steps-per-epoch', type=int, default=None)
    parser.add_argument('--ext', type=str, default='tfrec')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--no-debug', dest='debug', action='store_false')
    parser.set_defaults(debug=False)
    args = parser.parse_args()

    if args.debug:
        tf.data.experimental.enable_debug_mode()

    epoch_dir = f'{args.output}/{args.artist}/epoch{args.epochs}'
    weights_dir = f'{epoch_dir}/weights'
    log_dir = f'{epoch_dir}/logs/train'
    fit_log_dir = f'{epoch_dir}/logs/fit/{datetime.now().strftime("%Y%m%d-%H%M%S")}'

    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=fit_log_dir)

    configure_logger(log_dir=log_dir)
    log_args(args=args)

    painting_filenames = get_filenames(image_dir=args.painting_dir, ext=args.ext)
    photo_filenames = get_filenames(image_dir=args.photo_dir, ext=args.ext)

    count_painting_samples = count_tfrec_items(tfrec_filenames=painting_filenames)
    count_photo_samples = count_tfrec_items(tfrec_filenames=photo_filenames)

    if args.num_painting >= 0:
        count_painting_samples = args.num_painting

    if args.num_photo >= 0:
        count_photo_samples = args.num_photo

    if not args.steps_per_epoch:
        steps_per_epoch = max(count_painting_samples, count_photo_samples) // args.batch_size
    else:
        steps_per_epoch = args.steps_per_epoch

    dataset = load_dataset(painting_dir=args.painting_dir,
                           photo_dir=args.photo_dir,
                           augment=(augment_image if args.augment else None),
                           repeat=args.repeat,
                           shuffle=args.shuffle,
                           batch_size=args.batch_size,
                           painting_sample_size=args.num_painting,
                           photo_sample_size=args.num_photo)

    model = create_cyclegan_model()

    train_model(cyclegan_model=model,
                loss_rate=args.loss_rate,
                train_dataset=dataset,
                epochs=args.epochs,
                steps_per_epoch=steps_per_epoch,
                tensorboard_callback=tensorboard_callback)

    save_weights(cyclegan_model=model,
                 weights_dir=weights_dir)


if __name__ == '__main__':
    main()
