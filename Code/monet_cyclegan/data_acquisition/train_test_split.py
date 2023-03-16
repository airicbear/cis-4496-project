import os

from .augment import save_augmented_image
from ..consts import IMAGE_SIZE, CHANNELS
from ..utils import random_number, read_image, save_image, tensor_to_image


def add_train_to_test(jpg_train_dir: str,
                      jpg_test_dir: str,
                      percent: float,
                      apply_augmentation: bool = False) -> None:
    """Add a percent of the train set to the test set.

    Args:
        jpg_train_dir: Directory of JPG train set.
        jpg_test_dir: Directory of JPG test set.
        percent: Percent of training set to include in the testing set.
        apply_augmentation: Apply image augmentations to the train set sample if True.
    """

    if not os.path.exists(jpg_train_dir):
        raise FileNotFoundError('Error: The train file path does not exist')

    number_of_values_in_train_directory = len(os.listdir(jpg_train_dir))
    ten_percent_of_values = float(number_of_values_in_train_directory) * percent
    ten_percent_rounded = round(ten_percent_of_values)
    indexes_already_used = set()

    while len(indexes_already_used) < ten_percent_rounded:
        random_index_candidate = round(random_number(0, number_of_values_in_train_directory - 1))

        if random_index_candidate not in indexes_already_used:
            picture_path_to_add_and_augment = os.listdir(jpg_train_dir)[random_index_candidate]
            input_path = f'{jpg_train_dir}/{picture_path_to_add_and_augment}'

            if apply_augmentation:
                save_augmented_image(input_path=input_path,
                                     output_dir=jpg_test_dir,
                                     apply_crop=False)
            else:
                image = read_image(path=input_path,
                                   width=IMAGE_SIZE[0],
                                   height=IMAGE_SIZE[1],
                                   channels=CHANNELS)[0]

                image = tensor_to_image(image)

                filename = os.path.basename(input_path)

                output_path = f'{jpg_test_dir}/train-{filename}'

                save_image(image=image, output_path=output_path)

            indexes_already_used.add(random_index_candidate)
