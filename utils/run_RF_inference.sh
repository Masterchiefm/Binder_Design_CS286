#!/bin/bash
source ~/miniconda3/bin/activate binder_design
# cd ..
pwd
python env_config/RFdiffusion/scripts/run_inference.py   $1 