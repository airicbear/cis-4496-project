from argparse import ArgumentParser

from ..consts import MONET_TFREC_DIR, PHOTO_TFREC_DIR, LOSS_RATE, EPOCHS, WEIGHT_OUTPUT_DIR, \
    BATCH_SIZE, MONET_GENERATOR_WEIGHT_PATH, PHOTO_GENERATOR_WEIGHT_PATH
from ..data_acquisition.datasets import load_dataset
from ..modeling.create_model import create_cyclegan_model
from ..modeling.train import train_model, save_weights


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument('--monet_dir', type=str, default=MONET_TFREC_DIR)
    parser.add_argument('--photo_dir', type=str, default=PHOTO_TFREC_DIR)
    parser.add_argument('--loss_rate', '-lr', type=float, default=LOSS_RATE)
    parser.add_argument('--epochs', type=int, default=EPOCHS)
    parser.add_argument('--output', '-o', type=str, default=WEIGHT_OUTPUT_DIR)
    parser.add_argument('--num_monet', type=int, default=None)
    parser.add_argument('--num_photo', type=int, default=None)
    args = parser.parse_args()

    dataset = load_dataset(monet_dir=args.monet_dir, photo_dir=args.photo_dir, batch_size=BATCH_SIZE)

    model = create_cyclegan_model()

    train_model(cyclegan_model=model,
                loss_rate=args.loss_rate,
                train_dataset=dataset,
                epochs=args.epochs)

    save_weights(cyclegan_model=model,
                 monet_generator_path=f'{args.output}/epoch{args.epochs}/{MONET_GENERATOR_WEIGHT_PATH}',
                 photo_generator_path=f'{args.output}/epoch{args.epochs}/{PHOTO_GENERATOR_WEIGHT_PATH}')


if __name__ == '__main__':
    main()
