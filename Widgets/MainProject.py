import os
import sys
sys.path.append('../UI')
from random import shuffle
from datetime import date
from PySide6.QtWidgets import QWidget, QDockWidget, QMainWindow, QTextBrowser, QApplication, QFileDialog, QMessageBox, QProgressDialog, QInputDialog, QErrorMessage
from PySide6.QtCore import Qt, QThread
from LogWindow import QLogTextEditor
import ExpInfo
from MainProject_ui import Ui_MainWindow
import Log_Form
import Config_Form
import PreProcess 
import logging
from ScoringWidget import ScoringWidget, PairWiseScoringWidget
import xlsxwriter
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
        self.log_path='./Logs'
        if not os.path.exists(self.log_path):
            os.mkdir(self.log_path)
        today_str=date.today().strftime("%Y-%m-%d")
        self.log_file=os.path.join(self.log_path,today_str+'.log')
        self.file_handler=logging.FileHandler(self.log_file)
        logger.addHandler(self.file_handler)
        self.action_new_project.triggered.connect(self.NewProject)
        self.action_load_project.triggered.connect(self.LoadProject)
        self.action_preprocessing.triggered.connect(self.preprocess)
        self.action_start_training.triggered.connect(lambda: self.StartExperiment('training'))
        self.action_start_test.triggered.connect(lambda: self.StartExperiment("test"))
    
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
        self.ShowProjectSetting()
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

    def StartExperiment(self,mode='training'):
        if self.cur_project.exp_setting.has_preprocess==False:
            self.ShowMessage("Please preprocess the experiment first!",1)
            logger.warning("Please preprocess the experiment first!")
            return
        self.training_LFI_info=self.cur_project.training_LFI_info
        self.test_LFI_info=self.cur_project.test_LFI_info
        self.exp_setting=self.cur_project.exp_setting

        if self.cur_project is None:
            self.ShowMessage("Please select one project first!",1)
            logger.warning("Please select one project first!")
            return

        subject_name, ok =QInputDialog.getText(self, 'Subject Record', 'Enter your name:')
        if not ok:
            logger.warning("Experiment cancelled.")
            return
        if not subject_name:
            tmp=QErrorMessage(self)
            tmp.setWindowTitle('Error')
            tmp.showMessage('Do not allow empty name, nothing will be recorded.')
            return

        if mode == "training":
            show_list=ExpInfo.GetShowList(self.training_LFI_info,self.exp_setting,"training")
            score_info=self.training_LFI_info
            show_index=list(range(len(show_list)))
            new_show_list=show_list
        else:
            show_list=ExpInfo.GetShowList(self.test_LFI_info,self.exp_setting,"test")
            score_info=self.test_LFI_info
            show_index,new_show_list=self.GetRandomShowList(show_list)
        
        if self.exp_setting.comparison_type ==  ExpInfo.ComparisonType.PairComparison:
            score_page=PairWiseScoringWidget(score_info,self.exp_setting,new_show_list)
        else:
            score_page=ScoringWidget(score_info,self.exp_setting,new_show_list)

        self.hide()
        score_page.show()
        score_page.scoring_finished.connect(lambda all_results: self.GetAndSaveResult(all_results,subject_name,show_index,new_show_list))
    
    def GetAndSaveResult(self,all_results,subject_name,show_index,show_list):
        self.output_folder=self.cur_project.project_path
        logger.info("The evaluation has been finished. Now saving results to %s ..." % self.output_folder)
        if self.exp_setting.save_format == ExpInfo.SaveFormat.CSV:
            self.SaveCSV(all_results,subject_name,show_index,show_list)
        else:
            self.SaveExcel(all_results,subject_name,show_index,show_list)
        self.show()
    
    def SaveExcel(self,all_results,subject_name,show_index,show_list):
        save_file=os.path.join(self.output_folder,subject_name+'.xlsx')
        workbook=xlsxwriter.Workbook(save_file)
        worksheet=workbook.add_worksheet(subject_name)
        worksheet.write(0,0,'Image Index') 
        worksheet.write(0,1,'Image Name')

        if self.exp_setting.comparison_type != ExpInfo.ComparisonType.PairComparison:
            worksheet.write(0,2,'distortion')
            worksheet.write(0,3,'Image Quality')
            worksheet.write(0,4,'Overall Score')
            for i in range(len(show_index)):
                cur_img_name=show_list[i][0]
                distortion=show_list[i][1]+'_'+str(show_list[i][2])
                worksheet.write(i+1,0,show_index[i])
                worksheet.write(i+1,1,cur_img_name)
                worksheet.write(i+1,2,distortion)
                worksheet.write(i+1,3,all_results[i][0])
                worksheet.write(i+1,4,all_results[i][1])
        else:
            view_changing_score=all_results[0]
            refocusing_score=all_results[1]
            if ExpInfo.LFIFeatures.Active_ViewChanging in self.exp_setting.lfi_features and ExpInfo.LFIFeatures.Active_Refocusing in self.exp_setting.lfi_features:
                worksheet.write(0,2,'Overall Score')
                for i in range(len(show_index)):
                    tmp=[str(x) for x in show_list[i]]
                    cur_img_name='_'.join(tmp)
                    worksheet.write(i+1,0,show_index[i])
                    worksheet.write(i+1,1,cur_img_name)
                    worksheet.write(i+1,2,view_changing_score[i])
            
            else:
                save_array=[]
                for i in range(len(show_index)):
                    save_array.append([])
                    if all_results[0] is not None:
                        save_array[i].append(view_changing_score[i])
                    if all_results[1] is not None:
                        save_array[i].append(refocusing_score[i])

                current_col=2
                if view_changing_score is not None:
                    worksheet.write(0,current_col,'View Changing Score')
                    current_col+=1
                if refocusing_score is not None:
                    worksheet.write(0,current_col,'Refocusing Score')
                
                for i in range(len(show_index)):
                    tmp=[str(x) for x in show_list[i]]
                    cur_img_name='_'.join(tmp)
                    worksheet.write(i+1,0,show_index[i])
                    worksheet.write(i+1,1,cur_img_name)
                    current_col=2
                    for value in save_array[i]:
                        worksheet.write(i+1,current_col,value)
                        current_col+=1
        workbook.close()
    
    def SaveCSV(self,all_results,subject_name,show_index,show_list):
        save_file=os.path.join(self.output_folder,subject_name+'.csv')
        with open(save_file,'w') as fid:
            fid.write('Image Index,Image Name')
            if self.exp_setting.comparison_type != ExpInfo.ComparisonType.PairComparison:
                fid.write(',distortion,Image Quality Score, Overall Score\n')
                for i in range(len(show_index)):
                    cur_img_name=show_list[i][0]
                    distortion=show_list[i][1]+'_'+str(show_list[i][2])
                    fid.write(f'{show_index[i]},{cur_img_name},{distortion},{all_results[i][0]},{all_results[i][1]}\n')
            else:
                view_changing_score=all_results[0]
                refocusing_score=all_results[1]
                if ExpInfo.LFIFeatures.Active_ViewChanging in self.exp_setting.lfi_features and ExpInfo.LFIFeatures.Active_Refocusing in self.exp_setting.lfi_features:
                    fid.write(',Overall Score\n')
                    for i in range(len(show_index)):
                        tmp=[str(x) for x in show_list[i]]
                        cur_img_name='_'.join(tmp)
                        fid.write(f'{show_index[i]},{cur_img_name},{view_changing_score[i]}\n')
            
                else:
                    save_array=[]
                    for i in range(len(show_index)):
                        save_array.append([])
                        if all_results[0] is not None:
                            save_array[i].append(view_changing_score[i])
                        if all_results[1] is not None:
                            save_array[i].append(refocusing_score[i])

                    current_col=2
                    if view_changing_score is not None:
                        fid.write(',View Changing Score')
                        current_col+=1
                    if refocusing_score is not None:
                        fid.write(',Refocusing Score')
                    fid.write('\n')
                
                    for i in range(len(show_index)):
                        tmp=[str(x) for x in show_list[i]]
                        cur_img_name='_'.join(tmp)
                        fid.write(f'{show_index[i]},{cur_img_name}')
                        current_col=2
                        for value in save_array[i]:
                            fid.write(f',{value}')
                            current_col+=1
                        fid.write('\n')
        
    def GetRandomShowList(self,show_list):
        show_index=list(range(len(show_list)))
        shuffle(show_index)
        return show_index,[show_list[i] for i in show_index]


    
if __name__ == "__main__":
    app=QApplication()
    main_window=MainProject()
    main_window.show()
    sys.exit(app.exec())
