import logging
import os
from pathlib import Path

from ..consts import KAGGLE_DATASET_PATH, KAGGLE_DATASET_URL
from ..utils import download_extract_zip

logger = logging.getLogger(__name__)


def download_kaggle_dataset(url: str = KAGGLE_DATASET_URL,
                            output_dir: str = KAGGLE_DATASET_PATH) -> None:
    """Download the Kaggle dataset.

    Args:
        url: The URL of the Kaggle dataset.
        output_dir: The directory where the Kaggle dataset will be extracted to.
    """

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    if len(os.listdir(output_dir)) != 0:
        msg = f"Directory '{output_dir}' is not empty."
        logger.error(msg)
        raise OSError(msg)

    download_extract_zip(url, output_dir)
