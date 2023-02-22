# CIS4496 Project Source Code

This folder hosts the code for the project.

- `monet_cyclegan`: Python package to train and build the "photo to monet" model

  - `python -m monet_cyclegan.modeling.train`: Train the model and save the generator weights

  - `python -m monet_cyclegan.deployment.generate_images`: Load the generator weights and generate the images to `../submission_images`
