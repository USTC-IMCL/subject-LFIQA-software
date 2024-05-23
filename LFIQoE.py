import sys
import os
sys.path.append('./Widgets')
sys.path.append('./UI')
sys.path.append('./Utils')
os.environ['PATH']+=';./'
from PySide6 import QtWidgets
import MainProject


if __name__ == '__main__':
    app = QtWidgets.QApplication()
    window = MainProject.MainProject()
    window.show()
    sys.exit(app.exec())
    
