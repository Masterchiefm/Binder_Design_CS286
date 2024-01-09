#!/bin/bash
# This File helps you setup RFdiffusion and ProteinMPNN quickly.
# Author: Moqiqin
cd env_config
bash 0_create_env.sh
python3 1_get_RFdffusion.py
python3 2_get_ProteinMPNN.py

print("\n\n\n\Every thing is done! Enjoin binder designing!")
print("""
==================================================================================
Now you can design the binder using the interactive script by typing the following 
commands and press Enter to run:

    python3 ./design_binder.py


----------------------------------------------------------------------------------
If you want to use RFdiffution and ProteinMPNN manually,
Please activate the conda env by:

    conda activate binder_design

Then navigate to 'env_config' folder, you can see the two repo:

    RFdiffusion
    dl_binder_design

Then you may design binder yourself.

==================================================================================

    If you want to share your script, please create an issue or pull request,
    I will combine it to help more people.


""")