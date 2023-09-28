from typing import Optional
import PySide6.QtCore
import PySide6.QtWidgets
import sys
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
import xlsxreader

class AboutForm(QtWidgets.QWidget,AboutForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

class PreProcessThread(QtCore.QThread):
    def __init__(self,training_LFI_info,test_LFI_info,exp_setting):
        super().__init__()
        self.training_LFI_info=training_LFI_info
        self.test_LFI_info=test_LFI_info
        self.exp_setting=exp_setting

    def run(self):
        training_preprocess=PreProcess.ExpPreprocessing(self.training_LFI_info,self.exp_setting)
        test_preprocess=PreProcess.ExpPreprocessing(self.test_LFI_info,self.exp_setting)
        training_preprocess.Run()
        test_preprocess.Run()
        
class LogForm(QtWidgets.QWidget,LogForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.button_exit.clicked.connect(self.BtnExitClick)
        self.button_about.clicked.connect(self.BtnAboutClick)
        self.button_new_experiment.clicked.connect(self.BtnNewExperimentClick)
        self.training_LFI_info=None
        self.test_LFI_info=None
        self.exp_setting=None

        self.about_form=AboutForm()
        self.New_Experiment = None
        self.config_file_post='lfqoe'

        self.button_start_training.clicked.connect(lambda: self.StartExperiment('training'))
        self.button_start_test.clicked.connect(lambda: self.StartExperiment('test'))

    def StartExperiment(self,mode='training'):
        #self.hide()
        self.Preprocess()

        subject_name, ok = QtWidgets.QInputDialog.getText(self, 'Subject Recorder', 'Enter your name:')
        if not ok:
            return
        if not subject_name:
            tmp=QtWidgets.QErrorMessage(self)
            tmp.setWindowTitle('Error')
            tmp.showMessage('Do not allowed empty name, nothing will be recorded.')
            return

        if mode == "training":
            show_list=GetShowList(self.training_LFI_info,self.exp_setting)
            score_info=self.training_LFI_info
            show_index=list(range(len(show_list)))
            new_show_list=show_list
        else:
            show_list=GetShowList(self.test_LFI_info,self.exp_setting)
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
        if self.exp_setting.save_format == SaveFormat.CSV:
            self.SaveCSV(all_results,subject_name,show_index,show_list)
        else:
            self.SaveExcel(all_results,subject_name,show_index,show_list)
    
    def SaveExcel(self,all_results,subject_name,show_index,show_list):
        save_file='./'+subject_name+'.xlsx'
        workbood=xlsxwriter.Workbook(save_file)
        worksheet=workbood.add_worksheet(subject_name)
        worksheet.write(0,0,'Image Index') 
        worksheet.write(0,1,'Image Name')

        if self.exp_setting.comparison_type != ComparisonType.PairComparison:
            worksheet.write(0,2,'Score')
            for i in range(len(all_results)):
                worksheet.write(i+1,0,show_index[i])
                worksheet.write(i+1,1,show_list[i])
                worksheet.write(i+1,2,all_results[i])
        else:
            view_changing_score=all_results[0]
            refocusing_score=all_results[1]
            if LFIFeatures.Active_ViewChanging in self.exp_setting.lfi_features and LFIFeatures.Active_Refocusing in self.exp_setting.lfi_features:
                worksheet.write(0,2,'overall_score')
                for i in range(len(all_results)):
                    worksheet.write(i+1,0,show_index[i])
                    worksheet.write(i+1,1,show_list[i])
                    worksheet.write(i+1,2,view_changing_score[i])
            
            else:
                save_array=[]
                for i in range(len(all_results)):
                    if all_results[0] is not None:
                        save_array.append(view_changing_score[i])
                    if all_results[1] is not None:
                        save_array.append(refocusing_score[i])

                current_col=2
                if view_changing_score is not None:
                    worksheet.write(0,current_col,'view_changing_score')
                    current_col+=1
                if refocusing_score is not None:
                    worksheet.write(0,current_col,'refocusing_score')
                
                for i in range(len(all_results)):
                    worksheet.write(i+1,0,show_index[i])
                    worksheet.write(i+1,1,show_list[i])
                    current_col=2
                    for value in save_array[i]:
                        worksheet.write(i+1,current_col,value)
                        current_col+=1
        workbood.close()
    
    def SaveCSV(self,all_results,subject_name,show_index,show_list):
        save_file='./'+subject_name+'.csv'
        with open(save_file,'w') as fid:
            fid.write('Image Index,Image Name')
            
            if self.exp_setting.comparison_type != ComparisonType.PairComparison:
                fid.write(',Score\n')
                for i in range(len(all_results)):
                    fid.write(f'{show_index[i]},{show_list[i]},{all_results[i]}\n')
            else:
                view_changing_score=all_results[0]
                refocusing_score=all_results[1]
                if LFIFeatures.Active_ViewChanging in self.exp_setting.lfi_features and LFIFeatures.Active_Refocusing in self.exp_setting.lfi_features:
                    fid.write(',overall_score\n')
                    for i in range(len(all_results)):
                        fid.write(f'{show_index[i]},{show_list[i]},{view_changing_score[i]}\n')
            
                else:
                    save_array=[]
                    for i in range(len(all_results)):
                        if all_results[0] is not None:
                            save_array.append(view_changing_score[i])
                        if all_results[1] is not None:
                            save_array.append(refocusing_score[i])

                    current_col=2
                    if view_changing_score is not None:
                        fid.write(',view_changing_score')
                        current_col+=1
                    if refocusing_score is not None:
                        fid.write(',refocusing_score')
                    fid.write('\n')
                
                    for i in range(len(all_results)):
                        fid.write(f'{show_index[i]},{show_list[i]}')
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
        pass
    
    def BtnExitClick(self):
        self.about_form.close()
        self.close()
    
    def BtnStartExperimentClick(self):
        pass
    
    def BtnNewExperimentClick(self):
        self.hide()
        self.New_Experiment=CreateNewExperiment()
        self.New_Experiment.show()
        self.New_Experiment.CancelClosed.connect(self.CreateCanceled)
        self.New_Experiment.Finished.connect(self.CreateFinished)

    def Preprocess(self):
        self.exp_config_file=QtWidgets.QFileDialog.getOpenFileName(self,'Open Experiment Config File','./',f'*.{self.config_file_post}')[0]
        if self.exp_config_file=='':
            return
        
        training_LFI_info,test_LFI_info,exp_setting=ReadExpConfig(self.exp_config_file)
        self.training_LFI_info=training_LFI_info
        self.test_LFI_info=test_LFI_info
        self.exp_setting=exp_setting
        #exp_setting.has_preprocess=False
        if exp_setting.has_preprocess:
            return

        preprocessing_dialog=QtWidgets.QProgressDialog(self)
        preprocessing_dialog.setWindowTitle('Now Preprocessing')
        preprocessing_dialog.setValue(0)
        preprocessing_dialog.setLabelText('It may take 10 minuts, please wait...')
        preprocessing_dialog.setCancelButton(None)
        preprocessing_dialog.setWindowModality(QtCore.Qt.WindowModal)
        preprocessing_dialog.show()

        training_preprocess=PreProcess.ExpPreprocessing(training_LFI_info,exp_setting)
        test_preprocess=PreProcess.ExpPreprocessing(test_LFI_info,exp_setting)

        preprocessing_dialog.setLabelText('Now Preprocessing Training Data...')
        training_preprocess.Run()
        preprocessing_dialog.setValue(50)
        preprocessing_dialog.setLabelText('Now Preprocessing Test Data...')
        test_preprocess.Run()
        preprocessing_dialog.setValue(100)
        preprocessing_dialog.close()

        exp_setting.has_preprocess=True

        with open(self.exp_config_file,'wb') as fid:
            pickle.dump(training_LFI_info,fid)
            pickle.dump(test_LFI_info,fid)
            pickle.dump(exp_setting,fid)
        
    
    def CreateFinished(self,b_preprocessing_now):
        #print(b_preprocessing_now)
        self.show()
        self.New_Experiment=None
    
    def CreateCanceled(self):
        self.show()
        self.NewExperiment=None
    

if __name__ == "__main__":
    app = QtWidgets.QApplication()
    window = LogForm()
    window.show()
    sys.exit(app.exec())