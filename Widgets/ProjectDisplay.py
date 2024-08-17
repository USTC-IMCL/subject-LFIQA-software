import sys
from PySide6 import QtWidgets,QtCore, QtGui
from PySide6.QtWidgets import QSizePolicy
sys.path.append('../Utils')
sys.path.append('../UI')
import UI_res_rc
from ExpInfo import ProjectInfo, AllScoringLFI, ScoringExpLFIInfo

class ImageUnit(QtWidgets.QFrame):
    def __init__(self, unit_info:ScoringExpLFIInfo=None, img_size=[80,80], *args,**kwargs) -> None:
        super().__init__(*args,**kwargs)
        self.scoring_info=unit_info

        self.label_layout=QtWidgets.QVBoxLayout()
        self.setLayout(self.label_layout)

        self.logo_label=QtWidgets.QLabel(self)
        self.logo_title_label=QtWidgets.QLabel(self)

        self.logo_label.setPixmap(QtGui.QPixmap(":/icons/res/icon_add.png"))
        self.logo_label.setGeometry(QtCore.QRect(0, 0, 80, 80))

        self.logo_title_label.setText('Add New')
        self.logo_title_label.adjustSize()
        title_label_width=self.logo_title_label.width()
        title_label_height=self.logo_title_label.height()
        self.logo_title_label.setGeometry(QtCore.QRect((img_size[1]-title_label_width)//2, 80, title_label_width, title_label_height))
    

class MaterialFolderFrame(QtWidgets.QFrame):
    def __init__(self, unit_list: AllScoringLFI, *args,**kwargs) -> None:
        super().__init__(*args,**kwargs)
        self.resize(800,600)
        self.unit_size=[100,100] # height x width
        self.unit_list=unit_list
        self.unit_list_labels=[]
        self.h_space=10
        self.v_space=10
        self.unit_col_num=0

        self.item_index=[None]*(1+self.unit_list.exp_lfi_info_num) #[[row, col]]
        self.item_pos=[None]*(1+self.unit_list.exp_lfi_info_num) #[height,width]
        self.need_update=True

        self.MakeUnitLabels()
        self.UpdateLabelPos()
    
    def MakeColRowIndex(self):
        old_unit_col_num=self.unit_col_num
        self.unit_col_num=(self.width()+self.h_space)//(self.unit_size[1]+self.h_space)
        if self.unit_col_num < 1:
            self.unit_col_num=1
        if old_unit_col_num == self.unit_col_num:
            self.need_update=False
            return
        
        for list_index in range(self.unit_list.exp_lfi_info_num+1):
            row=list_index//self.unit_col_num
            col=list_index-row*self.unit_col_num
            self.item_index [list_index]=[row,col]
            self.item_pos[list_index]=[row*(self.unit_size[0]+self.h_space),col*(self.unit_size[1]+self.h_space)]
    
    def MakeUnitLabels(self):
        self.unit_list_labels.append(ImageUnit(parent=self))
        for i in range(self.unit_list.exp_lfi_info_num):
            self.unit_list_labels.append(ImageUnit(unit_info=self.unit_list.GetScoringExpLFIInfo(i),parent=self))

    def UpdateLabelPos(self):
        self.MakeColRowIndex()
        print(f'now colnum is {self.unit_col_num}')
        if self.need_update:
            self.need_update=False
            for i in range(self.unit_list.exp_lfi_info_num+1):
                self.unit_list_labels[i].setGeometry(self.item_pos[i][1],self.item_pos[i][0],self.unit_size[1],self.unit_size[0])

    def resizeEvent(self, event):
        print('resized')
        self.need_update=True
        self.UpdateLabelPos()


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

        self.cur_project=cur_project

        self.main_layout=QtWidgets.QHBoxLayout()
        self.setLayout(self.main_layout)

        #self.h_splitter=QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal,self)
        #self.main_layout.addWidget(self.h_splitter)

        self.left_panel=QtWidgets.QWidget(self)
        self.left_panel.setStyleSheet("background-color: lightgray;")
        self.left_panel.setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Expanding)
        self.left_panel.setFixedWidth(150)
        self.main_layout.addWidget(self.left_panel)

        self.right_stack_splitter=QtWidgets.QSplitter(QtCore.Qt.Orientation.Vertical,self)
        self.main_layout.addWidget(self.right_stack_splitter)

        self.right_stack=QtWidgets.QStackedWidget(self)
        self.right_stack.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,QtWidgets.QSizePolicy.Policy.Expanding)
        #self.main_layout.addWidget(self.right_stack)

        self.right_text_editor=QtWidgets.QTextEdit()
        self.right_text_editor.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,QtWidgets.QSizePolicy.Policy.Expanding)

        self.right_stack_splitter.addWidget(self.right_stack)
        self.right_stack_splitter.addWidget(self.right_text_editor)

        self.right_stack_splitter.setSizes([self.height()*0.8,self.height()*0.2])

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

    project_info=ProjectInfo('test_1','../Projects/')

    material_frame=MaterialFolderFrame(project_info.training_scoring_lfi_info)

    material_frame.show()


    sys.exit(app.exec())