import logging

from ..utils import make_directory

from ..consts import BUILD_DIR
from ..data_acquisition.download_dataset import download_kaggle_dataset


def main():
    make_directory(BUILD_DIR)
    logging.basicConfig(filename=f'{BUILD_DIR}/download_dataset.log',
                        filemode='a',
                        format='%(asctime)s.%(msecs)03d %(name)s.%(funcName)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.DEBUG)

    download_kaggle_dataset()


if __name__ == '__main__':
    main()
