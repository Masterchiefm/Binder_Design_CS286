#!/bin/python
# CS286 Project, ShanghaiTech.
# This file is used to calculate Rg Score of a protein chain.
# Support H,C,N,O and S atoms.
# Created by M.Q.
# Contributed by Zhang Hao, Chen Ken


try:
    import numpy as np
except:
    import os
    os.system('pip install numpy')
    import numpy as np

try:
    import pandas as pd
except:
    import os
    os.system('pip install pandas')
    import pandas as pd
    
    
    
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

# Contributed by Chen Ken:
def get_min_dis_and_direction(pdb_file_path, chain_1_id="A", chain_2_id="B"):
    """
    get the min distance between two chain, and the corresponding vector direction A -> B

    params:
      pdb_file_path, chain_1_id, chain_2_id: same as get_min_distance
    
    return:
      min_d: float, the min distance between two surfaces
      min_direction: np.array, the corresponding vector direction, A -> B
    """
    
    loc_B = get_all_attom_location(pdb_file_path,chain_2_id)
    loc_A = get_all_attom_location(pdb_file_path,chain_1_id)

    ret_dict = {}
    min_d = float("inf")
    for a in loc_A:
        for b in loc_B:
            d = ((a - b) **2 ).sum()**0.5
            if d < min_d:
                min_d = d
                ret_dict["a"] = a
                ret_dict["b"] = b
    direction = ret_dict["a"] - ret_dict["b"]
    direction_norm = np.linalg.norm(direction)
    min_direction = direction / direction_norm
    return min_d, min_direction

def get_min_dis_of_surface(pdb_file_path, chain_1_id="A", chain_2_id="B",rank=10, num_of_aa_in_surface=5):
    '''
    compute the min distance between two surfaces
    
    params:
      pdb_file_path, chain_1_id, chain_2_id, rank: same as get_min_distance
      num_of_aa_in_surface: int, num of aa we select in each surface
    
    return:
      min_sur(signed): float, the min distance between two surfaces
    '''
    loc_A = get_all_attom_location(pdb_file_path, chain_1_id)
    loc_B = get_all_attom_location(pdb_file_path, chain_2_id)

    assert len(loc_A) >= num_of_aa_in_surface and len(loc_B) >= num_of_aa_in_surface, "error, len of chain is less than the num of aa in surfaces"

    # get the min dis and the corresponding direction
    min_d, min_direction = get_min_dis_and_direction(pdb_file_path)
    limitaion = 2 * min_d
    
    # select aa which is close to the other chain
    A_sel = []
    B_sel = []
    for a in loc_A:
        for b in loc_B:
            d = ((a - b) **2 ).sum()**0.5
            if d <= limitaion:
                A_sel.append(a)
                B_sel.append(b)
    
    # surface := mid point of aa in the surface
    mid_point_of_sur_A = []
    mid_point_of_sur_B = []
    # for index_A in itertools.combinations(range(len(A_sel)), num_of_aa_in_surface):
    #     mid_point = np.zeros(3)
    #     for i in list(index_A):
    #         mid_point += A_sel[i]
    #     mid_point /= len(list(index_A))
    #     mid_point_of_sur_A.append(mid_point)
    
    # for index_B in itertools.combinations(range(len(B_sel)), num_of_aa_in_surface):
    #     mid_point = np.zeros(3)
    #     for i in list(index_B):
    #         mid_point += B_sel[i]
    #     mid_point /= len(list(index_B))
    #     mid_point_of_sur_B.append(mid_point)
    
    for i in range(0, len(A_sel)-num_of_aa_in_surface+1):
        mid_point = np.zeros(3)
        for j in range(0, num_of_aa_in_surface):
            mid_point += A_sel[i+j]
        mid_point /= num_of_aa_in_surface
        mid_point_of_sur_A.append(mid_point)

    for i in range(0, len(B_sel)-num_of_aa_in_surface+1):
        mid_point = np.zeros(3)
        for j in range(0, num_of_aa_in_surface):
            mid_point += B_sel[i+j]
        mid_point /= num_of_aa_in_surface
        mid_point_of_sur_B.append(mid_point)

    # compute the min dis of surface, and compare the direction to figure out
    # weather the dis shall be less than 0
    min_sur = float("inf")
    direction_dict = {}
    for a_sur in mid_point_of_sur_A:
        for b_sur in mid_point_of_sur_B:
            d = ((a_sur - b_sur) ** 2).sum()**0.5
            if d < min_sur:
                min_sur = d
                direction_dict["A"] = a_sur
                direction_dict["B"] = b_sur
    
    # the direcion of min sur, A -> B
    sur_dirction = direction_dict["A"] - direction_dict["B"]
    sign = 1
    if (sur_dirction * min_direction).sum() <= 0:
        sign = -1
    min_sur *= sign

    return min_sur


# Contributed by Zhang Hao. But I'm going to apply them a little bit later. 
def get_pocket_center(pdb_file_path,pocket_index,chain_id='B'):
    with open(pdb_file_path, 'r') as f:
        data = f.readlines()
    loc = []
    x_sum = 0
    y_sum = 0
    z_sum = 0
    valid_count = 0
    b_chain_start = 0
    start_flag = 0
    for i in data:
        if "ATOM" in i[:5]:
            # print(atom)
            atom_info = i.split()
            atom_type = atom_info[2]

            if atom_type != "CA":
                continue
            if atom_info[4] != chain_id:
                continue
            elif not start_flag:
                start_flag = 1
                b_chain_start = int(atom_info[5])-1
            if start_flag:

                x = float(atom_info[6])
                y = float(atom_info[7])
                z = float(atom_info[8])
                res_id = int(atom_info[5])
                if res_id-b_chain_start in pocket_index:
                    x_sum += x
                    y_sum += y
                    z_sum += z
                    valid_count += 1
    if valid_count == 0:
        raise RuntimeError
    position = np.array([x_sum,y_sum,z_sum])/valid_count
    return position

def get_avg_distance(pdb_file_path,center_loc):

    distance = []
    counter = 0
    loc_A = get_all_attom_location(pdb_file_path, "A")
    for a in loc_A:
        d = ((a - center_loc) ** 2).sum() ** 0.5
        distance.append(d)
    avg_d = np.average(distance)
    return avg_d
        