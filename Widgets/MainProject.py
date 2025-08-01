import os
import sys
sys.path.append('../UI')
from random import shuffle
from datetime import date
from PySide6.QtWidgets import QWidget, QDockWidget, QMainWindow, QTextBrowser, QApplication, QFileDialog, QMessageBox, QProgressDialog, QInputDialog, QErrorMessage, QDialog
from PySide6.QtGui import QAction, QActionGroup,QTextCursor
from PySide6.QtCore import Qt, QThread
from LogWindow import QLogTextEditor , StreamToLogger
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
import FontSetting
import SubjectInfo
from ProjectDisplay import ProjectDisplay
from PlayList import MakeDSCSPCList, MakePCPairs
from PassiveTools import ConcatPCFilesCMD, WorkerManager
from SessionConnector import SessionConnector
from ExpSession import ExperimentSession
import copy
import JPLMessageBox
logger=logging.getLogger("LogWindow")

class AboutJPEGForm(QWidget,Ui_About_JPEG_Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

class MainProject(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #self.make_dock_widget()
        self.text_browser=None #QTextBrowser()
        self.cur_project_name=None
        self.project_display=None
        self.cur_project=None
        self.init_screen=True
        self.project_root='./Projects'
        #self.log_form=Log_Form.LogForm()
        #self.log_form.hide()
        custom_init_path='./SoftwareConfig.json'
        '''
        inner_json=os.path.join(os.path.dirname(sys.executable),'Utils','SoftwareConfig.json')
        if not os.path.exists(inner_json):
            inner_json='./Utils/SoftwareConfig.json'
        '''
        custom_log_level=PathManager.SoftWarePathManager.ReadLogLevelOnly(custom_init_path)
        self.software_manager=PathManager.SoftWarePathManager()
        if custom_log_level is not None:
            self.software_manager.log_level=custom_log_level

        self.software_manager.file_path=custom_init_path
        self.software_manager.SaveInfo()
        self.log_path=self.software_manager.logs_path
        if not os.path.exists(self.log_path):
            os.mkdir(self.log_path)
        today_str=date.today().strftime("%Y-%m-%d")
        self.log_file=os.path.join(self.log_path,today_str+'.log')
        self.file_handler=logging.FileHandler(self.log_file)
        format_str='%(asctime)s [%(levelname)s]: %(message)s'
        self.file_handler.setFormatter(logging.Formatter(fmt=format_str,datefmt='%Y-%m-%d-%H:%M'))
        logger.addHandler(self.file_handler)
        logger.setLevel(self.software_manager.log_level)

        sys.stdout=StreamToLogger(logger, logging.INFO)
        sys.stderr=StreamToLogger(logger, logging.ERROR)

        # set a new processing to run PC content generation CMDs
        self.back_thread= WorkerManager()  
        self.session_player=None
        self.session_connector=None
        self.all_sessions=[]  # a list containing all sessions' mode
        self.exp_screen_index=0

        self.cur_exp_mode="training"
        self.InitTrigger()
    
    def InitTrigger(self):
        #self.action_log=self.log_dock.toggleViewAction()
        #self.menuView.addAction(self.action_log)
        self.action_new_project.triggered.connect(self.NewProject)
        self.action_load_project.triggered.connect(self.LoadProject)
        self.action_preprocessing.deleteLater()
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
        self.actionTable_Font_Size.triggered.connect(lambda: self.SetCustomFont("Table"))
        self.actionHint_Text_Size.triggered.connect(lambda: self.SetCustomFont("Hint_text"))
        self.font_setting_dialog=None

        self.log_level_group=QActionGroup(self)
        self.log_level_group.setExclusive(True)
        self.log_level_group.addAction(self.actionDebug)
        self.log_level_group.addAction(self.actionInfo)
        self.log_level_group.addAction(self.actionError)
        self.log_level_group.addAction(self.actionWarning)

        self.action_setting_interchange_data.triggered.connect(self.SetInterchangeData)

        self.log_level_group.triggered.connect(self.GroupSetLevel)
        self.SetLogActionTriggered()
    
    def SetInterchangeData(self):
        pass

    def SetLogActionTriggered(self):
        if logger.level == logging.DEBUG:
            self.actionDebug.setChecked(True)
            return
        if logger.level == logging.INFO:
            self.actionInfo.setChecked(True)
            return 
        if logger.level == logging.WARNING:
            self.actionWarning.setChecked(True)
            return 
        if logger.level == logging.ERROR:
            self.actionError.setChecked(True)
            return 

    def GroupSetLevel(self):
        if self.actionDebug.isChecked():
            self.SetLogLevel('debug')
            return
        if self.actionInfo.isChecked():
            self.SetLogLevel('info')
            return
        if self.actionWarning.isChecked():
            self.SetLogLevel('warning')
            return
        if self.actionError.isChecked():
            self.SetLogLevel('error')
            return

    def SetLogLevel(self,mode):
        self.software_manager.log_level=mode.upper()
        self.software_manager.SaveInfo()
        if mode == 'debug':
            logger.setLevel(logging.DEBUG)
            return
        if mode == 'info':
            logger.setLevel(logging.INFO)
            return
        if mode == 'error':
            logger.setLevel(logging.ERROR)
            return
        if mode == 'warning':
            logger.setLevel(logging.WARNING)
            return
    
    def SetProject(self,project_name):
        self.cur_project_name=project_name
        self.cur_project=ExpInfo.ProjectInfo(project_name,self.project_root)
        '''
        if self.init_screen:
            self.log_dock.show()
            self.init_screen=False
        '''
        if self.project_display is not None:
            self.project_display.hide()
            logger.removeHandler(self.project_display.right_text_editor_handler)
            self.project_display.deleteLater()
            self.project_display=None
        
        self.ShowProjectSetting()
        
    def LoadProject(self):
        project_file=QFileDialog.getOpenFileName(self,'Open Project File','./Projects/','*.lfqoe')[0]
        if project_file == '':
            logger.warning("No project file is selected, loading cancelled...")
            return
        project_name=project_file.split('/')[-1]
        project_name=project_name.split('.')[0]
        project_root=os.path.dirname(os.path.dirname(project_file))

        #TODO: implement an update function
        if self.project_display is not None:
            self.project_display.hide()
            logger.removeHandler(self.project_display.right_text_editor_handler)
            self.project_display.deleteLater()
        self.cur_project_name=project_name
        self.cur_project=ExpInfo.ProjectInfo(project_name,project_root)
        self.ShowProjectSetting()
    
    def CloseProject(self):
        self.cur_project=None
        self.cur_project_name=None
        #self.text_label.show()
        #self.logo_label.show()
        self.project_display.hide()
        logger.removeHandler(self.project_display.right_text_editor_handler)
        self.project_display.deleteLater()
        self.project_display=None
        self.setupUi(self)
        self.InitTrigger()

    def ShowProjectSetting(self):
        self.project_display=ProjectDisplay(self.cur_project)
        self.setCentralWidget(self.project_display)
        # TODO : put the log show into the project display
        if os.path.exists(self.log_file):
            with open(self.log_file,'r') as f:
                log_text=f.read()
                self.project_display.right_text_editor.setText(log_text)
                self.project_display.right_text_editor.moveCursor(QTextCursor.End)
    
    def NewProject(self):
        print("Create a new project now.")
        config_form=Config_Form.CreateNewExperiment()
        config_form.output_folder_root=self.project_root
        config_form.show()
        config_form.CancelClosed.connect(self.CreateCanceled)
        config_form.Finished.connect(self.CreateFinished)
    
    '''
    def make_dock_widget(self):
        self.log_dock = QDockWidget("Logs", self)
        self.log_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea | Qt.BottomDockWidgetArea)
        self.log_text_editor=QLogTextEditor()
        self.log_text_editor.setStyleSheet("background: gray;\ncolor: rgb(255, 255, 255);")
        self.log_dock.setWidget(self.log_text_editor)
        self.addDockWidget(Qt.RightDockWidgetArea, self.log_dock)
        self.log_dock.hide()
    '''

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

    def sessiondebugfinished(self):
        self.session_player.deleteLater()
        self.session_player=None

    def StartExperiment(self,mode='training'):
        self.cur_exp_mode=mode
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

        if not self.CheckLFIImages(mode) and (not self.exp_setting.two_folder_mode):
            self.ShowMessage("Something is wrong! Please Check your log carefully.",2)
            logger.error("Something is Wrong! Please check the logs above and fix it.")
            return

        subject_info={}
        self.all_sessions=[]
        self.cur_person_info=ExpInfo.PersonInfo()
        if mode == "training":
            all_scoring_lfi_info=self.cur_project.training_scoring_lfi_info
        else:
            all_scoring_lfi_info=self.cur_project.test_scoring_lfi_info
            subjectinfo_dialog=SubjectInfo.SubjectInfo()
            if subjectinfo_dialog.exec() == QDialog.Accepted:
                subject_info=subjectinfo_dialog.GetResult()
                self.cur_person_info=ExpInfo.PersonInfo()
                self.cur_person_info.InitWithSubjectInfo(subject_info)
            else:
                logger.warning("Experiment cancelled.")
                return

        # TODO: divide the experiment into several sessions.
        # Now only DSCSPC contains two sessions.
        if mode=="test" and (self.exp_setting.comparison_type == ExpInfo.ComparisonType.DSCS_PC_BASE or self.exp_setting.comparison_type == ExpInfo.ComparisonType.DSCS_PC_CCG):
            self.all_sessions=[ExpInfo.ComparisonType.DoubleStimuli, ExpInfo.ComparisonType.PairComparison]
        else:
            self.all_sessions=[ExpInfo.ComparisonType.DoubleStimuli]
        
        self.sessions_num=len(self.all_sessions)

        self.session_player=ExperimentSession(all_scoring_lfi_info,self.exp_setting,mode=mode)
        self.session_player.SetScreenIndex(self.exp_screen_index)
        self.session_player.exp_finished.connect(self.SessionConnector)
        self.hide()
        cur_session=self.all_sessions[0]
        self.all_sessions.pop(0)
        self.session_player.StartExperiment(cur_session)
    
    def StartSession(self,all_scoring_lfi_info:ExpInfo.AllScoringLFI,mode):
        self.session_player=ExperimentSession(all_scoring_lfi_info,self.exp_setting,mode)
        self.session_player.SetScreenIndex(self.exp_screen_index)
        self.session_player.exp_finished.connect(self.SessionConnector)
        self.hide()
        cur_session=self.all_sessions[0]
        self.all_sessions.pop(0)
        self.session_player.StartExperiment(cur_session)

    def SessionConnector(self):
        logger.info("Session finished!")
        self.show()
        all_results=copy.deepcopy(self.session_player.GetResult())
        all_show_index=copy.deepcopy(self.session_player.GetShowIndex())
        res_session_cmp_type=self.session_player.cur_cmp_type
        cur_all_scoring_lfi=self.session_player.all_scoring_lfi
        self.session_player.exp_finished.disconnect(self.SessionConnector)
        self.session_player.deleteLater()
        self.session_player=None

        # only testing mode could have multiple sessions
        # now we need to handle some jobs first. E.g. videos generation.
        if self.cur_exp_mode == "training":
            logger.info("Training finished!")
            JPLMessageBox.ShowInformationMessage("Training finished.")
            return
        
        result_session_index=self.sessions_num-len(self.all_sessions)-1

        save_file=os.path.join(self.cur_project.project_path,PathManager.subject_results_folder,f"{self.cur_person_info.GetName()}_session_{result_session_index}")


        # TODO: how to save the results?
        # Not a good solution now. Only works for passive mode

        if len(self.all_sessions)>0:
            JPLMessageBox.ShowInformationMessage("Session finished! Thank you and have a rest now.")
            update_project=False
            self.GetAndSaveResult(all_results,self.cur_person_info,all_show_index,cur_all_scoring_lfi,cmp_type=res_session_cmp_type,save_file=save_file,update_project=update_project)

            self.MakeDSCSPC(all_results,self.cur_person_info,all_show_index,self.cur_project.test_scoring_lfi_info)
        else:
            JPLMessageBox.ShowInformationMessage("Experiment finished! Thank you!")
            logger.info("Experiment finished!")
            update_project=True
            self.GetAndSaveResult(all_results,self.cur_person_info,all_show_index,cur_all_scoring_lfi,cmp_type=res_session_cmp_type,save_file=save_file,update_project=update_project)


    def MakeDSCSPC(self,all_results,subject_info,all_show_index,all_scoring_lfi_info:ExpInfo.AllScoringLFI):
        # now dscs with pc assumes only one score name
        all_scores=[0 for i in range(all_scoring_lfi_info.GetLFINum())]
        lfi_names=[]
        for i, show_index in enumerate(all_show_index):
            cur_scoring_lfi=all_scoring_lfi_info.GetScoringExpLFIInfo(i)
            lfi_names.append(os.path.basename(cur_scoring_lfi.passive_view_video_path))
            all_scores[show_index]=all_results[i][0]
        
        if self.exp_setting.comparison_type == ExpInfo.ComparisonType.DSCS_PC_BASE:
            dscs_pc_method="base"
        elif self.exp_setting.comparison_type == ExpInfo.ComparisonType.DSCS_PC_CCG:
            dscs_pc_method="ccg"

        group_num=self.exp_setting.grading_num
        grading_scales=self.exp_setting.grading_scales
        pc_list=MakeDSCSPCList(lfi_names,all_scores,group_num,grading_scales,dscs_pc_method)

        show_pairs={}
        for class_name in pc_list.keys():
            if class_name not in show_pairs.keys():
                show_pairs[class_name]=[]
                if self.exp_setting.high_quality_only:
                    cur_group_pairs=MakePCPairs(pc_list[class_name][0])
                    if len(cur_group_pairs)> 0:
                        show_pairs[class_name]+=cur_group_pairs
                else:
                    for i in range(len(pc_list[class_name])):
                        cur_group=pc_list[class_name][i]
                        cur_group_pairs=MakePCPairs(cur_group)
                        if len(cur_group_pairs)> 0:
                            show_pairs[class_name]+=cur_group_pairs
         
        # make another all_scoring_lfi_info
        pc_root=os.path.join(self.cur_project.project_path,PathManager.dscs_folder,self.cur_exp_mode)
        if not os.path.exists(pc_root):
            os.makedirs(pc_root)
        
        all_pc_cmds=[]
        video_save_type_str=self.exp_setting.VideoSaveTypeStr 
        self.pc_show_list=ExpInfo.TwoFolderLFIInfo(None,video_save_type_str,in_mode="test")
        for class_name in show_pairs.keys():
            cur_all_pairs=show_pairs[class_name]
            for cur_pairs in cur_all_pairs:
                scoring_lfi_1=all_scoring_lfi_info.GetScoringExpLFIInfo(cur_pairs[0][0])
                scoring_lfi_2=all_scoring_lfi_info.GetScoringExpLFIInfo(cur_pairs[1][0])

                file_1=scoring_lfi_1.passive_view_video_path
                file_part_1=os.path.basename(file_1)
                post_fix_1='.'+file_part_1.split(".")[-1]

                file_2=scoring_lfi_2.passive_view_video_path
                file_part_2=os.path.basename(file_2)
                post_fix_2='.'+file_part_2.split(".")[-1]

                file_part_1=file_part_1.replace(post_fix_1,"")[len(class_name):]
                file_part_2=file_part_2.replace(post_fix_2,"")[len(class_name):]
                output_file=os.path.join(pc_root,f"{class_name}_{file_part_1}_vs_{file_part_2}.{video_save_type_str}")

                target_scoring_lfi=ExpInfo.ScoringExpLFIInfo()
                target_scoring_lfi.passive_view_video_path=output_file
                target_scoring_lfi.passive_refocusing_folder=output_file
                self.pc_show_list.AddScoringLFI(target_scoring_lfi)

                if os.path.exists(output_file):
                    logger.debug(f"File {output_file} already exists. Skip the generation.")
                    continue
                else:
                    cur_cmd=ConcatPCFilesCMD(file_1,file_2,output_file)
                    all_pc_cmds.append(cur_cmd)
        
        if len(all_pc_cmds) > 0:
            logger.debug("Print the cmds now")
            for i, cmd in enumerate(all_pc_cmds):
                logger.debug(f"index {i}, CMD: {cmd}")
            logger.info("Now making DSCS PC refinement material ...")
            self.back_thread.Reset()
            self.back_thread.SetCMDs(all_pc_cmds)
            self.session_connector=SessionConnector(len(all_pc_cmds))
            self.back_thread.cmd_value_changed.connect(self.session_connector.UpdateProgress)
            self.session_connector.task_finished.connect(self.MakeDSCSPCFinished)

            self.session_connector.show()
            self.back_thread.RunTasks()
        else:
            logger.info("All material for next session already exists. You may enter the next session now.")
            JPLMessageBox.ShowInformationMessage("All material for next session already exists. Click OK to enter next session.")
            self.StartSession(self.pc_show_list,"test")

    def MakeDSCSPCFinished(self):
        logger.info("DSCS PC tasks are done. Checking....")
        all_errors=self.back_thread.error_cmds
        if len(all_errors) > 0:
            logger.error("Some errors occured during generation.")
            logger.error("=============================================")
            for error_info in all_errors:
                logger.error(f"CMD index {error_info.idx}, CMD: {error_info.cmd}, Error: {error_info.stderr}")
            logger.error("=============================================")
        self.back_thread.Reset() 
        self.back_thread.SetCMDs([])
        self.session_connector.hide()
        self.session_connector.deleteLater()

        if len(all_errors)>0:
            JPLMessageBox.ShowErrorMessage(f"{len(all_errors)} errors occured during generation. Please check the log file.")
        else:
            JPLMessageBox.ShowInformationMessage("DSCS PC refinement material has been generated successfully. You can now go to the next session.")
            self.StartSession(self.pc_show_list,"test")
        
    
    def GetAndSaveResult(self,all_results,person_info:ExpInfo.PersonInfo,all_show_index,show_list:ExpInfo.AllScoringLFI, update_project=True,cmp_type=None,save_file=None):
        subject_name=person_info.GetName()
        self.output_folder=os.path.join(self.cur_project.project_path,PathManager.subject_results_folder)
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        logger.info("The evaluation has been finished. Now saving results to %s ..." % self.output_folder)
        if self.exp_setting.save_format == ExpInfo.SaveFormat.CSV:
            if self.exp_setting.two_folder_mode:
                if save_file is not None:
                    if ".csv" not in save_file:
                        save_file=save_file+".csv"
                self.SaveCSV_TwoFolderMode(all_results,subject_name,all_show_index,show_list,cmp_type,save_file)
            else:
                self.SaveCSV(all_results,subject_name,all_show_index,show_list)
        else:
            if self.exp_setting.two_folder_mode:
                if save_file is not None:
                    if ".xlsx" not in save_file:
                        save_file=save_file+".xlsx"
                self.SaveExcel_TwoFolderMode(all_results,subject_name,all_show_index,show_list,cmp_type,save_file)
            else:
                self.SaveExcel(all_results,subject_name,all_show_index,show_list)

        if update_project:
            self.show()
            self.cur_project.subject_list.append(subject_name)
            save_file=os.path.join(self.output_folder,PathManager.all_subject_info_file)
            person_info.AppendToCSV(save_file)
            self.cur_project.SaveToFile()
            #self.ShowProjectSetting()
            self.SetProject(self.cur_project_name)
    
    def SaveExcel_TwoFolderMode(self,all_results,subject_name,all_show_index,show_list:ExpInfo.AllScoringLFI,cmp_type=None,save_file=None):
        if save_file is None:
            save_file=os.path.join(self.output_folder,subject_name+'.xlsx')
        workbook=xlsxwriter.Workbook(save_file)
        worksheet=workbook.add_worksheet(subject_name)
        worksheet.write(0,0,'Image Index') 
        worksheet.write(0,1,'Image Path')
        all_score_names=self.exp_setting.score_names
        if cmp_type is None:
            cmp_type=self.exp_setting.comparison_type
        if cmp_type != ExpInfo.ComparisonType.PairComparison:
            for i,score_name in enumerate(all_score_names):
                worksheet.write(0,i+2,score_name)
            for i, scoring_index in enumerate(all_show_index):
                cur_scoring_lfi_info=show_list.GetScoringExpLFIInfo(scoring_index)
                worksheet.write(i+1,0,scoring_index)
                worksheet.write(i+1,1,cur_scoring_lfi_info.passive_view_video_path)
                for k in range(len(all_score_names)):
                    worksheet.write(i+1,k+2,all_results[i][k])
        else:
            worksheet.write(0,2,"Pair Comparison")
            for i, scoring_index in enumerate(all_show_index):
                cur_scoring_lfi_info=show_list.GetScoringExpLFIInfo(scoring_index)
                worksheet.write(i+1,0,scoring_index)
                worksheet.write(i+1,1,cur_scoring_lfi_info.passive_view_video_path)
                worksheet.write(i+1,2,all_results[0][i])
        workbook.close()
    
    def SaveExcel(self,all_results,subject_name,all_show_index,show_list:ExpInfo.AllScoringLFI):
        save_file=os.path.join(self.output_folder,subject_name+'.xlsx')
        workbook=xlsxwriter.Workbook(save_file)
        worksheet=workbook.add_worksheet(subject_name)
        worksheet.write(0,0,'Image Index') 
        worksheet.write(0,1,'Image Name')
        all_score_names=self.exp_setting.score_names
        if self.exp_setting.comparison_type != ExpInfo.ComparisonType.PairComparison:
            worksheet.write(0,2,'distortion')
            for i,score_name in enumerate(all_score_names):
                worksheet.write(0,i+3,score_name)
            for i,scoring_index in enumerate(all_show_index):
                cur_scoring_lfi_info=show_list.GetScoringExpLFIInfo(scoring_index)
                cur_img_name=cur_scoring_lfi_info.lfi_name
                distortion=cur_scoring_lfi_info.exp_name
                worksheet.write(i+1,0,scoring_index)
                worksheet.write(i+1,1,cur_img_name)
                worksheet.write(i+1,2,distortion)
                for k in range(len(all_score_names)):
                    worksheet.write(i+1,k+3,all_results[i][k])
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
    
    def SaveCSV_TwoFolderMode(self,all_results,subject_name,all_show_index,show_list:ExpInfo.AllScoringLFI,cmp_type=None,save_file=None):
        if save_file is None:
            save_file=os.path.join(self.output_folder,subject_name+'.csv')
        with open(save_file,'w') as fid:
            fid.write("Image Index, Image Path")
            all_score_names=self.exp_setting.score_names
            if cmp_type is None:
                cmp_type=self.exp_setting.comparison_type
            if cmp_type != ExpInfo.ComparisonType.PairComparison:
                for i,score_name in enumerate(all_score_names):
                    fid.write(",%s" %score_name)
                fid.write('\n')
                for i, scoring_index in enumerate(all_show_index):
                    cur_scoring_lfi_info=show_list.GetScoringExpLFIInfo(scoring_index)
                    fid.write("{},{}".format(scoring_index,cur_scoring_lfi_info.passive_view_video_path))
                    for k in range(len(all_score_names)):
                        fid.write(",%d" %all_results[i][k])
                    fid.write('\n')
            else:
                fid.write(",Pair Comparison\n")
                for i, scoring_index in enumerate(all_show_index):
                    cur_scoring_lfi_info=show_list.GetScoringExpLFIInfo(scoring_index)
                    fid.write("{},{},{}\n".format(scoring_index,cur_scoring_lfi_info.passive_view_video_path,all_results[0][i]))
        
    
    def SaveCSV(self,all_results,subject_name,all_show_index,show_list:ExpInfo.AllScoringLFI):
        save_file=os.path.join(self.output_folder,subject_name+'.csv')
        with open(save_file,'w') as fid:
            fid.write('Image Index,Image Name')
            all_score_names=self.exp_setting.score_names
            if self.exp_setting.comparison_type != ExpInfo.ComparisonType.PairComparison:
                fid.write(',distortion')
                for i,score_name in enumerate(all_score_names):
                    fid.write(",%s" %score_name)
                fid.write('\n')
                for i, scoring_index in enumerate(all_show_index):
                    cur_scoring_lfi_info=show_list.GetScoringExpLFIInfo(scoring_index)
                    cur_img_name=cur_scoring_lfi_info.lfi_name
                    distortion=cur_scoring_lfi_info.exp_name
                    fid.write("{},{},{}".format(scoring_index,cur_img_name,distortion))
                    for k in range(len(all_score_names)):
                        fid.write(",%d" %all_results[i][k])
                    fid.write('\n')
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

    def SetCustomFont(self,font_target):
        if  self.cur_project is None:
            self.ShowMessage("Please select one project first!",1)
            logger.warning('Please select one project first!')
            return

        exp_setting=self.cur_project.exp_setting
        font_size=20
        if font_target.lower() == "table":
            font_size=exp_setting.table_font_size
        if font_target.lower() == "hint_text":
            font_size=exp_setting.hint_text_font_size
        font_setting_dialog=FontSetting.FontSettingDialog(font_size=font_size)
        if font_setting_dialog.exec() == QDialog.Accepted:
            self.SetFontValue(font_target,font_setting_dialog.GetFontValue())

    def SetFontValue(self,font_target,font_value):       
        exp_setting=self.cur_project.exp_setting
        self.font_setting_dialog=None
        if font_value<=0:
            return
        if font_target.lower() == "table":
            exp_setting.table_font_size=font_value
            self.SaveProject()
            return
        if font_target.lower() == "hint_text":
            exp_setting.hint_text_font_size=font_value
            self.SaveProject()
            return

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
                if not os.path.exists(cur_lfi_scoring_info.refocusing_mask_file):
                    logger.error(f"Can not find the refocusing mask {cur_lfi_scoring_info.refocusing_mask_file}! The active refocusing needs a depth image to map your clicking position to a certain refocusing image. Please check your data carefully. Quit now...")
                    return False
                all_depth_value=cur_lfi_scoring_info.GetAllPossibleMaskVal()
                for depth_value in all_depth_value:
                    image_name=os.path.join(show_refocus_path,f'{depth_value}.{cur_lfi_scoring_info.img_post_fix}')
                    if not os.path.exists(image_name):
                        logger.error("Can not find the image %s! Please check yor files carefully. The experiment will be cancelled. Quit now..." % image_name)
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
