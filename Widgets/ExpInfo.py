import os
import cv2
from enum import IntEnum
from PySide6.QtWidgets import QApplication
import json
import pickle
import logging
logger=logging.getLogger("LogWindow")

class CompTypes(IntEnum):
    Origin=0
    Distorted=1
    
class LFITypes(IntEnum):
    Sparse=0
    Dense=1

class AngularFormat(IntEnum):
    XY=0
    HW=1
    
class SaveFormat(IntEnum):
    Excel=0
    CSV=1
    
class PostProcessType(IntEnum):
    SROCC=0
    
class LFIFeatures(IntEnum):
    Active_ViewChanging=0
    Passive_ViewChanging=1
    Refocusing=2
    Active_Refocusing=3
    Passive_Refocusing=4
    Stereo_horizontal=5
    Stereo_vertical=6
    Stereo_full=7
    TwoD=8
    None_ViewChanging=9
    None_Refocusing=10 

class ComparisonType(IntEnum):
    SingleStimuli=0
    DoubleStimuli=1
    PairComparison=2

class ViewSaveType(IntEnum):
    png=0
    jpg=1
    bmp=2
    ppm=3

ViewSaveTypeDict={
    ViewSaveType.png:"png",
    ViewSaveType.jpg:"jpg",
    ViewSaveType.bmp:"bmp",
    ViewSaveType.ppm:"ppm"
}

class VideoSaveType(IntEnum):
    avi=0
    mp4=1
    
VideoSaveTypeDict={
    VideoSaveType.avi:"avi",
    VideoSaveType.mp4:"mp4"
}

def MakeAJsonTemplate(output_path_file):
    json_dict={}
    json_dict["LFI_Info"]=[
        {
            "Name": "Your Light field image name",
            "Origin_Path": "The path of your origin light field image",
            "Distorted_Path": "The path of your distorted light field image",
            "Type": "The type of your light field image, Sparse or Dense",
            "Angular_Format": "The angular format of your light field image, XY or HW"
        },
        {
            "Name": "Your second Light field image name",
            "Origin_Path": "The path of your origin light field image",
            "Distorted_Path": "The path of your distorted light field image",
            "Type": "The type of your light field image, Sparse or Dense",
            "Angular_Format": "The angular format of your light field image, XY or HW"
        }
    ]
    json_dict["Exp_Info"]={
        "Display_Type": "2D or 3D",
        "ThreeD_Type": "Horizontal or Vertical or Full, keep empty if 2D",
        "View_Changing": "Active or Passive or None",
        "Refocusing": "Active or Passive or None",
        "Comparison_Type": "SingleStimuli or DoubleStimuli or PairComparison",
        "Pair_Wise_Config": "The config of pair wise comparison, keep empty if not pair wise comparison",
        "Save_Format": "Excel or CSV"
    }

    with open(output_path_file,'w') as f:
        json.dump(json_dict,f,indent=4)
    
class SingleLFIInfo:
    def __init__(self, lfi_name="", type_name="", type=CompTypes.Distorted, lfi_type=LFITypes.Dense, angular_format=AngularFormat.XY, views_path=""):
        '''
        type_name: Origin, or the name of the distortion type
        type: CompTypes, Origin or Distorted
        lfi_type: LFITypes, Sparse or Dense
        angular_format: AngularFormat, XY or HW 
        views_path: the path of the views
        '''
        self.lfi_name=lfi_name
        self.type_name=type_name
        self.type=type
        self.dist_level=0 # 1-5, 5 degrees
        self.angular_format=angular_format
        self.view_path=views_path
        self.lfi_type=lfi_type

        self.refocusing_views_path=os.path.join(views_path,"views_refocusing")
        self.show_refocusing_views_path=None
        self.show_views_path=None
        self.passive_refocusing_video=None
        self.passive_video=None
        self.depth_path=None
        self.lambda_path=None

        self.img_width=0
        self.img_height=0
        self.angular_width=0
        self.angular_height=0
        self.path_dict={}

        self.max_height=0
        self.max_width=0
        self.min_height=10000
        self.min_width=10000

        self.post_fix='png' # default is png

        ret_info=self.ParseFolder(views_path)
        self.is_valid=True

        if ret_info is not None:
            self.angular_height,self.angular_width,self.img_height,self.img_width,self.path_dict=ret_info
    
    def FromViewIndexToFileIndex(self,input_hw):
        return (input_hw[0]+self.min_height,input_hw[1]+self.min_width)

    def ParseFolder(self,folder_path):
        if not os.path.exists(folder_path):
            self.is_valid=False
            return None
        all_files=os.listdir(folder_path)
        max_height=0
        max_width=0
        min_height=10000
        min_width=10000

        for img_file in all_files:
            if "depth" in img_file:
                continue
            if "lambda" in img_file or 'Lambda' in img_file:
                continue
            if os.path.isdir(os.path.join(folder_path,img_file)):
                continue
            test_img_name=img_file

        self.post_fix=test_img_name.split('.')[-1]
        path_dict={}
        for img_file in all_files:
            if "depth" in img_file:
                self.depth_path=os.path.join(folder_path,img_file)
                continue
            if "lambda" in img_file or 'Lambda' in img_file:
                self.lambda_path=os.path.join(folder_path,img_file)
                continue
            if os.path.isdir(os.path.join(folder_path,img_file)):
                continue
            temp_list=img_file.split('.')[0].split('_')
            if self.angular_format == 0:
                cur_width,cur_height=int(temp_list[0]), int(temp_list[1])
            else:
                cur_height,cur_width=int(temp_list[0]), int(temp_list[1])
            path_dict[(cur_width,cur_height)]=os.path.join(folder_path,img_file)
            if cur_height>max_height:
                max_height=cur_height
            if cur_height<min_height:
                min_height=cur_height
            if cur_width>max_width:
                max_width=cur_width
            if cur_width<min_width:
                min_width=cur_width

        test_img=cv2.imread(os.path.join(folder_path,test_img_name))
        img_height,img_width=test_img.shape[0],test_img.shape[1]

        self.max_height=max_height
        self.max_width=max_width
        self.min_height=min_height
        self.min_width=min_width
        return (max_height-min_height+1,max_width-min_width+1,img_height,img_width,path_dict)
    
    def GetViewPath(self, a_w,a_h):
        if a_w>=0 and a_w<self.angular_width and a_h>=0 and a_h<self.angular_height:
            a_h,a_w=self.FromViewIndexToFileIndex((a_h,a_w))
            return self.path_dict[(a_w,a_h)]
    
    def GetViewName(self,a_w,a_h):
        a_h,a_w=self.FromViewIndexToFileIndex((a_h,a_w))
        if self.angular_format ==  AngularFormat.XY:
            return str(a_w)+"_"+str(a_h)+"."+self.post_fix
        else:
            return str(a_h)+"_"+str(a_w)+"."+self.post_fix
        
    def GetPureViewName(self,a_w,a_h):
        a_h,a_w=self.FromViewIndexToFileIndex((a_h,a_w))
        if self.angular_format ==  AngularFormat.XY:
            return str(a_w)+"_"+str(a_h)
        else:
            return str(a_h)+"_"+str(a_w)
    
    @property
    def IsValid(self):
        return self.is_valid
    @IsValid.setter
    def IsValid(self, value):
        self.is_valid=value
    
    @property
    def RefocusingViewsPath(self):
        return self.refocusing_views_path

    @RefocusingViewsPath.setter 
    def RefocusingViewsPath(self, value):
        self.refocusing_views_path=value
    
    @property
    def PassiveVideo(self):
        return self.passive_video
    @PassiveVideo.setter
    def PassiveVideo(self, value):
        self.passive_video=value
        
    
class ExpLFIInfo:
    def __init__(self,lfi_name,ori_path=[],dist_path=[],lfi_type=[],angular_format=AngularFormat.XY):
        '''
        angular_format: 0: x_y, 1: h_w
        '''
        self.ori_paths=ori_path
        self.dist_paths=dist_path
        self.lfi_types=lfi_type
        self.angular_format=angular_format

        self.lfi_names=lfi_name
        self.all_LFI_info={}

        self.InitLFIsInfo()
        self.broken_names=self.LFIsInfoCheck()
        if len(self.broken_names)>0:
            self.is_valid=False
        else:
            self.is_valid=True

    def InitLFIsInfo(self):
        for lfi_name_index in range(len(self.lfi_names)):
            lfi_name=self.lfi_names[lfi_name_index]
            lfi_type=self.lfi_types[lfi_name_index]

            self.all_LFI_info[lfi_name]={}
            if len(self.ori_paths)==0:
                self.all_LFI_info[lfi_name]["Origin"]=None
            else:
                self.all_LFI_info[lfi_name]["Origin"]=SingleLFIInfo(
                    lfi_name=lfi_name,
                    type_name="Origin",
                    type=CompTypes.Origin,
                    lfi_type=lfi_type,
                    angular_format=self.angular_format,
                    views_path=self.ori_paths[lfi_name_index])

            all_dist_folders=self.WalkDistFolder(self.dist_paths[lfi_name_index])
            for dist_folder_name in all_dist_folders:
                dist_folder=os.path.join(self.dist_paths[lfi_name_index],dist_folder_name)
                self.all_LFI_info[lfi_name][dist_folder_name]={}
                for dist_level in range(1,6):
                    self.all_LFI_info[lfi_name][dist_folder_name][dist_level]=SingleLFIInfo(
                        lfi_name=lfi_name,
                        type_name=dist_folder_name,
                        type=CompTypes.Distorted,
                        lfi_type=lfi_type,
                        angular_format=self.angular_format,
                        views_path=os.path.join(dist_folder,str(dist_level)))
                    self.all_LFI_info[lfi_name][dist_folder_name][dist_level].dist_level=dist_level
    
    def AddLFIInfo(self,lfi_name,ori_path,dist_path):
        check_path=["Origin"]
        all_dist_folders=os.listdir(dist_path)
        for dist_folder in all_dist_folders:
            dist_folder=os.path.join(dist_path,dist_folder)
            if os.path.isdir(dist_folder):
                dist_folder_name=os.path.basename(dist_folder)
            check_path.append(dist_folder_name)
        if not self.CheckLFIInfo(0,check_path):
            return False

        self.lfi_names.append(lfi_name)
        self.ori_paths.append(ori_path)
        self.dist_paths.append(dist_path)
        self.all_LFI_info[lfi_name]={}
        self.all_LFI_info[lfi_name]["Origin"]=SingleLFIInfo(lfi_name,"Origin",LFITypes.Origin,self.angular_format,ori_path)

        all_dist_folders=os.listdir(dist_path)
        for dist_folder in all_dist_folders:
            dist_folder=os.path.join(dist_path,dist_folder)
            if os.path.isdir(dist_folder):
                dist_folder_name=os.path.basename(dist_folder)
                self.all_LFI_info[lfi_name][dist_folder_name]=SingleLFIInfo(lfi_name,dist_folder_name,LFITypes.Distorted,self.angular_format,dist_path)
        return True
    
    def GetOriginLFIInfo(self,lfi_name):
        return self.all_LFI_info[lfi_name]["Origin"]
    
    def GetCertainDistLFIInfo(self,lfi_name,dist_name,i=0):
        return self.all_LFI_info[lfi_name][dist_name][i]

    def GetAllLFNames(self):
        return list(self.all_LFI_info.keys())
    
    def GetAllDistNames(self,lfi_name):
        tmp=list(self.all_LFI_info[lfi_name].keys())
        tmp.remove("Origin")
        return tmp
    
    def GetLFIInfo(self,lfi_name,dist_type,i=0):
        '''
        Not safe now
        '''
        if dist_type == "Origin":
            return self.all_LFI_info[lfi_name]["Origin"]
        else:
            return self.all_LFI_info[lfi_name][dist_type][i]
    
    def WalkDistFolder(self,root_path):
        all_dist_types=[]
        all_dist_folders=os.listdir(root_path)
        for dist_folder in all_dist_folders:
            dist_folder=os.path.join(root_path,dist_folder)
            if os.path.isdir(dist_folder):
                dist_folder_name=os.path.basename(dist_folder)
                all_dist_types.append(dist_folder_name)
        return all_dist_types
             
    def LFIsInfoCheck(self):
        test_name=self.lfi_names[0]
        test_lfi=self.all_LFI_info[test_name]
        test_dist_name=list(test_lfi.keys())
        ret_names=[]
        for lfi_name_index in range(1,len(self.lfi_names)):
            if not self.CheckLFIInfo(lfi_name_index,test_dist_name):
                ret_names.append(self.lfi_names[lfi_name_index])
        return ret_names
        
    def CheckLFIInfo(self,lfi_name_index,all_dist_name):
        cur_lfi_name=self.lfi_names[lfi_name_index]
        cur_lfi_info=self.all_LFI_info[cur_lfi_name]
        if len(cur_lfi_info.keys()) != len(all_dist_name):
            return False
        for dist_name in all_dist_name:
            if dist_name not in cur_lfi_info.keys():
                return False
        return True

class ExpSetting:
    def __init__(self,lfi_features=[],comparison_type=ComparisonType.DoubleStimuli,save_format=SaveFormat.CSV,post_processing=PostProcessType.SROCC):
        self.lfi_features=lfi_features
        self.comparison_type=comparison_type
        self.save_format=save_format
        self.post_processing=post_processing

        self.pair_wise_config=""
        self.has_preprocess=False

        self.training_show_list=[]
        self.test_show_list=[]

        screen=QApplication.primaryScreen().geometry()
        self.screen_width,self.screen_height=screen.width(),screen.height()
        self.VideoSaveType=VideoSaveType.mp4
        self.ViewSaveType=ViewSaveType.png
        self.ViewSaveTypeStr=ViewSaveTypeDict[self.ViewSaveType]
        self.VideoSaveTypeStr=VideoSaveTypeDict[self.VideoSaveType]
    
def GetShowList(lfi_info:ExpLFIInfo, exp_setting:ExpSetting,mode="trainging"):
    '''
    return a list of show list
    '''
    show_list=[]
    if exp_setting.comparison_type == ComparisonType.PairComparison:
        pair_wise_config=exp_setting.pair_wise_config
        with open(pair_wise_config,'r') as f:
            pair_wise_dict=json.load(f)
        if mode == "training":
            pair_wise_dict=pair_wise_dict['training']
        else:
            pair_wise_dict=pair_wise_dict['test']
        for cmp_key in pair_wise_dict.keys():
            cur_info=pair_wise_dict[cmp_key]
            show_list.append([cur_info["lfi_name"],cur_info["left"],int(cur_info["left_level"]),cur_info["right"],int(cur_info["right_level"])])
    else:
        for lfi_name in lfi_info.GetAllLFNames():
            origin_type="Origin"
            for dist_name in lfi_info.GetAllDistNames(lfi_name):
                for i in range(1,6):
                    show_list.append([lfi_name,dist_name,i,origin_type,0])
    return show_list


class ProjectInfo:
    '''
    A whole project managing class
    '''
    def __init__(self,project_path=None,software_version='2.0'):
        self.project_path=project_path
        self.software_version=software_version
        if not os.path.exists(project_path) or project_path is None:
            self.project_name=None
            self.training_LFI_info=None
            self.test_LFI_info=None
            self.exp_setting=None
            self.version=None
            self.subject_list=[]
        else:
            self.ReadFromFile()
    
    def ReadFromFile(self):
        with open(self.project_path,'rb') as fid:
            self.project_version=pickle.load(fid)
            if self.project_version != self.software_version:
                logger.error("The software version is not matched! The software version is %s, but the project version is %s"%(self.software_version,self.project_version))
                return False
            self.project_name=pickle.load(fid)
            self.training_LFI_info=pickle.load(fid)
            self.test_LFI_info=pickle.load(fid)
            self.exp_setting=pickle.load(fid)
            self.subject_list=pickle.load(fid)

    def SaveToFile(self,save_file): 
        with open(save_file,'wb') as fid:
            pickle.dump(self.project_version,fid)
            pickle.dump(self.project_name,fid)
            pickle.dump(self.training_LFI_info,fid)
            pickle.dump(self.test_LFI_info,fid)
            pickle.dump(self.exp_setting,fid)
            pickle.dump(self.subject_list)
    
    def PrintAll(self):
        ret_str=''
        ret_str+=f"Project Name: {self.project_name}\n"
        ret_str+=f"Project Version: {self.project_version}\n"
        ret_str+="-----------Training LFI Info-----------\n"
        ret_str+=self.PrintLFIInfo(self.training_LFI_info)
        ret_str+="-----------Test LFI Info-----------\n"
        ret_str+=self.PrintLFIInfo(self.test_LFI_info)


    
    def PrintLFIInfo(self,lfi_info:ExpLFIInfo):
        ret_str=''
        ret_str+="All LFI:\n"
        all_lfi_names=lfi_info.GetAllLFNames()
        all_dist_names=lfi_info.GetAllDistNames()
        dist_names_str=['%s ' % x for x in all_dist_names]
        ret_str+="All Distortion: " + dist_names_str +"\n"
        ret_str+="All LFI: \n"
        for idx, lif_name in enumerate(all_lfi_names):
            origin_path=lfi_info.ori_paths[idx]
            dist_path=lfi_info.dist_paths[idx]
            lfi_type=lfi_info.lfi_types[idx]
            angular_format=lfi_info.angular_formats[idx]
            ret_str+="Light field image name: %s\n" % lif_name
            ret_str+="Original path: %s\n" %origin_path
            ret_str+="Distortion path: %s\n" %dist_path
            if lfi_type == LFITypes.Sparse:
                ret_str+="Light field image type: Sparse\n"
            else:
                ret_str+="Light field image type: Dense\n"
            if angular_format == AngularFormat.XY:
                ret_str+="Angular format: XY\n"
            else:
                ret_str+="Angular format: HW\n"
        return ret_str

def ReadExpConfig(file_path):
    training_LFI_info=None
    test_LFI_info=None
    exp_setting=None
    with open(file_path,'rb') as fid:
        training_LFI_info=pickle.load(fid)
        test_LFI_info=pickle.load(fid)
        exp_setting=pickle.load(fid)
    return training_LFI_info,test_LFI_info,exp_setting
