import sys
from PySide6 import QtWidgets,QtCore, QtGui
from PySide6.QtWidgets import QSizePolicy
sys.path.append('../Utils')
sys.path.append('../UI')
import UI_res_rc

from ExpInfo import ProjectInfo

class ProjectMenuLabel(QtWidgets.QFrame):
    '''
    A box containing an icon
    '''
    clicked = QtCore.Signal()
    def __init__(self,index,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.index=index
        self.icon_label=QtWidgets.QLabel(self)
        self.is_selected=False
        self.active_icon=None
        self.deactive_icon=None
        self.animation=False
        self.icon_width=100
        self.icon_height=100
    
    def SetIcons(self,deactive_icon,active_icon=None):
        self.deactive_icon=deactive_icon
        self.active_icon=active_icon
        self.icon_label.setGeometry((self.width()-self.icon_width)//2,(self.height()-self.icon_height)//2,self.icon_width,self.icon_height)
        self.icon_label.setPixmap(QtGui.QPixmap(self.deactive_icon).scaled(self.icon_width,self.icon_height))
        if self.active_icon is None or (self.active_icon == self.deactive_icon):
            self.animation=False
        else:
            self.animation=True
    
    def mousePressEvent(self, event):
        self.setStyleSheet("background-color: lightblue;")
        self.is_selected=True
        if self.animation:
            self.icon_label.setPixmap(QtGui.QPixmap(self.active_icon).scaled(self.icon_width,self.icon_height))
        self.clicked.emit()

    def DeActive(self):
        self.is_selected=False
        self.setStyleSheet("background-color: white;")
        if self.animation:
            self.icon_label.setPixmap(QtGui.QPixmap(self.deactive_icon).scaled(self.icon_width,self.icon_height))

class ProjectDisplay(QtWidgets.QFrame):
    def __init__(self,cur_project: ProjectInfo=None, parent=None):
        super(ProjectDisplay,self).__init__(parent=parent)

        self.main_layout=QtWidgets.QHBoxLayout()
        self.setLayout(self.main_layout)

        #self.h_splitter=QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal,self)
        #self.main_layout.addWidget(self.h_splitter)

        self.left_panel=QtWidgets.QScrollArea(self)
        self.left_panel.setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Expanding)
        self.left_panel.setFixedWidth(150)
        self.main_layout.addWidget(self.left_panel)

        self.right_stack=QtWidgets.QStackedWidget(self)
        self.right_stack.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,QtWidgets.QSizePolicy.Policy.Expanding)
        self.main_layout.addWidget(self.right_stack)

        self.right_stack.addWidget(QtWidgets.QLabel("test"))

        self.MakeLeftPanel()
        self.MakeRightPanel()

    def MakeLeftPanel(self):
        self.left_panel_layout=QtWidgets.QVBoxLayout()
        self.left_panel_layout.setContentsMargins(0,0,0,0)
        self.left_panel_layout.setSpacing(3)

        panel_width=self.left_panel.width()-2*v_space

        self.label_material=ProjectMenuLabel(0,self.left_panel)
        self.label_material.setGeometry(v_space,v_space,panel_width,panel_width)
        self.label_material.setToolTip("The training and testing material")
        self.label_material.SetIcons(u":/icons/res/folder_close.svg",u":/icons/res/folder_open.svg")

        self.label_setting=ProjectMenuLabel(1,self.left_panel)
        self.label_setting.setFixedSize(panel_width,panel_width)
        self.label_setting.setToolTip('Setting the project and experiment')
        self.label_setting.SetIcons(u':/icons/res/setting.svg')

        self.label_subjects=ProjectMenuLabel(2,self.left_panel)
        self.label_subjects.SetIcons(u':/icons/res/subject.png')
        self.label_subjects.setToolTip("Manage your subjects here.")

    def MakeRightPanel(self):
        pass

if __name__ == "__main__":
    app=QtWidgets.QApplication()

    project_display=ProjectDisplay()
    project_display.resize(800,600)
    project_display.show()

    sys.exit(app.exec())