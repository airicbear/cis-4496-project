# Monet CycleGAN

A [CycleGAN](https://junyanz.github.io/CycleGAN/) implementation used to translate photos to paintings.

### Usage

**Train model:**

```commandline
python -m monet_cyclegan.scripts.train
```

**Generate images:**

```commandline
python -m monet_cyclegan.scripts.generate_images
```

**Calculate FID:**

```commandline
python -m monet_cyclegan.scripts.calculate_fid
```

**Download dataset:**

```commandline
python -m monet_cyclegan.scripts.download_dataset
```

For more information on each command, add `--help` to the end of the command.

### Files/Folders

This folder and all of its subfolders represent
a [Python package](https://docs.python.org/3/tutorial/modules.html#packages) (called "subpackage" for subfolders).
Each file ending with `.py` represents a [Python module](https://docs.python.org/3/tutorial/modules.html).

- `data_acquisition` - Data storage, processing, exploration, etc.

- `deployment` - Model scoring, performance, monitoring, etc.

- `modeling` - Model tuning, training, evaluation, etc.

- `consts.py` - Constants used throughout the package.

- `utils.py` - Helper methods used throughout the package.

- `environment-macos.yaml` - Conda environment configuration for macOS users.

- `environment-windows.yaml` - Conda environment configuration for Windows users only using CPU.

- `environment-cuda.yaml` - Conda environment configuration for Windows users with NVIDIA GPUs.

- `__init__.py` - Required to represent the folder as a package

### Setup (macOS)

- Install [Anaconda](https://www.anaconda.com/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

- Create and activate the Conda environment:

  ```commandline
  conda env create -f environment-macos.yaml
  conda activate monet-cyclegan-macos
  ```

### Setup (Windows, CPU only)

- Install [Anaconda](https://www.anaconda.com/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

- Search for "Environment Variables" on your desktop.

- In the User Variables, edit the "Path" variable.

- Add the following folders to the top of the list:

    - `%USERPROFILE%\anaconda3`

    - `%USERPROFILE%\anaconda3\Scripts`

- Click each OK to exit the window.

- Open your terminal in this folder and create and activate the Conda environment:

  ```commandline
  conda env create -f environment-windows.yaml
  conda activate monet-cyclegan-windows
  ```

### Setup (Windows, NVIDIA/CUDA)

- [Download NVIDIA Drivers](https://www.nvidia.com/Download/index.aspx)

- Search for "Windows Features" on your desktop and enable "Windows Subsystem for Linux" (requires restart)

- Install WSL in Windows Terminal/Command Prompt:

  ```commandline
  wsl --install Ubuntu
  ```

- Open WSL and remove old GPG key:

  ```commandline
  sudo apt-key del 7fa2af80
  ```

-
Install [Linux x86 CUDA Toolkit](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=22.04&target_type=deb_local):

```commandline
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin
sudo mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/12.0.1/local_installers/cuda-repo-ubuntu2204-12-0-local_12.0.1-525.85.12-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu2204-12-0-local_12.0.1-525.85.12-1_amd64.deb
sudo cp /var/cuda-repo-ubuntu2204-12-0-local/cuda-*-keyring.gpg /usr/share/keyrings/
sudo apt-get update
sudo apt-get -y install cuda
```

- After CUDA installation completes in WSL, **restart your computer**

- In WSL, check to see if you have NVIDIA drivers installed properly:

  ```commandline
  nvidia-smi
  ```

- Install [NVIDIA cuDNN](https://developer.nvidia.com/cudnn):

  ```commandline
  sudo apt install nvidia-cudnn
  ```

- Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html):

  ```commandline
  mkdir -p ~/miniconda3
  wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
  bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
  rm -rf ~/miniconda3/miniconda.sh
  ~/miniconda3/bin/conda init bash
  ```

- Setup system path configuration:

  ```commandline
  mkdir -p $CONDA_PREFIX/etc/conda/activate.d
  echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/' > $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
  ```

- Open WSL in this folder and create and activate the Conda environment:

  ```commandline
  conda env create -f environment-cuda.yaml
  conda activate monet-cyclegan-cuda
  ```

For additional information on setting up CUDA on WSL, see
the [CUDA on WSL User Guide](https://docs.nvidia.com/cuda/wsl-user-guide/index.html).
