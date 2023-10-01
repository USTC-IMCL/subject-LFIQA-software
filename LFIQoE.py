import sys
sys.path.append('./Widgets')
sys.path.append('./UI')
from Log_Form import *
from PySide6 import QtWidgets, QtCore, QtGui


if __name__ == '__main__':
    app = QtWidgets.QApplication()
    window = LogForm()
    window.show()
    sys.exit(app.exec())