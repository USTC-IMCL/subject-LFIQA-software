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
    clicked = QtCore.Signal(int)
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
        self.setStyleSheet("background-color: gray;")
        self.is_selected=True
        if self.animation:
            self.icon_label.setPixmap(QtGui.QPixmap(self.active_icon).scaled(self.icon_width,self.icon_height))
        self.clicked.emit(self.index)

    def DeActive(self):
        self.is_selected=False
        self.setStyleSheet("background-color: lightgray;")
        if self.animation:
            self.icon_label.setPixmap(QtGui.QPixmap(self.deactive_icon).scaled(self.icon_width,self.icon_height))

class ProjectDisplay(QtWidgets.QFrame):
    def __init__(self,cur_project: ProjectInfo=None, parent=None):
        super(ProjectDisplay,self).__init__(parent=parent)

        self.main_layout=QtWidgets.QHBoxLayout()
        self.setLayout(self.main_layout)

        #self.h_splitter=QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal,self)
        #self.main_layout.addWidget(self.h_splitter)

        self.left_panel=QtWidgets.QWidget(self)
        self.left_panel.setStyleSheet("background-color: lightgray;")
        self.left_panel.setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Expanding)
        self.left_panel.setFixedWidth(150)
        self.main_layout.addWidget(self.left_panel)

        self.right_stack=QtWidgets.QStackedWidget(self)
        self.right_stack.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,QtWidgets.QSizePolicy.Policy.Expanding)
        self.main_layout.addWidget(self.right_stack)

        self.main_layout.setStretch(1,1)

        self.right_stack.addWidget(QtWidgets.QWidget())

        self.MakeRightPanel()
        self.MakeLeftPanel()

    def MakeLeftPanel(self):
        self.left_panel_layout=QtWidgets.QVBoxLayout()
        self.left_panel_layout.setContentsMargins(0,0,0,0)
        self.left_panel_layout.setSpacing(3)
        self.left_panel_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.left_panel.setLayout(self.left_panel_layout)

        panel_width=self.left_panel.width()

        self.all_menu_labels=[]
        self.label_material=ProjectMenuLabel(0)
        self.label_material.setFixedSize(panel_width,panel_width)
        self.left_panel_layout.addWidget(self.label_material)
        self.label_material.setToolTip("The training and testing material")
        self.label_material.SetIcons(u":/icons/res/folder_close.svg",u":/icons/res/folder_open.svg")
        self.label_material.clicked.connect(lambda index: self.ActivateMenuLabel(index))
        self.all_menu_labels.append(self.label_material)

        self.label_setting=ProjectMenuLabel(1)
        self.label_setting.setFixedSize(panel_width,panel_width)
        self.label_setting.setToolTip('Setting the project and experiment')
        self.label_setting.SetIcons(u':/icons/res/setting.svg')
        self.left_panel_layout.addWidget(self.label_setting)
        self.label_setting.clicked.connect(lambda index: self.ActivateMenuLabel(index))
        self.all_menu_labels.append(self.label_setting)

        self.label_subjects=ProjectMenuLabel(2)
        self.label_subjects.setFixedSize(panel_width,panel_width)
        self.label_subjects.SetIcons(u':/icons/res/subject.png')
        self.label_subjects.setToolTip("Manage your subjects here.")
        self.label_subjects.clicked.connect(lambda index: self.ActivateMenuLabel(index))
        self.left_panel_layout.addWidget(self.label_subjects)
        self.all_menu_labels.append(self.label_subjects)

    def MakeRightPanel(self):
        self.MakeMaterialWidget()
        self.MakeSettingWidget()

    def MakeMaterialWidget(self):
        right_stack_width=self.right_stack.width()
        right_stack_height=self.right_stack.height()

        self.material_widget=QtWidgets.QTabWidget()
        self.right_stack.addWidget(self.material_widget)
        self.material_widget.setGeometry(0,0,right_stack_width,right_stack_height)

        self.material_widget.addTab(QtWidgets.QFrame(),u"Training")
        self.material_widget.addTab(QtWidgets.QFrame(),u"Testing")

    def MakeSettingWidget(self):
        self.right_stack.addWidget(QtWidgets.QFrame())
        cur_widget=self.right_stack.widget(2) #currentWidget()
        cur_widget.setStyleSheet("background-color: lightblue;")
        
    def MakeSubjectsWidget(self):
        self.right_stack.addWidget(QtWidgets.QFrame())


    def ActivateMenuLabel(self,index):
        self.right_stack.setCurrentIndex(index+1)
        for label in self.all_menu_labels:
            if label.index==index:
                continue
            else:
                label.DeActive()


if __name__ == "__main__":
    app=QtWidgets.QApplication()

    project_display=ProjectDisplay()
    project_display.resize(800,600)
    project_display.show()

    sys.exit(app.exec())