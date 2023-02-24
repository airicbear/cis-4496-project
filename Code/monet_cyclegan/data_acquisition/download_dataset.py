import os
from argparse import ArgumentParser
from pathlib import Path

from .utils import download_extract_zip
from ..consts import KAGGLE_DATASET_PATH, KAGGLE_DATASET_URL


def download_kaggle_dataset(url: str = KAGGLE_DATASET_URL,
                            output_dir: str = KAGGLE_DATASET_PATH) -> None:
    """Download the Kaggle dataset.

    Args:
        url: The URL of the Kaggle dataset.
        output_dir: The directory where the Kaggle dataset will be extracted to.
    """

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    if len(os.listdir(output_dir)) != 0:
        raise OSError(f'Directory "{output_dir}" is not empty.')

    download_extract_zip(url, output_dir)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--dir', type=str, default=PHOTO_TFREC_DIR)
    parser.add_argument('--ext', type=str, default='tfrec')
    parser.add_argument('--file', '-f', type=str)
    parser.add_argument('--output', '-o', type=str, default=OUTPUT_DIR)
    args = parser.parse_args()

    download_kaggle_dataset()
