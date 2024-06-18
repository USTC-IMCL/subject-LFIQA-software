from PySide6 import QtWidgets
from PySide6 import QtCore
import sys
sys.path.append('../UI')
import FontSetting_ui

class FontSettingDialog(QtWidgets.QDialog,FontSetting_ui.Ui_Dialog):
    on_confirm = QtCore.Signal(int)
    def __init__(self, parent=None, font_size=20):
        super().__init__(parent)
        self.setupUi(self)
        self.font_spinbox.setValue(font_size)
    
    def accept(self):
        if self.CheckInput():
            self.on_confirm.emit(self.font_spinbox.value()) 
            self.deleteLater()
        else:
            QtWidgets.QErrorMessage(self).showMessage("Please input a number between 1 and 100 !")
    
    def reject(self):
        self.on_confirm.emit(0)
        self.deleteLater()

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
    window.on_confirm.connect(lambda x: print(x))
    window.show()

    sys.exit(app.exec())