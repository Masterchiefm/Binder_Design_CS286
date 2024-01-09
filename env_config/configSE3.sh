#!/bin/bash
# This file is to install SE3-Transformer
source ~/miniconda3/bin/activate binder_design
conda info -e
cd RFdiffusion/env/SE3Transformer
pip install --no-cache-dir -r requirements.txt
python setup.py install
cd ../.. # change into the root directory of the repository
pip install -e . 