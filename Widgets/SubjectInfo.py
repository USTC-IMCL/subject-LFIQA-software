import sys
sys.path.append('../UI')
sys.path.append('../Utils')
from SubjectInfo_ui import Ui_SubjectIfo
from ExpInfo import PersonInfo

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




if __name__ == '__main__':
    app = QtWidgets.QApplication()
    window = SubjectInfo()
    if window.exec() == QtWidgets.QDialog.Accepted:
        print(window.GetResult())
    else:
        print('Cancelled')
    sys.exit(app.exec())

