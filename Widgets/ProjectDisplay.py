import sys
from PySide6 import QtWidgets

class ProjectDisplay(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(ProjectDisplay,self).__init__(parent=parent)

        self.h_layout=QtWidgets.QHBoxLayout()
        self.setLayout(self.h_layout)

        self.left_panel=QtWidgets.QScrollArea(self)
        self.h_layout.addWidget(self.left_panel,stretch=1)

        self.right_stack=QtWidgets.QStackedWidget(self)
        self.h_layout.addWidget(self.right_panel,stretch=3)

        





if __name__ == "__main__":
    app=QtWidgets.QApplication()
    project_display=ProjectDisplay()

    project_display.resize(800,600)
    project_display.show()

    sys.exit(app.exec())