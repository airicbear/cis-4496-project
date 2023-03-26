# Scripts

This folder contains all executable scripts related to the package.

- `add_train_to_test` - Adds a percentage of the training data to the test data.

- `augment_images` - Demonstrate image augmentation.

- `calculate_fid` - Calculate the FID score of the pretrained model.

- `convert_to_tfrec` - Creates a folder of images in the TFREC format that were previously in the JPG format.

- `download_dataset` - Download the full Kaggle dataset into `Sample_Data/Raw/Kaggle_Dataset`.

- `generate_images` - Use the painting generator of a pretrained model to translate a set of images.

- `h5_to_saved_model` - Converts a HDF5 model into a SavedModel format.

- `plot_rgb_distribution` - Plot the RGB distribution of a given image file.

- `save_tfjs_weights` - Converts a model in the SavedModel format into a format for use on the web.

- `save_tfrec_to_jpg` - Converts TFREC files to JPG files and saves them in a folder.

- `train` - Trains a given model and saves the weights in HDF5 and SavedModel formats.
