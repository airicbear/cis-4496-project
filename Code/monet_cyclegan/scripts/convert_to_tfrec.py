from argparse import ArgumentParser

from ..utils import generate_tfrec_records


def main():
    parser = ArgumentParser()
    parser.add_argument('--input', '-i', type=str)
    parser.add_argument('--output', '-o', type=str)
    parser.add_argument('--artist', type=str, default='monet')
    parser.add_argument('--ext', type=str, default='jpg')
    args = parser.parse_args()

    generate_tfrec_records(input_dir=args.input,
                           output_dir=args.output,
                           artist=args.artist,
                           ext=args.ext)


if __name__ == '__main__':
    main()
