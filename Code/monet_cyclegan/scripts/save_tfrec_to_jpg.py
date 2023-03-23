from argparse import ArgumentParser

from ..utils import save_tfrec_to_jpg


def main():
    parser = ArgumentParser()
    parser.add_argument('--input-dir', '-i', type=str, required=True)
    parser.add_argument('--output-dir', '-o', type=str, required=True)
    parser.add_argument('--num', '-n', type=int)
    args = parser.parse_args()

    save_tfrec_to_jpg(input_dir=args.input_dir,
                      output_dir=args.output_dir,
                      num=args.num)


if __name__ == '__main__':
    main()
