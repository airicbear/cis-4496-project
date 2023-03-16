from argparse import ArgumentParser

from ..data_acquisition.train_test_split import add_train_to_test


def main():
    parser = ArgumentParser()
    parser.add_argument('--train', type=str, required=True)
    parser.add_argument('--test', type=str, required=True)
    parser.add_argument('--percent', type=float, default=0.10)
    parser.add_argument('--augment', action='store_true')
    parser.add_argument('--no-augment', dest='augment', action='store_false')
    parser.set_defaults(augment=False)
    args = parser.parse_args()

    add_train_to_test(jpg_train_dir=args.train,
                      jpg_test_dir=args.test,
                      percent=args.percent,
                      apply_augmentation=args.augment)


if __name__ == '__main__':
    main()
