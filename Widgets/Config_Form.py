import os
import sys

import PySide6.QtGui
sys.path.append('../UI')
sys.path.append('../Widgets/')
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Signal, Slot
from PySide6.QtCore import QRect
from PySide6.QtWidgets import QWidget,QMessageBox
from NewExperiment_ui import Ui_NewExperimentForm as NewExperimentForm
from LFIGroupBox_ui import Ui_LFIGroupWidget
from ExpInfo import *
import pickle
import PreProcess


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
    Finished = Signal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.current_page_index=0
        self.ConfigStackWidget.setCurrentIndex(self.current_page_index)

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
            return 
        project_post_fix='lfqoe'
        save_file=self.GetSaveFileName()
        if save_file is None:
            self.ShowMessage("Invalid path! Please check the path again!",2)
            return
        else:
            if not save_file.endswith(project_post_fix):
                save_file=save_file+'.'+project_post_fix
        
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

        with open(save_file,'wb') as f:
            pickle.dump(self.training_all_lfi_info,f)
            pickle.dump(self.test_all_lfi_info,f)
            pickle.dump(exp_setting,f)
        
        bPreProcess=self.OptionDialog("Do you want to preprocess the data now?")
        self.Finished.emit(bPreProcess)

        self.deleteLater()
        
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
        self.CancelClosed.emit()
        self.deleteLater()
        
    def Page0Next(self):
        if self.radio_btn_manually.isChecked():
            self.current_page_index+=1
            self.ConfigStackWidget.setCurrentIndex(self.current_page_index)
        else:
            json_path=self.page_0_json_path.text()
            ret_info=self.ConfigFromJson(json_path)
            if ret_info[0]:
                self.CancelClose()
            else:
                dlg=QMessageBox(self)
                dlg.setWindowTitle("Warning!")
                dlg.setStandardButtons(QMessageBox.Ok)
                dlg.setIcon(QMessageBox.Warning)
                dlg.setText(ret_info[1])
                dlg.exec()
    
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
            return False , "Invalid path! Please Check the Json Path again!"
        '''
        config with json here 
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