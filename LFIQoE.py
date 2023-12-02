import sys
sys.path.append('./Widgets')
sys.path.append('./UI')
import logging
from Log_Form import *
from PySide6 import QtWidgets, QtCore, QtGui
import MainProject


if __name__ == '__main__':
    app = QtWidgets.QApplication()
    window = MainProject.MainProject()
    window.show()
    sys.exit(app.exec())
