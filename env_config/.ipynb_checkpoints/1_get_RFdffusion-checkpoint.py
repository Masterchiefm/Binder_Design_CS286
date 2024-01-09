#!/bin/python
# CS286 Project, ShanghaiTech
# This file is created to get RFdiffusion
# Author: Mo Qiqin, ShanghaiTech

import os

if os.path.isdir("RFdiffusion"):
    q = input("Found RFdiffusion folder, deleate and re-install? \n y/N:")
    if q.upper() == "Y":
        os.system("rm -rf RFdiffusion")
        os.system("git clone https://github.com/RosettaCommons/RFdiffusion.git")
    else:
        print("Skip and keep the old one.")
else:
    os.system("git clone https://github.com/RosettaCommons/RFdiffusion.git")
    


if os.path.isdir("RFdiffusion/models"):
    q = input("Found RFdiffusion weight folder, deleate and re-install? \n y/N:")
    if q.upper() == "Y":
        os.system("rm -rf RFdiffusion/models")
        os.system("bash get_weights.sh")
    else:
        print("Skip and keep the old one.")
else:
    os.system("bash get_weights.sh")


# example scaffold files to run the scaffolded protein binder design (PPI) 
print("Unzip example scaffold files to run the scaffolded protein binder design (PPI)")
os.system("tar -xvf RFdiffusion/examples/ppi_scaffolds_subset.tar.gz -C RFdiffusion/examples/")
print("Finnish unzip example scaffold files to run the scaffolded protein binder design (PPI)")

# install SE3-Transformer
os.system("bash configSE3.sh")