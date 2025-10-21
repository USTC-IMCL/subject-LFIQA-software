import random
import os
import logging
from random import shuffle

logger=logging.getLogger("LogWindow")

def GetRound(in_num):
    ret_num=int(in_num)
    if in_num-ret_num>=0.5:
        ret_num+=1
    return ret_num

def AllocateToBins(in_bins,in_num):
    bin_num=len(in_bins)

    bins_sum=sum(in_bins)
    ret_list=[in_num*in_bins[i]/bins_sum for i in range(bin_num)]

    ret_int=[GetRound(i) for i in ret_list]

    ret_sum=sum(ret_int)
    if ret_sum<in_num:
        error_sum=in_num-ret_sum
        error_bins=[in_bins[i]-ret_int[i] for i in range(bin_num)]
        while(error_sum>0):
            max_index=error_bins.index(max(error_bins))
            error_bins[max_index]-=1
            ret_int[max_index]+=1
            error_sum-=1
    '''???'''
    if ret_sum>in_num:
        error_sum=ret_sum-in_num
        error_bins=[ret_int[i]-in_bins[i] for i in range(bin_num)]
        while(error_sum>0):
            max_index=error_bins.index(max(error_bins))
            error_bins[max_index]-=1
            ret_int[max_index]-=1
            error_sum-=1
    return ret_int

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
            logger.debug("false to get the random element. re-generate the list now...")
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

def MakeDSCSPCList(in_list,in_scores,group_num,grading_scales, method="base"):
    '''
        input: a list of names in string
        Note that all images are from high quality to low quality
        So the grading scales should be in descending order

        output: pc_list, a dictionary.
        pc_list[class_name][group_index]=[index1,index2,...]
        the index are the index in the input list
    '''
    #1. Get the file name
    class_dict={}
    all_classes=[]

    pc_list={}

    grading_scales.sort(reverse=True)
    # base method, the group num must be the grading scales
    if method == 'base':
        logger.debug("Base mode is used. The group number is set to the number of grading scales.")
        group_num = len(grading_scales)
        '''
        if len(grading_scales)!=group_num:
            logger.error('The number of grading scales is not equal to the number of groups!')
            logger.error('The program will exit now.')
            return None
        '''
    else:
        logger.debug(f"CCG mode is used. Currently the group number is {group_num}")
    
    gs_2_index={}
    for i in range(len(grading_scales)):
        gs_2_index[grading_scales[i]]=i


    for in_index in range(len(in_list)):
        file_name=in_list[in_index]
        cur_score=in_scores[in_index]

        class_name=file_name.split('_')[0]
        all_classes.append(class_name)

        if class_name not in class_dict.keys():
            class_dict[class_name]=[]
        class_dict[class_name].append([in_index,cur_score])

    method=method.lower()
    
    for class_name in class_dict.keys():
        cur_class_elements=class_dict[class_name]

        # divide to K groups
        pc_list[class_name]=[]
        if method=="base":
            for group_index in range(group_num):
                pc_list[class_name].append([])
            for element_index in range(len(cur_class_elements)):
                cur_score=cur_class_elements[element_index][1]
                cur_group_index=gs_2_index[cur_score]
                pc_list[class_name][cur_group_index].append(cur_class_elements[element_index])
        elif method=="ccg":
            # biggest to smallest
            cur_class_elements.sort(key=lambda x:x[1],reverse=True)
            for i in range(group_num):
                pc_list[class_name].append([])
            element_num=len(cur_class_elements)
            num_for_each_group=[element_num//group_num for i in range(group_num)]
            for i in range(1,element_num%group_num+1):
                num_for_each_group[-i]+=1
            for i,ele_len in enumerate(num_for_each_group):
                start_point=sum(num_for_each_group[:i])
                pc_list[class_name][i]+=cur_class_elements[start_point:start_point+ele_len]
        else:
            logger.error('The method is not supported!')
            return None

    return pc_list

def MakePCPairs(in_list):
    ret_list=[]
    list_len=len(in_list)
    if list_len<2:
        return ret_list

    for start_index in range(list_len):
        for end_index in range(start_index+1,list_len):
            ret_list.append([in_list[start_index],in_list[end_index]])
    return ret_list

def AllocateThresholds(pc_list,pc_group_index, max_num,mode="percent"):
    all_keys=list(pc_list.keys())
    all_thresholds={}

    scenes_num={}
    bin_num=[0 for i in range(max(pc_index))]
    pairs_sum=0

    for class_name in all_keys:
        logger.debug(f"Class name: {class_name}")
        if class_name not in scenes_num.keys():
            scenes_num[class_name]=[None for i in range(max(pc_group_index))]
            all_thresholds[class_name]=[None for i in range(max(pc_group_index))]
        for pc_index in pc_group_index:
            bin_len=len(pc_list[class_name][pc_index])
            bin_len=bin_len*(bin_len-1)//2
            scenes_num[class_name][pc_index]=bin_len
            bin_num[pc_index]+=bin_len
            pairs_sum+=bin_len
            logger.debug(f"bin index {pc_index} has {bin_len} pairs")
    for pc_index in pc_group_index:
        logger.debug(f"bin index {pc_index} has {bin_num[pc_index]} pairs")
    
    if mode=="uniform":
        pass
    else:
        all_bins=[]
        for class_name in all_keys:
            for pc_index in pc_group_index:
                all_bins.append(scenes_num[class_name][pc_index])
        bin_threashold=AllocateToBins(all_bins, max_num)

        for class_name in all_keys:
            for pc_index in pc_group_index:
                all_thresholds[class_name][pc_index]=bin_threashold[pc_index]
    return all_thresholds

def MakePCPairsWithThreshold(in_list, bin_threshold):
    # if the bin pairs number is less than threshold, no reduction is needed
    if bin_threshold <=0:
        logger.debug("Warning! One bin has a threshold less than 0. This means an unbalanced bin usually.")
        return []
    all_bin_pairs=MakePCPairs(in_list)

    if len(all_bin_pairs) <= bin_threshold:
        return all_bin_pairs

    # if the bin pairs number is more than threshold, reduce the number
    # so we have three sets now : a basic set, and an circle set, then completed connected set

    pair_index=list(range(len(in_list)))
    shuffle(pair_index)
    basic_set=[]
    circle_set=[]
    completed_set=[]

    for i in range(len(pair_index)//2):
        first=i*2
        second=i*2+1
        basic_set.append([in_list[pair_index[first]],in_list[pair_index[second]]])
    
    if len(pair_index)%2==1:
        first=pair_index[-2]
        second=pair_index[-1]
        basic_set.append([in_list[pair_index[first]],in_list[pair_index[second]]])

    for i in range(1,len(pair_index)//2*2-1,2):
        circle_set.append([in_list[pair_index[i]],in_list[pair_index[i+1]]])
    
    for first in range(len(pair_index)-1):
        for second in range(first+2,len(pair_index)):
            completed_set.append([in_list[pair_index[first]],in_list[pair_index[second]]])
    
    # so we have three sets now : a basic set, and an circle set, then completed connected set
    basic_num=len(basic_set)
    circle_num=len(circle_set)
    completed_num=len(completed_set)

    ret_pairs=[]
    basic_sample_num=min(basic_num,bin_threshold)
    basic_sample_pairs=SampleRandomly(basic_set,basic_sample_num)

    circle_threshold=bin_threshold-basic_sample_num
    circle_sample_num=min(circle_num,circle_threshold)
    circle_sample_num=max(circle_sample_num,0)
    circle_sample_pairs=SampleRandomly(circle_set,circle_sample_num)

    completed_threshold=circle_threshold-circle_sample_num
    completed_sample_num=min(completed_num,completed_threshold)
    completed_sample_num=max(completed_sample_num,0)
    completed_sample_pairs=SampleRandomly(completed_set,completed_sample_num)

    ret_pairs=basic_sample_pairs+circle_sample_pairs+completed_sample_pairs
    return ret_pairs

def FromPCListToPairs(pc_list,pc_group_index,max_num):
    all_keys=list(pc_list.keys())
    all_threasholds=AllocateThresholds(pc_list,pc_group_index, max_num)

    ret_pairs={}
    for class_name in all_keys:
        if class_name not in ret_pairs.keys():
            ret_pairs[class_name]=[None for i in range(max(pc_group_index))]
        for pc_index in pc_group_index:
            ret_pairs[class_name][pc_index]=MakePCPairsWithThreshold(pc_list[class_name][pc_index],all_threasholds[class_name][pc_index])
    return ret_pairs

def SampleRandomly(in_list,sample_num):
    ret_list=[]
    if sample_num<=0:
        return ret_list
    if sample_num>=len(in_list):
        return in_list
    
    sample_index=random.sample(range(len(in_list)),sample_num)
    ret_list=[in_list[i] for i in sample_index]
    return ret_list
        





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

    in_root='/home/heathcliff/Downloads/Serpentine_Left_Reference/two_folder/test'
    all_files=os.listdir(in_root)
    all_files=[os.path.join(in_root,i) for i in all_files]

    out_list,out_class=MakeARandomScoringList(all_files)
    print(out_list)
    print(out_class)

    '''
    from datetime import date
    log_path='../../Logs'
    today_str=date.today().strftime("%Y-%m-%d")
    log_file=os.path.join(log_path,today_str+'.log')
    file_handler=logging.FileHandler(log_file)
    format_str='%(asctime)s [%(levelname)s]: %(message)s'
    file_handler.setFormatter(logging.Formatter(fmt=format_str,datefmt='%Y-%m-%d-%H:%M'))
    logger.addHandler(file_handler)
    logger.setLevel('debug')




    










