import os
import sys
sys.path.append('../UI')
from PySide6.QtWidgets import QWidget, QDockWidget, QMainWindow, QTextBrowser, QApplication, QFileDialog, QMessageBox, QProgressDialog
from PySide6.QtCore import Qt, QThread
from LogWindow import QLogTextEditor
import ExpInfo
from MainProject_ui import Ui_MainWindow
import Log_Form
import Config_Form
import PreProcess 
import logging
logger=logging.getLogger("LogWindow")

class MainProject(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.make_dock_widget()
        self.text_browser=QTextBrowser()
        self.setCentralWidget(self.text_browser)
        self.cur_project_name=None
        self.cur_project=None
        #self.log_form=Log_Form.LogForm()
        #self.log_form.hide()
        self.action_new_project.triggered.connect(self.NewProject)
        self.action_load_project.triggered.connect(self.LoadProject)
        self.action_preprocessing.triggered.connect(self.preprocess)
    
    def SetProject(self,project_name):
        self.cur_project_name=project_name
        self.cur_project=ExpInfo.ProjectInfo(project_name)
        self.ShowProjectSetting()
        
    def LoadProject(self):
        project_file=QFileDialog.getOpenFileName(self,'Open Project File','./','*.lfqoe')[0]
        project_name=project_file.split('/')[-1]
        project_name=project_name.split('.')[0]
        project_root=os.path.dirname(os.path.dirname(project_file))

        self.cur_project_name=project_name
        self.cur_project=ExpInfo.ProjectInfo(project_name,project_root)
        self.ShowProjectSetting()

    def ShowProjectSetting(self):
        self.text_browser.clear()
        self.text_browser.setText(self.cur_project.PrintAll())
    
    def NewProject(self):
        print("Create a new project now.")
        config_form=Config_Form.CreateNewExperiment()
        config_form.show()
        config_form.CancelClosed.connect(self.CreateCanceled)
        config_form.Finished.connect(self.CreateFinished)

    def make_dock_widget(self):
        self.log_dock = QDockWidget("Logs", self)
        self.log_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea | Qt.BottomDockWidgetArea)
        self.log_text_editor=QLogTextEditor()
        self.log_text_editor.setStyleSheet("background: gray;\ncolor: rgb(255, 255, 255);")
        self.log_dock.setWidget(self.log_text_editor)
        self.addDockWidget(Qt.RightDockWidgetArea, self.log_dock)
        self.menuView.addAction(self.log_dock.toggleViewAction())

    def preprocess(self):
        if self.cur_project is None:
            self.ShowMessage("Please select one project first!",1)
            logger.error("Please select one project first!")
            return
        training_LFI_info=self.cur_project.training_LFI_info
        test_LFI_info=self.cur_project.test_LFI_info
        exp_setting=self.cur_project.exp_setting

        if exp_setting.has_preprocess:
            b_preprocess=QMessageBox.question(self,"Preprocess","The experiment has been preprocessed, do you want to re-preprocess?",QMessageBox.Yes|QMessageBox.No)
            if b_preprocess==QMessageBox.No:
                logger.info("The experiment preprocessing is cancelled.")
                return

        exp_setting.has_preprocess=False
        logger.info("Now we start preprocessing the experiment.")

        self.preprocessing_dialog=QProgressDialog(self)
        self.preprocessing_dialog.setWindowTitle('Now Preprocessing')
        self.preprocessing_dialog.setValue(0)
        self.preprocessing_dialog.setLabelText('It takes around 10 minuts, please wait...')
        self.preprocessing_dialog.setCancelButton(None)
        #self.preprocessing_dialog.setWindowModality(Qt.WindowModal)
        self.preprocessing_dialog.show()

        self.preprocessing_thread=QThread(self)
        self.preprocessing_worker=PreProcess.PreProcessThread(training_LFI_info,test_LFI_info,exp_setting)
        self.preprocessing_worker.moveToThread(self.preprocessing_thread)
        self.preprocessing_worker.sub_task_finished.connect(lambda i, s: self.SetPreprocessingDialog(self.preprocessing_dialog,i,s))
        self.preprocessing_worker.total_finished.connect(self.PreprosessingFinishedCallback)
        self.preprocessing_thread.started.connect(self.preprocessing_worker.run)

        self.preprocessing_thread.start()
        
        return True
    
    def SetPreprocessingDialog(self,preprocessing_dialog:QProgressDialog,i:int,show_message:str): 
        preprocessing_dialog.setLabelText(show_message)
        preprocessing_dialog.setValue(i)
    
    def PreprosessingFinishedCallback(self):
        self.cur_project.exp_setting.has_preprocess=True
        self.cur_project.SaveToFile()

        self.preprocessing_dialog.deleteLater()
        self.preprocessing_worker.deleteLater()
        #self.preprocessing_thread.deleteLater()

    def CreateFinished(self,b_preprocessing_now,target_config_file):
        #print(b_preprocessing_now)
        self.SetProject(target_config_file)

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

    def CreateCanceled(self):
        pass



    
if __name__ == "__main__":
    app=QApplication()
    main_window=MainProject()
    main_window.show()
    sys.exit(app.exec())
