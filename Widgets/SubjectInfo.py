import sys
sys.path.append('../UI')
from SubjectInfo_ui import Ui_SubjectIfo

from PySide6 import QtWidgets, QtCore, QtGui
import logging
logger = logging.getLogger("LogWindow")

class SubjectInfo(QtWidgets.QDialog,Ui_SubjectIfo):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.lineEdit_list={
            'name': self.lineEdit_name,
            'gender': self.lineEdit_gender,
            'age': self.lineEdit_age,
            'job': self.lineEdit_job
        }

        self.lineEdit_age.setValidator(QtGui.QIntValidator(1, 100, self.lineEdit_age))

    def accept(self):
        if self.CheckInput():
            super().accept()
        else:
            return
    
    def GetResult(self):
        subject_info={}
        for key,line_editor in self.lineEdit_list.items():
            subject_info[key]=line_editor.text()
        subject_info['age']=int(subject_info['age'])
        return subject_info

    def CheckInput(self):
        for key,line_editor in self.lineEdit_list.items():
            if line_editor.text()=='':
                logger.warning(f"The {key} is empty.")
                QtWidgets.QMessageBox.warning(self, "Warning", f"The {key} is empty.")   
                return False
        return True

class PersonInfo:
    def __init__(self) -> None:
        self.name=None
        self.age=None
        self.job=None
        self.gender=None

        self.subject_info={
            'name':self.name,
            'gender':self.gender,
            'age':self.age,
            'job':self.job

        }
    
    def GetName(self):
        return self.name
    
    def GetAge(self):
        return self.age
    
    def GetJob(self):
        return self.job
    
    def GetGender(self):
        return self.gender
    
    def InitWithSubjectInfo(self,subject_info):
        self.subject_info=subject_info
        self.age=int(subject_info['age'])
        self.gender=subject_info['gender']
        self.name=subject_info['name']
        self.job=subject_info['job']
    
    def AppendToCSV(self,file_name):
        with open(file_name,'a+') as fid:
            fid.write(f"Name:, {self.name}\n")
            fid.write(f'Gender:,{self.gender}\n')
            fid.write(f'Age:,{self.age}\n')
            fid.write(f'Job:,{self.job}\n')
            fid.write('\n')


if __name__ == '__main__':
    app = QtWidgets.QApplication()
    window = SubjectInfo()
    if window.exec() == QtWidgets.QDialog.Accepted:
        print(window.GetResult())
    else:
        print('Cancelled')
    sys.exit(app.exec())

