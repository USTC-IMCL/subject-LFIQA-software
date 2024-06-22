import sys
sys.path.append('../UI')
from SubjectInfo_ui import Ui_SubjectIfo

from PySide6 import QtWidgets, QtCore, QtGui
import logging
logger = logging.getLogger("LogWindow")

class SubjectInfo(QtWidgets.QWidget,Ui_SubjectIfo):
    on_confirm = QtCore.Signal(dict)
    on_cancel = QtCore.Signal()
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
            subject_info={}
            for key,line_editor in self.lineEdit_list.items():
                subject_info[key]=line_editor.text()
            subject_info['age']=int(subject_info['age'])
            self.on_confirm.emit(subject_info)
            self.deleteLater()

    def reject(self):
        self.on_cancel.emit()
        self.deleteLater()
    
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
    window.show()
    window.on_confirm.connect(lambda x: print(x))
    window.on_cancel.connect(lambda: print('cancel'))
    sys.exit(app.exec())

