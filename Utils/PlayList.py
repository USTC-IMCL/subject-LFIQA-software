import random


'''
    To make sure the ajacent elements are not the same.
    Not a general solution.
    input parameters:
    in_dict: mapping index to class name
'''
def GetRandomElement(in_dict,in_index_list,pre_class,pre_index):
    cur_class=pre_class
    cur_index=None
    while cur_class==pre_class:
        if GetClassNum(in_dict,in_index_list)==1:
            return -1
        cur_index=random.choice(in_index_list)
        cur_class=in_dict[cur_index]
    return cur_index

def GetClassNum(in_dict,in_index_list):
    all_class=[]
    for index in in_index_list:
        all_class.append(in_dict[index])
    return len(set(all_class))

def GetRandomShowList(in_dict):
    all_num=len(in_dict)
    show_index=list(range(all_num))


