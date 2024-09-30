import os
import cv2
from enum import IntEnum
from PySide6.QtWidgets import QApplication
import json
import pickle
import logging
from numpy import unique
import sys
import shutil
from random import shuffle
import weakref
sys.path.append('../Utils/')

import PathManager
import PlayList

logger=logging.getLogger("LogWindow")

class CompTypes(IntEnum):
    '''compression types, not comparison'''
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

class DisplayType(IntEnum):
    TwoD=0
    ThreeD_LR=1
    ThreeD_UD=2
    ThreeD_Full=3

class FeatureType(IntEnum):
    Active=0
    Passive=1
    None_Type=2

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
    mov=2
    wmv=3
    webm=4
    mkv=5
    mpg=6
    flv=7
    swf=8
    ogg=9
    
VideoSaveTypeDict={
    VideoSaveType.avi:"avi",
    VideoSaveType.mp4:"mp4",
    VideoSaveType.mov:"mov",
    VideoSaveType.wmv:"wmv",
    VideoSaveType.webm:"webm",
    VideoSaveType.mkv:"mkv",
    VideoSaveType.mpg:"mpg",
    VideoSaveType.flv:"flv",
    VideoSaveType.swf:"swf",
    VideoSaveType.ogg:"ogg"
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
    def __init__(self, lfi_name="", type_name="", type=CompTypes.Distorted, lfi_type=LFITypes.Dense, angular_format=AngularFormat.XY, views_path="",skip_preprocessing=False):
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

        self.refocusing_views_path=os.path.join(views_path,PathManager.inner_views_refocusing_path)
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

        self.is_valid=True
        if not skip_preprocessing:
            ret_info=self.ParseFolder(views_path)
            if ret_info is not None:
                self.angular_height,self.angular_width,self.img_height,self.img_width,self.path_dict=ret_info
    
    def FromViewIndexToFileIndex(self,input_hw):
        return (input_hw[0]+self.min_height,input_hw[1]+self.min_width)

    def ParseFolder(self,folder_path):
        if not os.path.exists(folder_path):
            self.is_valid=False
            return None
        all_files=os.listdir(folder_path)
        if len(all_files)==0:
            self.is_valid=False
            return None
        view_num=0
        for img_file in all_files:
            if self.post_fix in img_file and PathManager.thumbnail_name not in img_file:
                view_num+=1
        if view_num==0:
            return None
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
    
    def GetAllPossibleDepthVal(self):
        depth_map=cv2.imread(self.depth_path,cv2.IMREAD_GRAYSCALE)
        if depth_map.shape[0]!=self.img_height or depth_map.shape[1]!=self.img_width:
            depth_map=cv2.resize(depth_map,(self.img_width,self.img_height))

        all_depth_values=unique(depth_map)
        return all_depth_values
    
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
    def __init__(self,lfi_name=None,ori_path=[],dist_path=[],lfi_type=[],angular_format=AngularFormat.XY):
        '''
        angular_format: 0: x_y, 1: h_w
        '''
        self.ori_paths=ori_path
        self.dist_paths=dist_path
        self.lfi_types=lfi_type
        self.angular_format=angular_format

        self.lfi_names=lfi_name
        self.all_dist_types={}
        self.all_dist_levels={}

        self.all_LFI_info={}

        if self.lfi_names is not None:
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
            self.all_dist_types[lfi_name]=all_dist_folders
            self.all_dist_levels[lfi_name]={}

            for dist_folder_name in all_dist_folders:
                dist_folder=os.path.join(self.dist_paths[lfi_name_index],dist_folder_name)
                self.all_LFI_info[lfi_name][dist_folder_name]={}
                self.all_dist_levels[lfi_name][dist_folder_name]=[]
                all_dist_levels=os.listdir(dist_folder)
                for dist_level in all_dist_levels:
                    if not os.path.isdir(os.path.join(dist_folder,dist_level)):
                        continue
                    self.all_LFI_info[lfi_name][dist_folder_name][dist_level]=SingleLFIInfo(
                        lfi_name=lfi_name,
                        type_name=dist_folder_name,
                        type=CompTypes.Distorted,
                        lfi_type=lfi_type,
                        angular_format=self.angular_format,
                        views_path=os.path.join(dist_folder,str(dist_level)))
                    self.all_dist_levels[lfi_name][dist_folder_name].append(dist_level)
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

    def ParseLFFolder(self,in_path):
        all_dist=os.listdir(in_path)
        all_dist_types=[]
        all_dist_levels={}
        for dist_name in all_dist:
            if not os.path.isdir(os.path.join(in_path,dist_name)):
                continue
            all_dist_types.append(dist_name)
            all_dist_levels[dist_name]=[]

            dist_path=os.path.join(in_path,dist_name)
            all_levels=os.listdir(dist_path)
            for level_name in all_levels:
                if not os.path.isdir(os.path.join(dist_path,level_name)):
                    continue
                all_dist_levels[dist_name].append(level_name)
        return all_dist_types,all_dist_levels
    
    def AddOriginLF(self,lfi_name,in_lfi_type,in_angular_format,spatial_size,angular_size,in_view_path):
        if lfi_name not in self.all_LFI_info.keys():
            self.all_LFI_info[lfi_name]={}
        if in_view_path == "":
            return
        self.all_LFI_info[lfi_name]["Origin"]=SingleLFIInfo(
            lfi_name=lfi_name,
            type_name="Origin",
            type=CompTypes.Origin,
            lfi_type=in_lfi_type,
            angular_format=in_angular_format,
            views_path=in_view_path,
            skip_preprocessing=False
        )
        
    def AddSingleLFIInfo(self,lfi_name,in_lfi_type,in_angular_format,spatial_size,angular_size,dist_type,dist_level,in_view_path,skip_preprocessing=False,cmp_type=ComparisonType.DoubleStimuli):
        if lfi_name not in self.all_LFI_info.keys():
            self.all_LFI_info[lfi_name]={}
        if dist_type not in self.all_LFI_info[lfi_name].keys():
            self.all_LFI_info[lfi_name][dist_type]={}
        cur_lf_info=SingleLFIInfo(
            lfi_name=lfi_name,
            type_name=dist_type,
            type=CompTypes.Distorted,
            lfi_type=in_lfi_type,
            angular_format=in_angular_format,
            views_path=in_view_path,skip_preprocessing=skip_preprocessing)
        
        in_height,in_width=spatial_size
        in_angular_height,in_angular_width=angular_size 

        if not skip_preprocessing:
            if cur_lf_info.img_height!= in_height or cur_lf_info.img_width != in_width or cur_lf_info.angular_height != in_angular_height or cur_lf_info.angular_width != in_angular_width:
                logger.error(f"Input image height: {in_height}, width: {in_width}, angular height: {in_angular_height}, angular width: {in_angular_width}; Size from folder image height {cur_lf_info.img_height}, width: {cur_lf_info.img_width}, angular height: {cur_lf_info.angular_height}, angular width: {cur_lf_info.angular_width}")
                logger.error("The input data size does not match the size in the Json file! Please Check it carefully!")
        else:
            cur_lf_info.img_width=in_width
            cur_lf_info.img_height=in_height
            cur_lf_info.angular_height=in_angular_height
            cur_lf_info.angular_width=in_angular_width

            show_view_path=os.path.join(in_view_path,PathManager.inner_show_views_path)
            if os.path.exists(show_view_path):
                cur_lf_info.show_views_path=show_view_path
            
            show_refocusing_path=os.path.join(in_view_path,PathManager.inner_show_refocusing_path)
            if os.path.exists(show_refocusing_path):
                cur_lf_info.show_refocusing_views_path=show_refocusing_path
            
            passive_view_video=os.path.join(show_view_path,PathManager.passive_view_video_name)
            passive_refocusing_video=os.path.join(show_refocusing_path,PathManager.passive_refocusing_video_name)
            depth_path=os.path.join(show_view_path,PathManager.inner_depth_map)

            if os.path.exists(passive_view_video):
                cur_lf_info.passive_video=passive_view_video
            if os.path.exists(passive_refocusing_video):
                cur_lf_info.passive_refocusing_video=passive_refocusing_video
            if os.path.join(depth_path):
                cur_lf_info.depth_path=depth_path

            cur_lf_info.ParseFolder(show_view_path)

        self.all_LFI_info[lfi_name][dist_type][dist_level]=cur_lf_info

    def AddLFIInfo(self,lfi_name,in_lfi_type,in_angular_format,spatial_size,angular_size,in_path):
        all_dist_types,all_dist_levels=self.ParseLFFolder(in_path)
        spatial_height,spatial_width=spatial_size
        angular_height,angular_width=angular_size
        
        for dist_type in all_dist_types:
            self.all_LFI_info[lfi_name]={}
            self.all_LFI_info[lfi_name][dist_type]={}
            for dist_level in all_dist_levels:
                cur_lf_info=SingleLFIInfo(
                    lfi_name=lfi_name,
                    type_name=dist_type,
                    type=CompTypes.Distorted,
                    lfi_type=in_lfi_type,
                    angular_format=in_angular_format,
                    views_path="")
                cur_lf_info.angular_height=angular_height
                cur_lf_info.angular_width=angular_width
                cur_lf_info.img_height=spatial_height
                cur_lf_info.img_width=spatial_width

                cur_lf_info.dist_level=dist_level

                show_view_path=os.path.join(in_path,dist_type,dist_level,PathManager.inner_show_views_path)
                if os.path.exists(show_view_path):
                    cur_lf_info.show_views_path=show_view_path
                
                show_refocusing_path=os.path.join(in_path,dist_type,dist_level,PathManager.inner_show_refocusing_path)
                if os.path.exists(show_refocusing_path):
                    cur_lf_info.show_refocusing_views_path=show_refocusing_path
                
                passive_view_video=os.path.join(show_view_path,PathManager.passive_view_video_name)
                passive_refocusing_video=os.path.join(show_refocusing_path,PathManager.passive_refocusing_video_name)
                depth_path=os.path.join(show_view_path,PathManager.inner_depth_map)

                if os.path.exists(passive_view_video):
                    cur_lf_info.passive_video=passive_view_video
                if os.path.exists(passive_refocusing_video):
                    cur_lf_info.passive_refocusing_video=passive_refocusing_video
                if os.path.join(depth_path):
                    cur_lf_info.depth_path=depth_path

                cur_lf_info.view_path=os.path.join(in_path,)

                cur_lf_info.ParseFolder(show_view_path)
                
                self.all_LFI_info[lfi_name][dist_type][dist_level]=cur_lf_info
    
    def GetOriginLFIInfo(self,lfi_name):
        return self.all_LFI_info[lfi_name]["Origin"]
    
    def GetCertainDistLFIInfo(self,lfi_name,dist_name,i=0):
        return self.all_LFI_info[lfi_name][dist_name][i]

    def GetAllLFNames(self):
        return list(self.all_LFI_info.keys())
    
    def GetAllDistNames(self,lfi_name):
        tmp=list(self.all_LFI_info[lfi_name].keys())
        if "Origin" in tmp:
            tmp.remove("Origin")
        return tmp
    
    def GetAllDistLevels(self,lfi_name,dist_name):
        return list(self.all_LFI_info[lfi_name][dist_name].keys())
    
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
    def __init__(self,lfi_features=[],comparison_type=ComparisonType.DoubleStimuli,save_format=SaveFormat.CSV,post_processing=PostProcessType.SROCC,two_folder_mode=False):
        self.lfi_features=lfi_features
        self.comparison_type=comparison_type
        self.save_format=save_format
        self.post_processing=post_processing

        self.project_info_ref=None

        if LFIFeatures.Active_Refocusing in self.lfi_features:
            self.refocusing_type=FeatureType.Active
        elif LFIFeatures.Passive_Refocusing in self.lfi_features:
            self.refocusing_type=FeatureType.Passive
        else:
            self.refocusing_type=FeatureType.None_Type
        
        if LFIFeatures.Active_ViewChanging in self.lfi_features:
            self.view_changing_type=FeatureType.Active
        elif LFIFeatures.Passive_ViewChanging in self.lfi_features:
            self.view_changing_type=FeatureType.Passive
        else:
            self.view_changing_type=FeatureType.None_Type
        
        self.display_type=DisplayType.TwoD
        if LFIFeatures.TwoD in self.lfi_features:
            self.display_type=DisplayType.TwoD
        elif LFIFeatures.ThreeD in self.lfi_features:
            if LFIFeatures.Stereo_horizontal in self.lfi_features:
                self.display_type=DisplayType.ThreeD_LR
            if LFIFeatures.Stereo_vertical in self.lfi_features:
                self.display_type=DisplayType.ThreeD_UD
            if LFIFeatures.Stereo_full in self.lfi_features:
                self.display_type=DisplayType.ThreeD_Full

        self.pair_wise_config=""
        self.pair_wise_dict={}
        self.skip_preprocessing=False
        self.has_preprocess=False

        self.training_show_list=[]
        self.test_show_list=[]

        screen=QApplication.primaryScreen().geometry()
        self.screen_width,self.screen_height=screen.width(),screen.height()
        self.ViewSaveType=ViewSaveType.png
        self.VideoSaveType=VideoSaveType.mp4
        self.ViewSaveTypeStr=ViewSaveTypeDict[self.ViewSaveType]
        self.VideoSaveTypeStr=VideoSaveTypeDict[self.VideoSaveType]

        # self.VideoSaveTypeStr=VideoSaveTypeDict[self.VideoSaveType]
        # May exist more than one possible video types
        self.input_video_type=[]
        self.input_video_type_str=[]        

        self.two_folder_mode=two_folder_mode

        self.auto_play=True
        self.loop_times=-1 # infinit
        self.fps=-1  # decided by the input video

        self.score_levels=[5,5]
        self.score_values=[]
        self.score_definition=None
        self.score_names=['Overall quality','Image quality']
        self.auto_transition=False
        self.pause_allowed=False
        self.passive_control_backend='MPV' # depreted now
        self.first_loop_skip=False
        self.skip_hint_text=""
        self.hint_text_font_size=PathManager.hint_text_font_size
        self.table_font_size=PathManager.scoring_table_point_size
        self.allow_undistinguishable=True
    
    def AddInputVideoType(self,video_type):
        if isinstance(video_type,VideoSaveType):
            self.input_video_type.append(video_type)
            self.input_video_type_str.append(VideoSaveTypeDict[video_type])
        if isinstance(video_type,str):
            for key in VideoSaveTypeDict.keys():
                if VideoSaveTypeDict[key].lower() == video_type.lower():
                    self.input_video_type.append(VideoSaveTypeDict[key])
                    self.input_video_type_str.append(video_type)
                    break
    
    def GetProjectInfo(self):
        return self.project_info_ref()

    def SetProjectInfo(self,project_info):
        self.project_info_ref=weakref.ref(project_info)
    
def GetShowList(lfi_info:ExpLFIInfo, exp_setting:ExpSetting, mode="trainging"):
    '''
    return a list of show list
    '''
    show_list=[]
    view_post_fix=exp_setting.ViewSaveTypeStr
    video_post_fix=exp_setting.VideoSaveTypeStr
    if exp_setting.comparison_type == ComparisonType.PairComparison:
        pair_wise_dict=exp_setting.pair_wise_dict
        if mode == "training":
            pair_wise_dict=pair_wise_dict['training']
        else:
            pair_wise_dict=pair_wise_dict['test']
        for cmp_key in pair_wise_dict.keys():
            cur_info=pair_wise_dict[cmp_key]
            cur_lfi_info=lfi_info.GetLFIInfo(cur_info['lfi_name'],cur_info['left'],cur_info['left_level'])
            cur_exp_show_path_manager=PathManager.ExpShowPathManager(cur_lfi_info.view_path,mode,True,video_post_fix=video_post_fix,out_img_post_fix=view_post_fix,pair_comparison_index=cmp_key)
            show_list.append([cur_info["lfi_name"],cur_info["left"],cur_info["left_level"],cur_info["right"],cur_info["right_level"],cur_exp_show_path_manager])
    else:
        for lfi_name in lfi_info.GetAllLFNames():
            origin_type="Origin"
            for dist_name in lfi_info.GetAllDistNames(lfi_name):
                all_dist_levels=lfi_info.GetAllDistLevels(lfi_name,dist_name)
                for dist_level in all_dist_levels:
                    cur_lfi_info=lfi_info.GetLFIInfo(lfi_name,dist_name, dist_level)
                    cur_exp_show_path_manager=PathManager.ExpShowPathManager(cur_lfi_info.view_path,mode,use_pair_comparison=False,video_post_fix=video_post_fix,out_img_post_fix=view_post_fix)
                    show_list.append([lfi_name,dist_name,dist_level,origin_type,0,cur_exp_show_path_manager])
    return show_list

class ProjectInfo:
    '''
    A whole project managing class
    '''
    def __init__(self,project_name=None,root_path='./',project_version='2.0'):
        self.project_name=project_name
        self.root_path=root_path

        if self.project_name is None:
            self.project_path=None
            self.project_file=None
        else:
            self.project_path=os.path.join(root_path,project_name)
            self.project_file=os.path.join(self.project_path,project_name+'.lfqoe')
            if not os.path.exists(self.project_path):
                os.makedirs(self.project_path)

        self.software_version=PathManager.software_version
        self.project_version=project_version
        self.training_scoring_lfi_info=AllScoringLFI("training")
        self.test_scoring_lfi_info=AllScoringLFI("test")

        if not os.path.exists(self.project_file) or self.project_path is None:
            self.training_LFI_info=None
            self.test_LFI_info=None
            self.exp_setting=None
            self.project_version=PathManager.software_version
            self.subject_list=[]
        else:
            self.ReadFromFile()
    
    def InitAllScoringLFIInfo(self):
        if self.exp_setting.two_folder_mode:
            self.training_scoring_lfi_info=self.training_LFI_info
            self.test_scoring_lfi_info=self.test_LFI_info
            self.training_scoring_lfi_info.mode="training"
            self.test_scoring_lfi_info.mode="test"
            return
        if self.exp_setting.has_preprocess:
            self.training_scoring_lfi_info.GetAllScoringLFI(self.exp_setting,self.training_LFI_info)
            self.test_scoring_lfi_info.GetAllScoringLFI(self.exp_setting,self.test_LFI_info)
            
    def SetParameters(self,training_lfi_info,test_lfi_info,exp_setting):
        self.training_LFI_info=training_lfi_info
        self.test_LFI_info=test_lfi_info
        self.exp_setting=exp_setting
    

    def ReadFromFile(self):
        with open(self.project_file,'rb') as fid:
            self.project_version=pickle.load(fid)
            '''
            if self.project_version != self.software_version:
                logger.error("The software version is not matched! The software version is %s, but the project version is %s"%(self.software_version,self.project_version))
                return False
            '''
            self.project_name=pickle.load(fid)
            self.project_path=pickle.load(fid)
            self.training_LFI_info=pickle.load(fid)
            self.test_LFI_info=pickle.load(fid)
            exp_setting=pickle.load(fid)
            self.exp_setting=ExpSetting(exp_setting.lfi_features,exp_setting.comparison_type,exp_setting.save_format,exp_setting.post_processing,exp_setting.two_folder_mode)

            all_exp_setting_vars=dir(exp_setting)
            all_exp_setting_vars=[x for x in all_exp_setting_vars if not x.startswith('__') and not x.startswith('_')]
            all_exp_setting_vars=[x for  x in all_exp_setting_vars if not callable(getattr(exp_setting,x))]

            for var in all_exp_setting_vars:
                setattr(self.exp_setting,var,getattr(exp_setting,var))

            self.subject_list=pickle.load(fid)
        
        self.exp_setting.SetProjectInfo(self)
        self.InitAllScoringLFIInfo()

    def SaveToFile(self,save_file=None): 
        if save_file is None:
            save_file=self.project_file
        else:
            self.project_file=save_file
            self.project_path=os.path.dirname(self.project_path)
            if not os.path.exists(self.project_path):
                os.makedirs(self.project_path)

        with open(save_file,'wb') as fid:
            pickle.dump(self.project_version,fid)
            pickle.dump(self.project_name,fid)
            pickle.dump(self.project_path,fid)
            pickle.dump(self.training_LFI_info,fid)
            pickle.dump(self.test_LFI_info,fid)
            self.exp_setting.project_info_ref=None
            pickle.dump(self.exp_setting,fid)
            pickle.dump(self.subject_list,fid)
        self.exp_setting.SetProjectInfo(self)
    
    def PrintAll(self):
        ret_str=''
        ret_str+=f"Project Name: {self.project_name}\n"
        ret_str+=f"Project Version: {self.project_version}\n"
        ret_str+="-----------Training LFI Info-----------\n"
        ret_str+=self.PrintLFIInfo(self.training_LFI_info)
        ret_str+="-----------Test LFI Info-----------\n"
        ret_str+=self.PrintLFIInfo(self.test_LFI_info)
        ret_str+="-----------Experiment Setting-----------\n"
        if LFIFeatures.TwoD in self.exp_setting.lfi_features:
            ret_str+="Display type: 2D\n"
        else:
            ret_str+="Dispylay type: 3D\n"

        if LFIFeatures.Active_Refocusing in self.exp_setting.lfi_features:
            ret_str+="Refocusing feature: active\n"
        if LFIFeatures.Passive_Refocusing in self.exp_setting.lfi_features:
            ret_str+="Refocusing feature: passive\n"
        if LFIFeatures.None_Refocusing in self.exp_setting.lfi_features:
            ret_str+="Refocusing feature: none\n"
        
        if LFIFeatures.Active_ViewChanging in self.exp_setting.lfi_features:
            ret_str+="View changing feature: active\n"
        if LFIFeatures.Passive_ViewChanging in self.exp_setting.lfi_features:
            ret_str+="View changing feature: passive\n"
        if LFIFeatures.None_ViewChanging in self.exp_setting.lfi_features:
            ret_str+="View changing feature: none\n"

        if self.exp_setting.comparison_type == ComparisonType.DoubleStimuli:
            ret_str+=f"Comparison type: Double Stimuli\n"
        if self.exp_setting.comparison_type == ComparisonType.SingleStimuli:
            ret_str+=f"Comparison type: Single Stimuli\n"
        if self.exp_setting.comparison_type == ComparisonType.PairComparison:
            ret_str+=f"Comparison type: Pair Comparison\n"
        if self.exp_setting.save_format == SaveFormat.CSV:
            ret_str+=f"Save format: CSV\n"
        else:
            ret_str+=f"Save format: Excel\n"
        
        if self.exp_setting.post_processing == PostProcessType.SROCC:
            ret_str+=f"Post processing: SROCC\n"
        ret_str+=f"Video save type: {self.exp_setting.VideoSaveTypeStr}\n"
        ret_str+=f"View save type: {self.exp_setting.ViewSaveTypeStr}\n"

        if self.exp_setting.has_preprocess:
            ret_str+="Has been preprocessed: Yes\n"
        else:
            ret_str+="Has been preprocessed: No\n"

        if self.exp_setting.auto_play:
            ret_str+="Auto play the passive mode: Yes\n"
        else:
            ret_str+="Auto play the passive mode: No\n"

        if self.exp_setting.loop_times !=0 and self.exp_setting.loop_times != 1:
            ret_str+="Loop the passive mode: Yes\n"
            loop_times=self.exp_setting.loop_times
            if loop_times<0:
                loop_times="Inf\n"
            ret_str+="Loop times: {}\n".format(loop_times)
        else:
            ret_str+="Loop the passive mode: No\n"
            ret_str+="Loop times: does not loop\n"
        
        if self.exp_setting.fps<0:
            ret_str+="The passive mode FPS: following the input video\n" 
        else:
            ret_str+="The passive mode FPS: fixed to %d\n" %(self.exp_setting.fps) 

        ret_str+="-----------Subject List-----------\n"
        ret_str+="Num of subjects: %d\n" % len(self.subject_list)
        for idx,subject_name in enumerate(self.subject_list):
            ret_str+="Subject %d name: %s\n" %(idx+1, subject_name)
        return ret_str
    
    def PrintLFIInfo(self,lfi_info:ExpLFIInfo):
        ret_str=''
        if self.exp_setting.two_folder_mode:
            ret_str+="The test folder is %s\n" %(lfi_info.in_folder_path)
            return ret_str
        all_lfi_names=lfi_info.GetAllLFNames()
        all_name_str='['+' '.join(['%s ' % x for x in all_lfi_names])+']'
        ret_str+="All LFIs: " + all_name_str + "\n"
        ret_str+=f"Num of LFIs: {len(all_lfi_names)}\n"
        all_dist_names=lfi_info.GetAllDistNames(all_lfi_names[0])
        dist_names_str='['+' '.join(['%s ' % x for x in all_dist_names])+']'
        ret_str+="All Distortion: " + dist_names_str +"\n"
        ret_str+="All LFI: \n"
        for idx, lfi_name in enumerate(all_lfi_names):
            if self.exp_setting.skip_preprocessing:
                origin_path='--no input'
            if "Origin" in lfi_info.all_LFI_info[lfi_name].keys():
                origin_path=lfi_info.all_LFI_info[lfi_name]["Origin"].view_path
            else:
                origin_path="# no input #"
            if origin_path == "":
                origin_path="# no input #"
            ret_str+="Light field image name: %s\n" % lfi_name
            ret_str+="SRC path: %s\n" %origin_path
            
            all_dist_types=lfi_info.GetAllDistNames(lfi_name)
            test_all_level=lfi_info.GetAllDistLevels(lfi_name,all_dist_types[0])

            test_lfi_info=lfi_info.GetLFIInfo(lfi_name,all_dist_types[0],test_all_level[0])
            lfi_type=test_lfi_info.lfi_type
            angular_format=lfi_info.angular_format
            if lfi_type == LFITypes.Sparse:
                ret_str+="Light field image type: Sparse\n"
            else:
                ret_str+="Light field image type: Dense\n"
            if angular_format == AngularFormat.XY:
                ret_str+="Angular format: XY\n"
            else:
                ret_str+="Angular format: HW\n"

            for dist_type in all_dist_types:
                all_dist_levels=lfi_info.GetAllDistLevels(lfi_name,dist_type)
                ret_str+="  Distortion type: %s\n" %dist_type
                for dist_level in all_dist_levels:
                    ret_str+=f"    Distortion level: {dist_level}\n"
                    cur_lfi_info=lfi_info.GetLFIInfo(lfi_name,dist_type,dist_level)
                    dist_path=cur_lfi_info.view_path
                    ret_str+=f"    Distortion path: {dist_path}\n"
        return ret_str

    def GetExpSetting(self):
        return self.exp_setting

def ReadExpConfig(file_path):
    training_LFI_info=None
    test_LFI_info=None
    exp_setting=None
    with open(file_path,'rb') as fid:
        training_LFI_info=pickle.load(fid)
        test_LFI_info=pickle.load(fid)
        exp_setting=pickle.load(fid)
    return training_LFI_info,test_LFI_info,exp_setting


class ScoringExpLFIInfo:
    '''
    Used for the scoring stage.
    With this we do not need to parse the folder or calculate the directions.
    It helps make things easier and is more efficient.
    '''
    def __init__(self) -> None:
        self.img_height=None
        self.img_width=None
        self.angular_height=None
        self.angular_width=None
        self.angular_format=None

        self.lfi_name=None
        self.methodology=None
        # use a exp name to identify the test.
        # 
        self.distortion_type=None
        self.distortion_level=None
        self.exp_name=None

        self.active_view_path=None
        self.active_refocusing_path=None
        
        self.passive_view_video_path=None
        self.passive_view_folder=None
        self.passive_refocusing_video_path=None
        self.passive_refocusing_folder=None

        self.min_height=None
        self.max_height=None
        self.min_width=None
        self.max_width=None

        self.depth_path=None
        self.img_post_fix=None
        self.video_post_fix=None
        self.cmp_index=None

        self.passive_view_thumbnail=None
        self.passive_refocusing_thumbnail=None

        self.show_path_manager=None

        self.view_dict={}
        self.all_depth_values=None
        self.all_depth_values=None

        # cache path, for project management display
        # cache path, for project management display
        # cache path, for project management display
        self.cache_path=None
        self.cache_thumbnail_file=None
        self.show_name=None
        self.show_name=None

        self.project_ref=None

    def SetProjectInfoRef(self,project_info):
        self.project_ref=weakref.ref(project_info)
    
    def GetProjectInfo(self):
        return self.project_ref()

    def InitFromLFIInfo(self,in_lfi_info:SingleLFIInfo,exp_setting:ExpSetting,exp_name:str,mode="training",cmp_index=0):
        self.img_height=in_lfi_info.img_height
        self.img_width=in_lfi_info.img_width
        self.angular_height=in_lfi_info.angular_height
        self.angular_width=in_lfi_info.angular_width # TODO Check the -1 carefully

        self.min_height=in_lfi_info.min_height
        self.max_height=in_lfi_info.max_height
        self.min_width=in_lfi_info.min_width
        self.max_width=in_lfi_info.max_width

        if LFIFeatures.Stereo_horizontal in exp_setting.lfi_features and exp_setting.comparison_type==ComparisonType.DoubleStimuli:
            self.angular_width-=1
            self.max_width-=1

        if type(in_lfi_info.angular_format) == str:
            if in_lfi_info.angular_format == "HW":
                in_lfi_info.angular_format=AngularFormat.HW
            else:
                in_lfi_info.angular_format=AngularFormat.XY

        self.angular_format=in_lfi_info.angular_format
        self.depth_path=in_lfi_info.depth_path

        if self.depth_path is not None:
            self.all_depth_values=self.GetAllPossibleDepthVal()  

        self.lfi_name=in_lfi_info.lfi_name
        in_path=in_lfi_info.view_path

        self.distortion_type=in_lfi_info.type_name
        self.distortion_level=in_lfi_info.dist_level

        use_pair_comparison=ComparisonType.PairComparison == exp_setting.comparison_type

        img_post_fix=exp_setting.ViewSaveTypeStr
        video_post_fix=exp_setting.VideoSaveTypeStr
        self.img_post_fix=img_post_fix
        self.video_post_fix=video_post_fix
        self.cmp_index=cmp_index

        self.show_path_manager=PathManager.ExpShowPathManager(in_path,mode,use_pair_comparison=use_pair_comparison,video_post_fix=video_post_fix,out_img_post_fix=img_post_fix,pair_comparison_index=cmp_index)

        self.active_view_path=self.show_path_manager.Get_show_view_path()
        self.active_refocusing_path=self.show_path_manager.Get_show_refocus_path()

        self.passive_view_video_path=self.show_path_manager.Get_passive_view_video_path()
        self.passive_refocusing_video_path=self.show_path_manager.Get_passive_refocus_video_path()

        if os.path.exists(self.passive_view_video_path):
            self.passive_view_folder=os.path.dirname(self.passive_view_video_path)
            self.passive_view_thumbnail=os.path.join(self.passive_view_folder,f"{PathManager.thumbnail_name}.{self.img_post_fix}")
            if not os.path.exists(self.passive_view_thumbnail):
                self.GetThumbnail(self.passive_view_video_path,self.passive_view_thumbnail)
        if os.path.exists(self.passive_refocusing_video_path):
            self.passive_refocusing_folder=os.path.dirname(self.passive_refocusing_video_path)
            self.passive_refocusing_thumbnail=os.path.join(self.passive_refocusing_folder,f"{PathManager.thumbnail_name}.{self.img_post_fix}")
            if not os.path.exists(self.passive_refocusing_thumbnail):
                self.GetThumbnail(self.passive_refocusing_video_path,self.passive_refocusing_thumbnail)

        all_views=os.listdir(self.active_view_path)
        view_num=0
        for file_name in all_views:
            if img_post_fix in file_name:
                view_num+=1
        if view_num>0:
            self.GetViewDict(all_views,img_post_fix) 

        self.methodology=exp_setting.comparison_type
        self.exp_name=exp_name

        if self.exp_name is not None:
            self.show_name = self.exp_name
        else:
            self.show_name=self.passive_view_video_path
    
    def DetectPostfix(self,in_folder):
        all_files=os.listdir(in_folder)
        all_post_fix={}
        for file in all_files:
            cur_post_fix=file.split('.')[-1]
            if cur_post_fix not in all_post_fix.keys():
                all_post_fix[cur_post_fix]=0
            all_post_fix[cur_post_fix]+=1

        all_post_fix_str=[]
        all_post_fix_num=[]
        for keys,values in all_post_fix.items():
            all_post_fix_str.append(keys)
            all_post_fix_num.append(values)
        
        largest_post_fix=all_post_fix_str[all_post_fix_num.index(max(all_post_fix_num))]
        return largest_post_fix
    
    def CheckAllInput(self):
        if self.CheckActiveRefocusing() or self.CheckPassiveRefocusing() or self.CheckActiveView() or self.CheckPassiveView():
            return True
        else:
            return False    
    
    def CheckPassiveRefocusing(self):
        if self.passive_refocusing_video_path is None:
            return False
        passive_video_name=self.passive_view_video_path.split('/')[-1]
        passive_video_post_fix=passive_video_name.split('.')[-1]

        if passive_video_post_fix in VideoSaveTypeDict.values():
            return True
        else:
            logger.error(f'Can not recogize the input video type {passive_video_post_fix}, or it is not supported.')
            return False 
    
    def CheckActiveRefocusing(self):
        if self.active_refocusing_path is not None:
            return True
    
    def CheckPassiveView(self):
        if self.passive_view_video_path is not None:
            return True

    def CheckActiveView(self):
        if self.active_view_path is None:
            return False
        
        if self.img_post_fix is None:
            self.img_post_fix=self.DetectPostfix(self.active_view_path)
        
        return self.ParseFolder(self.active_view_path)

    def GetThumbnail(self,in_video,out_img):
        ffmpeg_cmd=f"{PathManager.ffmpeg_path} -i {in_video} -ss 00:00:00 -frames:v 1 {out_img}"
        os.system(ffmpeg_cmd)

    def MakeThumbnail(self,out_img):
        if self.active_view_path is not None:
            show_view=self.GetActiveView(0,0)
            shutil.copy(show_view,out_img)
            return
        elif self.active_refocusing_path is not None:
            show_view=self.GetRefocusImg(self.all_depth_values[0])
            shutil.copy(show_view,out_img)
            return
        elif self.passive_view_video_path is not None:
            self.GetThumbnail(self.passive_view_video_path,out_img)
            return
        elif self.passive_refocusing_video_path is not None:
            self.GetThumbnail(self.passive_refocusing_video_path,out_img)
            return
    
    def GetViewDict(self,all_files,img_post_fix):
        for file_name in all_files:
            if img_post_fix in file_name and PathManager.thumbnail_name not in file_name:
                pure_file_name = file_name.split('.')[0]
                if self.angular_format ==  AngularFormat.HW:
                    row,col=pure_file_name.split('_')
                else:
                    col,row=pure_file_name.split('_')
                row=int(row)-self.min_height
                col=int(col)-self.min_width
                self.view_dict[(row,col)]=file_name
    
    def ParseFolder(self,folder_path):
        '''only active view changing is supported now'''
        if not os.path.exists(folder_path):
            self.is_valid=False
            return False
        all_files=os.listdir(folder_path)
        if len(all_files)==0:
            self.is_valid=False
            return False
        view_num=0
        for img_file in all_files:
            if self.img_post_fix in img_file and PathManager.thumbnail_name not in img_file:
                view_num+=1
        if view_num==0:
            return False
        max_height=0
        max_width=0
        min_height=10000
        min_width=10000

        path_dict={}
        for img_file in all_files:
            if "depth" in img_file:
                self.depth_path=os.path.join(folder_path,img_file)
                continue
            if os.path.isdir(os.path.join(folder_path,img_file)):
                continue
            test_img_name=img_file
            temp_list=img_file.split('.')[0].split('_')
            if self.angular_format == AngularFormat.XY:
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

        self.angular_height=max_height-min_height+1
        self.angular_width=max_width-min_width+1
        self.img_height=img_height
        self.img_width=img_width 

        self.GetViewDict(all_files,self.img_post_fix)
        return True

    def GetActiveView(self,v_row,v_col):
        #v_row+=self.min_height
        #v_col+=self.min_width
        return os.path.join(self.active_view_path,self.view_dict[(v_row,v_col)])
    
    def GetRefocusImg(self,depth_value):
        return os.path.join(self.active_refocusing_path,f"{depth_value}.{self.img_post_fix}")
    
    def GetShowViewsPath(self):
        return self.active_view_path
    
    def GetActiveViewPath(self):
        return self.active_view_path
    
    def GetShowRefocusingPath(self):
        return self.active_refocusing_path
    def GetActiveRefocusingPath(self):
        return self.active_refocusing_path
    
    def GetAllPossibleDepthVal(self):
        depth_map=cv2.imread(self.depth_path,cv2.IMREAD_GRAYSCALE)
        if depth_map.shape[0]!=self.img_height or depth_map.shape[1]!=self.img_width:
            depth_map=cv2.resize(depth_map,(self.img_width,self.img_height))

        all_depth_values=unique(depth_map)
        return all_depth_values

class AllScoringLFI:
    def __init__(self,in_mode):
        self.all_exp_lfi_info=[]
        self.exp_lfi_info_num=0
        self.mode=in_mode
    
    def GetLFINum(self)->int:
        return len(self.all_exp_lfi_info)

    def GetRandomShowOrder(self):
        if self.exp_lfi_info_num==0:
            return []
        show_order=list(range(self.exp_lfi_info_num))
        shuffle(show_order)
        return show_order
    
    def GetScoringExpLFIInfo(self,index:int) -> ScoringExpLFIInfo:
        return self.all_exp_lfi_info[index]
    
    def GetAllScoringLFI(self,exp_setting:ExpSetting,all_lfi_info:ExpLFIInfo):
        if exp_setting.comparison_type == ComparisonType.PairComparison:
            pair_wise_list=exp_setting.pair_wise_dict
            config_list=pair_wise_list[self.mode]
            for cmp_index,config in config_list.items():
                cur_lfi_name=config["lfi_name"]
                dist_type=config["left"]
                dist_level=config["left_level"]

                right_dist_type=config["right"]
                right_dist_level=config["right_level"]
                cur_lfi_info=all_lfi_info.GetLFIInfo(cur_lfi_name,dist_type,dist_level)
                exp_name=f"{cur_lfi_name}_{dist_type}_{dist_level}_VS_{right_dist_type}_{right_dist_level}"
                self.AddOne(exp_setting,cur_lfi_info,exp_name,cmp_index)
        else:
            all_lfi_names=all_lfi_info.GetAllLFNames()
            for lfi_name in all_lfi_names:
                all_dist_types=all_lfi_info.GetAllDistNames(lfi_name)
                for dist_type in all_dist_types:
                    all_dist_levels=all_lfi_info.GetAllDistLevels(lfi_name,dist_type)
                    for dist_level in all_dist_levels:
                        cur_lfi_info=all_lfi_info.GetLFIInfo(lfi_name,dist_type,dist_level)
                        exp_name=f"{lfi_name}_{dist_type}_{dist_level}"
                        self.AddOne(exp_setting,cur_lfi_info,exp_name)
    
    def DeleteScoringLFI(self,index:int):
        self.exp_lfi_info_num-=1
        self.all_exp_lfi_info.pop(index)
    
    def AddOne(self,exp_setting:ExpSetting,lfi_info:SingleLFIInfo,exp_name,cmp_index=0):
        self.exp_lfi_info_num+=1
        cur_scoring_lfi_info=ScoringExpLFIInfo()
        cur_scoring_lfi_info.InitFromLFIInfo(lfi_info,exp_setting,exp_name,self.mode,cmp_index)
        self.all_exp_lfi_info.append(cur_scoring_lfi_info)
    
    def AddScoringLFI(self,scoring_lfi_info:ScoringExpLFIInfo):
        self.exp_lfi_info_num+=1
        self.all_exp_lfi_info.append(scoring_lfi_info)

    
class TwoFolderLFIInfo(AllScoringLFI):
    def __init__(self, in_folder_path,video_postfix_str,in_mode="None"):
        super().__init__(in_mode)
        self.in_folder_path=in_folder_path
        self.video_post_fix=video_postfix_str
        self.all_videos=[]

        all_files=os.listdir(in_folder_path)
        for file_name in all_files:
            name_postfix=file_name.split('.')[-1]
            if name_postfix in video_postfix_str:
                self.all_videos.append(file_name)
                cur_single_scoring_lfi_info=ScoringExpLFIInfo()
                cur_single_scoring_lfi_info.passive_view_video_path=os.path.join(in_folder_path,file_name)
                cur_single_scoring_lfi_info.passive_refocusing_video_path=os.path.join(in_folder_path,file_name)
                self.all_exp_lfi_info.append(cur_single_scoring_lfi_info)
        self.exp_lfi_info_num=len(self.all_exp_lfi_info)
    
    def GetRandomShowOrder(self):
        logger.debug("Use the tow-folder mode random order generation now.")
        all_string_list=[]
        for i in range(self.exp_lfi_info_num):
            all_string_list.append(self.all_exp_lfi_info[i].passive_view_video_path)
        random_order=PlayList.MakeARandomScoringList(all_string_list)
        return random_order[0]

class ActiveTwoFolderLFIInfo(AllScoringLFI):
    def __init__(self, in_folder_path,in_mode="None"):
        super().__init__(in_mode)
        self.in_folder_path=in_folder_path

        all_folders=os.listdir(in_folder_path)
        for folder_name in all_folders:
            cur_single_scoring_lfi_info=ScoringExpLFIInfo()
            img_post_fix=cur_single_scoring_lfi_info.DetectPostfix(os.path.join(in_folder_path,folder_name))
            cur_single_scoring_lfi_info.img_post_fix=img_post_fix

            cur_single_scoring_lfi_info.active_view_path=os.path.join(in_folder_path,folder_name)
            cur_single_scoring_lfi_info.active_refocusing_path=None

            cur_single_scoring_lfi_info.ParseFolder(cur_single_scoring_lfi_info.active_view_path)

            self.all_exp_lfi_info.append(cur_single_scoring_lfi_info)
        self.exp_lfi_info_num=len(self.all_exp_lfi_info)

class PorjectPathManager():
    '''
        At first it is barely a handy class
        The project paths include: 
            - project root path
            - 
    '''
    def __init__(self,project_root,exp_setting:ExpSetting,in_json) -> None:
        # all features: passive,view_changing,refocusing
        # all features: active,view_changing,refocusing
        self.project_root=project_root
        self.intermediate_data_root=os.path.join(self.project_root,'IntermediateData')
        self.CheckInnerPath(self.intermediate_data_root)

        self.training_data_root=os.path.join(self.project_root,'TrainingData')
        self.CheckInnerPath(self.training_data_root)

        self.test_data_root=os.path.join(self.project_root,'TestData')
        self.CheckInnerPath(self.test_data_root)

        self.exp_setting=exp_setting

        self.all_lf_names=[]
        self.all_dist={}
        self.dist_levels={}
        self.all_paths=[]
        self.path_to_info={}

    def InitFromExpLFInfo(self,exp_lf_info:ExpLFIInfo,mode="training"):
        self.all_lf_names=[]
        self.all_dist={}
        self.dist_levels={}
        self.all_paths=[]
        self.path_to_info={}

        all_lfi_names=exp_lf_info.GetAllLFNames()
        self.all_lf_names=all_lfi_names

        if mode == "training":
            target_root=self.training_data_root
        else:
            target_root=self.test_data_root

        for lf_name in all_lfi_names:
            all_dist_types=exp_lf_info.GetAllDistNames(lf_name)
            self.all_dist[lf_name]=all_dist_types
            self.dist_levels[lf_name]={}

            target_lf_root=os.path.join(target_root,lf_name)
            self.CheckInnerPath(target_lf_root)

            for dist_type in all_dist_types:
                all_dist_levels=exp_lf_info.GetAllDistLevels(lf_name,dist_type)
                self.dist_levels[lf_name][dist_type]=all_dist_levels
                target_dist_root=os.path.join(target_lf_root,dist_type)
                self.CheckInnerPath(target_dist_root)

                for dist_level in all_dist_levels:
                    cur_single_lfi_info=exp_lf_info.GetLFIInfo(lf_name,dist_type,dist_level)

                    self.CopyFolderToFolder(cur_single_lfi_info.view_path,target_dist_root)

                    target_dist_level_path=os.path.join(target_dist_root,dist_level)
                    self.all_paths.append(target_dist_level_path)
                    self.path_to_info[target_dist_level_path]=(lf_name,dist_type,dist_level)

                    if cur_single_lfi_info.show_view_path is not None:
                        cur_single_lfi_info.show_view_path = os.path.join(target_dist_level_path,PathManager.inner_show_views_path)
                    if cur_single_lfi_info.show_refocusing_path is not None:
                        cur_single_lfi_info.show_refocusing_path = os.path.join(target_dist_level_path,PathManager.inner_show_refocusing_path)
                    if cur_single_lfi_info.passive_view_video is not None:
                        cur_single_lfi_info.passive_view_video = os.path.join(target_dist_level_path,PathManager.passive_view_video_name)
                    if cur_single_lfi_info.passive_refocusing_video is not None:
                        cur_single_lfi_info.passive_refocusing_video = os.path.join(target_dist_level_path,PathManager.passive_refocusing_video_name)
                    if cur_single_lfi_info.depth_path is not None:
                        cur_single_lfi_info.depth_path = os.path.join(target_dist_level_path,PathManager.inner_depth_map)

    def CopyFolderToFolder(self,from_folder,to_folder):
        if from_folder == to_folder:
            return
        if not os.path.exists(from_folder):
            return
        shutil.copytree(from_folder,to_folder,dirs_exist_ok=True) 
    
    def CopyFileToFolder(self,file_path,to_folder):
        file_base_path=os.path.dirname(file_path)
        if file_base_path == to_folder:
            return
        if not os.path.exists(file_path):
            return
        shutil.copy(file_path,to_folder)

    @staticmethod
    def ParseLFFolder(self,in_path):
        all_dist=os.listdir(in_path)
        all_dist_types=[]
        all_dist_levels={}
        for dist_name in all_dist:
            if not os.path.isdir(os.path.join(in_path,dist_name)):
                continue
            all_dist_types.append(dist_name)
            all_dist_levels[dist_name]=[]

            dist_path=os.path.join(in_path,dist_name)
            all_levels=os.listdir(dist_path)
            for level_name in all_levels:
                if not os.path.isdir(os.path.join(dist_path,level_name)):
                    continue
                all_dist_levels[dist_name].append(level_name)
        return all_dist_types,all_dist_levels

    def ParseFolder(self,in_path):
        all_folders=os.listdir(in_path)
        for folder_name in all_folders:
            if not os.path.isdir(os.path.join(in_path,folder_name)):
                continue
            self.all_lf_names.append(folder_name)
            self.all_dist[folder_name]=[]
            self.dist_levels[folder_name]={}

            lf_path=os.path.join(os.path.folder_name)
            all_dist=os.listdir(lf_path)
            for dist_name in all_dist:
                if not os.path.isdir(os.path.join(lf_path,dist_name)):
                    continue
                self.all_dist[folder_name].append(dist_name)
                self.dist_levels[folder_name][dist_name]=[]

                dist_path=os.path.join(lf_path,dist_name)
                all_levels=os.listdir(dist_path)
                for level_name in all_levels:
                    if not os.path.isdir(os.path.join(dist_path,level_name)):
                        continue
                    self.dist_levels[folder_name][dist_name].append(level_name)
                    self.all_paths.append(os.path.join(dist_path,level_name))
                    self.path_to_info[os.path.join(dist_path,level_name)]=(folder_name,dist_name,level_name)
    
    
    def CheckFiles(self):
        for cur_path in self.all_paths:
            lf_name, dist_name, dist_level =self.path_to_info[cur_path]
            view_path=os.path.join(cur_path,PathManager.inner_show_views_path)
            refocusing_path=os.path.join(cur_path,PathManager.inner_show_refocusing_path)
            if not os.path.exists(view_path):
                logger.error(f"Does not exist showing view folder for {cur_path}! Please check the data for the {lf_name}, distortion type {dist_name}, level {dist_level}")
            if not os.path.exists(refocusing_path):
                logger.error(f"Does not exist showing refocusing folder for {cur_path}! Please check the data for the {lf_name}, distortion type {dist_name}, level {dist_level}")
            
            if LFIFeatures.Passive_ViewChanging in self.exp_setting.lfi_features:
                video_save_type=self.exp_setting.VideoSaveTypeStr
                output_video=os.path.join(view_path,f"view.{video_save_type}")
                if not os.path.exists(output_video):
                    logger.error(f"Does not exist the passive views video for {cur_path}! Please check the data for the {lf_name}, distortion type {dist_name}, level {dist_level}")

            if LFIFeatures.Passive_Refocusing in self.exp_setting.lfi_features:
                video_save_type=self.exp_setting.VideoSaveTypeStr
                output_video=os.path.join(refocusing_path,f"refocus.{video_save_type}")
                if not os.path.exists(output_video):
                    logger.error(f"Does not exist the passive refocusing video for {cur_path}! Please check the data for the {lf_name}, distortion type {dist_name}, level {dist_level}")
    
    def CheckInnerPath(self,path):
        if not os.path.exists(path):
            os.makedirs(path)