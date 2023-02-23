import os
from pathlib import Path

from .utils import download_extract_zip
from ..consts import KAGGLE_DATASET_PATH, KAGGLE_DATASET_URL


def download_kaggle_dataset(url: str = KAGGLE_DATASET_URL,
                            output_dir: str = KAGGLE_DATASET_PATH) -> None:
    """Download the Kaggle dataset."""

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    if len(os.listdir(output_dir)) != 0:
        raise OSError(f'Directory "{output_dir}" is not empty.')

    download_extract_zip(url, output_dir)


if __name__ == '__main__':
    download_kaggle_dataset()
