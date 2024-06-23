from PySide6 import QtWidgets
from PySide6 import QtCore
import sys
sys.path.append('../UI')
import FontSetting_ui

class FontSettingDialog(QtWidgets.QDialog,FontSetting_ui.Ui_Dialog):
    def __init__(self, parent=None, font_size=20):
        super().__init__(parent)
        self.setupUi(self)
        self.font_value=font_size
        self.font_spinbox.setValue(font_size)

    def accept(self):
        if not self.CheckInput():
            QtWidgets.QErrorMessage(self).showMessage("Please input a number between 1 and 100 !")
            return
        else:
            self.font_value=self.font_spinbox.value()
            return super().accept()
    
    def GetFontValue(self):
        return self.font_value

    def CheckInput(self): 
        input_val=self.font_spinbox.value()
        if input_val<=0:
            self.font_spinbox.setValue(1)
            return False
        if input_val>101:
            self.font_spinbox.setValue(100)
            return False
        return True
    
    def SetValue(self,font_size):
        self.font_spinbox.setValue(font_size)
    

if __name__ == "__main__":
    app = QtWidgets.QApplication()
    window = FontSettingDialog()
    if window.exec()== QtWidgets.QDialog.Accepted:
        print('ok')
        print(window.font_value)
    else:
        print('cancelled')
    sys.exit(app.exec())