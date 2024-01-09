#!/bin/bash
source ~/miniconda3/bin/activate binder_design
cd ..
env_config/RFdiffusion/helper_scripts/make_secstruc_adj.py --pdb_dir $1 --out_dir $2