# Monet CycleGAN

### Conda Environment Setup (Windows)

- [Install Anaconda](https://www.anaconda.com/)
- [Install WSL](https://learn.microsoft.com/en-us/windows/wsl/install) (WSL is required for GPU support on Windows)

```
conda env create -f environment-windows.yaml
conda activate monet-cyclegan-windows
```

### Conda Environment Setup (macOS)

- [Install Anaconda](https://www.anaconda.com/)

```
conda env create -f environment-macos.yaml
conda activate monet-cyclegan-macos
```

### Run modules

Run modules from the parent directory of the package.
Example:

```
python -m monet_cyclegan.train
```

### Files/Folders

This folder represents a [Python package](https://docs.python.org/3/tutorial/modules.html#packages).
Each file in this folder represents a [Python module](https://docs.python.org/3/tutorial/modules.html).

- `__init__.py`: Required to represent the folder as a package

- `create_model.py`: The configured model.
  This is where the loss functions and optimizers are defined.

- `datasets.py`: Load the Monet and photo images in `TFRecordDataset` format.

- `discriminator.py`: The discriminator model.

- `generate_images.py`: Generate images from the trained model.

- `generator.py`: The generator model.

- `layers.py`: Common layers used in the models.

- `model.py`: The CycleGAN model.

- `train.py`: Train the configured model.

- `utils.py`: Common utilities used throughout the project.
