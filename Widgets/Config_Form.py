import os
import sys

import PySide6.QtGui
sys.path.append('../UI')
sys.path.append('../Widgets/')
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Signal, Slot
from PySide6.QtCore import QRect
from PySide6.QtWidgets import QWidget,QMessageBox, QInputDialog
from NewExperiment_ui import Ui_NewExperimentForm as NewExperimentForm
from LFIGroupBox_ui import Ui_LFIGroupWidget
from ExpInfo import *
import pickle
import PreProcess
import logging
logger=logging.getLogger("LogWindow")


class LFIGroupBox(QtWidgets.QWidget,Ui_LFIGroupWidget,QtCore.QObject):
    return_signal=Signal(int)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.isVisible=True
        self.btn_del.clicked.connect(self.DeleteSelfLater)
        self.box_index=0
        self.button_select_ori.clicked.connect(lambda: self.GetFilePath(self.line_editor_ori))
        self.button_select_dist.clicked.connect(lambda: self.GetFilePath(self.line_editor_dist))

    def DeleteSelfLater(self):
        try:
            self.return_signal.emit(self.box_index)
        except:
            pass
        self.deleteLater()
    
    def GetLFIType(self):
        if self.radio_btn_dense.isChecked():
            return LFITypes.Dense
        if self.radio_btn_sparse.isChecked():
            return LFITypes.Sparse
        return LFITypes.Dense
    
    def GetFilePath(self,line_editor):
        director_select=QtWidgets.QFileDialog.getExistingDirectory(self)
        line_editor.setText(director_select)

# The configuration contains 3 parts:
# 1. The training part
# 2. The testing part
# 3. The experiment information
class CreateNewExperiment(QtWidgets.QWidget,NewExperimentForm):
    CancelClosed = Signal()
    Finished = Signal(bool,str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.current_page_index=0
        self.ConfigStackWidget.setCurrentIndex(self.current_page_index)

        self.output_folder_root=None

        # page 0
        self.page_0_btn_cancel.clicked.connect(self.CancelClose)
        self.page_0_btn_next.clicked.connect(self.Page0Next)
        self.btn_select_json.clicked.connect(lambda: self.SelectFile(self.page_0_json_path))

        #####
        self.lfi_margin_x=10
        self.lfi_margin_y=0

        # page 1: training page
        self.ConfigScrollAreaTrain.setWidgetResizable(False)

        self.training_all_lfi_boxes = []
        self.training_lf_box_num=0

        self.training_all_lfi_info=None
        self.training_angular_format=AngularFormat.XY

        self.page_1_btn_add_group.clicked.connect(lambda: self.AddLFIBox(self.scrollAreaWidgetContents_training,self.training_all_lfi_boxes,self.LFILayout_training))
        self.page_1_btn_cancel.clicked.connect(self.CancelClose)
        self.page_1_btn_next.clicked.connect(self.MakeTrainingLFInfo)
        self.page_1_btn_prev.clicked.connect(self.StackPrev)

        # page 2: test page
        self.ConfigScrollAreaTest.setWidgetResizable(False)

        self.test_all_lfi_boxes = []
        self.test_all_lfi_boxes=[]
        self.test_lf_box_num=0
        
        self.test_all_lfi_info=None
        self.test_angular_format=AngularFormat.XY

        self.page_2_btn_add_group.clicked.connect(lambda: self.AddLFIBox(self.scrollAreaWidgetContents_test,self.test_all_lfi_boxes,self.LFILayout_test))
        self.page_2_btn_cancel.clicked.connect(self.CancelClose)
        self.page_2_btn_next.clicked.connect(self.MakeTestLFInfo)
        self.page_2_btn_prev.clicked.connect(self.StackPrev)

        # page 3
        #self.ConfigStackWidget.setCurrentIndex(3)
        self.label_3d_ns.setAutoFillBackground(True)
        self.label_3d_ns.hide()

        self.button_group_display_type=QtWidgets.QButtonGroup(self)
        self.button_group_display_type.setExclusive(True)
        self.button_group_display_type.addButton(self.radio_btn_disp_2D,int(LFIFeatures.TwoD))
        self.button_group_display_type.addButton(self.radio_btn_disp_3D_LR,int(LFIFeatures.Stereo_horizontal))
        self.button_group_display_type.addButton(self.radio_btn_disp_3D_full,int(LFIFeatures.Stereo_full))
        self.radio_btn_disp_2D.setChecked(True)
        self.radio_btn_disp_3D_full.setCheckable(False)
        self.radio_btn_disp_3D_full.pressed.connect(lambda: self.label_3d_ns.show())
        self.radio_btn_disp_3D_full.released.connect(lambda: self.label_3d_ns.hide())

        self.button_group_view_change=QtWidgets.QButtonGroup(self)
        self.button_group_view_change.addButton(self.radio_btn_view_change_passive,int(LFIFeatures.Passive_ViewChanging))
        self.button_group_view_change.addButton(self.radio_btn_view_change_active,int(LFIFeatures.Active_ViewChanging))
        self.button_group_view_change.addButton(self.radio_btn_view_change_none,int(LFIFeatures.None_ViewChanging))
        self.button_group_view_change.setExclusive(True)
        self.radio_btn_view_change_active.setChecked(True)
        
        self.button_group_refocusing=QtWidgets.QButtonGroup(self)
        self.button_group_refocusing.addButton(self.radio_btn_refocusing_passive,int(LFIFeatures.Passive_Refocusing))
        self.button_group_refocusing.addButton(self.radio_btn_refocusing_active,int(LFIFeatures.Active_Refocusing))
        self.button_group_refocusing.addButton(self.radio_btn_refocusing_none,int(LFIFeatures.None_Refocusing))
        self.button_group_refocusing.setExclusive(True)
        self.radio_btn_refocusing_active.setChecked(True)
        
        self.button_group_cmp_type=QtWidgets.QButtonGroup(self)
        self.button_group_cmp_type.addButton(self.radio_btn_cmp_double,int(ComparisonType.DoubleStimuli))
        self.button_group_cmp_type.addButton(self.radio_btn_cmp_single,int(ComparisonType.SingleStimuli))
        self.button_group_cmp_type.addButton(self.radio_btn_cmp_pair,int(ComparisonType.PairComparison))
        self.btn_pair_line_editor.clicked.connect(lambda: self.GetFilePath(self.pair_line_editor,"*.json"))
        self.button_group_cmp_type.setExclusive(True)
        self.radio_btn_cmp_double.setChecked(True)

        self.button_group_save_format=QtWidgets.QButtonGroup(self)
        self.button_group_save_format.addButton(self.radio_btn_save_csv,int(SaveFormat.CSV))
        self.button_group_save_format.addButton(self.radio_btn_save_excel,int(SaveFormat.Excel))
        self.radio_btn_save_csv.setChecked(True)
        self.button_group_save_format.setExclusive(True)
         
        self.page_3_btn_cancel.clicked.connect(self.CancelClose)
        self.page_3_btn_prev.clicked.connect(self.StackPrev)
        self.page_3_btn_finish.clicked.connect(self.FinishConfig)
    
    def ShowNotice(self):
        current_mouse_pos=QtGui.QCursor.pos()
        self.label_3d_ns.setGeometry(QRect(current_mouse_pos.x(),current_mouse_pos.y(),self.label_3d_ns.width(),self.label_3d_ns.height()))
        self.label_3d_ns.show()
        
    def FinishConfig(self):
        if self.radio_btn_refocusing_none.isChecked() and self.radio_btn_view_change_none.isChecked():
            self.ShowMessage("You must select at least one feature!",2)
            logger.error("In config experiment settings, you must select at least one feature!")
            return 
        project_post_fix='lfqoe'
        self.project_post_fix=project_post_fix
        save_name=self.GetProjectName()
        if save_name is None:
            self.ShowMessage("Invalid name! Please check the name again!",2)
            logger.error("Invalid name! Please check the saving name of the project!")
            return
        
        disp_type=LFIFeatures(self.button_group_display_type.checkedId())
        view_change_type=LFIFeatures(self.button_group_view_change.checkedId())
        refocusing_type=LFIFeatures(self.button_group_refocusing.checkedId())
        cmp_type=ComparisonType(self.button_group_cmp_type.checkedId())
        pair_wise_path=self.pair_line_editor.text()
        save_format_type=SaveFormat(self.button_group_save_format.checkedId())

        all_lfi_features=[disp_type,view_change_type,refocusing_type]
        if LFIFeatures.Active_Refocusing in all_lfi_features or LFIFeatures.Passive_Refocusing in all_lfi_features:
            all_lfi_features.append(LFIFeatures.Refocusing)

        exp_setting=ExpSetting(all_lfi_features,cmp_type,save_format_type)
        exp_setting.pair_wise_config=pair_wise_path
        self.exp_setting=exp_setting

        if self.output_folder_root is not None:
            project_info=ProjectInfo(save_name,self.output_folder_root)
        else:
            project_info=ProjectInfo(save_name)
        project_info.SetParameters(self.training_all_lfi_info,self.test_all_lfi_info,exp_setting)
        project_info.SaveToFile()
        
        self.Finished.emit(False,save_name)

        self.deleteLater()
        
    def GetProjectName(self):
        project_name, ok = QtWidgets.QInputDialog.getText(self, 'Project Name', 'Please input the project name:')
        if ok:
            return project_name
        else:
            logger.error("The project name can not be empty!")
            return None

    def GetSaveFileName(self):
        file_selected=QtWidgets.QFileDialog.getSaveFileName(self)
        file_selected=file_selected[0]
        if file_selected=="":
            return None
        else:
            return file_selected

    def GetFilePath(self,line_editor,in_filter="*.txt"):
        file_selected=QtWidgets.QFileDialog.getOpenFileName(self,filter=in_filter)
        file_selected=file_selected[0]
        line_editor.setText(file_selected)

    def MakeTrainingLFInfo(self):
        if self.training_radio_btn_xy.isChecked():
            self.training_angular_format=AngularFormat.XY
        else:
            self.training_angular_format=AngularFormat.HW
        self.training_all_lfi_info=self.GetAllLFIInfo(self.training_all_lfi_boxes,self.training_angular_format) 
        self.StackNext()
    
    def MakeTestLFInfo(self):
        if self.test_radio_btn_xy.isChecked():
            self.test_angular_format=AngularFormat.XY
        else:
            self.test_angular_format=AngularFormat.HW
        self.test_all_lfi_info=self.GetAllLFIInfo(self.test_all_lfi_boxes,self.test_angular_format)
        self.StackNext()

    def StackNext(self):
        self.current_page_index+=1
        self.ConfigStackWidget.setCurrentIndex(self.current_page_index)
    
    def StackPrev(self):
        self.current_page_index-=1
        self.ConfigStackWidget.setCurrentIndex(self.current_page_index)
    
    def closeEvent(self, event) -> None:
        self.CancelClosed.emit()
        self.deleteLater()
        
    def CancelClose(self):
        logger.warning("Configuring cancelled...")
        self.CancelClosed.emit()
        self.deleteLater()
        
    def Page0Next(self):
        if self.radio_btn_json.isChecked():
            json_path=self.page_0_json_path.text()
            ret_info=self.ConfigFromJson(json_path)
            if ret_info[0]:
                self.SaveJsonConfig()
            else:
                dlg=QMessageBox(self)
                dlg.setWindowTitle("Warning!")
                dlg.setStandardButtons(QMessageBox.Ok)
                dlg.setIcon(QMessageBox.Warning)
                dlg.setText(ret_info[1])
                dlg.exec()
    
    def SaveJsonConfig(self):
        project_post_fix='lfqoe'
        self.project_post_fix=project_post_fix
        save_name=self.GetProjectName()
        if save_name is None:
            logger.error("Invalid name! Please check the saving path of the project!")
            self.ShowMessage("Invalid path! Please check the path again!",2)
            return

        if self.output_folder_root is not None:
            project_info=ProjectInfo(save_name,self.output_folder_root) 
        else:
            project_info=ProjectInfo(save_name)


        project_info.SetParameters(self.training_all_lfi_info,self.test_all_lfi_info,self.exp_setting)
        project_info.SaveToFile()

        self.Finished.emit(False,save_name)

        self.deleteLater()
        
    def ShowMessage(self,message_text,message_mode):
        '''
        message_mode: 0: info 1: warning  2: error
        '''
        dlg=QMessageBox(self)
        dlg.setStandardButtons(QMessageBox.Ok)
        if message_mode==0:
            dlg.setWindowTitle("Notice")
            dlg.setIcon(QMessageBox.Information)
        elif message_mode==1:
            dlg.setWindowTitle("Warning!")
            dlg.setIcon(QMessageBox.Warning)
        else:
            dlg.setWindowTitle("Error!")
            dlg.setIcon(QMessageBox.Critical)
        dlg.setText(message_text)
        dlg.exec()
    
    def OptionDialog(self,question):
        dlg=QMessageBox(self)
        dlg.setWindowTitle("Notice")
        dlg.setText(question)
        dlg.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        dlg.setIcon(QMessageBox.Question)
        
        button=dlg.exec()
        if button==QMessageBox.Yes:
            return True
        else:
            return False
    
    def SelectFile(self,line_editor):
        self.radio_btn_json.setChecked(True)
        file_dialog=QtWidgets.QFileDialog(self)
        file_dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptMode.AcceptOpen)
        file_dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("*.json") 
        file_dialog.fileSelected.connect(lambda path: line_editor.setText(path))
        file_dialog.open()
            
    def ConfigFromJson(self,config_path):
        if config_path=="" or not os.path.exists(config_path):
            logger.error("Invalid path! Please Check the Json Path again!")
            return False , "Invalid path! Please Check the Json Path again!"
        '''
        config with json here 
        '''
        with open(config_path,'r') as fid:
            all_config=json.load(fid)
        
        if "Training" not in all_config.keys():
            logger.error("Invalid json! There should be a Training key to config the training!")
            return False, "Invalid json! There should be a Training key to config the training!"
        if "Test" not in all_config.keys():
            logger.error("Invalid json! There should be a Test key to config the training!")
            return False, "Invalid json! There should be a Test key to config the training!"
        if "Exp_Info" not in all_config.keys():
            logger.error("Invalid json! There should be an Exp_Info key to config the experiment!")
            return False, "Invalid json! There should be an Exp_Info key to config the experiment!"
        training_lfi_config=all_config['Training']
        test_lfi_config=all_config['Test']
        exp_setting_config=all_config['Exp_Info']

        self.exp_setting=self.GetConfigExpSetting(exp_setting_config)
        if self.exp_setting is None:
            logger.error("Invalid json! For refocusing and view-changing features, at least you need to choose one of them!")
            return False, "Invalid json! For refocusing and view-changing features, at least you need to choose one of them!"

        skip_preprocessing=exp_setting_config["Skip_Preprocessing"]

        if self.exp_setting.two_folder_mode:
            skip_preprocessing=True
            training_lfi_info=self.TwoFolderConfiguration(training_lfi_config)
            test_lfi_info=self.TwoFolderConfiguration(test_lfi_config)
        else:
            training_lfi_info=self.GetConfigInfoWithSpecificJson(training_lfi_config)
            test_lfi_info=self.GetConfigInfoWithSpecificJson(test_lfi_config)
        if skip_preprocessing:
            self.exp_setting.has_preprocess=True

        self.training_all_lfi_info=training_lfi_info
        self.test_all_lfi_info=test_lfi_info

        return True,None

    def TwoFolderConfiguration(self,all_lfi_config):
        if not isinstance(all_lfi_config,str):
            logger.error("For the two folders configuration, the input should be a string!")
            return None
        all_lfi_config=TwoFolderLFIInfo(all_lfi_config,self.exp_setting.VideoSaveTypeStr)
        return all_lfi_config
    
    def GetConfigInfoWithSpecificJson(self,all_lfi_config):
        skip_preprocessing=self.exp_setting.skip_preprocessing
        if len(all_lfi_config) == 0:
            logger.warning("A blank configuration!")
            return None
        angular_format=all_lfi_config[0]["Angular_Format"]
        if angular_format == "HW":
            angular_format=AngularFormat.HW
        else:
            angular_format=AngularFormat.XY
        all_lfi_info=ExpLFIInfo(angular_format=angular_format)

        for lif_config in all_lfi_config:
            spatial_height=lif_config["Height"]
            spatial_width=lif_config["Width"]
            angular_height=lif_config["Angular_Height"]
            angular_width=lif_config["Angular_Width"]
            spatial_size=(spatial_height,spatial_width)
            angular_size=(angular_height,angular_width)

            lf_type=lif_config["Type"]
            lfi_angular_format=lif_config["Angular_Format"]
            if lfi_angular_format == "HW":
                lfi_angular_format=AngularFormat.HW
            else:
                lfi_angular_format=AngularFormat.XY
            lfi_name=lif_config["Name"]

            SRC_path=lif_config["SRC"]
            if SRC_path is not None or SRC_path != "":
                all_lfi_info.AddOriginLF(lfi_name,lf_type,lfi_angular_format,spatial_size,angular_size,SRC_path)
            
            all_dist_lfi=lif_config["HRC"]
            for dist_lfi in all_dist_lfi:
                cur_dist_type=dist_lfi["Distortion_Type"]
                cur_dist_level=dist_lfi["Distortion_Level"]
                cur_dist_path=dist_lfi["Distortion_Path"]
                all_lfi_info.AddSingleLFIInfo(lfi_name,lf_type,lfi_angular_format,spatial_size,angular_size,cur_dist_type,cur_dist_level,cur_dist_path,skip_preprocessing,self.exp_setting.comparison_type)

            return all_lfi_info

    def GetConfigAllLFIInfoWithoutPreprocessing(self,all_lfi_config):
        if len(all_lfi_config) == 0:
            return None
        angular_format=all_lfi_config[0]["Angular_Format"]
        if angular_format == "HW":
            angular_format=AngularFormat.HW
        else:
            angular_format=AngularFormat.XY
        all_lfi_info=ExpLFIInfo(angular_format=angular_format)

        for lfi_config in all_lfi_config:
            spatial_height=lfi_config["Height"]
            spatial_width=lfi_config["Width"]
            angular_height=lfi_config["Angular_Height"]
            angular_width=lfi_config["Angular_Width"]
            spatial_size=(spatial_height,spatial_width)
            angular_size=(angular_height,angular_width)

            SRC_path=lfi_config["SRC"]
            
            in_path=lfi_config["Input_Folder"]
            lf_type=lfi_config["Type"]
            lfi_angular_format=lfi_config["Angular_Format"]
            if lfi_angular_format=="HW":
                lfi_angular_format=AngularFormat.HW
            else:
                lfi_angular_format=AngularFormat.XY
            lfi_name=lfi_config["Name"]
            all_lfi_info.AddLFIInfo(lfi_name,lf_type,lfi_angular_format,spatial_size,angular_size,in_path)
        return all_lfi_info

    def GetConfigExpSetting(self,exp_config):
        exp_keys=list(exp_config.keys())
        disp_type=exp_config["Display_Type"]
        threed_type=exp_config["ThreeD_Type"]
        view_change_type=exp_config["View_Changing"]
        refocusing_type=exp_config["Refocusing"]
        cmp_type=exp_config["Comparison"]
        save_format_type=exp_config["Save_Format"]

        all_lfi_features=[]

        disp_type=disp_type.lower()
        threed_type=threed_type.lower()
        if disp_type == '2d':
            all_lfi_features.append(LFIFeatures.TwoD)
        if disp_type == '3d':
            if threed_type == "lr" or threed_type =="leftright":
                all_lfi_features.append(LFIFeatures.Stereo_horizontal)

        view_change_type=view_change_type.lower()
        if view_change_type == "active":
            all_lfi_features.append(LFIFeatures.Active_ViewChanging) 
        if view_change_type == "passive":
            all_lfi_features.append(LFIFeatures.Passive_ViewChanging)
        if view_change_type == "none":
            all_lfi_features.append(LFIFeatures.None_ViewChanging)
        
        refocusing_type=refocusing_type.lower()
        if refocusing_type == "active":
            all_lfi_features.append(LFIFeatures.Active_Refocusing)
        if refocusing_type == "passive":
            all_lfi_features.append(LFIFeatures.Passive_Refocusing)
        if refocusing_type == "none":
            all_lfi_features.append(LFIFeatures.None_Refocusing)
        
        if LFIFeatures.None_Refocusing in all_lfi_features and LFIFeatures.None_ViewChanging in all_lfi_features:
            return None

        cmp_type_str=cmp_type.lower()
        if "double" in cmp_type_str:
            cmp_type=ComparisonType.DoubleStimuli
        if "single" in cmp_type_str:
            cmp_type=ComparisonType.SingleStimuli
        if "pair" in cmp_type_str:
            cmp_type=ComparisonType.PairComparison
            
        if LFIFeatures.Active_Refocusing in all_lfi_features or LFIFeatures.Passive_Refocusing in all_lfi_features:
            all_lfi_features.append(LFIFeatures.Refocusing)
        
        save_format_type=save_format_type.lower()
        if save_format_type == "csv":
            save_format=SaveFormat.CSV
        if save_format_type == "excel":
            save_format=SaveFormat.Excel

        exp_setting=ExpSetting(all_lfi_features,cmp_type,save_format)
        
        if "Two_Folder_Mode" in exp_keys:
            exp_setting.two_folder_mode=exp_config["Two_Folder_Mode"]
        if "Auto_Play" in exp_keys:
            exp_setting.auto_play=exp_config["Auto_Play"]
        if "Loop_Play" in exp_keys:
            exp_setting.loop_play=exp_config["Loop_Play"]
        if "Loop_Times" in exp_keys:
            exp_setting.loop_times=exp_config["Loop_Times"]
        if "FPS" in exp_keys:
            exp_setting.fps=exp_config["FPS"]
        
        if "Score_Names" in exp_keys:
            exp_setting.score_names=exp_config["Score_Names"]
        if "Score_Levels" in exp_keys:
            cur_score_levels=exp_config["Score_Levels"]
            if type(cur_score_levels) == int:
                cur_score_levels=[cur_score_levels]*len(exp_setting.score_names)
            exp_setting.score_levels=cur_score_levels
        
        if cmp_type==ComparisonType.PairComparison and (not exp_setting.two_folder_mode):
            if "PairWise_List" not in exp_keys:
                logger.error("No PairWise_List in the configuration json file! Please check your file carefully!")
                return None
            else:
                exp_setting.pair_wise_dict=exp_config["PairWise_List"]
        exp_setting.skip_preprocessing=exp_config["Skip_Preprocessing"]

        return exp_setting

    '''
    def GetConfigAllLFIInfo(self,all_config):
        lfi_num=len(all_config)

        if lfi_num==0:
            return None
        
        all_lfi_names=[]
        all_lfi_ori_paths=[]
        all_lfi_dist_paths=[]
        all_lfi_types=[]
        angular_format=None

        for cur_config in all_config:
            cur_lfi_name=cur_config["Name"]
            cur_lfi_origin_path=cur_config["SRC"]
            cur_lfi_dist_path=cur_config["Distorted_Path"]
            cur_lfi_type=cur_config["Type"]
            cur_lfi_format=cur_config["Angular_Format"]

            all_lfi_names.append(cur_lfi_name)
            all_lfi_ori_paths.append(cur_lfi_origin_path)
            all_lfi_dist_paths.append(cur_lfi_dist_path)

            if cur_lfi_type.lower() == "dense":
                all_lfi_types.append(LFITypes.Dense)
            if cur_lfi_type.lower() == "sparse":
                all_lfi_types.append(LFITypes.Sparse)

            if cur_lfi_format == "XY":
                angular_format=AngularFormat.XY
            else:
                angular_format=AngularFormat.HW

        return ExpLFIInfo(all_lfi_names,all_lfi_ori_paths,all_lfi_dist_paths,all_lfi_types,angular_format)
    '''
        
    def GetAllLFIInfo(self,all_lfi_boxes,angular_format):
        lfi_box_num=len(all_lfi_boxes)
        if lfi_box_num==0:
            return None
        all_lfi_names=[]
        all_lfi_ori_paths=[]
        all_lfi_dist_paths=[]
        all_lfi_types=[]
        for i in range(lfi_box_num):
            cur_lfi_box=all_lfi_boxes[i]
            cur_lfi_name=cur_lfi_box.line_editor_name.text()
            cur_ori_path=cur_lfi_box.line_editor_ori.text()
            cur_dist_path=cur_lfi_box.line_editor_dist.text()
            cur_lfi_type=cur_lfi_box.GetLFIType()
            all_lfi_names.append(cur_lfi_name)
            all_lfi_ori_paths.append(cur_ori_path)
            all_lfi_dist_paths.append(cur_dist_path)
            all_lfi_types.append(cur_lfi_type)
        return ExpLFIInfo(all_lfi_names,all_lfi_ori_paths,all_lfi_dist_paths,all_lfi_types,angular_format)
    
    def DeleteBox(self,box_index,scrollAreaWidgetContents,all_lfi_boxes):
        lf_box_num=len(all_lfi_boxes)-1
        all_lfi_boxes.pop(box_index)
        for i in range(lf_box_num):
            all_lfi_boxes[i].box_index=i

        if lf_box_num>0:
            height=all_lfi_boxes[-1].height()
        else:
            height=0
        scrollAreaWidgetContents.resize(scrollAreaWidgetContents.width(), (self.lfi_margin_y+height)*lf_box_num+100)
        self.UpdateLFINum()

        
    def AddLFIBox(self,scrollAreaWidgetContents,all_lfi_boxes,LFILayout):
        lf_box_num=len(all_lfi_boxes)+1
        all_lfi_boxes.append(LFIGroupBox())
        all_lfi_boxes[-1].box_index=lf_box_num-1
        all_lfi_boxes[-1].return_signal.connect(lambda box_index: self.DeleteBox(box_index,scrollAreaWidgetContents,all_lfi_boxes))
        
        LFILayout.addWidget(all_lfi_boxes[-1])
        height=all_lfi_boxes[-1].height()

        scrollAreaWidgetContents.resize(scrollAreaWidgetContents.width(), (self.lfi_margin_y+height)*lf_box_num+100)
        self.UpdateLFINum()
    
    def UpdateLFINum(self):
        self.training_lf_box_num=len(self.training_all_lfi_boxes)
        self.test_lf_box_num=len(self.test_all_lfi_boxes)
        



if __name__ == "__main__":
    app = QtWidgets.QApplication()
    window = CreateNewExperiment()
    window.show()
    sys.exit(app.exec())