#!/bin/bash
# This file is to create binder design env via mamba.

mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
bash ~/miniconda3/bin/conda init

cd env_config
source ~/miniconda3/bin/activate
echo Creating binder_design env...

# Use mamba to accelarate.
conda clean -i -y
conda install conda-forge::mamba -y

mamba env create -f  binder_design.yml
source ~/miniconda3/bin/activate binder_design

# If I put pytorch into the yml file, torch will have difficulties to use cuda, I don't know why.
# So I install pytorch in the following lines.
mamba install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia -y

# To avoid numpy erro by:
# Ref: https://blog.csdn.net/qlkaicx/article/details/134571905
# Ref: https://discuss.tensorflow.org/t/attributeerror-module-numpy-has-no-attribute-typedict/14929/9
# mamba install numpy=1.19
pip install --upgrade h5py

# fix tensorflow erro:
mamba remove tensorflow -y
mamba install tensorflow=2.12 -y