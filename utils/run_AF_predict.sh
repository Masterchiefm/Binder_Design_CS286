#!/bin/bash
source ~/miniconda3/bin/activate binder_design
# cd ..
pwd
python env_config/dl_binder_design/af2_initial_guess/predict.py  -pdbdir  $1 -outpdbdir $2 