 # CIS 4496 Capstone Project
 
by Team "Artificially Creative" ([George Aeillo](https://github.com/GeorgeFAeillo), [Eric Nguyen](https://github.com/airicbear), [Arun Agarwal](https://github.com/aagarwal17)) 

This repository hosts all code, documentation, and data related our team's solution to the Kaggle competition, [*I'm Something Of A Painter Myself*](https://www.kaggle.com/competitions/gan-getting-started). 
The challenge of this competition is to translate a photo to a Monet painting.
Our current approach involves implementing a [CycleGAN](https://junyanz.github.io/CycleGAN/), an unpaired image-to-image translation model.

Links: [Project Charter](./Docs/Project/Charter.md), [Website](https://cis-4496-project.vercel.app/)

### Repository Structure

The `Code` directory hosts code related to the project and its corresponding documentation.

The `Docs` directory hosts documentation for the project.
This directory primarily hosts design documentation, reports, and presentations.
For code documentation, see the `Code` directory.

The `Sample_Data` directory hosts a small sample of the data needed for the models.
The full dataset for the competition is available [here](https://github.com/airicbear/cis-4496-project/releases/tag/kaggle-dataset) or by running `python -m monet_cyclegan.scripts.download_dataset` in the `Code` folder and is saved in `Sample_Data/Raw/Kaggle_Dataset` by default.
