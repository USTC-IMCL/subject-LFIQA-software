import sys
from PySide6 import QtWidgets,QtCore, QtGui
sys.path.append('../Utils')
sys.path.append('../UI')
import UI_res_rc

from ExpInfo import ProjectInfo

class ProjectMenuLabel(QtWidgets.QLabel):
    clicked = QtCore.Signal()


class ProjectDisplay(QtWidgets.QWidget):
    def __init__(self,cur_project: ProjectInfo=None, parent=None):
        super(ProjectDisplay,self).__init__(parent=parent)

        self.main_layout=QtWidgets.QHBoxLayout()
        self.setLayout(self.main_layout)

        #self.h_splitter=QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal,self)
        #self.main_layout.addWidget(self.h_splitter)

        self.left_panel=QtWidgets.QScrollArea(self)
        self.left_panel.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.left_panel.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.left_panel.setFixedWidth(150)
        self.main_layout.addWidget(self.left_panel)

        self.right_stack=QtWidgets.QStackedWidget(self)
        self.right_stack.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,QtWidgets.QSizePolicy.Policy.Expanding)
        self.main_layout.addWidget(self.right_stack)

        self.right_stack.addWidget(QtWidgets.QLabel("test"))

        self.MakeLeftPanel()
        

    def MakeLeftPanel(self):
        self.left_panel_layout=QtWidgets.QVBoxLayout()
        self.left_panel_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignHCenter)
        #self.left_panel_layout.setContentsMargins(0,25,0,25)
        self.left_panel.setLayout(self.left_panel_layout)

        self.label_imgs=QtWidgets.QLabel()
        self.label_imgs.setToolTip("The training and testing material")
        '''
        now get image from :/icons/res/folder_close.svg
        '''
        self.label_imgs.setPixmap(QtGui.QPixmap(u":/icons/res/folder_close.svg").scaled(100,100))
        self.label_imgs.mousePressEvent = lambda event: self.label_imgs.setPixmap(QtGui.QPixmap(u":/icons/res/folder_open.svg").scaled(100,100))
        self.left_panel_layout.addWidget(self.label_imgs)

        self.label_setting=QtWidgets.QLabel()
        self.label_setting.setToolTip('Setting the project and experiment')
        self.label_setting.setPixmap(QtGui.QPixmap(u":/icons/res/setting.svg").scaled(100,100))


        self.left_panel_layout.addWidget(self.label_setting)


if __name__ == "__main__":
    app=QtWidgets.QApplication()
    project_display=ProjectDisplay()

    project_display.resize(800,600)
    project_display.show()

    sys.exit(app.exec())