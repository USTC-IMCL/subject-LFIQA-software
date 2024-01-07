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
from Log_Form import AboutForm
from About_JPEG_ui import Ui_About_JPEG_Form
import PostProcess
import PathManager
logger=logging.getLogger("LogWindow")

class AboutJPEGForm(QWidget,Ui_About_JPEG_Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

class MainProject(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.make_dock_widget()
        self.text_browser=None #QTextBrowser()
        self.cur_project_name=None
        self.cur_project=None
        self.init_screen=True
        self.project_root='./Projects'
        #self.log_form=Log_Form.LogForm()
        #self.log_form.hide()
        self.log_path='./Logs'
        if not os.path.exists(self.log_path):
            os.mkdir(self.log_path)
        today_str=date.today().strftime("%Y-%m-%d")
        self.log_file=os.path.join(self.log_path,today_str+'.log')
        self.file_handler=logging.FileHandler(self.log_file)
        self.file_handler.setFormatter(self.log_text_editor.log_format)
        logger.addHandler(self.file_handler)
        self.action_new_project.triggered.connect(self.NewProject)
        self.action_load_project.triggered.connect(self.LoadProject)
        self.action_preprocessing.triggered.connect(self.preprocess)
        #self.action_preprocessing.triggered.connect(self.PreprosessingFinishedCallback)
        self.action_start_training.triggered.connect(lambda: self.StartExperiment('training'))
        self.action_start_test.triggered.connect(lambda: self.StartExperiment("test"))
        self.action_about_imcl.triggered.connect(lambda: self.AboutIMCL())
        self.action_about_JPEG.triggered.connect(lambda: self.AboutJPEG())
        self.action_close.triggered.connect(lambda: self.CloseProject())
        self.action_post_processing.triggered.connect(lambda: self.PostProcessing())
        self.about_imcl_form=None
        self.about_JPEG_form=None
        self.output_folder=None
    
    def SetProject(self,project_name):
        self.cur_project_name=project_name
        self.cur_project=ExpInfo.ProjectInfo(project_name,self.project_root)
        if self.init_screen:
            self.log_dock.show()
            self.init_screen=False
        self.ShowProjectSetting()
        
    def LoadProject(self):
        project_file=QFileDialog.getOpenFileName(self,'Open Project File','./Projects/','*.lfqoe')[0]
        if project_file == '':
            logger.warning("No project file is selected, loading cancelled...")
            return
        project_name=project_file.split('/')[-1]
        project_name=project_name.split('.')[0]
        project_root=os.path.dirname(os.path.dirname(project_file))

        self.cur_project_name=project_name
        self.cur_project=ExpInfo.ProjectInfo(project_name,project_root)
        if self.init_screen:
            self.log_dock.show()
            self.init_screen=False
        self.ShowProjectSetting()
    
    def CloseProject(self):
        self.cur_project=None
        self.cur_project_name=None
        if self.text_browser is not None:
            self.text_browser.clear()
            self.text_browser.deleteLater()
            self.text_browser=None
        self.text_label.show()
        self.logo_label.show()
        self.init_screen=True
        self.log_dock.hide()

    def ShowProjectSetting(self):
        if self.text_browser is None:
            self.text_browser=QTextBrowser()
            self.setCentralWidget(self.text_browser)
        self.text_browser.show()
        self.text_browser.clear()
        self.text_browser.setText(self.cur_project.PrintAll())
    
    def NewProject(self):
        print("Create a new project now.")
        config_form=Config_Form.CreateNewExperiment()
        config_form.output_folder_root=self.project_root
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
        self.log_dock.hide()
        self.action_log=self.log_dock.toggleViewAction()
        self.menuView.addAction(self.action_log)

    def preprocess(self):
        if self.cur_project is None:
            self.ShowMessage("Please select one project first!",1)
            logger.warning("Please select one project first!")
            return
        
        if self.action_skip_all.isChecked():
            self.ShowMessage("Skip all is checked. All preprocessing is skipped!",1)
            logger.warning("Skip all is checked. All preprocessing is skipped!")
            return

        training_LFI_info=self.cur_project.training_LFI_info
        test_LFI_info=self.cur_project.test_LFI_info
        exp_setting=self.cur_project.exp_setting

        if exp_setting.skip_preprocessing:
            self.ShowMessage("The skip preprocessing is used during the configuration. You must preprocess it manually!",1)
            logger.warning("The skip preprocessing is used during the configuration. You must preprocess it manually!")
            return

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

        skip_refocusing=self.action_skip_refocusing.isChecked()
        self.preprocessing_thread=QThread(self)
        self.preprocessing_worker=PreProcess.PreProcessThread(training_LFI_info,test_LFI_info,exp_setting)
        self.preprocessing_worker.skip_refocusing=skip_refocusing
        self.preprocessing_worker.moveToThread(self.preprocessing_thread)
        self.preprocessing_worker.sub_task_finished.connect(lambda i, s: self.SetPreprocessingDialog(self.preprocessing_dialog,i,s))
        self.preprocessing_worker.total_finished.connect(self.PreprosessingFinishedCallback)
        self.preprocessing_thread.started.connect(self.preprocessing_worker.run)

        self.preprocessing_thread.start()
        #self.preprocessing_worker.run()

        return True
    
    def SetPreprocessingDialog(self,preprocessing_dialog:QProgressDialog,i:int,show_message:str): 
        preprocessing_dialog.setLabelText(show_message)
        preprocessing_dialog.setValue(i)
    
    def PreprosessingFinishedCallback(self):
        self.cur_project.exp_setting.has_preprocess=True
        self.cur_project.InitAllScoringLFIInfo()
        self.cur_project.SaveToFile()

        self.preprocessing_dialog.deleteLater()
        #self.preprocessing_worker.deleteLater()
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
        if self.cur_project is None:
            self.ShowMessage("Please select one project first!",1)
            logger.warning("Please select one project first!")
            return

        if self.cur_project.exp_setting.has_preprocess==False:
                self.ShowMessage("Please preprocess the experiment first!",1)
                logger.warning("Please preprocess the experiment first!")
                return
        
        self.training_LFI_info=self.cur_project.training_LFI_info
        self.test_LFI_info=self.cur_project.test_LFI_info
        self.exp_setting=self.cur_project.exp_setting

        if not self.CheckLFIImages(mode):
            self.ShowMessage("Something is wrong! Please Check your log carefully.",2)
            logger.error("Something is Wrong! Please check the logs above and fix it.")
            return

        if mode == "training":
            subject_name=''
            ok=True
            all_scoring_lfi_info=self.cur_project.training_scoring_lfi_info
        else:
            all_scoring_lfi_info=self.cur_project.test_scoring_lfi_info
            subject_name, ok =QInputDialog.getText(self, 'Subject Record', 'Enter your name:')
        if not ok:
            logger.warning("Experiment cancelled.")
            return
        if not subject_name and mode != "training":
            tmp=QErrorMessage(self)
            tmp.setWindowTitle('Error')
            tmp.showMessage('Do not allow empty name, nothing will be recorded.')
            return

        '''
        if mode == "training":
            show_list=ExpInfo.GetShowList(self.training_LFI_info,self.exp_setting,"training")
            score_info=self.training_LFI_info
            show_index=list(range(len(show_list)))
            new_show_list=show_list
        else:
            show_list=ExpInfo.GetShowList(self.test_LFI_info,self.exp_setting,"test")
            score_info=self.test_LFI_info
            show_index,new_show_list=self.GetRandomShowList(show_list)
        '''

        show_lfi_num=all_scoring_lfi_info.GetLFINum()
        if mode ==  "training":
            all_show_index=list(range(show_lfi_num))
        else:
            all_show_index=all_scoring_lfi_info.GetRandomShowOrder()
        
        if self.exp_setting.comparison_type ==  ExpInfo.ComparisonType.PairComparison:
            score_page=PairWiseScoringWidget(all_scoring_lfi_info,self.exp_setting,all_show_index)
        else:
            score_page=ScoringWidget(all_scoring_lfi_info,self.exp_setting,all_show_index)

        self.hide()
        score_page.show()
        if mode == "test":
            score_page.scoring_finished.connect(lambda all_results: self.GetAndSaveResult(all_results,subject_name,all_show_index,all_scoring_lfi_info))
        else:
            score_page.scoring_finished.connect(lambda all_results: self.show())
    
    def GetAndSaveResult(self,all_results,subject_name,all_show_index,show_list:ExpInfo.AllScoringLFI):
        self.output_folder=os.path.join(self.cur_project.project_path,PathManager.subject_results_folder)
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        logger.info("The evaluation has been finished. Now saving results to %s ..." % self.output_folder)
        self.cur_project.subject_list.append(subject_name)
        if self.exp_setting.save_format == ExpInfo.SaveFormat.CSV:
            self.SaveCSV(all_results,subject_name,all_show_index,show_list)
        else:
            self.SaveExcel(all_results,subject_name,all_show_index,show_list)
        self.show()
        self.cur_project.SaveToFile()
        self.ShowProjectSetting()
    
    def SaveExcel(self,all_results,subject_name,all_show_index,show_list:ExpInfo.AllScoringLFI):
        save_file=os.path.join(self.output_folder,subject_name+'.xlsx')
        workbook=xlsxwriter.Workbook(save_file)
        worksheet=workbook.add_worksheet(subject_name)
        worksheet.write(0,0,'Image Index') 
        worksheet.write(0,1,'Image Name')

        if self.exp_setting.comparison_type != ExpInfo.ComparisonType.PairComparison:
            worksheet.write(0,2,'distortion')
            worksheet.write(0,3,'Image Quality')
            worksheet.write(0,4,'Overall Score')
            for i,scoring_index in enumerate(all_show_index):
                cur_scoring_lfi_info=show_list.GetScoringExpLFIInfo(scoring_index)
                cur_img_name=cur_scoring_lfi_info.lfi_name
                distortion=cur_scoring_lfi_info.exp_name
                worksheet.write(i+1,0,scoring_index)
                worksheet.write(i+1,1,cur_img_name)
                worksheet.write(i+1,2,distortion)
                worksheet.write(i+1,3,all_results[i][0])
                worksheet.write(i+1,4,all_results[i][1])
        else:
            view_changing_score=all_results[0]
            refocusing_score=all_results[1]
            if ExpInfo.LFIFeatures.Active_ViewChanging in self.exp_setting.lfi_features and ExpInfo.LFIFeatures.Active_Refocusing in self.exp_setting.lfi_features:
                worksheet.write(0,2,'Overall Score')
                for i,scoring_index in enumerate(all_show_index):
                    cur_scoring_lfi_info=show_list.GetScoringExpLFIInfo(scoring_index)
                    cur_img_name=cur_scoring_lfi_info.exp_name
                    worksheet.write(i+1,0,scoring_index)
                    worksheet.write(i+1,1,cur_img_name)
                    worksheet.write(i+1,2,view_changing_score[i])
            
            else:
                save_array=[]
                for i,scoring_index in range(all_show_index):
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
                
                for i,scoring_index in enumerate(all_show_index):
                    cur_scoring_lfi_info=show_list.GetScoringExpLFIInfo(scoring_index)
                    cur_img_name=cur_scoring_lfi_info.exp_name
                    worksheet.write(i+1,0,scoring_index)
                    worksheet.write(i+1,1,cur_img_name)
                    current_col=2
                    for value in save_array[i]:
                        worksheet.write(i+1,current_col,value)
                        current_col+=1
        workbook.close()
    
    def SaveCSV(self,all_results,subject_name,all_show_index,show_list:ExpInfo.AllScoringLFI):
        save_file=os.path.join(self.output_folder,subject_name+'.csv')
        with open(save_file,'w') as fid:
            fid.write('Image Index,Image Name')
            if self.exp_setting.comparison_type != ExpInfo.ComparisonType.PairComparison:
                fid.write(',distortion,Image Quality Score, Overall Score\n')
                for i,scoring_index in enumerate(all_show_index):
                    cur_scoring_lfi_info=show_list.GetScoringExpLFIInfo(scoring_index)
                    cur_img_name=cur_scoring_lfi_info.lfi_name
                    distortion=cur_scoring_lfi_info.exp_name
                    fid.write(f'{scoring_index},{cur_img_name},{distortion},{all_results[i][0]},{all_results[i][1]}\n')
            else:
                view_changing_score=all_results[0]
                refocusing_score=all_results[1]
                if ExpInfo.LFIFeatures.Active_ViewChanging in self.exp_setting.lfi_features and ExpInfo.LFIFeatures.Active_Refocusing in self.exp_setting.lfi_features:
                    fid.write(',Overall Score\n')
                    for i,scoring_index in enumerate(all_show_index):
                        cur_scoring_lfi_info=show_list.GetScoringExpLFIInfo(scoring_index)
                        cur_img_name=cur_scoring_lfi_info.exp_name
                        fid.write(f'{scoring_index},{cur_img_name},{view_changing_score[i]}\n')
            
                else:
                    save_array=[]
                    for i in range(len(all_show_index)):
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
                
                    for i,scoring_index in enumerate(all_show_index):
                        cur_scoring_lfi_info=show_list.GetScoringExpLFIInfo(scoring_index)
                        cur_img_name=cur_scoring_lfi_info.exp_name
                        fid.write(f'{scoring_index},{cur_img_name}')
                        current_col=2
                        for value in save_array[i]:
                            fid.write(f',{value}')
                            current_col+=1
                        fid.write('\n')
        
    def GetRandomShowList(self,show_list):
        show_index=list(range(len(show_list)))
        shuffle(show_index)
        return show_index,[show_list[i] for i in show_index]
    
    def SaveProject(self):
        if self.cur_project is not None:
            self.cur_project.SaveToFile()
            self.ShowProjectSetting()
    
    def AboutIMCL(self):
        if self.about_imcl_form is None:
            self.about_imcl_form=AboutForm()
            self.about_imcl_form.destroyed.connect(lambda: self.ClearAboutIMCL)
        self.about_imcl_form.show()
    
    def ClearAboutIMCL(self):
        self.about_imcl_form=None
    
    def AboutJPEG(self):
        if self.about_JPEG_form is None:
            self.about_JPEG_form=AboutJPEGForm()
            self.about_JPEG_form.destroyed.connect(lambda: self.ClearAboutJPEG)
        self.about_JPEG_form.show()
    
    def ClearAboutJPEG(self):
        self.about_JPEG_form=None

    def CheckLFIImages(self,mode="training"):
        '''
        To check if the images for the experiment are all exist.
        '''
        if mode == "training":
            logger.info("Before starting the training, check all images/videos...")
            all_lfi_info=self.cur_project.training_scoring_lfi_info
        else:
            logger.info("Before starting the test, check all images/videos...")
            all_lfi_info=self.cur_project.test_scoring_lfi_info
        exp_setting=self.cur_project.exp_setting
        
        '''
        Check the show images if view feature is active, passive or None
        The right way is to get the show list first.
        '''
        scoring_num=all_lfi_info.GetLFINum()
        for scoring_index in range(scoring_num):
            cur_lfi_scoring_info=all_lfi_info.GetScoringExpLFIInfo(scoring_index)
            lfi_name=cur_lfi_scoring_info.lfi_name

            show_refocus_path=cur_lfi_scoring_info.active_refocusing_path
            angular_width=cur_lfi_scoring_info.angular_width
            angular_height=cur_lfi_scoring_info.angular_height

            if ExpInfo.LFIFeatures.Active_ViewChanging in exp_setting.lfi_features:
                for row_index in range(angular_height):
                    for col_index in range(angular_width):
                        show_view_name=cur_lfi_scoring_info.GetActiveView(row_index,col_index)
                        if not os.path.exists(show_view_name):
                            logger.error("Can not find the image %s! Please check yor preprocessing carefully. The experiment will be cancelled. Quit now..." % show_view_name)
                            return False
            if ExpInfo.LFIFeatures.Passive_ViewChanging in exp_setting.lfi_features:
                show_view_video=cur_lfi_scoring_info.passive_view_video_path
                if not os.path.exists(show_view_video):
                    logger.error("Can not find the video %s! Please check yor preprocessing carefully. The experiment will be cancelled. Quit now..." % show_view_video)
                    return False
            if ExpInfo.LFIFeatures.Active_Refocusing in exp_setting.lfi_features:
                if not os.path.exists(cur_lfi_scoring_info.depth_path):
                    logger.error(f"Can not find the depth map {cur_lfi_scoring_info.depth_path}! The active refocusing needs a depth image to map you clicking position to a certain refocusing depth. Please check your data carefully. Quit now...")
                    return False
                all_depth_value=cur_lfi_scoring_info.GetAllPossibleDepthVal()
                for depth_value in all_depth_value:
                    image_name=os.path.join(show_refocus_path,f'{depth_value}.{cur_lfi_scoring_info.img_post_fix}')
                    if not os.path.exists(image_name):
                        logger.error("Can not find the image %s! Please check yor preprocessing carefully. The experiment will be cancelled. Quit now..." % image_name)
                        return False
            if ExpInfo.LFIFeatures.Passive_Refocusing in exp_setting.lfi_features:
                show_refocusing_video=cur_lfi_scoring_info.passive_refocusing_video_path
                if not os.path.exists(show_refocusing_video):
                    logger.error("Can not find the video %s! Please check yor preprocessing carefully. The experiment will be cancelled. Quit now..." % show_refocusing_video)
                    return False
        logger.info("Everything is Ok. Start the experiment...")
        return True

    def PostProcessing(self):
        if self.cur_project is None:
            self.ShowMessage("Please select one project first!",1)
            logger.warning("Please select one project first!")
            return
        subject_list=self.cur_project.subject_list
        if len(subject_list)<2:
            self.ShowMessage("The subjects number should be greater than 2. Not enough subjects.",1)
            logger.warning("The subjects number should be greater than 2. Not enough subjects.")
            return
        if self.output_folder is None:
            self.output_folder=os.path.join(self.cur_project.project_path,PathManager.subject_results_folder)
        exp_setting=self.cur_project.exp_setting
        PostProcess.PostProcess(exp_setting,self.output_folder)
        
        
    def closeEvent(self, closeEvent) -> None: 
        if self.about_imcl_form is not None:
            self.about_imcl_form.deleteLater()
        if self.about_JPEG_form is not None:
            self.about_JPEG_form.deleteLater()
        closeEvent.accept()
        self.deleteLater()
    

if __name__ == "__main__":
    app=QApplication()
    main_window=MainProject()
    main_window.show()
    sys.exit(app.exec())
