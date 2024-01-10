#!/bin/python
# CS286 Project, ShanghaiTech
# This file is created to get RFdiffusion
# Author: Mo Qiqin, ShanghaiTech

import os

# get dl_binder_design
if os.path.isdir("dl_binder_design"):
    q = input("Found dl_binder_design folder, deleate and re-install? \n y/N:")
    if q.upper() == "Y":
        os.system("rm -rf dl_binder_design")
        os.system("git clone https://github.com/nrbennet/dl_binder_design.git")
    else:
        print("Skip and keep the old one.")
else:
    os.system("git clone https://github.com/nrbennet/dl_binder_design.git")
    
# get protein_MPNN
if os.path.isdir("dl_binder_design/mpnn_fr/ProteinMPNN"):
    q = input("Found mpnn folder, deleate and re-install? \n y/N:")
    if q.upper() == "Y":
        os.system("rm -rf dl_binder_design/mpnn_fr/ProteinMPNN")
        # comment this because github is too slow in China, which might lost connection with git. 
        # os.system("git clone https://github.com/dauparas/ProteinMPNN.git dl_binder_design/mpnn_fr/ProteinMPNN")
        os.system("git clone https://gitee.com/MasterChiefm/ProteinMPNN.git dl_binder_design/mpnn_fr/ProteinMPNN")
    else:
        print("Skip and keep the old one.")
else:
    # os.system("git config --global http.postBuffer 4024288000 && git clone https://github.com/dauparas/ProteinMPNN.git dl_binder_design/mpnn_fr/ProteinMPNN")
    os.system("git clone https://gitee.com/MasterChiefm/ProteinMPNN.git dl_binder_design/mpnn_fr/ProteinMPNN")

# get AF weights.
print("Getting AlphaFold weights...")
if os.path.isdir("dl_binder_design/af2_initial_guess/model_weights/params"):
    q = input("Found AF2 weights folder, deleate and re-install? \n y/N:")
    if q.upper() == "Y":
        os.system("rm -rf dl_binder_design/af2_initial_guess/model_weights/params")
        os.system("mkdir -p dl_binder_design/af2_initial_guess/model_weights/params")
        os.system("wget https://storage.googleapis.com/alphafold/alphafold_params_2022-12-06.tar -O dl_binder_design/af2_initial_guess/model_weights/params/alphafold_params_2022-12-06.tar")
        # os.system("wget http://hub.mahhlab.org/downloads/alphafold_params_2022-12-06.tar -O dl_binder_design/af2_initial_guess/model_weights/params/alphafold_params_2022-12-06.tar")
        
        
        os.system("cd dl_binder_design/af2_initial_guess/model_weights/params && tar --extract --verbose --file=alphafold_params_2022-12-06.tar")
    else:
        print("Skip and keep the old one.")
else:
    os.system("mkdir -p dl_binder_design/af2_initial_guess/model_weights/params")
    os.system("wget https://storage.googleapis.com/alphafold/alphafold_params_2022-12-06.tar -O dl_binder_design/af2_initial_guess/model_weights/params/alphafold_params_2022-12-06.tar")
    # os.system("wget http://hub.mahhlab.org/downloads/alphafold_params_2022-12-06.tar -O dl_binder_design/af2_initial_guess/model_weights/params/alphafold_params_2022-12-06.tar")
    os.system("cd dl_binder_design/af2_initial_guess/model_weights/params && tar --extract --verbose --file=alphafold_params_2022-12-06.tar")
    
