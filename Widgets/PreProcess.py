import os
import numpy as np
import cv2
from ExpInfo import *
from DenseRefocusFunction import *
import shutil
from time import sleep
from PySide6.QtCore import QObject,QThread,Signal
import logging
logger=logging.getLogger("LogWindow")

gray_color=(128,128,128)
ffmpeg_path='.\\ffmpeg.exe'

class PreProcessThread(QObject):
    sub_task_finished=Signal(int,str)
    total_finished=Signal()

    def __init__(self,training_LFI_info:ExpLFIInfo,test_LFI_info:ExpLFIInfo,exp_setting:ExpSetting):
        super().__init__()
        self.training_LFI_info=training_LFI_info
        self.test_LFI_info=test_LFI_info
        self.exp_setting=exp_setting

    def run(self):
        self.sub_task_finished.emit(0,"Now start training data preprocessing")
        logger.info("Now start training data preprocessing")
        if self.training_LFI_info is not None:
            training_preprocess=ExpPreprocessing(self.training_LFI_info,self.exp_setting)
            training_preprocess.mode="training"
            training_show_list=GetShowList(self.training_LFI_info,self.exp_setting,mode="training")
            training_preprocess.show_list=training_show_list
            training_preprocess.Run()
        else:
            self.sub_task_finished.emit(50,"The training data is None, skip the stage...")
            sleep(2)

        self.sub_task_finished.emit(50,"Now start test data preprocessing")
        if self.test_LFI_info is not None:
            test_preprocess=ExpPreprocessing(self.test_LFI_info,self.exp_setting)
            test_preprocess.mode="test"
            test_show_list=GetShowList(self.test_LFI_info,self.exp_setting,mode="test")
            test_preprocess.show_list=test_show_list
            test_preprocess.Run()
        else:
            self.sub_task_finished.emit(100,"The test data is None, skip the stage...")
            sleep(2)

        self.sub_task_finished.emit(100,"All has been done!")
        sleep(2)

        self.total_finished.emit()

class PictureMask:
    def __init__(self,img_height=0,img_width=0,lfi_features=None,comparison_type=None) -> None:
        screen = QApplication.primaryScreen().geometry()
        self.screen_width=screen.width()
        self.screen_height=screen.height()
        self.img_num=0
        self.img_rect=[]
        self.img_height=int(img_height)
        self.img_width=int(img_width)
        self.widget_height=0
        self.widget_width=0
        self.SetLFIFeatures(lfi_features,comparison_type)
        
    def StichingPictures(self,images):
        ret_img=np.zeros((self.widget_height,self.widget_width,3),dtype=np.uint8)+128
        for i in range(self.img_num):
            cur_img=images[i]
            if cur_img.shape[0]!=self.img_height or cur_img.shape[1]!=self.img_width:
                cur_img=cv2.resize(cur_img,(self.img_width,self.img_height))
            # 10 bit images
            if cur_img.max()>255:
                cur_img=cur_img//4
            ret_img[self.img_rect[i][1]:self.img_rect[i][1]+self.img_height,self.img_rect[i][0]:self.img_rect[i][0]+self.img_width,:]=cur_img
        return ret_img
        
    def SetLFIFeatures(self, lfi_features, comparison_type):
        if lfi_features is None or comparison_type is None:
            return
        self.img_num=1
        self.lfi_features=lfi_features
        self.comparison_type=comparison_type
        img_num_scale=1
        if self.comparison_type == ComparisonType.SingleStimuli:
            img_num_scale*=1
        else:
            img_num_scale*=2
        if LFIFeatures.Stereo_horizontal in self.lfi_features or LFIFeatures.Stereo_vertical in self.lfi_features:
            img_num_scale*=2
        if LFIFeatures.Stereo_horizontal in self.lfi_features:
            self.img_width=self.img_width//2
            
        self.img_num*=img_num_scale
        
        self.widget_height=self.img_height

        self.img_gap=int(self.screen_width//self.img_num-self.img_width)
        self.widget_width=int(self.img_width*self.img_num+(self.img_num-1)*self.img_gap)

        '''
        need to further developped for 3D vertical display type
        '''
        for i in range(self.img_num):
            self.img_rect.append([i*(self.img_width+self.img_gap),0,self.img_width,self.img_height])
        self.screen_widget_x=self.screen_width//2-self.widget_width//2
        self.screen_widget_y=self.screen_height//2-self.widget_height//2

    def IsInRect(self,x,y):
        # not a good solution 
        # TODO: think about it. Maybe a class to descrie the coordinate layer is better.
        x=x-self.screen_widget_x
        y=y-self.screen_widget_y
        for i in range(self.img_num):
            cur_rect_x0=self.img_rect[i][0]
            cur_rect_x1=self.img_rect[i][0]+self.img_rect[i][2]
            cur_rect_y0=self.img_rect[i][1]
            cur_rect_y1=self.img_rect[i][1]+self.img_rect[i][3]
            if x>=cur_rect_x0 and x<=cur_rect_x1 and y>=cur_rect_y0 and y<=cur_rect_y1:
                return True, (x-cur_rect_x0, y-cur_rect_y0), i
        return False, None, None
    
    def IsInHoverRect(self,x,y):
        x-=self.screen_widget_x
        y-=self.screen_widget_y
        for i in range(self.img_num):
            cur_rect_x0=self.screen_widget_x+self.img_rect[i][0]
            cur_rect_x1=self.screen_widget_y+self.img_rect[i][0]+self.img_rect[i][2]
            cur_rect_y0=self.screen_widget_y+self.img_rect[i][1]
            cur_rect_y1=self.screen_widget_y+self.img_rect[i][1]+self.img_rect[i][3]
            start_x=(cur_rect_x0+cur_rect_x1)*2//5
            end_x=(cur_rect_x0+cur_rect_x1)*3//5
            start_y=(cur_rect_y0+cur_rect_y1)*2//5
            end_y=(cur_rect_y0+cur_rect_y1)*3//5
            if x>=start_x and x<=end_x and y>=start_y and y<=end_y:
                return True
        return False
    
    def GetRectCenter(self,i):
        cur_rect_x0=self.screen_widget_x+self.img_rect[i][0]
        cur_rect_x1=self.screen_widget_y+self.img_rect[i][0]+self.img_rect[i][2]
        cur_rect_y0=self.screen_widget_y+self.img_rect[i][1]
        cur_rect_y1=self.screen_widget_y+self.img_rect[i][1]+self.img_rect[i][3]
        return (cur_rect_x0+cur_rect_x1)//2,(cur_rect_y0+cur_rect_y1)//2
    
    def GetRectCenterInScreen(self,i):
        x,y=self.GetRectCenter(i)
        return x+self.screen_widget_x,y+self.screen_widget_y


def GenerateRefocusedImg(lfi_info:SingleLFIInfo,post_fix='png'):
    CheckPath(lfi_info.refocusing_views_path)    
    if lfi_info.lfi_type == LFITypes.Sparse:
        CalSparseRefocusing(lfi_info,post_fix)
    else: 
        CalDenseRefocusing(lfi_info,post_fix)
        return True

def CalDenseRefocusing(lfi_info:SingleLFIInfo,post_fix):
    lambda_file=lfi_info.lambda_path
    meta_data=None
    refocusing_folder=lfi_info.refocusing_views_path

    angular_height=lfi_info.angular_height
    angular_width=lfi_info.angular_width

    lf_image=np.zeros((angular_height,angular_width,lfi_info.img_height,lfi_info.img_width,3),dtype=np.uint8)

    for row in range(lfi_info.angular_height):
        for col in range(lfi_info.angular_width):
            cur_view_path=lfi_info.GetViewPath(col,row) 
            temp=cv2.imread(cur_view_path,-1)
            if temp.max()>255:
                temp=temp//4#temp.max()*255
            lf_image[row,col]=temp.astype(np.uint8)
    
    with open(lambda_file,'r') as fid:
        meta_data=json.load(fid)
    min_lambda=meta_data['LambdaMin']
    max_lambda=meta_data['LambdaMax']

    device_meta=meta_data

    depth_map=cv2.imread(lfi_info.depth_path,cv2.IMREAD_GRAYSCALE)
    if depth_map.shape[0]!=lfi_info.img_height or depth_map.shape[1]!=lfi_info.img_width:
        depth_map=cv2.resize(depth_map,(lfi_info.img_width,lfi_info.img_height))

    all_depth_values=np.unique(depth_map)
    for depth_val in all_depth_values:
        output_name=os.path.join(refocusing_folder,f'{depth_val}.{post_fix}')
        if os.path.exists(output_name):
            continue
        refocus_img=run_refocus(lf_image,device_meta,meta_data,depth_val,{'InterpMethod':'cubic'})
        output_img=refocus_img[:,:,:3]
        cv2.imwrite(output_name,output_img)
        
def CalSparseRefocusing(lfi_info,post_fix):
    pass


def OrderGenerator(angular_height,angular_width):
    '''
    Replace this function with your own order generator! 
    It will be called automatically by GetPassiveVideo
    '''
    all_orders=[]
    for row in range(angular_height):
        for col in range(angular_width):
            all_orders.append((row,col))
    return all_orders

def CheckPath(path):
    if not os.path.exists(path):
        os.makedirs(path)

class ExpPreprocessing(QObject):
    process_percent_changed=Signal(int)

    def __init__(self,all_lfi_info:ExpLFIInfo,exp_setting:ExpSetting) -> None:
        self.exp_setting=exp_setting
        self.all_lfi_info=all_lfi_info
        
        self.all_lfi_name=self.all_lfi_info.GetAllLFNames()
        self.all_distortion_type=self.all_lfi_info.GetAllDistNames(self.all_lfi_name[0])

        self.show_list=None
        self.mode="training"

    def Run(self):
        if self.exp_setting.comparison_type == ComparisonType.PairComparison:
            self.RunPairWise()
        else:
            self.RunDoubleOrSingle()

    def RunDoubleOrSingle(self):
        all_lfi_num=len(self.all_lfi_name)
        for idx,lf_name in enumerate(self.all_lfi_name):
            cur_ori_lfi_info=self.all_lfi_info.GetOriginLFIInfo(lf_name)
            if LFIFeatures.None_Refocusing not in self.exp_setting.lfi_features:
                GenerateRefocusedImg(cur_ori_lfi_info)
                logger.info("Generate refocused images for %s" % lf_name)
            self.process_percent_changed.emit(int((idx+1)/all_lfi_num*50/6*1))
            for dist_type in self.all_distortion_type:
                for i in range(1,6):
                    single_lfi_info=self.all_lfi_info.GetLFIInfo(lf_name,dist_type,i)
                    cur_processor=SinglePreProcessing(single_lfi_info,self.exp_setting)
                    logger.info("Generate refocused images for %s, dist type %s, level %d" %(lf_name,dist_type,i))
                    cur_processor.SetOriginLFIInfo(cur_ori_lfi_info)
                    cur_processor.Run()
                    self.process_percent_changed.emit(int((idx+1)/all_lfi_num*50/6*(i+1)))
            
    def RunPairWise(self):
        show_list=self.show_list
        for info_index,show_info in enumerate(show_list):
            left_lfi_info=self.all_lfi_info.GetLFIInfo(show_info[0],show_info[1],show_info[2])
            right_lfi_info=self.all_lfi_info.GetLFIInfo(show_info[0],show_info[3],show_info[4])

            cur_preprocessor=SinglePreProcessing(left_lfi_info,self.exp_setting)
            cur_preprocessor.SetOriginLFIInfo(right_lfi_info)
            cur_preprocessor.cmp_root=os.path.join(left_lfi_info.view_path,'%s/cmp_%d' % (self.mode,info_index))
            cur_preprocessor.Run()

class SinglePreProcessing:
    def __init__(self,lfi_info:SingleLFIInfo,exp_setting:ExpSetting):
        self.lfi_info=lfi_info
        self.exp_setting=exp_setting
        self.image_height=lfi_info.img_height
        self.image_width=lfi_info.img_width
        
        self.picture_mask=PictureMask(self.image_height,self.image_width,exp_setting.lfi_features,exp_setting.comparison_type)

        self.origin_lfi_info=None
        self.cmp_root=None
    
    def SetOriginLFIInfo(self,origin_lfi:SingleLFIInfo):
        self.origin_lfi_info=origin_lfi
        
    def Run(self):
        # handle the right one when using the pair-wise comparison
        if self.exp_setting.comparison_type == ComparisonType.PairComparison:
            self.Generate_origin_refucusing()
        if self.exp_setting.has_preprocess:
            return
        if self.lfi_info.type == CompTypes.Origin:
            #self.Generate_refocusing()
            return
        else:
            if LFIFeatures.Refocusing in self.exp_setting.lfi_features:
                self.Generate_refocusing()
            if LFIFeatures.Active_Refocusing in self.exp_setting.lfi_features:
                self.Generate_show_refocus(self.cmp_root)
            if LFIFeatures.Passive_Refocusing in self.exp_setting.lfi_features:
                self.Generate_passive_refocus_video()
            
            if LFIFeatures.Active_ViewChanging in self.exp_setting.lfi_features:
                self.Generate_show_views(self.cmp_root)
            if LFIFeatures.Passive_ViewChanging in self.exp_setting.lfi_features:
                self.Generaet_passive_view_video()

    def Generate_refocusing(self):
        GenerateRefocusedImg(self.lfi_info,self.exp_setting.ViewSaveTypeStr)
    
    def Generate_origin_refucusing(self):
        GenerateRefocusedImg(self.origin_lfi_info,self.exp_setting.ViewSaveTypeStr)
    
    def Generate_show_refocus(self,target_path=None):
        # Note that entering this function means we need an active refocusing
        # 1 view
        if LFIFeatures.TwoD in self.exp_setting.lfi_features and self.exp_setting.comparison_type == ComparisonType.SingleStimuli:
            self.lfi_info.show_refocusing_views_path=self.lfi_info.refocusing_views_path
            return

        # 2 view, but single stimuli and 3D display
        if target_path is None:
            target_path=self.lfi_info.refocusing_views_path
        self.lfi_info.show_refocusing_views_path=os.path.join(target_path,'show_refocusing')
        CheckPath(self.lfi_info.show_refocusing_views_path)
        all_refocus_views=os.listdir(self.lfi_info.refocusing_views_path)
        rem_names=[]
        for refocus_img in all_refocus_views:
            if not refocus_img.endswith(self.exp_setting.ViewSaveTypeStr):
                rem_names.append(refocus_img)
        for rem_name in rem_names:
            all_refocus_views.remove(rem_name)
        
        if LFIFeatures.Stereo_horizontal in self.exp_setting.lfi_features and self.exp_setting.comparison_type == ComparisonType.SingleStimuli:
            for dist_refocus_img in all_refocus_views:
                dist_refocus_img_path=os.path.join(self.lfi_info.refocusing_views_path,dist_refocus_img)
                output_path=os.path.join(self.lfi_info.show_refocusing_views_path,dist_refocus_img)
                self.StichingPictures([dist_refocus_img_path,dist_refocus_img_path],output_path,self.picture_mask)
        
        # 2 views, but double stimuli (or pair wise) and 2D display
        # here the origin_lfi may not be the true 'Origin', but maybe the distorted one to be compared with (i.e. in the case of pair wise comparison)
        if LFIFeatures.TwoD in self.exp_setting.lfi_features and self.exp_setting.comparison_type != ComparisonType.SingleStimuli:
            for dist_refocus_img in all_refocus_views:
                dist_refocus_img_path=os.path.join(self.lfi_info.refocusing_views_path,dist_refocus_img)
                origin_refocus_img_path=os.path.join(self.origin_lfi_info.refocusing_views_path,dist_refocus_img)
                output_path=os.path.join(self.lfi_info.show_refocusing_views_path,dist_refocus_img)
                self.StichingPictures([dist_refocus_img_path,origin_refocus_img_path],output_path,self.picture_mask)
        
        # 4 views, 3D + not single stimuli
        if LFIFeatures.Stereo_horizontal in self.exp_setting.lfi_features and self.exp_setting.comparison_type != ComparisonType.SingleStimuli:
            for dist_refocus_img in all_refocus_views:
                dist_refocus_img_path=os.path.join(self.lfi_info.refocusing_views_path,dist_refocus_img)
                origin_refocus_img_path=os.path.join(self.origin_lfi_info.refocusing_views_path,dist_refocus_img)
                output_path=os.path.join(self.lfi_info.show_refocusing_views_path,dist_refocus_img)
                self.StichingPictures([dist_refocus_img_path,dist_refocus_img_path,origin_refocus_img_path,origin_refocus_img_path],output_path,self.picture_mask)        

    def StichingPictures(self,views_paths,output_img,picture_mask):
        all_images=[]
        for image_path in views_paths:
            tmp=cv2.imread(image_path,-1)
            all_images.append(tmp)
        
        new_img=picture_mask.StichingPictures(all_images)
        cv2.imwrite(output_img,new_img)
    
    def Generate_passive_refocus_video(self):
        # currently only from nearest to farthest
        # but we still nee the show refocusing images first!
        self.Generate_show_refocus(self.cmp_root)
        show_path=self.lfi_info.show_refocusing_views_path
        all_show_views=os.listdir(show_path)
        # check the height and width
        for view in all_show_views:
            if view.endswith(self.exp_setting.ViewSaveTypeStr):
                cur_view=cv2.imread(os.path.join(show_path,view),-1)
                target_height,target_width=cur_view.shape[:2]
                if cur_view.shape[0]%2==1:
                    target_height+=1
                if cur_view.shape[1]%2==1:
                    target_width+=1 
                if target_height!=cur_view.shape[0] or target_width!=cur_view.shape[1]:
                    new_view=np.zeros((target_height,target_width,3),dtype=np.uint8)+128
                    new_view[:cur_view.shape[0],:cur_view.shape[1],:]=cur_view
                    cv2.imwrite(os.path.join(show_path,view),new_view)
            
        all_show_index=[]
        for view_name in all_show_views:
            if not view_name.endswith(self.exp_setting.ViewSaveTypeStr):
                continue
            if 'thumbnail' in view_name:
                continue
            show_index=int(view_name.split('.')[0])
            all_show_index.append(show_index)
        all_show_index.sort()
        shutil.copyfile(os.path.join(show_path,'%d.%s' % (all_show_index[0],self.exp_setting.ViewSaveTypeStr)),os.path.join(show_path,'thumbnail.%s' % self.exp_setting.ViewSaveTypeStr))
        view_post_fix=self.exp_setting.ViewSaveTypeStr
        video_post_fix=self.exp_setting.VideoSaveTypeStr

        output_txt=os.path.join('refocus.txt')
        with open(output_txt,'w') as fid:
            for index in all_show_index:
                file_name=os.path.join(show_path,'%d.%s' % (index,view_post_fix))
                file_name=file_name.replace('\\','/')
                fid.write('file %s\n' % file_name)

        output_video=os.path.join(self.lfi_info.show_refocusing_views_path,f"refocus.{video_post_fix}")
        self.lfi_info.passive_refocusing_video=output_video
        if os.path.exists(output_video):
            os.remove(output_video)

        #cmd=f'{ffmpeg_path} -f concat -safe 0 -r 30 -i {output_txt} -c:v libx26 -x265-params "lossless=1:qp=0" -r 30 -pix_fmt yuv420p {output_video}'
        cmd=f'ffmpeg -f concat -safe 0 -r 30 -i {output_txt} -c:v libx264 -qp 0 -r 30 -pix_fmt yuv420p {output_video}'
        os.system(cmd)
    
    def Generate_show_views(self,target_path=None):
        if LFIFeatures.TwoD in self.exp_setting.lfi_features and self.exp_setting.comparison_type == ComparisonType.SingleStimuli:
            self.lfi_info.show_views_path=self.lfi_info.view_path
            return

        # 2 view, but single stimuli and 3D display
        if target_path is None:
            target_path=self.lfi_info.view_path
        self.lfi_info.show_views_path=os.path.join(target_path,'show_views')
        CheckPath(self.lfi_info.show_views_path)
        
        if LFIFeatures.Stereo_horizontal in self.exp_setting.lfi_features and self.exp_setting.comparison_type == ComparisonType.SingleStimuli:
            for row in range(self.lfi_info.angular_height):
                for col in range(self.lfi_info.angular_width-1):
                    dist_view_path_left=self.lfi_info.GetViewPath(col,row)
                    dist_view_path_right=self.lfi_info.GetViewPath(col+1,row)
                    output_path=os.path.join(self.lfi_info.show_views_path,self.lfi_info.GetViewName(col,row))
                    if not output_path.endswith(self.exp_setting.ViewSaveTypeStr):
                        output_path=output_path.split('.')[0]+'.'+self.exp_setting.ViewSaveTypeStr
                        
                    self.StichingPictures([dist_view_path_left,dist_view_path_right],output_path,self.picture_mask)
        
        # 2 views, but double stimuli (or pair wise) and 2D display
        # here the origin_lfi may not be the true 'Origin', but maybe the distorted one to be compared with (i.e. in the case of pair wise comparison)
        if LFIFeatures.TwoD in self.exp_setting.lfi_features and self.exp_setting.comparison_type != ComparisonType.SingleStimuli:
            for row in range(self.lfi_info.angular_height):
                for col in range(self.lfi_info.angular_width):
                    dist_view_path=self.lfi_info.GetViewPath(col,row)
                    origin_view_path=self.origin_lfi_info.GetViewPath(col,row)
                    output_path=os.path.join(self.lfi_info.show_views_path,self.lfi_info.GetViewName(col,row))
                    if not output_path.endswith(self.exp_setting.ViewSaveTypeStr):
                        output_path=output_path.split('.')[0]+'.'+self.exp_setting.ViewSaveTypeStr
                    self.StichingPictures([dist_view_path,origin_view_path],output_path,self.picture_mask)
        
        # 4 views, 3D + not single stimuli
        if LFIFeatures.Stereo_horizontal in self.exp_setting.lfi_features and self.exp_setting.comparison_type != ComparisonType.SingleStimuli:
            for row in range(self.lfi_info.angular_height):
                for col in range(self.lfi_info.angular_width-1):
                    dist_view_path_left=self.lfi_info.GetViewPath(col,row)
                    dist_view_path_right=self.lfi_info.GetViewPath(col+1,row)
                    origin_view_path_left=self.origin_lfi_info.GetViewPath(col,row)
                    origin_view_path_right=self.origin_lfi_info.GetViewPath(col+1,row)
                    output_path=os.path.join(self.lfi_info.show_views_path,self.lfi_info.GetViewName(col,row))
                    if not output_path.endswith(self.exp_setting.ViewSaveTypeStr):
                        output_path=output_path.split('.')[0]+'.'+self.exp_setting.ViewSaveTypeStr
                    self.StichingPictures([dist_view_path_left,dist_view_path_right,origin_view_path_left,origin_view_path_right],output_path,self.picture_mask)

    def Generaet_passive_view_video(self):
        # currently only from nearest to farthest
        # but we still nee the show refocusing images first!
        self.Generate_show_views(self.cmp_root)
        show_path=self.lfi_info.show_views_path

        all_views=os.listdir(show_path)
        for view in all_views:
            if not view.endswith(self.exp_setting.ViewSaveTypeStr):
                continue
            cur_view=cv2.imread(os.path.join(show_path,view),-1)
            target_height,target_width=cur_view.shape[:2]
            if cur_view.shape[0]%2==1:
                target_height+=1
            if cur_view.shape[1]%2==1:
                target_width+=1
            if target_height!=cur_view.shape[0] or target_width!=cur_view.shape[1]:
                new_view=np.zeros((target_height,target_width,3),dtype=np.uint8)+128
                new_view[:cur_view.shape[0],:cur_view.shape[1],:]=cur_view
                cv2.imwrite(os.path.join(show_path,view),new_view)

        max_row=self.lfi_info.angular_height
        if LFIFeatures.Stereo_horizontal in self.exp_setting.lfi_features:
            max_width=self.lfi_info.angular_width-1
        else:
            max_width=self.lfi_info.angular_width
        
        order=OrderGenerator(max_row,max_width)    
        first_view_name=self.lfi_info.GetPureViewName(0,0)+'.'+self.exp_setting.ViewSaveTypeStr
        first_view_name=os.path.join(show_path,first_view_name)
        shutil.copyfile(first_view_name,os.path.join(show_path,'thumbnail.%s' % self.exp_setting.ViewSaveTypeStr))
        video_post_fix=self.exp_setting.VideoSaveTypeStr
        output_txt=os.path.join('views.txt')
        with open(output_txt,'w') as fid:
            for row,col in order:
                view_name=self.lfi_info.GetViewName(col,row)
                if not view_name.endswith(self.exp_setting.ViewSaveTypeStr):
                    view_name=view_name.split('.')[0]+'.'+self.exp_setting.ViewSaveTypeStr
                file_name=os.path.join(show_path,view_name)
                file_name=file_name.replace('\\','/')
                fid.write('file %s\n' % file_name)

        output_video=os.path.join(show_path,f"views.{video_post_fix}")
        self.lfi_info.passive_video=output_video

        if os.path.exists(output_video):
            os.remove(output_video)

        #cmd=f'{ffmpeg_path} -f concat -safe 0 -i {output_txt} -c:v libx265 -x265-params "lossless=1:qp=0" -r 30 -pix_fmt yuv420p {output_video}'
        cmd=f'ffmpeg -f concat -safe 0 -r 30 -i {output_txt} -c:v libx264 -qp 0 -r 30 -pix_fmt yuv420p {output_video}'
        os.system(cmd)


if __name__ == "__main__":
    test_file_path='../debug.lfqoe'
    training_LFI_info, test_LFI_info, exp_setting=ReadExpConfig(test_file_path)

    GenerateRefocusedImg(training_LFI_info.all_LFI_info["Bikes"]["Origin"])

    
    