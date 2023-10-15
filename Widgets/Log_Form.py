import sys
from time import sleep
from random import shuffle
sys.path.append('../UI')
from Log_UI_ui import Ui_LogForm as LogForm
from AboutForm_ui import Ui_AboutForm as AboutForm
from ExpInfo import *
from ScoringWidget import *
from Config_Form import CreateNewExperiment
#from Log_UI_ui import Ui_LogForm as logui
from PySide6 import QtWidgets, QtCore, QtGui
import PreProcess
import xlsxwriter
from PostProcess import PostProcess
from PySide6.QtCore import QObject, Signal, QThread

class AboutForm(QtWidgets.QWidget,AboutForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

class PreProcessThread(QObject):
    sub_task_finished=Signal(int,str)
    total_finished=Signal()

    def __init__(self,training_LFI_info,test_LFI_info,exp_setting):
        super().__init__()
        self.training_LFI_info=training_LFI_info
        self.test_LFI_info=test_LFI_info
        self.exp_setting=exp_setting

    def run(self):
        self.sub_task_finished.emit(0,"Now start training data preprocessing")
        if self.training_LFI_info is not None:
            training_preprocess=PreProcess.ExpPreprocessing(self.training_LFI_info,self.exp_setting)
            training_preprocess.mode="training"
            training_show_list=GetShowList(self.training_LFI_info,self.exp_setting,mode="training")
            training_preprocess.show_list=training_show_list
            training_preprocess.Run()
        else:
            self.sub_task_finished.emit(50,"The training data is None, skip the stage...")
            sleep(2)

        self.sub_task_finished.emit(50,"Now start test data preprocessing")
        if self.test_LFI_info is not None:
            test_preprocess=PreProcess.ExpPreprocessing(self.test_LFI_info,self.exp_setting)
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
        
class LogForm(QtWidgets.QWidget,LogForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.button_exit.clicked.connect(self.BtnExitClick)
        self.button_about.clicked.connect(self.BtnAboutClick)
        self.button_new_experiment.clicked.connect(self.BtnNewExperimentClick)
        self.button_post_processing.clicked.connect(self.BtnPostProcessClick)
        self.training_LFI_info=None
        self.test_LFI_info=None
        self.exp_setting=None

        self.about_form=AboutForm()
        self.New_Experiment = None
        self.config_file_post='lfqoe'

        self.exp_mode="training"

        self.button_start_training.clicked.connect(lambda: self.StartExperiment('training'))
        self.button_start_test.clicked.connect(lambda: self.StartExperiment('test'))

    def StartExperiment(self,mode='training'):
        self.exp_mode=mode
        if self.Preprocess(True) is None:
            return
        else:
            self._StartExp()

    def _StartExp(self):
        mode=self.exp_mode
        subject_name, ok = QtWidgets.QInputDialog.getText(self, 'Subject Recorder', 'Enter your name:')
        if not ok:
            return
        if not subject_name:
            tmp=QtWidgets.QErrorMessage(self)
            tmp.setWindowTitle('Error')
            tmp.showMessage('Do not allowed empty name, nothing will be recorded.')
            return

        if mode == "training":
            show_list=GetShowList(self.training_LFI_info,self.exp_setting,"training")
            score_info=self.training_LFI_info
            show_index=list(range(len(show_list)))
            new_show_list=show_list
        else:
            show_list=GetShowList(self.test_LFI_info,self.exp_setting,"test")
            score_info=self.test_LFI_info
            show_index,new_show_list=self.GetRandomShowList(show_list)
        
        if self.exp_setting.comparison_type ==  ComparisonType.PairComparison:
            score_page=PairWiseScoringWidget(score_info,self.exp_setting,new_show_list)
        else:
            score_page=ScoringWidget(score_info,self.exp_setting,new_show_list)

        self.hide()
        score_page.show()
        score_page.scoring_finished.connect(lambda all_results: self.GetAndSaveResult(all_results,subject_name,show_index,show_list))
    
    def GetAndSaveResult(self,all_results,subject_name,show_index,show_list):
        self.output_folder='./'
        if not os.path.exists(self.output_folder):
            os.mkdir(self.output_folder)
        if self.exp_setting.save_format == SaveFormat.CSV:
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

        if self.exp_setting.comparison_type != ComparisonType.PairComparison:
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
            if LFIFeatures.Active_ViewChanging in self.exp_setting.lfi_features and LFIFeatures.Active_Refocusing in self.exp_setting.lfi_features:
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
                    if all_results[0] is not None:
                        save_array.append(view_changing_score[i])
                    if all_results[1] is not None:
                        save_array.append(refocusing_score[i])

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
        save_file='./'+subject_name+'.csv'
        with open(save_file,'w') as fid:
            fid.write('Image Index,Image Name')
            
            if self.exp_setting.comparison_type != ComparisonType.PairComparison:
                fid.write(',distortion,Image Quality Score, Overall Score\n')
                for i in range(len(show_index)):
                    cur_img_name=show_list[i][0]
                    distortion=show_list[i][1]+'_'+str(show_list[i][2])
                    fid.write(f'{show_index[i]},{cur_img_name},{distortion},{all_results[i][0]},{all_results[i][1]}\n')
            else:
                view_changing_score=all_results[0]
                refocusing_score=all_results[1]
                if LFIFeatures.Active_ViewChanging in self.exp_setting.lfi_features and LFIFeatures.Active_Refocusing in self.exp_setting.lfi_features:
                    fid.write(',Overall Score\n')
                    for i in range(len(show_index)):
                        tmp=[str(x) for x in show_list[i]]
                        cur_img_name='_'.join(tmp)
                        fid.write(f'{show_index[i]},{cur_img_name},{view_changing_score[i]}\n')
            
                else:
                    save_array=[]
                    for i in range(len(show_index)):
                        if all_results[0] is not None:
                            save_array.append(view_changing_score[i])
                        if all_results[1] is not None:
                            save_array.append(refocusing_score[i])

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

    def BtnAboutClick(self):
        self.about_form.show()

    def BtnPostProcessClick(self):
        folder_name=QtWidgets.QFileDialog.getExistingDirectory(self,'select the Output Folder','./')
        project_file=QtWidgets.QFileDialog.getOpenFileName(self,'Open Project File','./',f'*.{self.config_file_post}')[0]

        training_lfi_info,test_lfi_info,exp_setting=ReadExpConfig(project_file)
        PostProcess(exp_setting,folder_name)
    
    def BtnExitClick(self):
        self.about_form.close()
        self.close()
    
    def BtnNewExperimentClick(self):
        self.hide()
        self.New_Experiment=CreateNewExperiment()
        self.New_Experiment.show()
        self.New_Experiment.CancelClosed.connect(self.CreateCanceled)
        self.New_Experiment.Finished.connect(self.CreateFinished)

    def Preprocess(self,start_exp):
        self.start_exp=start_exp
        self.exp_config_file=QtWidgets.QFileDialog.getOpenFileName(self,'Open Experiment Config File','./',f'*.{self.config_file_post}')[0]
        if self.exp_config_file=='':
            return None
        
        training_LFI_info,test_LFI_info,exp_setting=ReadExpConfig(self.exp_config_file)
        self.training_LFI_info=training_LFI_info
        self.test_LFI_info=test_LFI_info
        self.exp_setting=exp_setting
        #exp_setting.has_preprocess=False
        if exp_setting.has_preprocess:
            return True

        self.preprocessing_dialog=QtWidgets.QProgressDialog(self)
        self.preprocessing_dialog.setWindowTitle('Now Preprocessing')
        self.preprocessing_dialog.setValue(0)
        self.preprocessing_dialog.setLabelText('It may take 10 minuts, please wait...')
        self.preprocessing_dialog.setCancelButton(None)
        self.preprocessing_dialog.setWindowModality(QtCore.Qt.WindowModal)
        self.preprocessing_dialog.show()

        self.preprocessing_thread=QThread(self)
        self.preprocessing_worker=PreProcessThread(training_LFI_info,test_LFI_info,exp_setting)
        self.preprocessing_worker.moveToThread(self.preprocessing_thread)
        self.preprocessing_worker.sub_task_finished.connect(lambda i, s: self.SetPreprocessingDialog(self.preprocessing_dialog,i,s))
        self.preprocessing_worker.total_finished.connect(self.PreprosessingFinishedCallback)
        self.preprocessing_thread.started.connect(self.preprocessing_worker.run)

        self.preprocessing_thread.start()

        '''
        if training_LFI_info is not None:
            training_preprocess=PreProcess.ExpPreprocessing(training_LFI_info,exp_setting)
        if test_LFI_info is not None:
            test_preprocess=PreProcess.ExpPreprocessing(test_LFI_info,exp_setting)

        preprocessing_dialog.setLabelText('Now Preprocessing Training Data...')
        if training_LFI_info is not None:
            training_show_list=GetShowList(training_LFI_info,exp_setting,"training")
            training_preprocess.mode="training"
            training_preprocess.show_list=training_show_list
            training_preprocess.Run()
        preprocessing_dialog.setValue(50)

        preprocessing_dialog.setLabelText('Now Preprocessing Test Data...')
        if test_LFI_info is not None:
            test_show_list=GetShowList(test_LFI_info,exp_setting,"test")
            test_preprocess.mode="test"
            test_preprocess.show_list=test_show_list
            test_preprocess.Run()

        preprocessing_dialog.setValue(100)
        preprocessing_dialog.close()

        exp_setting.has_preprocess=True

        with open(self.exp_config_file,'wb') as fid:
            pickle.dump(training_LFI_info,fid)
            pickle.dump(test_LFI_info,fid)
            pickle.dump(exp_setting,fid)
        
        return True
        '''
    
    def PreprosessingFinishedCallback(self):
        self.exp_setting.has_preprocess=True
        with open(self.exp_config_file,'wb') as fid:
            pickle.dump(self.training_LFI_info,fid)
            pickle.dump(self.test_LFI_info,fid)
            pickle.dump(self.exp_setting,fid)
        self.preprocessing_dialog.deleteLater()
        self.preprocessing_worker.deleteLater()
        #self.preprocessing_thread.deleteLater()
        if self.start_exp:
            self._StartExp()

    def SetPreprocessingDialog(self,preprocessing_dialog:QtWidgets.QProgressDialog,i:int,show_message:str): 
        preprocessing_dialog.setLabelText(show_message)
        preprocessing_dialog.setValue(i)
    
    def CreateFinished(self,b_preprocessing_now):
        #print(b_preprocessing_now)
        self.show()
        self.New_Experiment=None
        if b_preprocessing_now:
            self.Preprocess(False)
    
    def CreateCanceled(self):
        self.show()
        self.NewExperiment=None
    

if __name__ == "__main__":
    app = QtWidgets.QApplication()
    window = LogForm()
    window.show()
    sys.exit(app.exec())
