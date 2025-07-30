import sys
sys.path.append('../UI')
sys.path.append('../Widgets/')
sys.path.append('../Utils')
import os
from typing import Optional
from PySide6 import QtCore, QtGui, QtWidgets
import PySide6.QtGui
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QUrl, QTimer
from ExpInfo import *
import PathManager
from ScoreTable_ui import Ui_ScoreTable as ScoreTable
import cv2
import numpy as np
import time
os.environ['PATH']+=';./'
import mpv
import logging
from concurrent.futures import InvalidStateError

logger=logging.getLogger("LogWindow")

import locale
locale.setlocale(locale.LC_NUMERIC, 'C')

class ImageMask:
    '''
    A simple mask class to support the scoring (Only experiment mode, along with the passive mode)
    The active mode needs image masks to indicate the clicing and dragging position.
    '''
    def __init__(self,img_height,img_width) -> None:
        screen = QApplication.primaryScreen().geometry()
        self.screen_width=screen.width()
        self.screen_height=screen.height()

        self.widget_height=img_height
        self.widget_width=img_width

        self.screen_widget_x=self.screen_width//2-self.widget_width//2
        self.screen_widget_y=self.screen_height//2-self.widget_height//2

class RefocusingScoringMask(ImageMask):
    def __init__(self, img_height,img_width,folder_name,mask_file=None,post_fix='png') -> None:
        # current mask: a png image file
        super().__init__(img_height,img_width)
        self.mask_file=mask_file
        self.img_height=img_height
        self.img_width=img_width
        self.post_fix=post_fix

        self.folder_name=folder_name
        self.event_mask=None

        self.screen_widget_x=self.screen_width//2-self.img_width//2
        self.screen_widget_y=self.screen_height//2-self.img_height//2

        self.widget_width=self.img_width
        self.widget_height=self.img_height
        self.MakeMask()
    
    def MakeMask(self):
        if self.mask_file is None:
            return
        # TODO: what if the mask is bigger?
        # TODO: do it without numpy ?
        event_mask=np.zeros([self.screen_height,self.screen_width],dtype=np.uint8)
        #event_mask-=1
        img_x_in_mask=self.screen_width//2-self.img_width//2
        img_y_in_mask=self.screen_height//2-self.img_height//2

        img_mask=cv2.imread(self.mask_file)
        if len(img_mask.shape)==3:
            img_mask=img_mask[:,:,0]
        event_mask[img_y_in_mask:img_y_in_mask+self.img_height,img_x_in_mask:img_x_in_mask+self.img_width]=img_mask
        self.event_mask=event_mask

    def GetRefocusingFile(self,h,w):
        if self.event_mask is None:
            return None
        # from mouse position to image position
        target_value=self.event_mask[h,w]
        if target_value <= 0:
            return None
        else:
            return os.path.join(self.folder_name,f"{str(target_value)}.{self.post_fix}")

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

class BlankScoringWidget(QtWidgets.QWidget):
    blank_timeout=QtCore.Signal()
    def __init__(self,screen_height,screen_width) -> None:
        # just a gray background
        super().__init__()
        self.setGeometry(0,0,screen_width, screen_height)
        self.b_timer=QTimer(self)
        self.b_timer.setInterval(1500)
        self.b_timer.timeout.connect(self.b_timeout)
      
    def wait_until_timeout(self,wait_time=1.5):
        self.b_timer.setInterval(int(wait_time*1000))
        self.b_timer.start()
    
    def b_timeout(self):
        self.b_timer.stop()
        self.blank_timeout.emit()
    
    def handle_key_press(self, key):
        #print('key press is ignored')
        key.ignore()
        pass

class PairWiseScoringWidget(QtWidgets.QStackedWidget):
    scoring_finished=QtCore.Signal(list)
    
    def __init__(self, all_lfi_info:AllScoringLFI, exp_setting:ExpSetting, all_show_index):
        super().__init__()

        self.setStyleSheet('background-color:gray;')

        self.all_lfi_info=all_lfi_info
        self.exp_setting=exp_setting
        self.all_show_index=all_show_index
        self.current_lfi_show_index=0

        self.all_view_scores=[]
        self.all_refocusing_scores=[]
        self.show_page_list=[] # view changing, refocusing

        self.current_page_index=0
        self.max_page_num=0

        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(0,0,screen.width(), screen.height())

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        #self.setAttribute(Qt.WA_TranslucentBackground)
        
        #cur_lf_info=self.GetSingleLFIInfo(self.current_lfi_show_index)
        cur_scoring_lfi_info=self.all_lfi_info.GetScoringExpLFIInfo(self.all_show_index[self.current_lfi_show_index])

        locale.setlocale(locale.LC_NUMERIC,"C")

        self.SetPageShowing(cur_scoring_lfi_info,init_flag=True)
        #self.SetPageShowing(cur_scoring_lfi_info)
        for page in self.show_page_list:
            if page is not None:
                page.setParent(self)

        ############ 
        self.blank_page=BlankScoringWidget(screen_height=screen.height(),screen_width=screen.width())
        self.blank_page.blank_timeout.connect(lambda: self.BlankPageNext())
        self.blank_page.setParent(self)
        self.addWidget(self.blank_page)

        self.finish_page=FinishPage(screen.width(),screen.height())
        self.finish_page.key_pressed.connect(lambda: self.FinishAll())
        self.finish_page.setParent(self)
        self.addWidget(self.finish_page)

        self.all_page_num=self.max_page_num+2
    
    def SetScoringScreen(self,screen_index):
        app=QApplication.instance()
        if app is None:
            app=QApplication([])
        self.setScreen(app.screens()[screen_index])
        cur_scree=self.screen()
        self.move(cur_scree.geometry().topLeft())
        self.resize(cur_scree.geometry().size())
        self.blank_page.resize(self.width(),self.height())
        self.blank_page.setGeometry(0,0,self.width(),self.height())
        self.finish_page.resize(self.width(),self.height())
        self.finish_page.setGeometry(0,0,self.width(),self.height())

    def GetSingleLFIInfo(self,show_index)->ScoringExpLFIInfo:
        cur_index=self.all_show_index[show_index]
        return self.all_lfi_info.GetScoringExpLFIInfo(cur_index)
    
    def ShowingNext(self,ret_score,score_list,i=0):
        if i+1>=self.max_page_num:
            self.RecordScore(ret_score,score_list)
        else:
            score_list.append(ret_score)
            self.NextPage()

    def RecordScore(self,ret_score,score_list):
        # get score, then set new lfi image
        logger.debug(f"Score is {ret_score}")
        score_list.append(ret_score)
        self.NextPage()
    
    def BlankPageNext(self):
        self.current_lfi_show_index+=1
        if self.current_lfi_show_index >= self.all_lfi_info.GetLFINum():
            self.current_page_index+=1
            self.setCurrentIndex(self.current_page_index)
            return
        cur_lfi_info=self.GetSingleLFIInfo(self.current_lfi_show_index)
        self.SetPageShowing(cur_lfi_info)

        self.current_page_index=0
        self.setCurrentIndex(self.current_page_index)
    
    def SetPageShowing(self,cur_lf_info:ScoringExpLFIInfo,init_flag=False):
        exp_setting=self.exp_setting

        if exp_setting.two_folder_mode and LFIFeatures.Passive_ViewChanging in exp_setting.lfi_features:
            if init_flag:
                page_showing=VideoPage(exp_setting,None,cur_lf_info.passive_view_video_path,cmp_type=ComparisonType.PairComparison)
                self.addWidget(page_showing)
                page_showing.pair_finished.connect(lambda x: self.ShowingNext(x,self.all_view_scores,0))
                self.max_page_num+=1
                self.show_page_list.append(page_showing)
            else:
                self.show_page_list[0].SetNewLFI(exp_setting,None,cur_lf_info.passive_view_video_path,cmp_type=ComparisonType.PairComparison)
            return

        if LFIFeatures.Active_Refocusing in exp_setting.lfi_features and LFIFeatures.Active_ViewChanging in exp_setting.lfi_features:
            if init_flag:
                page_showing=ImagePage(exp_setting,cur_lf_info,cur_lf_info.active_view_path,cur_lf_info.active_refocusing_path)
                self.addWidget(page_showing)
                page_showing.pair_finished.connect(lambda x: self.ShowingNext(x,self.all_view_scores,0))
                self.max_page_num+=1
                self.show_page_list.append(page_showing)
                self.show_page_list.append(None)
            else:
                self.show_page_list[0].SetNewLFI(exp_setting,cur_lf_info,cur_lf_info.active_view_path,cur_lf_info.active_refocusing_path)
            return 

        if LFIFeatures.Active_ViewChanging in exp_setting.lfi_features and LFIFeatures.Active_Refocusing not in exp_setting.lfi_features:
            if init_flag:
                page_showing=ImagePage(exp_setting,cur_lf_info,cur_lf_info.active_view_path,cur_lf_info.active_refocusing_path)
                self.addWidget(page_showing)
                page_showing.pair_finished.connect(lambda x: self.ShowingNext(x,self.all_view_scores,0))
                self.max_page_num+=1
                self.show_page_list.append(page_showing)
            else:
                self.show_page_list[0].SetNewLFI(exp_setting,cur_lf_info,cur_lf_info.active_view_path,cur_lf_info.active_refocusing_path)
        
        if LFIFeatures.Passive_ViewChanging in exp_setting.lfi_features:
            if init_flag:
                page_showing=VideoPage(exp_setting,cur_lf_info,cur_lf_info.passive_view_video_path)
                self.addWidget(page_showing)
                page_showing.pair_finished.connect(lambda x: self.ShowingNext(x,self.all_view_scores,0))
                self.max_page_num+=1
                self.show_page_list.append(page_showing)
            else:
                self.show_page_list[0].SetNewLFI(exp_setting,cur_lf_info,cur_lf_info.passive_view_video_path)
        
        if LFIFeatures.None_ViewChanging in exp_setting.lfi_features:
            if init_flag:
                self.show_page_list.append(None)
        
        if LFIFeatures.Active_Refocusing in exp_setting.lfi_features:
            if init_flag:
                page_showing=ImagePage(exp_setting,cur_lf_info,None,cur_lf_info.active_refocusing_path)
                self.addWidget(page_showing)
                page_showing.pair_finished.connect(lambda x: self.ShowingNext(x,self.all_refocusing_scores,1))
                self.max_page_num+=1
                self.show_page_list.append(page_showing)
            else:
                self.show_page_list[1].SetNewLFI(exp_setting,cur_lf_info,None,cur_lf_info.active_refocusing_path)
        
        if LFIFeatures.Passive_Refocusing in exp_setting.lfi_features:
            if init_flag:
                page_showing=VideoPage(exp_setting,cur_lf_info,cur_lf_info.passive_refocusing_video_path)
                self.addWidget(page_showing)
                page_showing.pair_finished.connect(lambda x: self.ShowingNext(x,self.all_refocusing_scores,1))
                self.max_page_num+=1
                self.show_page_list.append(page_showing)
            else:
                self.show_page_list[1].SetNewLFI(exp_setting,cur_lf_info,cur_lf_info.passive_refocusing_video_path)
        
        if LFIFeatures.None_Refocusing in exp_setting.lfi_features:
            if init_flag:
                self.show_page_list.append(None)
    
    def NextPage(self):
        '''
        Dirty Code
        '''
        self.current_page_index+=1
        if self.current_page_index >= self.all_page_num:
            self.current_page_index=0
        self.setCurrentIndex(self.current_page_index)
        if self.currentWidget() == self.blank_page:
            self.blank_page.wait_until_timeout(1.5)
    
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
        self.hide()
        self.scoring_finished.emit([self.all_view_scores,self.all_refocusing_scores])
        for page in self.show_page_list:
            if page is not None:
                if isinstance(page,VideoPage):
                    page.CloseVideoPlayer()
        self.deleteLater()
        
    def keyPressEvent(self, event) -> None:
        cur_page=self.currentWidget()
        cur_page.handle_key_press(event)
        return super().keyPressEvent(event)

class ScoringWidget(QtWidgets.QStackedWidget):
    scoring_finished=QtCore.Signal(list)
    
    def __init__(self, all_lfi_info:AllScoringLFI, exp_setting:ExpSetting, all_show_index):
        super().__init__()
        self.setStyleSheet('background-color:gray;')
        self.all_lfi_info=all_lfi_info
        self.exp_setting=exp_setting
        self.all_show_index=all_show_index

        all_level_names=exp_setting.score_names
        all_score_levels=exp_setting.score_levels

        self.current_lfi_show_index=0
        
        self.all_level_names=all_level_names
        if type(all_score_levels)==int:
            self.all_score_levels=[all_score_levels]*len(self.all_level_names)
        else:
            self.all_score_levels=all_score_levels
        
        self.all_score_definitions=exp_setting.score_definition

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
        
        cur_lfi_scoring_info=self.GetSingleLFIInfo(self.current_lfi_show_index)

        self.SetPageShowing(cur_lfi_scoring_info,init_flag=True)
        #self.SetPageShowing(cur_lfi_scoring_info)
        for show_page in self.show_page_list:
            if show_page is not None:
                show_page.setParent(self)


        ############
        self.page_scoring=ScoringPage(screen.height(),screen.width(),self.all_level_names,self.all_score_levels,self.all_score_definitions,self.exp_setting.score_values,font_size=self.exp_setting.table_font_size)
        self.page_scoring.setParent(self)
        self.page_scoring.RefreshAllTables()
        self.page_scoring.HasScored.connect(self.RecordScore)
        self.addWidget(self.page_scoring)

        ############ 
        self.finish_page=FinishPage(screen.width(),screen.height())
        self.finish_page.setParent(self)
        self.finish_page.key_pressed.connect(lambda: self.FinishAll())
        self.addWidget(self.finish_page)

        if self.exp_setting.comparison_type == ComparisonType.DSCS_PC_BASE or self.exp_setting.comparison_type == ComparisonType.DSCS_PC_CCG:
            self.finish_page.SetLabelContent("The double DSCS session has been finished.\n Please press ESC to escape.")

        self.setCurrentIndex(self.current_page_index)
        #self.setCurrentIndex(1)
        self.all_page_num=self.max_page_num+2
    
    def SetScoringScreen(self,screen_index):
        app=QApplication.instance()
        if app is None:
            app=QApplication([])
        self.setScreen(app.screens()[screen_index])
        cur_scree=self.screen()
        self.move(cur_scree.geometry().topLeft())
        self.resize(cur_scree.geometry().size())
        self.page_scoring.resize(cur_scree.geometry().size())
        self.page_scoring.setGeometry(0,0,self.width(),self.height())
        self.page_scoring.RefreshAllTables()
        self.finish_page.resize(self.width(),self.height())
        self.finish_page.setGeometry(0,0,self.width(),self.height())
        

    def GetSingleLFIInfo(self,show_index)->ScoringExpLFIInfo:
        cur_index=self.all_show_index[show_index]
        return self.all_lfi_info.GetScoringExpLFIInfo(cur_index)
    
    def RecordScore(self,ret_scores):
        # get score, then set new lfi image
        logger.debug(f'selected score is {ret_scores}')
        self.page_scoring.RefreshAllTables()
        self.all_scores.append(ret_scores)
        self.current_lfi_show_index+=1
        if self.current_lfi_show_index >= self.all_lfi_info.GetLFINum():
            self.current_page_index+=1
            self.setCurrentIndex(self.current_page_index)
            return
        cur_lfi_info=self.GetSingleLFIInfo(self.current_lfi_show_index)
        self.SetPageShowing(cur_lfi_info)

        self.current_page_index=0
        self.setCurrentIndex(self.current_page_index)
    
    def SetPageShowing(self,cur_lf_info:ScoringExpLFIInfo,init_flag=False):
        exp_setting=self.exp_setting
        if exp_setting.two_folder_mode and LFIFeatures.Passive_ViewChanging in exp_setting.lfi_features:
            if init_flag:
                #TODO: but it is not true!!!
                page_showing=VideoPage(exp_setting,None,cur_lf_info.passive_view_video_path,cmp_type=ComparisonType.DoubleStimuli)
                self.addWidget(page_showing)
                page_showing.finish_video.connect(self.NextPage)
                self.max_page_num+=1
                self.show_page_list.append(page_showing)
            else:
                self.show_page_list[0].SetNewLFI(exp_setting,None,cur_lf_info.passive_view_video_path,cmp_type=ComparisonType.DoubleStimuli)
            return

        if LFIFeatures.Active_Refocusing in exp_setting.lfi_features and LFIFeatures.Active_ViewChanging in exp_setting.lfi_features:
            if init_flag:
                page_showing=ImagePage(exp_setting,cur_lf_info,cur_lf_info.active_view_path,cur_lf_info.active_refocusing_path)
                page_showing.setParent(self)
                self.addWidget(page_showing)
                page_showing.eval_finished.connect(self.NextPage)
                self.max_page_num+=1
                self.show_page_list.append(page_showing)
                self.show_page_list.append(None)
            else:
                self.show_page_list[0].SetNewLFI(exp_setting,cur_lf_info,cur_lf_info.active_view_path,cur_lf_info.active_refocusing_path)
            return 

        if LFIFeatures.Active_ViewChanging in exp_setting.lfi_features and LFIFeatures.Active_Refocusing not in exp_setting.lfi_features:
            if init_flag:
                page_showing=ImagePage(exp_setting,cur_lf_info,cur_lf_info.active_view_path,cur_lf_info.active_refocusing_path)
                self.addWidget(page_showing)
                page_showing.eval_finished.connect(self.NextPage)
                self.max_page_num+=1
                self.show_page_list.append(page_showing)
            else:
                self.show_page_list[0].SetNewLFI(exp_setting,cur_lf_info,cur_lf_info.active_view_path,cur_lf_info.active_refocusing_path)
        
        if LFIFeatures.Passive_ViewChanging in exp_setting.lfi_features:
            if init_flag:
                page_showing=VideoPage(exp_setting,cur_lf_info,cur_lf_info.passive_view_video_path)
                self.addWidget(page_showing)
                page_showing.finish_video.connect(self.NextPage)
                self.max_page_num+=1
                self.show_page_list.append(page_showing)
            else:
                self.show_page_list[0].SetNewLFI(exp_setting,cur_lf_info,cur_lf_info.passive_view_video_path)
        
        if LFIFeatures.None_ViewChanging in exp_setting.lfi_features:
            if init_flag:
                self.show_page_list.append(None)
        
        if LFIFeatures.Active_Refocusing in exp_setting.lfi_features:
            if init_flag:
                page_showing=ImagePage(exp_setting,cur_lf_info,None,cur_lf_info.active_refocusing_path)
                self.addWidget(page_showing)
                page_showing.eval_finished.connect(self.NextPage)
                self.max_page_num+=1
                self.show_page_list.append(page_showing)
            else:
                self.show_page_list[1].SetNewLFI(exp_setting,cur_lf_info,None,cur_lf_info.active_refocusing_path)
        
        if LFIFeatures.Passive_Refocusing in exp_setting.lfi_features:
            if init_flag:
                page_showing=VideoPage(exp_setting,cur_lf_info,cur_lf_info.passive_refocusing_video_path)
                self.addWidget(page_showing)
                page_showing.finish_video.connect(self.NextPage)
                self.max_page_num+=1
                self.show_page_list.append(page_showing)
            else:
                self.show_page_list[1].SetNewLFI(exp_setting,cur_lf_info,cur_lf_info.passive_refocusing_video_path)
        
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
        self.hide()
        for page in self.show_page_list:
            if page is not None:
                if isinstance(page,VideoPage):
                    page.CloseVideoPlayer()
        #self.deleteLater()
    
    def keyPressEvent(self, event) -> None:
        cur_page=self.currentWidget()
        cur_page.handle_key_press(event)
        return super().keyPressEvent(event)
    
class FinishPage(QtWidgets.QWidget):
    key_pressed=QtCore.Signal()

    def __init__(self,screen_x,screen_y) -> None:
        super().__init__()
        self.screen_x=screen_x
        self.screen_y=screen_y
        self.setGeometry(0,0,screen_x,screen_y)
        self.label_content="The experiments are finished! Thank you!\n Please press Esc to escape."
        self.show_label=QtWidgets.QLabel(self.label_content,self)

        self.show_label.setGeometry(screen_x//2-400,screen_y//2-100,800,200)
        self.show_label.setFont(QtGui.QFont("Roman times",20,QtGui.QFont.Bold))
    
    def SetLabelContent(self,content):
        self.label_content=content
        self.show_label.setText(self.label_content)
        self.show_label.setGeometry(self.screen_x//2-400,self.screen_y//2-100,800,200)
        self.show_label.setFont(QtGui.QFont("Roman times",20,QtGui.QFont.Bold))

    def handle_key_press(self, event) -> None:
        event.ignore()
        #if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Escape or event.key() == Qt.Key_Return:
        if event.key() == Qt.Key_Escape:
            self.key_pressed.emit()
        #return super().keyPressEvent(event)

class ImagePage(QtWidgets.QWidget):
    eval_finished=QtCore.Signal()
    pair_finished=QtCore.Signal(int)
    
    def __init__(self, exp_setting:ExpSetting,dist_lfi_info:ScoringExpLFIInfo, view_path, refocusing_path=None):
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

        self.setMouseTracking(True)
        
        self.img_label=QtWidgets.QLabel(self)
        self.img_label.setMouseTracking(True)
        self.comparison_type=exp_setting.comparison_type
        self.clicking_mask=None

        self.left_btn=QtWidgets.QPushButton("Select Left",)
        self.left_btn.setParent(self)
        self.left_btn.setStyleSheet("QPushButton:focus {border: 2px solid white;}")
        self.left_btn.hide()
        self.left_btn.clicked.connect(lambda: self.pair_finished.emit(0))

        self.right_btn=QtWidgets.QPushButton("Select Right")
        self.right_btn.setParent(self)
        self.right_btn.setStyleSheet("QPushButton:focus {border: 2px solid white;}")
        self.right_btn.hide()
        self.right_btn.clicked.connect(lambda: self.pair_finished.emit(1))

        self.next_btn  =QtWidgets.QPushButton("Next")
        self.next_btn.setParent(self)
        self.next_btn.clicked.connect(lambda: self.eval_finished.emit())
        self.next_btn.hide()

        self.SetNewLFI(exp_setting,dist_lfi_info,view_path,refocusing_path)

    def SetNewLFI(self,exp_setting:ExpSetting,dist_lfi_info:ScoringExpLFIInfo, view_path, refocusing_path=None):
        self.exp_setting=exp_setting
        self.lfi_info=dist_lfi_info
        self.view_path=view_path
        self.refocusing_path=refocusing_path
        self.mask_file=dist_lfi_info.refocusing_mask_file

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

        #self.clicking_mask=EventMask(self.img_height,self.img_width,exp_setting.lfi_features,exp_setting.comparison_type)

        self.clicking_mask=RefocusingScoringMask(self.img_height,self.img_width,self.refocusing_path,self.mask_file)

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
        
        # now set the flags
        if LFIFeatures.Active_Refocusing in exp_setting.lfi_features:
            self.clicking_flag=True
        if LFIFeatures.Active_ViewChanging in exp_setting.lfi_features:
            self.hover_flag=True
        
        btn_height=PathManager.btn_height
        btn_width=PathManager.btn_width
        btn_pos_y=(self.clicking_mask.screen_height+self.clicking_mask.widget_height+self.clicking_mask.screen_widget_y)//2-btn_height//2

        if exp_setting.comparison_type == ComparisonType.PairComparison:
            '''
            left_btn_pos_x=1*self.clicking_mask.screen_width//8 - btn_width//2
            right_btn_pos_x=5*self.clicking_mask.screen_width//8 - btn_width//2
            '''
            left_btn_pos_x=self.clicking_mask.screen_widget_x + (self.clicking_mask.widget_width//2-btn_width)//2
            right_btn_pos_x=self.clicking_mask.screen_widget_x + (3*self.clicking_mask.widget_width//2-btn_width)//2

            self.left_btn.setGeometry(left_btn_pos_x,btn_pos_y,btn_width,btn_height)
            self.left_btn.show()
            self.right_btn.setGeometry(right_btn_pos_x,btn_pos_y,btn_width,btn_height)
            self.right_btn.show()
        else:
            next_btn_pos_x=self.clicking_mask.screen_width//2-btn_width//2
            self.next_btn.setGeometry(next_btn_pos_x,btn_pos_y,btn_width,btn_height)
            self.next_btn.show()
         
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
                    target_file=self.clicking_mask.GetRefocusingFile(event.y(),event.x())
                    if target_file is not None:
                        self.SetImage(target_file)
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
        event.ignore()
        if self.exp_setting.comparison_type ==  ComparisonType.PairComparison:
            if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
                if self.left_btn.hasFocus():
                    self.pair_finished.emit(0)
                else:
                    self.pair_finished.emit(1)
        else:
            if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
                self.eval_finished.emit()
        #return super().keyPressEvent(event)

    def MakeViewPath(self,angular_x,angular_y):
        view_path=self.lfi_info.GetActiveView(angular_y,angular_x)
        #view_name=self.lfi_info.GetPureViewName(angular_x,angular_y)
        #view_path=os.path.join(self.view_path,view_name+"."+self.post_fix)
        return view_path
        
    def MinMaxClip(self, in_value, min_value, max_value):
        if in_value < min_value:
            return min_value
        if in_value > max_value:
            return max_value
        return int(in_value)

class LFIVideoPlayer(QtWidgets.QLabel):
    OnOneLoopEnd=QtCore.Signal()
    OnVideoPlayerFinished=QtCore.Signal()

    def __init__(self,video_path,pos_x=0,pos_y=0,fps=25,loop_times=-1):
        super().__init__()
        self.pos_x=pos_x
        self.pos_y=pos_y
        self.OnOneLoopEnd.connect(self.OneLoopEnd)
        self.timer=QTimer()
        self.timer.timeout.connect(self.ShowNextFrame)
        self.fps=fps
        self.is_playing=False
        self.loop_times_record=loop_times

        if self.fps==0:
            self.fps=-1
        self.frame_duration=1000//self.fps

        self.InitTheVideo(video_path)
    
    def setVideoPath(self,video_path):
        self.StopPlaying()
        self.InitTheVideo(video_path)
    
    def ShowNextFrame(self):
        if self.cur_frame_index<self.frame_num:
            ret,self.cur_frame=self.cur_cap.read()
            if ret:
                self.cur_frame=cv2.cvtColor(self.cur_frame,cv2.COLOR_BGR2RGB)
                self.setPixmap(QtGui.QPixmap.fromImage(QtGui.QImage(self.cur_frame.data,self.video_width,self.video_height,3*self.video_width,QtGui.QImage.Format_RGB888)))
            self.cur_frame_index+=1
        else:
            self.timer.stop()
            self.is_playing=False
            self.OnOneLoopEnd.emit()
    
    def toogle_play_pause(self):
        if self.is_playing:
            self.timer.stop()
        else:
            self.timer.start(self.frame_duration)
        self.is_playing = not self.is_playing
    
    def InitTheVideo(self,video_path):
        self.cur_cap=cv2.VideoCapture(video_path)
        self.valid_video_flag=self.cur_cap.isOpened()

        self.video_path=video_path
        self.is_playing=False
        self.loop_times=self.loop_times_record

        # Self.fps=self.cur_cap.get(cv2.CAP_PROP_FPS)
        # 25 fps or decided by the users?

        if self.valid_video_flag:
            self.frame_num=int(self.cur_cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.video_height=int(self.cur_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.video_width=int(self.cur_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            if self.fps < 0:
                self.SetFPS(self.cur_cap.get(cv2.CAP_PROP_FPS))
            self.cur_frame_index=-1
        else:
            self.frame_num=0
            self.video_height=0
            self.video_width=0
            self.cur_frame_index=0
        self.cur_frame=None

        if self.frame_num>0:
            self.setGeometry(self.pos_x,self.pos_y,self.video_width,self.video_height)
            self.ShowNextFrame()
        else:
            self.video_height=0
            self.video_width=0
    
    def SetFPS(self,fps):
        self.fps=fps
        self.frame_duration=1000//self.fps
    
    def PlayVideo(self):
        if not self.is_playing:
            self.toogle_play_pause()
    
    def OneLoopEnd(self):
        if self.loop_times>0:
            self.loop_times-=1
        self.cur_frame_index=-1
        self.cur_cap.set(cv2.CAP_PROP_POS_FRAMES,0)
        if self.loop_times!=0:
            self.PlayVideo()
        else:
            self.StopPlaying()
            self.OnVideoPlayerFinished.emit()

    def PauseVideo(self):
        if self.is_playing:
            self.toogle_play_pause()
    
    def StopPlaying(self):
        self.timer.stop()
        self.is_playing=False
    
    def SetLoop(self,loop_times=-1):
        self.loop_times=loop_times
        self.loop_times_record =  self.loop_times

class MPVFramePlayer(QtWidgets.QWidget):
    '''
    a player based on the libmpv, frame by frame;
    keep the same API as LFIVideoPlayer
    '''
    OnOneLoopEnd=QtCore.Signal()
    OnVideoPlayerFinished=QtCore.Signal()
    def __init__(self,video_path,pos_x=0,pos_y=0,fps=0,loop_times=-1):
        super().__init__()
        self.pos_x=pos_x
        self.pos_y=pos_y
        self.OnOneLoopEnd.connect(self.OneLoopEnd)
        self.timer=QTimer()
        self.timer.timeout.connect(self.ShowNextFrame)
        self.fps=fps
        self.is_playing=False
        self.loop_times_record=loop_times

        if self.fps==0:
            self.fps=-1
        self.frame_duration=1000//self.fps

        self.player_container=QtWidgets.QWidget(self)
        self.player_container.setAttribute(Qt.WA_DontCreateNativeAncestors)
        self.player_container.setAttribute(Qt.WA_NativeWindow)

        self.InitTheVideo(video_path)
    
    def setVideoPath(self,video_path):
        self.StopPlaying()
        self.InitTheVideo(video_path)

    def toogle_play_pause(self):
        if self.is_playing:
            self.timer.stop()
        else:
            self.timer.start(self.frame_duration)
        self.is_playing =  not self.is_playing

    def InitTheVideo(self,video_path):
        '''
        here we use the mpv as a video capture.
        it shows the video frame by frame.
        '''
        #self.cur_cap=mpv.MPV(wid=str(int(self.player_container.winId())))
        self.cur_cap=mpv.MPV(wid=str(int(self.player_container.winId())),input_default_bindings=False,border=False,video_unscaled=True)
        self.video_path=video_path
        self.is_playing=False
        self.loop_times=self.loop_times_record
        self.cur_frame_index=0 # different from LFVideoPlayer, as we do not start from a blank beginning point

        self.cur_cap._loop = True
        self.cur_cap.play(self.video_path)
        self.cur_cap.pause=True

        video_capture=cv2.VideoCapture(self.video_path)
        if video_capture.isOpened():
            self.frame_num=int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
            self.video_height=int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.video_width=int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            if self.fps < 0:
                self.SetFPS(video_capture.get(cv2.CAP_PROP_FPS))
            self.cur_frame_index=-1
        else:
            self.frame_num=0
            self.video_height=0
            self.video_width=0
            self.cur_frame_index=0

        if self.frame_num>0:
            self.setGeometry(self.pos_x,self.pos_y,self.video_width,self.video_height)
        else:
            self.video_height=0
            self.video_width=0

    def SetFPS(self,fps):
        self.fps=fps
        self.frame_duration=1000//self.fps
    
    def PlayVideo(self):
        if not self.is_playing:
            self.toogle_play_pause()
    
    def OneLoopEnd(self):
        if self.loop_times>0:
            self.loop_times-=1
        self.cur_cap.command('seek',0,'absolute')
        if self.loop_times!=0:
            self.PlayVideo()
        else:
            self.StopPlaying()
            self.OnVideoPlayerFinished.emit()

    def PauseVideo(self):
        if self.is_playing:
            self.toogle_play_pause()

    def StopPlaying(self):
        self.timer.stop()
        self.is_playing=False
    
    def SetLoop(self,loop_times=-1):
        self.loop_times=loop_times

class MPVVideoPlayer(QtWidgets.QWidget):
    '''
    this plays the video with mpv.
    can not control the fps.
    '''
    OnVideoPlayerFinished=QtCore.Signal()
    OnFirstLoopFinished=QtCore.Signal()

    def __init__(self,video_path,pos_x=0,pos_y=0,fps=None,loop_times=-1,auto_transition=False):
        super().__init__()
        self.pos_x=pos_x
        self.pos_y=pos_y

        self.loop_times_record=loop_times

        self.fps=None # not used at all
        self.video_height=0
        self.video_width=0
        self.video_path=video_path

        self.player_container=QtWidgets.QWidget(self)
        self.setStyleSheet("background-color: gray;")
        self.player_container.setAttribute(Qt.WA_DontCreateNativeAncestors)
        self.player_container.setAttribute(Qt.WA_NativeWindow)

        self.auto_transition=auto_transition

        self.first_loop_finished=False

        self.has_finished=False

        '''
        self.player_guard=QTimer()
        self.b_player_crashed=False
        self.player_guard.setInterval(100)
        self.player_guard.timeout.connect(self.check_cur_cap)
        #self.player_guard.start()
        '''

        self.cur_cap=None
        self.GetVideoPara(video_path)
        #self.setVideoPath(video_path)

    def setVideoPath(self,video_path):
        if self.cur_cap is not None:
            self.StopPlaying()
        self.GetVideoPara(video_path)
        retry_count=0
        while not self.InitTheVideo(video_path):
            logger.warning(f'MPV player init failed, retrying {retry_count} times...')
            retry_count+=1
            if retry_count>10:
                logger.error(f'Failed to init the video, please check the path {self.video_path}')
                exit(-1)

    def SetFPS(self,fps):
        pass

    def GetVideoPara(self,video_path):
        video_capture=cv2.VideoCapture(self.video_path)
        if video_capture.isOpened():
            self.frame_num=int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
            self.video_height=int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.video_width=int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        else:
            self.frame_num=0
            self.video_height=0
        
        if self.frame_num > 0:
            self.resize(self.video_width,self.video_height)
            self.player_container.setGeometry(self.pos_x,self.pos_y,self.video_width,self.video_height)
        else:
            self.video_height=0
            self.video_width=0

    def InitTheVideo(self,video_path,raise_crash=True):
        import locale
        locale.setlocale(locale.LC_NUMERIC, 'C')
        self.cur_cap=mpv.MPV(wid=str(int(self.player_container.winId())),input_default_bindings=False,border=False,video_unscaled=True)
        self.video_path=video_path
        self.is_playing=False
        self.loop_times=self.loop_times_record
        self.has_finished=False

        self.cur_cap.play(self.video_path)
        try:
            self.cur_cap.wait_for_property('seekable')
        except:
            self.StopPlaying()
            return False
        self.cur_cap.command('seek',0,'absolute')

        if self.loop_times ==  0:
            self.loop_times+=1
        
        '''
        if self.loop_times > 0:
            self.cur_cap._set_property('loop-file',int(self.loop_times))
        else:
            self.cur_cap._set_property('loop-file','inf')
        '''
        
        self.cur_cap._set_property('loop-file','inf')
        self.cur_cap._set_property('keep-open','yes')

        '''
        if self.auto_transition:
            self.cur_cap.register_event_callback(self._loop_end)
        else:
            self.cur_cap._set_property('keep-open','yes')
        '''
        #self.cur_cap.register_event_callback(self.shut_down_handler)
        
        self.play_times=0
        return True
    
    def isReady(self):
        return self.width is not None

    def check_cur_cap(self):
        if self.b_player_crashed:
            self.b_player_crashed=False
            self.StopPlaying()
            self.setVideoPath(self.video_path,raise_crash=False)

    def shut_down_handler(self,event):
        if event.event_id.value == mpv.MpvEventID.SHUTDOWN:
            if not self.has_finished:
                print('mpv shuts down unexpectedly, restart it now...')
                self.b_player_crashed=True
            else:
                logger.info(f'{self.video_path} has finished playing, preparing next video now...')

    def _loop_times_recoding(self,event):
        if event.event_id.value == mpv.MpvEventID.SEEK:
            self.play_times+=1
            logger.debug(f'has already played {self.play_times} times')
            if self.play_times == 1:
                self.OnFirstLoopFinished.emit()
            if self.play_times >= self.loop_times and self.loop_times>0:
                self.cur_cap.pause=True
                self.has_finished=True
                if self.auto_transition:
                    self.OnVideoPlayerFinished.emit()

            '''
            print(f'has already played {self.play_times+1} times')
            if self.first_loop_finished:
                return
            self.first_loop_finished=True
            self.OnFirstLoopFinished.emit()
            '''
        
    def _loop_end(self,event):
        if event.event_id.value == mpv.MpvEventID.END_FILE:
            self.cur_cap.stop()
            self.is_playing=False
            self.OnVideoPlayerFinished.emit()
    
    def toogle_play_pause(self):
        if self.has_finished:
            return
        self.cur_cap.pause = not self.cur_cap.pause
        self.is_playing = not self.is_playing

    # not safe now
    def PlayVideo(self):
        self.cur_cap.pause = True
        self.cur_cap.command('seek',0,'absolute')
        self.cur_cap.pause = False
        self.cur_cap.wait_until_playing()
        self.is_playing = True
        self.has_finished=False
        self.cur_cap.register_event_callback(self._loop_times_recoding)

    def PauseVideo(self):
        if not self.cur_cap.pause:
            self.cur_cap.pause = not self.cur_cap.pause

    def StopPlaying(self):
        self.has_finished=True
        self.is_playing=False
        self.first_loop_finished=False
        if self.cur_cap is not None:
            self.cur_cap.terminate()
            self.cur_cap.wait_for_shutdown()
            self.cur_cap=None
        self.hide()
    
class VideoPage(QtWidgets.QWidget):
    finish_video=QtCore.Signal()
    pair_finished=QtCore.Signal(int)

    def __init__(self, exp_setting:ExpSetting,dist_lfi_info:ScoringExpLFIInfo, video_path,cmp_type=None):
        '''
        loop_times: the loop times of the video. We do not need a loop play flag to indicate whether the video will loop. The loop_times =1 means just playing once.

        loop_time_sec: the video will loop within loop_time_sec seconds. But it will not be used this version. 
        '''
        super().__init__()
        self.setStyleSheet("background-color:gray;")
        auto_play=exp_setting.auto_play
        loop_times=exp_setting.loop_times
        fps=exp_setting.fps

        if cmp_type is None:
            self.comparison_type=exp_setting.comparison_type
        else:
            self.comparison_type=cmp_type

        self.pause_allowed=exp_setting.pause_allowed

        self.auto_play=auto_play
        self.auto_play_delay_time=500


        self.loop_times=loop_times

        self.fps=fps

        self.auto_transition=exp_setting.auto_transition  # dirty code !
        if exp_setting.first_loop_skip:
            self.evaluate_enable=True
        else:
            self.evaluate_enable=False
        if self.comparison_type == ComparisonType.PairComparison:
            self.auto_transition=False
    
        #self.video_player=LFIVideoPlayer(video_path,fps=self.fps,loop_times=self.loop_times)
        if exp_setting.passive_control_backend.upper()=='MPV':
            self.video_player=MPVVideoPlayer(video_path,fps=self.fps,loop_times=self.loop_times,auto_transition=self.auto_transition)
            self.video_player.OnFirstLoopFinished.connect(self.enableAllButtons)
            logger.info('passive control backend: MPV')
        elif exp_setting.passive_control_backend.upper()=='QT': # not fully tested. 
            self.video_player=MPVFramePlayer(video_path,fps=self.fps,loop_times=self.loop_times)
            logger.info('passive control backend: Qt')
        else:
            self.video_player=LFIVideoPlayer(video_path,fps=self.fps,loop_times=self.loop_times)
            logger.info('passive control backend: OpenCV')
        self.fps=self.video_player.fps

        self.video_player.setParent(self)

        self.video_height=self.video_player.video_height
        self.video_width=self.video_player.video_width

        self.arrow_key_flag=False

        self.video_path=video_path

        # two buttons for pair comparison and one single button for single/double stimuli/ous
        self.next_btn=QtWidgets.QPushButton("Next")
        self.next_btn.setParent(self)
        self.next_btn.hide()
        self.next_btn.clicked.connect(lambda: self.finish_video.emit())
        self.next_btn.setStyleSheet("QPushButton:{background-color: gray;}")

        self.left_btn=QtWidgets.QPushButton("Select Left")
        #self.left_btn.setStyleSheet("QPushButton:focus { background-color: yellow; }")
        self.left_btn.setStyleSheet("QPushButton:focus {border: 2px solid white;}")
        self.left_btn.setParent(self)
        self.left_btn.hide()
        self.left_btn.clicked.connect(lambda: self.pair_finished.emit(0))


        self.right_btn=QtWidgets.QPushButton("Select Right")
        self.right_btn.setParent(self)
        self.right_btn.setStyleSheet("QPushButton:focus {border: 2px solid white;}")
        self.right_btn.hide()
        self.right_btn.clicked.connect(lambda: self.pair_finished.emit(1))

        self.left_btn.setFocusPolicy(Qt.NoFocus)
        self.right_btn.setFocusPolicy(Qt.NoFocus)

        if self.auto_transition:
            self.video_player.OnVideoPlayerFinished.connect(self.FinishVideo)

        self.selected_one=0
        
        self.use_hint_text=(not exp_setting.first_loop_skip) and (exp_setting.skip_hint_text!="")
        
        if self.use_hint_text:
            self.SetSkipHintText(exp_setting.screen_width,exp_setting.skip_hint_text,exp_setting.hint_text_font_size)

        self.SetNewLFI(exp_setting,dist_lfi_info,video_path,self.comparison_type)
    
    def FinishVideo(self):
        if self.use_hint_text:
            self.hint_label_window.hide()
        self.finish_video.emit()
    
    def SetSkipHintText(self,screen_width,skip_hint_text,hint_text_font_size):
        self.skip_hint_text=skip_hint_text
        self.hint_label_window=QtWidgets.QWidget()
        self.hint_label_window.setAttribute(Qt.WA_TranslucentBackground)
        self.hint_label_window.setWindowFlag(Qt.FramelessWindowHint)
        self.hint_label_window.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.hint_label_window.keyPressEvent = self.handle_key_press

        self.skip_hint_label=QtWidgets.QLabel(self.skip_hint_text)
        font=QtGui.QFont()
        font.setPointSize(hint_text_font_size)
        self.skip_hint_label.setFont(font)
        self.skip_hint_label.setParent(self.hint_label_window)
        self.skip_hint_label.adjustSize()
        pos_x=(screen_width-self.skip_hint_label.width())//2
        pos_y=50

        self.hint_label_window.setGeometry(pos_x,pos_y,self.skip_hint_label.width(),self.skip_hint_label.height())
        self.skip_hint_label.setGeometry(0,0,self.skip_hint_label.width(),self.skip_hint_label.height())

        self.hint_label_window.setFocusPolicy(Qt.NoFocus)
        self.hint_label_window.hide()

    # TODO: Need a new class to describe the session   
    def SetNewLFI(self,exp_setting:ExpSetting,dist_lfi_info:ScoringExpLFIInfo, video_path,cmp_type=None):
        self.exp_setting=exp_setting
        if cmp_type is None:
            self.comparison_type=exp_setting.comparison_type
        else:
            self.comparison_type=cmp_type
        self.dist_lfi_info=dist_lfi_info
        self.video_path=video_path
        if self.use_hint_text:
            self.hint_label_window.hide()
        if not exp_setting.first_loop_skip:
            self.disableAllButtons()

        self.base_path=os.path.dirname(video_path)

        self.video_player.SetFPS(self.fps)
        self.video_player.setVideoPath(video_path)
        self.video_height=self.video_player.video_height
        self.video_width=self.video_player.video_width

        video_height=self.video_height
        video_width=self.video_width

        if dist_lfi_info is None:
            self.event_mask=ImageMask(video_height,video_width)
            self.screen_height,self.screen_width=exp_setting.screen_height,exp_setting.screen_width
            self.setGeometry(0,0,self.event_mask.screen_width,self.event_mask.screen_height)
            self.video_player.setGeometry(self.event_mask.screen_widget_x,self.event_mask.screen_widget_y,self.event_mask.widget_width,self.event_mask.widget_height)
        else:
            img_width=dist_lfi_info.img_width
            img_height=dist_lfi_info.img_height
            self.screen_height,self.screen_width=exp_setting.screen_height,exp_setting.screen_width
            self.event_mask=EventMask(img_height,img_width,exp_setting.lfi_features,exp_setting.comparison_type)

            self.setGeometry(0,0,self.event_mask.screen_width,self.event_mask.screen_height)
            self.video_player.setGeometry(self.event_mask.screen_widget_x,self.event_mask.screen_widget_y,self.event_mask.widget_width,self.event_mask.widget_height)

        btn_height=50
        btn_width=226
        btn_pos_y=(self.event_mask.screen_widget_y+video_height+self.event_mask.screen_height)//2 - btn_height//2

        if not exp_setting.two_folder_mode:
            if self.comparison_type == ComparisonType.PairComparison:
                left_btn_pos_x=3*self.event_mask.screen_width//8 - btn_width//2
                right_btn_pos_x=5*self.event_mask.screen_width//8 - btn_width//2

                self.left_btn.setGeometry(left_btn_pos_x,btn_pos_y,btn_width,btn_height)
                self.left_btn.show()
                self.right_btn.setGeometry(right_btn_pos_x,btn_pos_y,btn_width,btn_height)
                self.right_btn.show()
                #self.left_btn.setFocus()
            else:
                next_btn_pos_x=self.event_mask.screen_width//2 - btn_width//2
                self.next_btn.setGeometry(next_btn_pos_x,btn_pos_y,btn_width,btn_height)
                if not self.auto_transition:
                    self.next_btn.show()
                else:
                    self.next_btn.hide()

        self.video_player.show()
        if self.comparison_type == ComparisonType.PairComparison:
            self.arrow_key_flag=True
        
        if self.auto_play:
            time.sleep(self.auto_play_delay_time/1000)
            self.video_player.PlayVideo()

    def SetFPS(self,fps):
        self.fps=fps
        self.video_player.SetFPS(fps)

    def SetLoopPlay(self,loop_times=-1):
        self.loop_times=loop_times
        self.video_player.SetLoop(loop_times)

    def SetEventMask(self, event_mask:EventMask):
        self.event_mask=event_mask
        
    def mousePressEvent(self, event) -> None:
        if self.pause_allowed:
            self.video_player.toogle_play_pause()
        if self.use_hint_text:
            if self.hint_label_window.isVisible():
                self.hint_label_window.raise_()
        #return super().mousePressEvent(event)

    def disableAllButtons(self):
        self.left_btn.setEnabled(False)
        self.right_btn.setEnabled(False)
        self.next_btn.setEnabled(False)
        self.evaluate_enable=False
        if self.use_hint_text:
            self.hint_label_window.hide()
    
    def enableAllButtons(self):
        logger.debug('now you can skip')
        #print(f'self.skip_hint_label geometry: {self.skip_hint_label.geometry()}')
        self.left_btn.setEnabled(True)
        self.right_btn.setEnabled(True)
        self.next_btn.setEnabled(True)
        self.evaluate_enable=True
        if self.use_hint_text:
            self.hint_label_window.show()
            self.setFocus()
    
    def handle_key_press(self, event) -> None:
    #def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        event.ignore()
        if self.comparison_type == ComparisonType.PairComparison:
            '''
            if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
                if self.left_btn.hasFocus():
                    self.pair_finished.emit(0)
                    return
                else:
                    self.pair_finished.emit(1)
                    return
            '''
            if not self.evaluate_enable:
                return 
            if event.key() == Qt.Key_Left:
                self.video_player.StopPlaying()
                self.pair_finished.emit(0)
                return
            if event.key() == Qt.Key_Right:
                self.video_player.StopPlaying()
                self.pair_finished.emit(1)
                return
            if event.key() == Qt.Key_Down:
                self.video_player.StopPlaying()
                self.pair_finished.emit(2)
                return
        else:
            if not self.evaluate_enable:
                return
            if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
                self.video_player.StopPlaying()
                if self.use_hint_text:
                    self.hint_label_window.hide()
                self.finish_video.emit()
        #return super().keyPressEvent(event)
    
    def CloseVideoPlayer(self):
        self.video_player.StopPlaying()
        if self.use_hint_text:
            self.hint_label_window.hide()
            self.hint_label_window.deleteLater()
    '''
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
    
    # Abandon the use of enter now. 
    # interaction operation has been changed.
    '''

class ScoringPage(QtWidgets.QWidget):
    HasScored=QtCore.Signal(list)

    def __init__(self,screen_height,screen_width,table_names=["Picture Quality","Overall Quality"],scoring_levels=[5,5],scoring_definition=None,score_values=None,font_size=PathManager.scoring_table_point_size) -> None:
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setGeometry(0,0,screen_width,screen_height)
        self.setStyleSheet("background-color:gray;")
        self.table_names=table_names
        self.current_focus_index=0
        self.all_table=[]
        self.all_table_list=list(range(len(self.table_names)))

        table_num=len(table_names)
        for table_index in range(len(self.table_names)):
            table_name=self.table_names[table_index]
            if scoring_definition is not None:
                cur_table_definition=scoring_definition[table_index]
            else:
                cur_table_definition=None
            if score_values is not None:
                cur_score_values=score_values[table_index]
            else:
                cur_score_values=None
            cur_table=ScoringTable(table_name,scoring_levels[table_index],scoring_definition=cur_table_definition,score_values=cur_score_values,font_size=font_size)

            cur_table.setParent(self)
            table_center_x= (2*table_index+1)*screen_width//(2*table_num)
            table_center_y=screen_height//2

            table_upper_left_x=table_center_x-cur_table.widget_width//2
            table_upper_left_y=table_center_y-cur_table.widget_height//2
            cur_table.setGeometry(table_upper_left_x,table_upper_left_y,cur_table.widget_width,cur_table.widget_height)
            cur_table.show()
            self.all_table.append(cur_table)

        for i in range(len(self.all_table)):
            self.all_table[i].table_index=i
            self.all_table[i].be_clicked.connect(lambda i: self.SetSingleFocusedTable(i))
        
        self.next_btn=QtWidgets.QPushButton("Next",self)
        btn_height=PathManager.btn_height
        btn_width=PathManager.btn_width
        btn_pos_x=(screen_width-btn_width)//2

        if table_num%2==0:
            left_index=table_num//2
            left_y=(screen_height + self.all_table[left_index].widget_height)//2
            btn_pos_y=(left_y+screen_height)//2-btn_height//2
        else:
            mid_index=(table_num-1)//2
            table_bottom_y=(screen_height + self.all_table[mid_index].widget_height)//2
            btn_pos_y=(table_bottom_y+screen_height)//2-btn_height//2
        
        self.next_btn.setGeometry(btn_pos_x,btn_pos_y,btn_width,btn_height)
        self.next_btn.clicked.connect(self.ReturnScores)
        self.next_btn.show()

    def RefreshAllTables(self):
        '''
        used to remove scoring bias during sequential evaluation 
        '''
        for scoring_table in self.all_table:
            scoring_table.RefreshTable()
        self.SetSingleFocusedTable(0)
    
    def GetScores(self):
        return [self.all_table[i].GetResult() for i in self.all_table_list]
    
    def ReturnScores(self):
        self.HasScored.emit(self.GetScores())

    '''
    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() ==  Qt.Key_Right:
            self.current_focus_index=(self.current_focus_index+1)%len(self.all_table)
        if event.key() == Qt.Key_Left:
            self.current_focus_index=(self.current_focus_index-1)%len(self.all_table)
        self.SetSigleFocusedTable(self.current_focus_index)
        return super().keyPressEvent(event)
    '''

    def handle_key_press(self, event: QtGui.QKeyEvent) -> None:
        event.ignore()
        if event.key() ==  Qt.Key_Right:
            self.current_focus_index=(self.current_focus_index+1)%len(self.all_table)
            self.SetSingleFocusedTable(self.current_focus_index)
        if event.key() == Qt.Key_Left:
            self.current_focus_index=(self.current_focus_index-1)%len(self.all_table)
            self.SetSingleFocusedTable(self.current_focus_index)
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.ReturnScores()
        #return super().keyPressEvent(event)
    
    def SetSingleFocusedTable(self,focus_i):
        for index in range(len(self.all_table)):
            if index == focus_i:
                self.all_table[index].SetMyFocused(True)
                self.current_focus_index=index
            else:
                self.all_table[index].SetMyFocused(False)
    
class ScoringBtn(QtWidgets.QRadioButton):
    def __init__(self,btn_score=0,btn_index=0):
        super().__init__()
        '''
        Index and score may not be the same. 
        '''
        self.btn_index=btn_index
        self.btn_score=btn_score
    
    def GetIndex(self):
        return self.btn_index
    def GetScore(self):
        return self.btn_score

class ScoringTable(QtWidgets.QWidget):
    be_clicked=QtCore.Signal(int)

    def __init__(self,widget_name,scoring_levels=5,scoring_definition=None,score_values=None,font_size=PathManager.scoring_table_point_size) -> None:
        super().__init__()
        self.widget_name=widget_name
        self.table_index=0
        self.scoring_levels=scoring_levels
        self.input_score_values=score_values
        self.font_size=font_size

        self.cur_radio_score=0
        self.cur_radio_index=0
        self.all_radio_index=list(range(scoring_levels))
        self.all_radio_score=[]
        self.radio_score_dict={}

        self.score_definition=scoring_definition

        self.scoring_name=QtWidgets.QGroupBox(self)
        #self.scoring_name.setTitle(widget_name)
        self.vertical_layout_widget=QtWidgets.QWidget(self.scoring_name)

        self.table_title=QtWidgets.QLabel(self)

        #self.SetTableSize()

        self.vertical_layout_box=QtWidgets.QVBoxLayout(self.vertical_layout_widget)
        self.vertical_layout_box.setSpacing(PathManager.table_spaceing)
        self.vertical_layout_box.setContentsMargins(0,0,0,10)

        self.all_radio_btns=[]
        '''
        TODO: Allow a custom score definition
        '''
        for i in range(self.scoring_levels):
            radio_index=i
            radio_score=self.GetBtnScore(i)
            radio_button=ScoringBtn(btn_index=radio_index,btn_score=radio_score)
            self.all_radio_score.append(radio_button.btn_score)
            self.radio_score_dict[radio_score]=radio_button
            radio_button.setParent(self.vertical_layout_widget)
            if scoring_definition is not None:
                radio_button.setText(scoring_definition[i])
            else:
                radio_button.setText("Score: "+str(radio_score))
            radio_button.clicked.connect(lambda: self.RadioBtnClicked())
            self.vertical_layout_box.addWidget(radio_button)
            self.all_radio_btns.append(radio_button)
        
        self.cur_radio_score=self.all_radio_btns[self.cur_radio_index].btn_score
        self.select_box_width=0
        self.select_box_height=0
        self.select_box_pos_x=0
        self.select_box_pos_y=0
        self.SetTableSize()
        
        self.all_radio_btns[0].setChecked(True) 

        self.border_label=QtWidgets.QLabel(self)
        self.border_label.setGeometry(self.select_box_pos_x,self.select_box_pos_y,self.select_box_width,self.select_box_height)
        self.setFocusPolicy(Qt.StrongFocus)
        self.border_label.setStyleSheet("border:3px dotted white;")
        self.border_label.hide()

        self.border_label.raise_()
        self.scoring_name.raise_()
    
    def GetBtnScore(self,i):
        '''
        TODO: use input from configuration file
        '''
        if self.input_score_values is not None:
            return self.input_score_values[i]
        else:
            return self.scoring_levels-i

    
    def GetClickedRadioBtn(self):
        for radio_btn in self.all_radio_btns:
            if radio_btn.isChecked():
                self.cur_radio_index=radio_btn.btn_index
                return radio_btn.btn_score

    def RadioBtnClicked(self):
        self.cur_radio_score=self.GetClickedRadioBtn()
        self.be_clicked.emit(self.table_index)
    
    def SetTableSize(self):
        #calculate the table size here
        self.setStyleSheet('color: black;')
        font=PySide6.QtGui.QFont()
        font.setPointSize(self.font_size)
        single_radio_btn_width=0
        for r_btn in self.all_radio_btns:
            r_btn.setFont(font)
            r_btn.adjustSize()
            if r_btn.width()>single_radio_btn_width:
                single_radio_btn_width=r_btn.width()

        single_radio_btn_height=PathManager.scoring_btn_height

        #single_radio_btn_width=Pathanager.scoring_btn_width
        group_box_pos_x=PathManager.table_horizontal_gap

        talbe_spacing=PathManager.table_spaceing

        vertical_layout_widget_height=40+single_radio_btn_height*self.scoring_levels+(self.scoring_levels)*talbe_spacing+2*PathManager.talbe_vertical_gap
        vertical_layout_widget_width=10+single_radio_btn_width

        group_box_height=2*PathManager.talbe_vertical_gap + vertical_layout_widget_height
        group_box_width= 2* PathManager.table_horizontal_gap + vertical_layout_widget_width

        self.select_box_width = group_box_width + 2* PathManager.table_horizontal_gap
        self.select_box_height=group_box_height+2*PathManager.talbe_vertical_gap 
        self.select_box_pos_x = 0

        self.widget_width=group_box_width+2*PathManager.table_horizontal_gap +10 

        title_width = self.widget_width
        title_width = max(title_width,PathManager.scoring_table_width+2*PathManager.table_horizontal_gap)

        if self.widget_width<title_width:
            delta=(title_width-self.widget_width)//2
            self.widget_width=title_width
            group_box_pos_x+=delta
            self.select_box_pos_x+=delta

        title_pos_y=0 #PathManager.talbe_vertical_gap
        title_pos_x=0
        self.table_title.setWordWrap(True)
        self.table_title.setText(self.widget_name)
        self.table_title.setFont(font)
        self.table_title.setFixedWidth(title_width)
        self.table_title.setAlignment(Qt.AlignCenter)
        self.table_title.adjustSize()
        title_height= self.table_title.height()
        title_width = self.table_title.width()
        self.table_title.setGeometry(title_pos_x,title_pos_y,title_width,title_height)

        group_box_pos_y=PathManager.talbe_vertical_gap *2 + title_height
        self.select_box_pos_y = PathManager.talbe_vertical_gap  +title_height


        self.widget_height=group_box_height+2*PathManager.talbe_vertical_gap + title_height +PathManager.talbe_vertical_gap
        self.resize(self.widget_width,self.widget_height)

        self.scoring_name.setGeometry(group_box_pos_x,group_box_pos_y,group_box_width,group_box_height)
        self.scoring_name.setTitle('')
        self.scoring_name.setFont(font)
        self.scoring_name.setFocusPolicy(Qt.StrongFocus)

        self.vertical_layout_widget.setGeometry(PathManager.table_horizontal_gap,PathManager.talbe_vertical_gap,vertical_layout_widget_width,vertical_layout_widget_height)

    def GetResult(self):
        return self.cur_radio_score
    
    def keyPressEvent(self, event) -> None:
        event.ignore()
        if event.key() == Qt.Key_Up:
            self.cur_radio_index=self.all_radio_index[self.cur_radio_index-1]
            self.cur_radio_score=self.all_radio_btns[self.cur_radio_index].btn_score
            self.all_radio_btns[self.cur_radio_index].setChecked(True)
            return super().keyPressEvent(event)
        if event.key() ==  Qt.Key_Down:
            self.cur_radio_index=self.all_radio_index[self.cur_radio_index+1-self.scoring_levels]
            self.cur_radio_score=self.all_radio_btns[self.cur_radio_index].btn_score
            self.all_radio_btns[self.cur_radio_index].setChecked(True)
            return super().keyPressEvent(event)

        key_num=self.GetKeyNum(event.key())
        if key_num in self.all_radio_score:
            self.cur_radio_score=key_num
            self.radio_score_dict[key_num].setChecked(True)
            self.cur_radio_index=self.radio_score_dict[key_num].btn_index
            return super().keyPressEvent(event)
    
    def GetKeyNum(self,in_key):
        if in_key == Qt.Key_1:
            return 1
        if in_key == Qt.Key_2:
            return 2
        if in_key == Qt.Key_3:
            return 3
        if in_key == Qt.Key_4:
            return 4
        if in_key == Qt.Key_5:
            return 5
        if in_key == Qt.Key_6:
            return 6
        if in_key == Qt.Key_7:
            return 7
        if in_key == Qt.Key_8:
            return 8
        if in_key == Qt.Key_9:
            return 9
        return None
    
    def mousePressEvent(self, event) -> None:
        self.be_clicked.emit(self.table_index)
        return super().mousePressEvent(event)

    def SetMyFocused(self,bfocus):
        if bfocus:
            self.setFocus()
            self.border_label.show()
        else:
            self.border_label.hide()
    
    def RefreshTable(self):
        for i in range(self.scoring_levels):
            self.all_radio_btns[i].setChecked(False)
        self.all_radio_btns[0].setChecked(True)
        self.cur_radio_index=0
        self.cur_radio_score=self.all_radio_btns[0].btn_score

def PrintVideoPage(a):
    print(a)

def VideoFinishPage():
    print("Video finished!")

def PrintScores(in_list):
    print("all the scores: ")
    print(in_list)

if __name__ == "__main__":
    app = QtWidgets.QApplication()
    #scoring_widget = ScoringPage(1440,2560)
    #scoring_widget.HasScored.connect(lambda x:print(x))
    #scoring_widget.show()

    screen = QtWidgets.QApplication.primaryScreen()
    finish_widget=FinishPage(screen.size().width(),screen.size().height())

    finish_widget.SetLabelContent("The DSCS session has been finished.\n Please press ESC to escape this session and have a rest.\n The next session will start after the rest.")
    finish_widget.setGeometry(0,0,screen.size().width(),screen.size().height())

    finish_widget.show()

    '''
    screen = QtWidgets.QApplication.primaryScreen()
    blank_widget=BlankScoringWidget(screen_height=screen.size().height(),screen_width=screen.size().width())

    blank_widget.show()

    screen = QtWidgets.QApplication.primaryScreen()
    scoring_definition=[['lasdjf;lajsdl;fkjaskl;dfja;l','Score: 2','Score: 3','Score: 4','Score: 5'],['Score: 1','Score: 2','Score: 3','Score: 4','Score: 5']]
    score_page=ScoringPage(screen.size().height(),screen.size().width(),table_names=['Image Quality','It is a very very long long long name'],scoring_definition=scoring_definition)

    score_page.HasScored.connect(PrintScores)
    score_page.show()

    '''
    '''
    locale.setlocale(locale.LC_NUMERIC, 'C')
    exp_setting=ExpSetting()
    exp_setting.comparison_type=ComparisonType.DoubleStimuli
    exp_setting.passive_control_backend="MPV"
    exp_setting.fps=30
    exp_setting.pause_allowed=True
    exp_setting.loop_times=3
    exp_setting.auto_transition=True
    exp_setting.auto_play=True
    exp_setting.skip_hint_text="You can skip the video by pressing Enter now."
    exp_setting.table_font_size=50

    video_path='/data_0/shengyang/Work/JPEG/LFIQA/examples/two_folder/foo_1/1.mp4'
    #video_path='C:/Users/ZSY/Downloads/examples/two_folder/foo_1/1.mp4'
    video_page=VideoPage(exp_setting,None,video_path)

    video_page.pair_finished.connect(PrintVideoPage)
    video_page.finish_video.connect(VideoFinishPage)

    video_page.show()
    '''

    '''
    scoring_definition=[['Score: -3 ','Score: -2','Score: -1','Score: 0','Score: 1','Score: 2','Score: 3'],['Score: 5','Score: 4','Score: 3','Score: 2','Score: 1']]
    screen = QtWidgets.QApplication.primaryScreen()
    score_values=[[-3,-2,-1,0,1,2,3],[5,4,3,2,1]]
    score_page=ScoringPage(screen.size().height(),screen.size().width(),scoring_levels=[7,5], table_names=['Image Quality','It is a very very long long long name'],scoring_definition=scoring_definition,score_values=score_values,font_size=exp_setting.table_font_size)

    score_page.HasScored.connect(PrintScores)
    score_page.show()#FullScreen()
    '''
    #video_path='/home/heathcliff/Documents/1.mov'

    sys.exit(app.exec())