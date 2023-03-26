# Data Acquisition

This folder contains all code needed to retrieve the data for training and testing the CycleGAN.

- `augment` - Augment the images as a preprocessing step.

- `download_dataset` - Download the Kaggle dataset onto local storage.

- `load_dataset` - Load the datasets into a format that is usable for training and testing the model.

- `preprocess` - Preprocess an entire dataset by applying augmentation, duplication, shuffling, sample size, and batch size.

- `rgb_distribution` - Plot the RGB distribution of an image as an exploratory data analysis (EDA) step.

- `train_test_split` - Generate a custom train/test split of the data given a test dataset and a training dataset.
