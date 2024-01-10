#!/bin/python
# This file is created to run binder design.
# Author: Mo Qiqin

# In [1]
################################################################################
#                     Please eidt the following cell
# Target Infomation
target_protein_pdb = "PD1_00.pdb"
ppi_hotspot_res="A31,A47,A48,A93,A96"



# Binder Information
## you may use one of the following two options:
## comment one of them to choose.
## option 1:
use_example = True

## option 2:
# use_example = False
# binder_template = "example_scaffold/ems_4hM_3692.pdb"

# or you can use:
# binder_template = "example_scaffold/pdbfiles/"



# Output Path
output_folder = "testout"


# Other configurations
## RF structure generation params
num_designs=4
noise_scale_ca=0.2
noise_scale_frame=0.1

## Structure Filter params
max_Rg = 13
max_distance = 5.5
top_n = 100

## ProteinMPNN Sequence generation params
temperature = 0.25
seqs_per_struct = 3

####################################################################


# In [2]
# Do NOT modify the following!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


import os
import sys
from os.path import abspath
from pathlib import Path

def check_output(path):
    """用来判断这一步是否完整执行。
    即执行完了文件夹中应该有PDB文件，若无，终止程序
    """
    files = os.listdir(path)
    for i in files:
        if "pdb" in i[-4:]:
            return
    print("Out put folder is empty! please check the erro above.")
    sys.exit()
    

# 根据输入修改成RF接受的样式。
target_protein_pdb = abspath(os.path.expanduser(target_protein_pdb))
target_name = Path(target_protein_pdb).stem
ppi_hotspot_res = f'ppi.hotspot_res=[{ppi_hotspot_res}]'

output_folder = abspath(os.path.expanduser(output_folder))
os.system(f'mkdir -p {output_folder}')


# target 骨架生成
os.system(f"mkdir -p structure_adj/{target_name}")
out = abspath(os.path.expanduser(f'structure_adj/{target_name}'))
os.system(f"utils/pdb_make_structure_adj.sh  {target_protein_pdb}  {out}")

target_ss = abspath(os.path.expanduser(f'structure_adj/{target_name}/{target_name}_ss.pt'))
target_adj = abspath(os.path.expanduser(f'structure_adj/{target_name}/{target_name}_adj.pt'))
#Binder 参考骨架生成
if use_example:
    binder_adj = os.path.expanduser("env_config/RFdiffusion/examples/ppi_scaffolds/")
else:
    if os.path.isfile(binder_template):
        # 提供的文件
        binder_name = Path(binder_template).stem
        os.system(f"mkdir -p structure_adj/{binder_name}")
        os.system(f"utils/pdb_make_structure_adj.sh  {binder_template}  structure_adj/{binder_name}")
    else:
        binder_name = Path(binder_template).stem
        os.system(f"mkdir -p structure_adj/{binder_name}")
        os.system(f"utils/pdb_dir_make_structure_adj.sh  {binder_template}  structure_adj/{binder_name}")

    binder_adj = abspath(os.path.expanduser(f"structure_adj/{binder_name}"))


# PPI 结构生成
# PPI 结构生成
RF_out = os.path.join(output_folder,'design_ppi_scaffolded/design_ppi_scaffolded')
# os.system(f'mkdir -p {RF_out}')
script = f"""scaffoldguided.target_path={target_protein_pdb}
inference.output_prefix={RF_out}
scaffoldguided.scaffoldguided=True
'{ppi_hotspot_res}'
scaffoldguided.target_pdb=True
scaffoldguided.target_ss={target_ss}
scaffoldguided.target_adj={target_adj}
scaffoldguided.scaffold_dir={binder_adj}
inference.num_designs={num_designs}
denoiser.noise_scale_ca={noise_scale_ca}
denoiser.noise_scale_frame={noise_scale_frame}
""".replace("\n","  ")

bash_script = f"""#!/bin/bash
source ~/miniconda3/bin/activate binder_design
# cd ..
pwd
python env_config/RFdiffusion/scripts/run_inference.py {script}"""

with open(".tmp.sh",'w') as f:
    f.write(bash_script)
    
os.system("chmod 777 .tmp.sh")

os.system("bash .tmp.sh")
os.system("rm -rf .tmp.sh")
#

# In [3]
#######################################################################################
# Filter out structures with long α-helix and 
# chains with long distance.

from utils.utils import get_Rg_score, get_min_distance, cal_mass
from tqdm import tqdm
# RF_out = "/home/chief/桌面/500_2/"
RF_out_path = os.path.dirname(RF_out)
check_output(RF_out_path)

structures = os.listdir(RF_out_path)
filtered_pdbs = []
filtered_pdb_path = os.path.join(output_folder,"filtered_structures")
os.system(f'mkdir -p {filtered_pdb_path}')

bar = tqdm(structures)
bar.set_description("Filtering PPI structures")
for i in bar:
    if "pdb" in i[-3:]:
        path = os.path.join(RF_out_path,i)
        rg = get_Rg_score(path, chain='A')

        ##########################
        #  To be updated to calculate the dstance between interaction surface.
        #  现在是只计算最短的两个点之间的距离。
        d = get_min_distance(path)
        ##########################


        
        # bar.set_postfix_str(f"{i}: Rg={rg:.2f}, distance={d:.2f}")
        if rg < max_Rg and d < max_distance:
            filtered_pdbs.append(path)
            os.system(f"cp {path} {filtered_pdb_path}")
p = len(filtered_pdbs)/len(structures) * 100
print(f"{len(filtered_pdbs)} of {len(structures)} passed the evaluation.({p:.1f}%)")

check_output(filtered_pdb_path)



# In [4] 
# Protein MPNN
##############################################################################
MPNN_out_path = abspath(os.path.join(output_folder,"MPNN_out"))
os.system(f"bash utils/run_MPNN_inference.sh {filtered_pdb_path} {MPNN_out_path}  {temperature} {seqs_per_struct}")
check_output(MPNN_out_path)

# In [5]
# AF predict and ranking
####################################################################################
AF_out_path = abspath(os.path.join(output_folder,"AF_out"))
os.system(f"bash utils/run_AF_predict.sh {MPNN_out_path} {AF_out_path}")
check_output(AF_out_path)

# In [6]
# Get the top n files.
#######################################################################################
import pandas as pd
with open("out.sc",'r') as f:
    content = f.readlines()
    
sheet = ""
for i in content:
    l = ",".join(i.split()) + '\n'
    sheet += l

score_file = abspath(os.path.join(output_folder,"score.csv"))

# 直接写入比操作pandas快
with open(score_file, 'w') as f:
    f.write(sheet)

sheet = pd.read_csv(score_file)
sorted_sheet = sheet.sort_values(by=sheet.columns[3])
top = sorted_sheet.head(top_n)
top_score_file = abspath(os.path.join(output_folder,"top_n_score.csv"))
top.to_csv(top_score_file, index=0)

top_file_path = abspath(os.path.join(output_folder,"top_n"))
os.system(f'mkdir -p {top_file_path}')

# In [7]
# Get the top n sequence.
# This part is generated by ChatGPT
#############################################################################
from Bio import PDB
def extract_chain_sequence(pdb_file_path, chain_id='A'):
    # 创建PDB解析器
    parser = PDB.PDBParser(QUIET=True)

    # 读取PDB文件
    structure = parser.get_structure('protein', pdb_file_path)

    # 初始化序列
    sequence = ''

    # 遍历模型
    for model in structure:
        # 遍历链
        for chain in model:
            # 检查链ID是否匹配
            if chain.id == chain_id:
                # 遍历链的残基
                for residue in chain:
                    # 获取残基的氨基酸代码
                    amino_acid = PDB.Polypeptide.three_to_one(residue.get_resname())
                    sequence += amino_acid

    return sequence
    
sequences = []
for i in top.index:
    name = top.loc[i]['description']
    pdb = os.path.join(AF_out_path, f'{name}.pdb')
    os.system(f"cp {pdb} {top_file_path}")
    seq = extract_chain_sequence(pdb)
    sequences.append(seq)
    
top = top.assign(sequence=sequences)
top.to_csv(top_score_file, index=0)


print(f"""



                    Binder Design Compet!
=====================================================================
                        
You can find your top n binders in {top_file_path}

All output structures can be found in {output_folder}
======================================================================
""")