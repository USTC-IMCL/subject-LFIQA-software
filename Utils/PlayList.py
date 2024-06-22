import random
import os
import logging

logger=logging.getLogger("LogWindow")
'''
    To make sure the ajacent elements are not the same.
    Not a general solution.
    input parameters:
    in_dict: mapping index to class name
'''
def GetRandomElement(in_dict,in_index_list,pre_class):
    cur_class=pre_class
    cur_index=None
    if len(in_index_list)==1:
        return in_index_list[0]
    while cur_class==pre_class:
        if GetClassNum(in_dict,in_index_list)==1:
            '''
              So ugly. But it works.
              TODO: just re-init for a short range of the list, or just exchange two elements randomly?
            '''
            return -1
        cur_index=random.choice(in_index_list)
        cur_class=in_dict[cur_index]
    return cur_index

def GetClassNum(in_dict,in_index_list):
    all_class=[]
    for index in in_index_list:
        if in_dict[index] not in all_class:
            all_class.append(in_dict[index])
    return len(set(all_class))

def GetRandomShowList(in_dict):
    all_num=len(in_dict)
    show_index=list(range(all_num))

    output_list=[]
    pre_class=None
    while len(output_list)<all_num:
        cur_index=GetRandomElement(in_dict,show_index,pre_class)
        if cur_index >= 0:
            output_list.append(cur_index)
            show_index.remove(cur_index)
            pre_class=in_dict[cur_index]
        else:
            show_index=list(range(all_num))
            output_list=[]
    return output_list

def CheckList(in_dict,in_list):
    for i in in_dict.keys():
        if i not in in_list:
            logger.error(f'Element {i} does not exist in the output list!')
            logger.info('re generate the list now...')
            return False
    
    pre_class = None
    for i in range(len(in_list)):
        cur_class = in_dict[in_list[i]]
        if cur_class != pre_class:
            pre_class = cur_class
        else:
            logger.error(f'Element {in_list[i]} is not unique!')
            logger.info('re generate the list now...')
            return False
    return True

def CheckAllLists(all_lists):
    diff_list=[]
    for i in all_lists:
        if i not in diff_list:
            diff_list.append(i)
        else:
            print('There are two vectors are the same!')

def MakeARandomScoringList(in_string_list):
    '''
        input: a list of the video names. 
    '''
    #1. Get the file name
    in_dict={}
    all_class=[]
    logger.info('Now generate a random play list while avoiding same content in a row...')
    for i,file_path in enumerate(in_string_list):
        file_name=os.path.basename(file_path)
        class_name=file_name.split('_')[0]
        in_dict[i]=class_name
        if class_name not in all_class:
            all_class.append(class_name)
    if len(all_class)==1:
        logger.warning('Can not find multiple contents by the file names. Checking the input fiels names may help.')
        logger.warning('The default shuffle will be used.')
        logger.info('Finish generating the random play list.')
        out_list=list(range(len(in_string_list)))
        random.shuffle(out_list)
        return out_list,[in_string_list[i] for i in out_list]
    
    out_list=GetRandomShowList(in_dict)
    while not CheckList(in_dict,out_list):
        out_list=GetRandomShowList(in_dict)
    logger.info('Finish generating the random play list.')
    logger.debug([in_string_list[i] for i in out_list])
    return out_list,[in_dict[i] for i in out_list]

if __name__=="__main__":
    '''
    k=0
    in_dict={}
    for i in range(300):
        in_dict[k]='a'
        k+=1
        in_dict[k]='b'
        k+=1
        in_dict[k]='c'
        k+=1

    all_lists=[]

    for i in range(1000):
        all_lists.append(GetRandomShowList(in_dict))
        print('get one list')
    
    print('Finish preparing all the lists.')
    for out_list in all_lists:
        CheckList(in_dict,out_list)
    
    CheckAllLists(all_lists)
    '''

    in_root='/home/heathcliff/Downloads/Serpentine_Left_Reference/two_folder/test'
    all_files=os.listdir(in_root)
    all_files=[os.path.join(in_root,i) for i in all_files]

    out_list,out_class=MakeARandomScoringList(all_files)
    print(out_list)
    print(out_class)

    










