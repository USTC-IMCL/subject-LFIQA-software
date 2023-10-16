import sys
import os
from typing import Optional
from PySide6 import QtCore, QtGui, QtWidgets
import PySide6.QtGui
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QUrl
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from ExpInfo import *
sys.path.append('../UI')
sys.path.append('../Widgets/')
from ScoreTable_ui import Ui_ScoreTable as ScoreTable
import cv2

class EventMask:
    def __init__(self,img_height=0,img_width=0,lfi_features=None,comparison_type=None) -> None:
        screen = QApplication.primaryScreen().geometry()
        self.screen_width=screen.width()
        self.screen_height=screen.height()
        self.img_num=0
        self.img_rect=[]
        self.img_height=img_height
        self.img_width=img_width
        self.widget_height=0
        self.widget_width=0
        self.SetLFIFeatures(lfi_features,comparison_type)
        
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

        self.img_gap=self.screen_width//self.img_num-self.img_width
        self.widget_width=self.img_width*self.img_num+(self.img_num-1)*self.img_gap

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

class PairWiseScoringWidget(QtWidgets.QStackedWidget):
    scoring_finished=QtCore.Signal(list)
    
    def __init__(self, all_lfi_info:ExpLFIInfo, exp_setting:ExpSetting, show_list):
        super().__init__()

        self.setStyleSheet('background-color:gray;')

        self.all_lfi_info=all_lfi_info
        self.exp_setting=exp_setting
        self.show_list=show_list
        self.current_lfi_show_index=0
        self.all_lfi_names=all_lfi_info.GetAllLFNames()
        self.all_dist_types=all_lfi_info.GetAllDistNames(self.all_lfi_names[0])
        self.all_view_scores=[]
        self.all_refocusing_scores=[]
        self.show_page_list=[] # view changing, refocusing

        self.current_page_index=0
        self.max_page_num=0

        screen = QApplication.primaryScreen().geometry()
        self.resize(screen.width(), screen.height())

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        #self.setAttribute(Qt.WA_TranslucentBackground)
        
        cur_lf_info=self.GetSingleLFIInfo(self.current_lfi_show_index)

        self.SetPageShowing(cur_lf_info,init_flag=True)
        self.SetPageShowing(cur_lf_info)
        for page in self.show_page_list:
            if page is not None:
                page.setParent(self)

        ############ 
        self.finish_page=FinishPage(screen.width(),screen.height())
        self.finish_page.key_pressed.connect(lambda: self.FinishAll())
        self.finish_page.setParent(self)
        self.addWidget(self.finish_page)

        self.all_page_num=self.max_page_num+1

    def GetSingleLFIInfo(self,show_index)->SingleLFIInfo:
        cur_lfi_name=self.show_list[show_index][0]
        cur_left_dist=self.show_list[show_index][1]
        cur_left_dist_level=self.show_list[show_index][2]
        return self.all_lfi_info.GetLFIInfo(cur_lfi_name,cur_left_dist,cur_left_dist_level)
    
    def ShowingNext(self,ret_score,score_list,i=0):
        if i+1>=self.max_page_num:
            self.RecordScore(ret_score,score_list)
        else:
            score_list.append(ret_score)
            self.NextPage()

    def RecordScore(self,ret_score,score_list):
        # get score, then set new lfi image
        score_list.append(ret_score)
        self.current_lfi_show_index+=1
        if self.current_lfi_show_index >= len(self.show_list):
            self.current_page_index+=1
            self.setCurrentIndex(self.current_page_index)
            return
        cur_lfi_info=self.GetSingleLFIInfo(self.current_lfi_show_index)
        self.SetPageShowing(cur_lfi_info)

        self.current_page_index=0
        self.setCurrentIndex(self.current_page_index)
    
    def SetPageShowing(self,cur_lf_info:SingleLFIInfo,init_flag=False):
        exp_setting=self.exp_setting
        if LFIFeatures.Active_Refocusing in exp_setting.lfi_features and LFIFeatures.Active_ViewChanging in exp_setting.lfi_features:
            if init_flag:
                page_showing=ImagePage(exp_setting,cur_lf_info,cur_lf_info.show_views_path,cur_lf_info.show_refocusing_views_path)
                self.addWidget(page_showing)
                page_showing.pair_finished.connect(lambda x: self.ShowingNext(x,self.all_view_scores,0))
                self.max_page_num+=1
                self.show_page_list.append(page_showing)
                self.show_page_list.append(None)
            else:
                self.show_page_list[0].SetNewLFI(exp_setting,cur_lf_info,cur_lf_info.show_views_path,cur_lf_info.show_refocusing_views_path)
            return 

        if LFIFeatures.Active_ViewChanging in exp_setting.lfi_features and LFIFeatures.Active_Refocusing not in exp_setting.lfi_features:
            if init_flag:
                page_showing=ImagePage(exp_setting,cur_lf_info,cur_lf_info.show_views_path,None)
                self.addWidget(page_showing)
                page_showing.pair_finished.connect(lambda x: self.ShowingNext(x,self.all_view_scores,0))
                self.max_page_num+=1
                self.show_page_list.append(page_showing)
            else:
                self.show_page_list[0].SetNewLFI(exp_setting,cur_lf_info,cur_lf_info.show_views_path,None)
        
        if LFIFeatures.Passive_ViewChanging in exp_setting.lfi_features:
            if init_flag:
                page_showing=VideoPage(exp_setting,cur_lf_info,cur_lf_info.passive_video)
                self.addWidget(page_showing)
                page_showing.pair_finished.connect(lambda x: self.ShowingNext(x,self.all_view_scores,0))
                self.max_page_num+=1
                self.show_page_list.append(page_showing)
            else:
                self.show_page_list[0].SetNewLFI(exp_setting,cur_lf_info,cur_lf_info.passive_video)
        
        if LFIFeatures.None_ViewChanging in exp_setting.lfi_features:
            if init_flag:
                self.show_page_list.append(None)
        
        if LFIFeatures.Active_Refocusing in exp_setting.lfi_features:
            if init_flag:
                page_showing=ImagePage(exp_setting,cur_lf_info,None,cur_lf_info.show_refocusing_views_path)
                self.addWidget(page_showing)
                page_showing.pair_finished.connect(lambda x: self.ShowingNext(x,self.all_refocusing_scores,1))
                self.max_page_num+=1
                self.show_page_list.append(page_showing)
            else:
                self.show_page_list[1].SetNewLFI(exp_setting,cur_lf_info,None,cur_lf_info.show_refocusing_views_path)
        
        if LFIFeatures.Passive_Refocusing in exp_setting.lfi_features:
            if init_flag:
                page_showing=VideoPage(exp_setting,cur_lf_info,cur_lf_info.passive_refocusing_video)
                self.addWidget(page_showing)
                page_showing.pair_finished.connect(lambda x: self.ShowingNext(x,self.all_refocusing_scores,1))
                self.max_page_num+=1
                self.show_page_list.append(page_showing)
            else:
                self.show_page_list[1].SetNewLFI(exp_setting,cur_lf_info,cur_lf_info.passive_refocusing_video)
        
        if LFIFeatures.None_Refocusing in exp_setting.lfi_features:
            if init_flag:
                self.show_page_list.append(None)
    
    def NextPage(self):
        self.current_page_index+=1
        if self.current_page_index >= self.all_page_num:
            self.current_page_index=0
        self.setCurrentIndex(self.current_page_index)
    
    def PrePage(self):
        self.current_page_index-=1
        if self.current_page_index < 0:
            self.current_page_index=self.max_page_num-1
        self.setCurrentIndex(self.current_page_index)

    def FinishAll(self):
        if len(self.all_view_scores)==0:
            self.all_view_scores=None
        if len(self.all_refocusing_scores)==0:
            self.all_refocusing_scores=None
        self.scoring_finished.emit([self.all_view_scores,self.all_refocusing_scores])
        self.deleteLater()
        
    def keyPressEvent(self, event) -> None:
        cur_page=self.currentWidget()
        cur_page.handle_key_press(event)
        return super().keyPressEvent(event)

class ScoringWidget(QtWidgets.QStackedWidget):
    scoring_finished=QtCore.Signal(list)
    
    def __init__(self, all_lfi_info:ExpLFIInfo, exp_setting:ExpSetting, show_list):
        super().__init__()
        self.setStyleSheet('background-color:gray;')
        self.all_lfi_info=all_lfi_info
        self.exp_setting=exp_setting
        self.show_list=show_list
        self.current_lfi_show_index=0
        self.all_lfi_names=all_lfi_info.GetAllLFNames()
        self.all_dist_types=all_lfi_info.GetAllDistNames(self.all_lfi_names[0])
        self.all_scores=[]
        self.show_page_list=[] # view changing, refocusing

        self.current_page_index=0
        self.max_page_num=0

        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(0,0,screen.width(), screen.height())
        #self.resize(screen.width(), screen.height())

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        #self.setAttribute(Qt.WA_TranslucentBackground)
        
        cur_lf_info=self.GetSingleLFIInfo(self.current_lfi_show_index)

        self.SetPageShowing(cur_lf_info,init_flag=True)
        self.SetPageShowing(cur_lf_info)
        for show_page in self.show_page_list:
            if show_page is not None:
                show_page.setParent(self)


        ############
        self.page_scoring=ScoringPage(screen.height(),screen.width())
        self.page_scoring.setParent(self)
        self.page_scoring.HasScored.connect(self.RecordScore)
        self.addWidget(self.page_scoring)

        ############ 
        self.finish_page=FinishPage(screen.width(),screen.height())
        self.finish_page.setParent(self)
        self.finish_page.key_pressed.connect(lambda: self.FinishAll())
        self.addWidget(self.finish_page)

        self.setCurrentIndex(self.current_page_index)
        #self.setCurrentIndex(1)
        self.all_page_num=self.max_page_num+2

    def GetSingleLFIInfo(self,show_index)->SingleLFIInfo:
        cur_lfi_name=self.show_list[show_index][0]
        cur_left_dist=self.show_list[show_index][1]
        cur_left_dist_level=self.show_list[show_index][2]
        return self.all_lfi_info.GetLFIInfo(cur_lfi_name,cur_left_dist,cur_left_dist_level)
    
    
    def RecordScore(self,ret_scores):
        # get score, then set new lfi image
        self.all_scores.append(ret_scores)
        self.current_lfi_show_index+=1
        if self.current_lfi_show_index >= len(self.show_list):
            self.current_page_index+=1
            self.setCurrentIndex(self.current_page_index)
            return
        cur_lfi_info=self.GetSingleLFIInfo(self.current_lfi_show_index)
        self.SetPageShowing(cur_lfi_info)

        self.current_page_index=0
        self.setCurrentIndex(self.current_page_index)
    
    def SetPageShowing(self,cur_lf_info:SingleLFIInfo,init_flag=False):
        exp_setting=self.exp_setting
        if LFIFeatures.Active_Refocusing in exp_setting.lfi_features and LFIFeatures.Active_ViewChanging in exp_setting.lfi_features:
            if init_flag:
                page_showing=ImagePage(exp_setting,cur_lf_info,cur_lf_info.show_views_path,cur_lf_info.show_refocusing_views_path)
                page_showing.setParent(self)
                self.addWidget(page_showing)
                page_showing.eval_finished.connect(self.NextPage)
                self.max_page_num+=1
                self.show_page_list.append(page_showing)
                self.show_page_list.append(None)
            else:
                self.show_page_list[0].SetNewLFI(exp_setting,cur_lf_info,cur_lf_info.show_views_path,cur_lf_info.show_refocusing_views_path)
            return 

        if LFIFeatures.Active_ViewChanging in exp_setting.lfi_features and LFIFeatures.Active_Refocusing not in exp_setting.lfi_features:
            if init_flag:
                page_showing=ImagePage(exp_setting,cur_lf_info,cur_lf_info.show_views_path,None)
                self.addWidget(page_showing)
                page_showing.eval_finished.connect(self.NextPage)
                self.max_page_num+=1
                self.show_page_list.append(page_showing)
            else:
                self.show_page_list[0].SetNewLFI(exp_setting,cur_lf_info,cur_lf_info.show_views_path,None)
        
        if LFIFeatures.Passive_ViewChanging in exp_setting.lfi_features:
            if init_flag:
                page_showing=VideoPage(exp_setting,cur_lf_info,cur_lf_info.passive_video)
                self.addWidget(page_showing)
                page_showing.finish_video.connect(self.NextPage)
                self.max_page_num+=1
                self.show_page_list.append(page_showing)
            else:
                self.show_page_list[0].SetNewLFI(exp_setting,cur_lf_info,cur_lf_info.passive_video)
        
        if LFIFeatures.None_ViewChanging in exp_setting.lfi_features:
            if init_flag:
                self.show_page_list.append(None)
        
        if LFIFeatures.Active_Refocusing in exp_setting.lfi_features:
            if init_flag:
                page_showing=ImagePage(exp_setting,cur_lf_info,None,cur_lf_info.show_refocusing_views_path)
                self.addWidget(page_showing)
                page_showing.eval_finished.connect(self.NextPage)
                self.max_page_num+=1
                self.show_page_list.append(page_showing)
            else:
                self.show_page_list[1].SetNewLFI(exp_setting,cur_lf_info,None,cur_lf_info.show_refocusing_views_path)
        
        if LFIFeatures.Passive_Refocusing in exp_setting.lfi_features:
            if init_flag:
                page_showing=VideoPage(exp_setting,cur_lf_info,cur_lf_info.passive_refocusing_video)
                self.addWidget(page_showing)
                page_showing.finish_video.connect(self.NextPage)
                self.max_page_num+=1
                self.show_page_list.append(page_showing)
            else:
                self.show_page_list[1].SetNewLFI(exp_setting,cur_lf_info,cur_lf_info.passive_refocusing_video)
        
        if LFIFeatures.None_Refocusing in exp_setting.lfi_features:
            if init_flag:
                self.show_page_list.append(None)
        
    def NextPage(self):
        self.current_page_index+=1
        if self.current_page_index >= self.all_page_num:
            self.current_page_index=0
        self.setCurrentIndex(self.current_page_index)
    
    def PrePage(self):
        self.current_page_index-=1
        if self.current_page_index < 0:
            self.current_page_index=self.all_page_num-1
        self.setCurrentIndex(self.current_page_index)

    def FinishAll(self):
        self.scoring_finished.emit(self.all_scores)
        self.deleteLater()
    
    def keyPressEvent(self, event) -> None:
        cur_page=self.currentWidget()
        cur_page.handle_key_press(event)
        return super().keyPressEvent(event)
    
class FinishPage(QtWidgets.QWidget):
    key_pressed=QtCore.Signal()

    def __init__(self,screen_x,screen_y) -> None:
        super().__init__()
        self.setGeometry(0,0,screen_x,screen_y)
        self.show_label=QtWidgets.QLabel("The experiments are finished! Thank you!\n Please press Esc to escape.",self)

        self.show_label.setGeometry(screen_x//2-400,screen_y//2-100,800,200)
        self.show_label.setFont(QtGui.QFont("Roman times",20,QtGui.QFont.Bold))
    
    def handle_key_press(self, event) -> None:
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Escape or event.key() == Qt.Key_Return:
            self.key_pressed.emit()
        return super().keyPressEvent(event)

class ImagePage(QtWidgets.QWidget):
    eval_finished=QtCore.Signal()
    pair_finished=QtCore.Signal(int)
    
    def __init__(self, exp_setting:ExpSetting,dist_lfi_info:SingleLFIInfo, view_path, refocusing_path=None):
        super().__init__()
        self.setStyleSheet("background-color:gray;")
        self.setMouseTracking(True)

        '''
        As all the light field views have the same resolution,
        we only need to get the resolution of one of them. 
        Also they are recorded in the config file. Thus, we can get them from outside the class.
        The operations include:
            1. view change by hover
            2. refocusing by clicking
            
        '''
        self.hover_open_flag=False
        self.hover_flag=False
        self.drag_flag=False
        self.clicking_flag=False
        self.arrow_key_flag=False
        self.better_one=0

        self.setMouseTracking(True)
        
        self.img_label=QtWidgets.QLabel(self)
        self.img_label.setMouseTracking(True)
        self.comparison_type=exp_setting.comparison_type
        self.clicking_mask=None
        self.SetNewLFI(exp_setting,dist_lfi_info,view_path,refocusing_path)

    def SetNewLFI(self,exp_setting:ExpSetting,dist_lfi_info:SingleLFIInfo, view_path, refocusing_path=None):
        self.lfi_info=dist_lfi_info
        self.view_path=view_path
        self.refocusing_path=refocusing_path
        self.depth_path=dist_lfi_info.depth_path

        self.max_angular_width=dist_lfi_info.max_width
        self.max_angular_height=dist_lfi_info.max_height
        self.min_angular_width=dist_lfi_info.min_width
        self.min_angular_height=dist_lfi_info.min_height

        if LFIFeatures.Stereo_horizontal in exp_setting.lfi_features:
            self.max_angular_width-=1
        
        self.img_width=dist_lfi_info.img_width
        self.img_height=dist_lfi_info.img_height
        self.screen_height,self.screen_width=exp_setting.screen_height,exp_setting.screen_width
        self.setGeometry(0,0,self.screen_width,self.screen_height)
        self.hover_open_flag=False
        self.hover_center_x=0
        self.hover_center_y=0

        self.clicking_mask=EventMask(self.img_height,self.img_width,exp_setting.lfi_features,exp_setting.comparison_type)

        self.img_label.setGeometry(self.clicking_mask.screen_widget_x,self.clicking_mask.screen_widget_y,self.clicking_mask.widget_width,self.clicking_mask.widget_height)

        self.angular_width=self.max_angular_width-self.min_angular_width+1
        self.angular_height=dist_lfi_info.angular_height
        center_x=self.angular_width//2
        center_y=self.angular_height//2
        self.current_x=center_x
        self.current_y=center_y
        self.move_x=center_x
        self.move_y=center_y
        
        post_fix=exp_setting.ViewSaveTypeStr
        self.post_fix=post_fix
        if self.view_path is None:
            all_refocusing_views=os.listdir(self.refocusing_path)
            first_view=all_refocusing_views[0]
            first_view=os.path.join(self.refocusing_path,first_view)
            self.SetImage(first_view)
        else:
            center_view_path=self.MakeViewPath(center_x,center_y)
            self.SetImage(center_view_path)
        
        if self.refocusing_path is not None:
            self.depth_img=cv2.imread(self.depth_path,cv2.IMREAD_GRAYSCALE)
            self.depth_img=cv2.resize(self.depth_img,(self.clicking_mask.img_width,self.clicking_mask.img_height))
        
        # now set the flags
        if LFIFeatures.Active_Refocusing in exp_setting.lfi_features:
            self.clicking_flag=True
        if LFIFeatures.Active_ViewChanging in exp_setting.lfi_features:
            self.hover_flag=True
        if exp_setting.comparison_type == ComparisonType.PairComparison:
            self.arrow_key_flag=True
         
    def SetImage(self,img_path):
        if img_path is None:
            return
        self.img_label.setPixmap(QtGui.QPixmap.fromImage(QtGui.QImage(img_path))) 
    
    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.RightButton and self.hover_flag:
            self.hover_open_flag=True
            self.hover_center_x,self.hover_center_y=event.x(),event.y()
            self.current_x=self.move_x
            self.current_y=self.move_y
            return super().mousePressEvent(event)
        if event.button()==Qt.MouseButton.LeftButton:
            self.hover_open_flag=False
            if self.clicking_flag:
                if self.clicking_mask is not None and self.refocusing_path is not None:
                    ret=self.clicking_mask.IsInRect(event.x(),event.y())
                    if ret[0]:
                        depth_value=self.depth_img[ret[1][1],ret[1][0]]
                        refocus_img_path=os.path.join(self.refocusing_path,f"{depth_value}.{self.post_fix}")
                        self.SetImage(refocus_img_path)
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if self.hover_open_flag and self.hover_flag:
            horizontal_dist=event.x()-self.hover_center_x
            vertical_dist=event.y()-self.hover_center_y
            angular_x=round(horizontal_dist/30)+self.current_x
            angular_y=round(vertical_dist/30)+self.current_y
            angular_x=self.MinMaxClip(angular_x,0,self.angular_width-1)
            angular_y=self.MinMaxClip(angular_y,0,self.angular_height-1)
            cur_img_path=self.MakeViewPath(angular_x,angular_y)
            self.move_x=angular_x
            self.move_y=angular_y
            self.SetImage(cur_img_path)
        return super().mouseMoveEvent(event)

    def handle_key_press(self, event) -> None:
        if not self.arrow_key_flag:
            if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
                self.eval_finished.emit()
            return super().keyPressEvent(event)
        else:
            if event.key() == Qt.Key_Left:
                self.better_one=0
                self.pair_finished.emit(self.better_one)
            if event.key() == Qt.Key_Right:
                self.better_one=1
                self.pair_finished.emit(self.better_one)
            return super().keyPressEvent(event)

    def MakeViewPath(self,angular_x,angular_y):
        view_name=self.lfi_info.GetPureViewName(angular_x,angular_y)
        view_path=os.path.join(self.view_path,view_name+"."+self.post_fix)
        return view_path
        
    def MinMaxClip(self, in_value, min_value, max_value):
        if in_value < min_value:
            return min_value
        if in_value > max_value:
            return max_value
        return int(in_value)

class VideoPage(QtWidgets.QWidget):
    finish_video=QtCore.Signal()
    pair_finished=QtCore.Signal(int)

    def __init__(self, exp_setting:ExpSetting,dist_lfi_info:SingleLFIInfo, video_path):
        super().__init__()
        self.setStyleSheet("background-color:gray;")
    
        self.video_height=0
        self.video_width=0
        self.player=QMediaPlayer()
        self.video_widget=QVideoWidget(self)
        self.player.setVideoOutput(self.video_widget)
        self.video_widget.hide()
        self.img_label=QtWidgets.QLabel(self)
        self.arrow_key_flag=False
        self.better_one=0
        self.video_path=None
        self.SetNewLFI(exp_setting,dist_lfi_info,video_path)
        
    def SetNewLFI(self,exp_setting:ExpSetting,dist_lfi_info:SingleLFIInfo, video_path):
        self.exp_setting=exp_setting
        self.dist_lfi_info=dist_lfi_info
        self.video_path=video_path
        self.base_path=os.path.dirname(video_path)
        self.img_label=QtWidgets.QLabel(self)
        self.thumbnail_path=os.path.join(self.base_path,"thumbnail."+exp_setting.ViewSaveTypeStr)

        img_width=dist_lfi_info.img_width
        img_height=dist_lfi_info.img_height
        self.screen_height,self.screen_width=exp_setting.screen_height,exp_setting.screen_width
        
        self.event_mask=EventMask(img_height,img_width,exp_setting.lfi_features,exp_setting.comparison_type)

        self.setGeometry(0,0,self.event_mask.screen_width,self.event_mask.screen_height)
        self.img_label.setGeometry(self.event_mask.screen_widget_x,self.event_mask.screen_widget_y,self.event_mask.widget_width,self.event_mask.widget_height)

        self.img_label.setPixmap(QtGui.QPixmap.fromImage(QtGui.QImage(self.thumbnail_path)))
        self.img_label.show()

        self.video_height,self.video_width=self.event_mask.widget_height,self.event_mask.widget_width
        self.SetVideo()
    
    def SetEventMask(self, event_mask:EventMask):
        self.event_mask=event_mask
        
    def SetVideo(self):
        self.video_widget.setGeometry(self.event_mask.screen_widget_x,self.event_mask.screen_widget_y,self.video_width,self.video_height)
        self.player.setSource(QUrl.fromLocalFile(self.video_path))

    def mousePressEvent(self, event) -> None:
        if not self.player.isPlaying():
            self.img_label.hide()
            self.video_widget.show()
            self.player.setPosition(0)
            self.player.play()
        return super().mousePressEvent(event)
    
    def handle_key_press(self, event) -> None:
        if not self.arrow_key_flag:
            if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
                self.finish_video.emit()
            return super().keyPressEvent(event)
        else:
            if event.key() == Qt.Key_Left:
                self.better_one=0
                self.pair_finished.emit(self.better_one)
            if event.key() == Qt.Key_Right:
                self.better_one=1
                self.pair_finished.emit(self.better_one)
            return super().keyPressEvent(event)

class ScoringPage(QtWidgets.QWidget):
    HasScored=QtCore.Signal(list)

    def __init__(self,screen_height,screen_width) -> None:
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setGeometry(0,0,screen_width,screen_height)
        self.setStyleSheet("background-color:gray;")
        self.current_focus_index=0
        self.all_table=[]

        self.table_1=ScoringTable("Picture Quality")
        self.table_1.setParent(self)
        self.table_1.setGeometry(screen_width//4-self.table_1.widget_width//2,screen_height//2-self.table_1.widget_height//2,self.table_1.widget_width,self.table_1.widget_height)


        self.table_2=ScoringTable("Overall Quality")
        self.table_2.setParent(self)
        self.table_2.setGeometry(screen_width*3//4-self.table_2.widget_width//2,screen_height//2-self.table_2.widget_height//2,self.table_2.widget_width,self.table_2.widget_height)

        self.all_table.append(self.table_1)
        self.all_table.append(self.table_2)
        self.all_table[self.current_focus_index].SetMyFocused(True)

        for i in range(len(self.all_table)):
            self.all_table[i].table_index=i
            self.all_table[i].be_clicked.connect(lambda i: self.SetSigleFocusedTable(i))

    def handle_key_press(self, event) -> None:
        last_index=0
        if event.key() ==  Qt.Key_Right:
            if self.current_focus_index == len(self.all_table)-1:
                self.current_focus_index=0
                last_index=len(self.all_table)-1
            else:
                self.current_focus_index+=1
                last_index=self.current_focus_index-1
        if event.key() == Qt.Key_Left:
            if self.current_focus_index == 0:
                self.current_focus_index=len(self.all_table)-1
                last_index=0
            else:
                self.current_focus_index-=1
                last_index=self.current_focus_index+1
        self.all_table[last_index].SetMyFocused(False)
        self.all_table[self.current_focus_index].SetMyFocused(True)

        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            all_scores=[]
            for table in self.all_table:
                all_scores.append(table.GetResult())
            self.HasScored.emit(all_scores)

        return super().keyPressEvent(event)
    
    def SetSigleFocusedTable(self,focus_i):
        for index in range(len(self.all_table)):
            if index == focus_i:
                self.all_table[index].SetMyFocused(True)
                self.current_focus_index=index
            else:
                self.all_table[index].SetMyFocused(False)
    

class ScoringTable(QtWidgets.QWidget,ScoreTable):
    be_clicked=QtCore.Signal(int)

    def __init__(self,widget_name) -> None:
        super().__init__()
        self.table_index=0
        self.setupUi(self)
        self.scoring_name.setTitle(widget_name)
        self.widget_width=self.width()
        self.widget_height=self.height()

        self.radioButton.clicked.connect(lambda: self.be_clicked.emit(self.table_index))
        self.radioButton_2.clicked.connect(lambda: self.be_clicked.emit(self.table_index))
        self.radioButton_3.clicked.connect(lambda: self.be_clicked.emit(self.table_index))
        self.radioButton_4.clicked.connect(lambda: self.be_clicked.emit(self.table_index))
        self.radioButton_5.clicked.connect(lambda: self.be_clicked.emit(self.table_index))
        
        self.radioButton.setChecked(True)
        self.border_label.setStyleSheet("border:3px dotted white;")
        self.border_label.hide()

    def GetResult(self):
        if self.radioButton.isChecked():
            return 5
        elif self.radioButton_2.isChecked():
            return 4
        elif self.radioButton_3.isChecked():
            return 3
        elif self.radioButton_4.isChecked():
            return 2
        elif self.radioButton_5.isChecked():
            return 1
        else:
            return -1
    
    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key_5:
            self.radioButton.setChecked(True)
        elif event.key() == Qt.Key_4:
            self.radioButton_2.setChecked(True)
        elif event.key() == Qt.Key_3:
            self.radioButton_3.setChecked(True)
        elif event.key() == Qt.Key_2:
            self.radioButton_4.setChecked(True)
        elif event.key() == Qt.Key_1:
            self.radioButton_5.setChecked(True)
        return super().keyPressEvent(event)
    
    def mousePressEvent(self, event) -> None:
        self.be_clicked.emit(self.table_index)
        return super().mousePressEvent(event)

    def SetMyFocused(self,bfocus):
        if bfocus:
            self.setFocus()
            self.border_label.show()
        else:
            self.border_label.hide()

if __name__ == "__main__":
    app = QtWidgets.QApplication()
    scoring_widget = ScoringPage(1440,2560)
    scoring_widget.HasScored.connect(lambda x:print(x))
    scoring_widget.show()
    sys.exit(app.exec())
