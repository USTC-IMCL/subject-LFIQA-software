import os
import sys
sys.path.append('../UI')
from PySide6.QtWidgets import QWidget, QDockWidget, QMainWindow, QTextBrowser, QApplication
from PySide6.QtCore import Qt
from LogWindow import QLogTextEditor
from MainProject_ui import Ui_MainWindow

class MainProject(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.make_dock_widget()
        self.text_browser=QTextBrowser()
        self.setCentralWidget(self.text_browser)
        
    def ShowProjectSetting(self):
        pass

    def make_dock_widget(self):
        self.log_dock = QDockWidget("Logs", self)
        self.log_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea | Qt.BottomDockWidgetArea)
        self.log_text_editor=QLogTextEditor()
        self.log_text_editor.setStyleSheet("background: gray;\ncolor: rgb(255, 255, 255);")
        self.log_dock.setWidget(self.log_text_editor)
        self.addDockWidget(Qt.RightDockWidgetArea, self.log_dock)
        self.menuView.addAction(self.log_dock.toggleViewAction())

    
if __name__ == "__main__":
    app=QApplication()
    main_window=MainProject()
    main_window.show()
    sys.exit(app.exec())
