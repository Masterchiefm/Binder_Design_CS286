#!/bin/python
# 打算将主文件里的各个部分拆分成多个函数放这里。
import os
import sys
import numpy as np

def check_dependence():
    """xxx"""
    try:
        from Bio import PDB
    except:
        os.system("python3 -m pip install biopython==1.78")
        from Bio import PDB
        
    try:
        import numpy as np
    except:
        os.system('python -m pip install numpy')
        import numpy as np
    
def check_output(path):
    """用来判断这一步是否完整执行。
    即执行完了文件夹中应该有PDB文件，若无，终止程序
    """
    try:
        files = os.listdir(path)
    except:
        print("Out put folder not found! please check the erro above.")
        sys.exit()
    for i in files:
        if "pdb" in i[-4:]:
            return
    print("Out put folder is empty! please check the erro above.")
    sys.exit()


def generate_RF_structure():
    pass


def generate_target_adj():
    """输入target蛋白pdb，输出ss和adj
    
    """


