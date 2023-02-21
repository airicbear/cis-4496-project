import os
from pathlib import Path

from .utils import download_extract_zip
from ..consts import KAGGLE_DATASET_PATH, KAGGLE_DATASET_URL


def download_kaggle_dataset() -> None:
    """Download the Kaggle dataset."""

    Path(KAGGLE_DATASET_PATH).mkdir(parents=True, exist_ok=True)

    if len(os.listdir(KAGGLE_DATASET_PATH)) != 0:
        print(f'ERROR: Directory "{KAGGLE_DATASET_PATH}" is not empty.')
        return

    download_extract_zip(KAGGLE_DATASET_URL, KAGGLE_DATASET_PATH)


if __name__ == '__main__':
    download_kaggle_dataset()
