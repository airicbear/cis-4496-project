# CIS4496 Project Source Code

This folder hosts the code for the project.

- `monet_cyclegan`: Python package to train and build the "photo to monet" model

  - `python -m monet_cyclegan.scripts.train`: Train the model and save the generator weights

  - `python -m monet_cyclegan.scripts.generate_images`: Load the generator weights and generate the images.

  - `python -m monet_cyclegan.scripts.calculate_fid`: Calculate the FID score of a pretrained CycleGAN.

  - `python -m monet_cyclegan.scripts.download_dataset`: Download the Kaggle dataset. 
