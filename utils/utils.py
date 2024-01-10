#!/bin/python
# CS286 Project, ShanghaiTech.
# This file is used to calculate Rg Score of a protein chain.
# Support H,C,N,O and S atoms.
# Created by M.Q.

try:
    import numpy as np
except:
    import os
    os.system('pip install numpy')
    
def cal_mass(atoms):
    """输入一串原子，输出总质量。
    Params: 
        atoms: str, 例如水分子"HOH"，只计算氨基酸有的元素HCNOPS
    Returns:
        mass: int, 质量
    """
    mass_dic = {
        'H':1,
        'C':12,
        'N':14,
        'O':16,    
        'S':32
    }
    mass = 0.001
    for i in atoms:
        m = mass_dic[i]
        mass += m
    return mass


def get_chain_center(pdb_file_path, chain='A'):
    """获取PDB某条链的质量中心
    Params:
        pdb_file_path: str, 例如:"/home/chief/桌面/design_ppi_2_dldesign_3.pdb"
        chain: str, 例如"A"
        
    Retruns:
        total_mass,(x,y,z): tuple, 第一个是总质量，第二个是质心坐标
    """
    with open(pdb_file_path, 'r') as f:
        A = f.readlines()
    total_mass = 0
    x_ = 0
    y_ = 0
    z_ = 0
    for i in A:
        if "ATOM" in i[:5]:
            # print(atom)
            atom_info = (i.split())
            atom = atom_info[2]
            atom = atom[0]
            chain = atom_info[4]
            x = float(atom_info[6])
            y = float(atom_info[7])
            z = float(atom_info[8])
            try:
                m = cal_mass(atom)
            except Exception as e:
                # print(atom_info)
                m = 0
            # print(chain, atom)
            if chain == "A":
                total_mass += m
                x_ += x*m
                y_ += y*m
                z_ += z*m
    
    x_c = x_/total_mass
    y_c = y_/total_mass
    z_c = z_/total_mass
    return total_mass, (x_c,y_c,z_c)

def get_Rg_score(pdb_file_path, chain='A'):
    """获取PDB某条链的质量中心
    Params:
        pdb_file_path: str, 例如:"/home/chief/桌面/design_ppi_2_dldesign_3.pdb"
        chain: str, 例如"A"
    Retruns:
        Rg_score: float，其定义为分子中原子与其共同质心的均方根距离。
        
        回转半径在聚合物研究中比较常用，用于描述聚合物的卷曲程度。
        得分越高，即分子离质心越远，也就是说分子倾向往外延展；
        得分越低，即分子离质心越近，也就是说分子倾向往内部聚集。

        用这个分数可以表征生成蛋白是聚合物还是长链条物体。支链越多应该
        更倾向聚集，而支链少则会倾向于往外部延申，也就是分数会更高。
    """
    with open(pdb_file_path, 'r') as f:
        A = f.readlines()
    score = 0
    x_ = 0
    y_ = 0
    z_ = 0
    total_m, center = get_chain_center(pdb_file_path,chain=chain)
    for i in A:
        if "ATOM" in i[:5]:
            # print(atom)
            atom_info = (i.split())
            atom = atom_info[2]
            atom = atom[0] # RF diffussion 生成的PDB文件中少了最后一列元素，所以会报错。
                                 # 后续改成判定第三列的信息来决定元素。
            chain = atom_info[4]
            x = float(atom_info[6])
            y = float(atom_info[7])
            z = float(atom_info[8])
            m = cal_mass(atom)
            # print(chain, atom)
            if chain == "A":
                score += m* ((x-center[0])**2)   +   m* ((y-center[1])**2)   +    m* ((z-center[2])**2)
    
    score = score/total_m
    score = score**0.5
    return score
            



def get_all_attom_location(pdb_file_path, chain_id):
    loc = []
    with open(pdb_file_path, 'r') as f:
        A = f.readlines()
    score = 0
    x_ = 0
    y_ = 0
    z_ = 0
    
    for i in A:
        if "ATOM" in i[:5]:
            # print(atom)
            atom_info = (i.split())
            atom_type = atom_info[2]
            
            if atom_type != "CA": # 只看主要的C 就够了
                continue
                    
            chain = atom_info[4]
            x = float(atom_info[6])
            y = float(atom_info[7])
            z = float(atom_info[8])
            if chain == chain_id:
                loc.append(np.array([x,y,z]))

    return loc

        
def get_min_distance(pdb_file_path, chain_1_id="A", chain_2_id="B"):
    """计算两个两个链之间的最短距离。
    Params:
        pdb_file_path: str, 例如:"/home/chief/桌面/design_ppi_2_dldesign_3.pdb"
        chain_1_id: str, 例如"A"
        chain_2_id: str, 例如"B"
        
    Returns:
        min_d: float, 两个链之间的最短距离
    """
    loc_B = get_all_attom_location(pdb_file_path,"B")
    loc_A = get_all_attom_location(pdb_file_path,"A")
    distance = []
    for a in loc_A:
        for b in loc_B:
            d = ((a - b) **2 ).sum()**0.5
            distance.append(d)
    min_d = np.array(distance).min()
    return min_d          

cal_mass("NNHOC")
        