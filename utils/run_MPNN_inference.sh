#!/bin/bash
source ~/miniconda3/bin/activate binder_design
# cd ..
pwd
python env_config/dl_binder_design/mpnn_fr/dl_interface_design.py  -pdbdir $1  -outpdbdir $2  -temperature $3 -relax_cycles 0 -seqs_per_struct $4 -debug