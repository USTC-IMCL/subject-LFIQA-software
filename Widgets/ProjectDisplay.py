import sys
from PySide6 import QtWidgets,QtCore, QtGui
from PySide6.QtWidgets import QSizePolicy
sys.path.append('../Utils')
sys.path.append('../UI')
import UI_res_rc
from ExpInfo import ProjectInfo, AllScoringLFI, ScoringExpLFIInfo, ExpSetting, FeatureType
import ExpInfo
import PathManager
import os
import shutil
import pickle
import logging
logger = logging.getLogger("LogWindow")

class NewLFISelector(QtWidgets.QFrame):
    on_cancel=QtCore.Signal()
    on_confirm=QtCore.Signal(dict)
    def __init__(self, exp_setting: ExpSetting,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exp_setting=exp_setting

        self.selector_layout=QtWidgets.QVBoxLayout()
        self.selector_layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.selector_layout)

        self.refocusing_line_editor=None
        self.view_changing_line_editor=None

        self.refocusing_path=None
        self.refocusing_video_path=None

        self.view_showing_path=None
        self.view_video_path=None

        self.refocusing_button=None
        self.view_changing_button=None

        self.ret_dict={}
        self.ret_dict['refocusing_active']=None
        self.ret_dict['refocusing_passive']=None
        self.ret_dict['view_changing_active']=None
        self.ret_dict['view_changing_passive']=None

        self.hint_label=QtWidgets.QLabel()

        if not hasattr(exp_setting, 'refocusing_type'):
            if ExpInfo.LFIFeatures.Active_Refocusing in exp_setting.lfi_features:
                refocusing_type=FeatureType.Active
            elif ExpInfo.LFIFeatures.Passive_Refocusing in exp_setting.lfi_features:
                refocusing_type=FeatureType.Passive
            else:
                refocusing_type=FeatureType.None_Type
        if not hasattr(exp_setting, 'view_changing_type'):
            if ExpInfo.LFIFeatures.Active_ViewChanging in exp_setting.lfi_features:
                view_changing_type=FeatureType.Active
            elif ExpInfo.LFIFeatures.Passive_ViewChanging in exp_setting.lfi_features:
                view_changing_type=FeatureType.Passive
            else:
                view_changing_type=FeatureType.None_Type


        if refocusing_type != FeatureType.None_Type:
            refocusing_label=QtWidgets.QLabel()
            refocusing_text_line=QtWidgets.QLineEdit()
            refocusing_layout=QtWidgets.QHBoxLayout()
            refocusing_button=QtWidgets.QPushButton('Browse')
            if refocusing_type == FeatureType.Active:
                refocusing_label.setText('Refocusing mode: Active, select the folder path: ')
            else:
                refocusing_label.setText('Refocusing mode: Passive, select the video path: ')
            
            refocusing_layout.setStretchFactor(refocusing_text_line, 8)
            refocusing_layout.setStretchFactor(refocusing_button, 2)
            refocusing_layout.addWidget(refocusing_text_line)
            refocusing_layout.addWidget(refocusing_button)

            self.selector_layout.addWidget(refocusing_label)
            self.selector_layout.addLayout(refocusing_layout)
        else:
            refocusing_text_line=None
        
        if view_changing_type != FeatureType.None_Type:
            view_changing_label=QtWidgets.QLabel()
            view_changing_text_line=QtWidgets.QLineEdit()
            view_changing_layout=QtWidgets.QHBoxLayout()
            view_changing_button=QtWidgets.QPushButton('Browse')
            if view_changing_type == FeatureType.Active:
                view_changing_label.setText('View changing mode: <font color="red">Active</font><br>Select the folder path: ')
            else:
                view_changing_label.setText('View changing mode: <font color="red">Passive</font><br>Select the video path: ')
            
            view_changing_layout.setStretchFactor(view_changing_text_line, 8)
            view_changing_layout.setStretchFactor(view_changing_button,2)
            view_changing_layout.addWidget(view_changing_text_line)
            view_changing_layout.addWidget(view_changing_button)

            self.selector_layout.addWidget(view_changing_label)
            self.selector_layout.addLayout(view_changing_layout)
        else:
            view_changing_text_line=None
        
        self.selector_layout.addWidget(self.hint_label)
        
        self.button_cancel=QtWidgets.QPushButton('Cancel')
        self.button_ok=QtWidgets.QPushButton('OK')

        self.button_cancel.clicked.connect(self.CancelClicked)
        self.button_ok.clicked.connect(self.ConfirmClicked)

        two_button_layout=QtWidgets.QHBoxLayout()
        two_button_layout.addWidget(self.button_cancel)
        two_button_layout.addWidget(self.button_ok)
        self.selector_layout.addLayout(two_button_layout)

        self.view_changing_type=view_changing_type
        self.refocusing_type=refocusing_type

        self.refocusing_line_editor=refocusing_text_line
        self.view_changing_line_editor=view_changing_text_line
        
    def ConfirmClicked(self):
        if self.refocusing_line_editor is not None:
            if self.refocusing_line_editor.text() == '':
                self.hint_label.setText('<font color="red">The path of refocusing is empty</font>')
                return
            if self.refocusing_type == FeatureType.Active:
                self.ret_dict['refocusing_active']=self.refocusing_line_editor.text()
            else:
                self.ret_dict['refocusing_passive']=self.refocusing_line_editor.text()

        if self.view_changing_type is not None:
            if self.view_changing_line_editor.text() == '':
                self.hint_label.setText('<font color="red">The path of view changing is empty</font>') 
                return
            if self.view_changing_type == FeatureType.Active:
                self.ret_dict['view_changing_active']=self.view_changing_line_editor.text()
            else:
                self.ret_dict['view_changing_passive']=self.view_changing_line_editor.text()
        
        is_valid=True
        for key in self.ret_dict.keys():
            if self.ret_dict[key] is not None:
                if not os.path.exists(self.ret_dict[key]):
                    logger.error('The path of {} does not exist, please make sure your path is correct!'.format(key))
                    error_message=f'The path of {key} does not exist!'
                    self.ret_dict[key]=None
                    is_valid=False
                    break
        
        if not is_valid:
            for key in self.ret_dict.keys():
                self.ret_dict[key]=None
            self.hint_label.setText(f'<font color="red">{error_message}</font>')
            return
        self.hide()
        self.on_confirm.emit(self.ret_dict)

    def CancelClicked(self):
        self.hide()
        logger.info('Add new LFI is cancelled.')
        self.on_cancel.emit()
        self.deleteLater()

class ImageUnit(QtWidgets.QFrame):
    clicked=QtCore.Signal()
    def __init__(self,unit_info:ScoringExpLFIInfo=None, logo_size=[80,80], icon_img=':/icons/res/icon_add.png', icon_title='New One', *args, **kwargs):
    def __init__(self,unit_info:ScoringExpLFIInfo=None, logo_size=[80,80], icon_img=':/icons/res/icon_add.png', icon_title='New One', *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.logo_size=logo_size
        self.SetBasicParam(unit_info)
        self.InitIconUI(icon_img, icon_title)
        
    def SetBasicParam(self, unit_info:ScoringExpLFIInfo=None):
        self.scoring_info=unit_info
        self.label_layout=QtWidgets.QVBoxLayout()
        self.setLayout(self.label_layout)
        self.logo_label=QtWidgets.QLabel(self)
        self.logo_title_label=QtWidgets.QLabel(self)

    def InitIconUI(self, icon_img, icon_title):
        self.logo_label.setPixmap(QtGui.QPixmap(icon_img).scaled(self.logo_size[1],self.logo_size[0]))
        self.logo_label.setGeometry(QtCore.QRect(0, 0, self.logo_size[1], self.logo_size[0]))

        self.logo_title_label.setText(icon_title)
        self.logo_title_label.setFixedWidth(self.logo_size[1])
        self.logo_title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.logo_title_label.adjustSize()
        title_label_width=self.logo_title_label.width()
        title_label_height=self.logo_title_label.height()
        self.logo_title_label.setGeometry(QtCore.QRect((self.logo_size[1]-title_label_width)//2, self.logo_size[0], title_label_width, title_label_height))
    
    def mousePressEvent(self, event):
        self.clicked.emit()
        event.ignore()
        return super().mousePressEvent(event) 

class ImageUnitInfoDisplay(QtWidgets.QFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args,**kwargs)
        self.unit_info=None
        self.unit_layout=QtWidgets.QHBoxLayout()
        self.setLayout(self.unit_layout)

        self.unit_label=QtWidgets.QLabel(self)
    
    def UpdateUnitInfo(self, unit_info:ScoringExpLFIInfo):
        pass

class MaterialFolderFrame(QtWidgets.QFrame):
    def __init__(self, unit_list: AllScoringLFI, exp_setting: ExpSetting, *args,**kwargs) -> None:
        super().__init__(*args,**kwargs)
        self.resize(800,600)
        self.unit_size=[100,100] # height x width
        self.unit_list=unit_list
        self.unit_list_labels=[] # QLabels to show the LFI info
        self.h_space=10
        self.v_space=10
        self.unit_col_num=0

        self.exp_setting=exp_setting

        self.item_index=[None]*(1+self.unit_list.exp_lfi_info_num) #[[row, col]]
        self.item_pos=[None]*(1+self.unit_list.exp_lfi_info_num) #[height,width]
        self.need_update=True

        self.project_path=None
        self.cache_root=None
        self.cache_desc_file=None
        self.folder_mode=self.unit_list.mode
        self.cache_folder=None

        self.unit_info_display=ImageUnitInfoDisplay(parent=self)
        self.add_form=None

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
        self.unit_list_labels[0].clicked.connect(self.AddNewLFI)
        for i in range(self.unit_list.exp_lfi_info_num):
            self.unit_list_labels.append(ImageUnit(unit_info=self.unit_list.GetScoringExpLFIInfo(i),icon_img=':/icons/res/image.png',icon_title=f'LFI {i}',parent=self))

    def UpdateLabelPos(self):
        self.MakeColRowIndex()
        if self.need_update:
            self.need_update=False
            for i in range(self.unit_list.exp_lfi_info_num+1):
                self.unit_list_labels[i].setGeometry(self.item_pos[i][1],self.item_pos[i][0],self.unit_size[1],self.unit_size[0])

    def resizeEvent(self, event):
        self.need_update=True
        self.UpdateLabelPos()

    def MakeCache(self, project_path):
        self.project_path=project_path
        self.folder_mode=self.unit_list.mode # training or testing

        self.cache_root=os.path.join(project_path,PathManager.cache_folder)
        if not os.path.exists(self.cache_root):
            os.makedirs(self.cache_root)
        self.cache_folder=os.path.join(self.cache_path,self.folder_mode)
        if not os.path.exists(self.cache_folder):
            os.makedirs(self.cache_folder)

        cache_file=os.path.join(self.cache_folder,PathManager.cache_desc)
        if os.path.exists(cache_file):
            with open(cache_file,'rb') as fid:
                all_mapping=pickle.load(fid)
        else:
            cache_desc_fid=open(cache_file,'wb')
            all_mapping={}

        for i in range(self.unit_list.GetLFINum()):
            cur_scoring_lfi=self.unit_list.GetScoringExpLFIInfo(i)
            cur_cache_folder=os.path.join(self.cache_folder,f'LFI_{i}')
            cur_cache_file=os.path.join(cur_cache_folder,PathManager.cache_desc)
            if not os.path.exists(cur_cache_folder):
                os.makedirs(cur_cache_folder)
            cache_img=os.path.join(cur_cache_folder,PathManager.cache_thumbnail)
            cur_scoring_lfi.MakeThumbnail(cache_img)

            cur_cache_fid=open(cur_cache_file,'wb')
            cur_mapping=[i,cur_cache_folder,cur_scoring_lfi.show_name]
            pickle.dump(cur_mapping,cur_cache_fid)
            all_mapping[i]=cur_mapping
            all_mapping[cur_scoring_lfi.show_name]=cur_mapping
            cur_cache_fid.close()
        
        pickle.dump(all_mapping,cache_desc_fid)
        cache_desc_fid.close()
    
    def AddNewLFI(self):
        self.add_form=NewLFISelector(self.exp_setting)
        self.add_form.resize(400,150)
        self.add_form.show()
        self.add_form.on_confirm.connect(self.ConfirmAddNewLFI)


    def ConfirmAddNewLFI(self,in_dict):
        '''
        in_dict:
            refocusing_active: str
            refocusing_passive: str
            view_changing_active: str
            view_changing_passive: str
        '''
        new_scoring_lfi=ScoringExpLFIInfo()
        new_scoring_lfi.active_view_path=in_dict['view_changing_active']
        new_scoring_lfi.active_refocusing_path=in_dict['refocusing_active']
        new_scoring_lfi.passive_refocusing_video_path=in_dict['refocusing_passive']
        new_scoring_lfi.passive_view_video_path=in_dict['view_changing_passive']


    def CancleAddNewLFI(self):
        self.add_form=None

    def DeleteFLI(self,index):
        pass
    
    def CheckCache(self,project_path):
        if self.cache_root is None:
            self.MakeCache(project_path)
            return
        
        if self.cache_desc_file is None or (not os.path.exists(self.cache_desc_file)):
            self.MakeCache(project_path)
            return
        
        with open(self.cache_desc_file,'rb') as fid:
            all_mapping=pickle.load(fid)
        if all_mapping is None:
            self.MakeCache(project_path)
            return
        
        if len(all_mapping) != self.unit_list.GetLFINum():
            logger.warning('The number of cache files is not matched! The number of cache files is %d, but the number of LFI is %d.'%(len(all_mapping),self.unit_list.GetLFINum()))
            logger.warning("Rebuilding cache files...")
            self.UpdateCache(project_path)
            return
        
        for i in range(self.unit_list.GetLFINum()):
            cur_mapping=all_mapping[i]
            cur_mapping_index=cur_mapping[0]
            cur_cache_folder=cur_mapping[1]
            cur_show_name=cur_mapping[2]

            if not os.path.exists(cur_cache_folder):
                logger.warning(f"The cache folder '{cur_cache_folder}' is not exist!")
                logger.warning("Rebuilding cache files...")
                self.UpdateCache(project_path)
                return
            
            if cur_mapping_index != i or cur_show_name != self.unit_list.GetScoringExpLFIInfo(i).show_name:
                logger.warning(f"The cache folder '{cur_cache_folder}' is not matched! The cache folder index is {cur_mapping_index}, but the LFI index is {i}, the cache LFI name is {cur_show_name}, but the LFI name is {self.unit_list.GetScoringExpLFIInfo(i).show_name}.")
                logger.warning("Rebuilding cache files...")
                self.UpdateCache(project_path)
                return
            
            cache_img=os.path.join(cur_cache_folder,PathManager.cache_thumbnail)
            if not os.path.exists(cache_img):
                logger.warning(f"The cache image '{cache_img}' is not exist!")
                logger.warning("Rebuilding cache files...")
                self.UpdateCache(project_path)
                return
            
            local_cache_desc_file=os.path.join(cur_cache_folder,PathManager.cache_desc)
            if not os.path.exists(local_cache_desc_file):
                logger.warning(f"The cache desc file '{local_cache_desc_file}' is not exist!")
                logger.warning("Rebuilding cache files...")
                self.UpdateCache(project_path)
                return

            with open(local_cache_desc_file,'rb') as fid:
                local_mapping=pickle.load(fid)
            if local_mapping is None:
                logger.warning(f"The cache desc file '{local_cache_desc_file}' is empty!")
                logger.warning("Rebuilding cache files...")
                self.UpdateCache(project_path)
                return
            
            local_mapping_index=local_mapping[0]
            local_cache_folder=local_mapping[1]
            local_show_name=local_mapping[2]

            if local_mapping_index != i or local_show_name != self.unit_list.GetScoringExpLFIInfo(i).show_name or local_cache_folder != cur_cache_folder:
                logger.error('Something is wrong. The local description and global record does not matche!')
                logger.warning("Rebuilding cache files...")
                self.UpdateCache(project_path)

    def UpdateCache(self,project_path):
        with open(self.cache_desc_file,'rb') as fid:
            all_mapping=pickle.load(fid)
        
        for i in range(self.unit_list.GetLFINum()):
            # check the cache one by one
            cur_lfi=self.unit_list.GetScoringExpLFIInfo(i)

            correct_index=i
            correct_cache_folder=os.path.join(self.cache_folder,f'LFI_{i}')
            correct_cache_file=os.path.join(correct_cache_folder,PathManager.cache_desc)
            correct_cache_img=os.path.join(correct_cache_folder,PathManager.cache_thumbnail)

            if cur_lfi.show_name in all_mapping.keys():
                saved_mapping=all_mapping[cur_lfi.show_name]
            
            # check if saved cache is correct
            saved_index=saved_mapping[0]
            saved_folder=saved_mapping[1]

            if saved_index != correct_index:
                if os.path.exists(correct_cache_folder):
                    shutil.rmtree(correct_cache_folder)
                    shutil.move(saved_folder,correct_cache_folder)

            all_mapping[cur_lfi.show_name]=[correct_index,correct_cache_folder,cur_lfi.show_name]
            all_mapping[i]=[correct_index,correct_cache_folder,cur_lfi.show_name]

            if not os.path.exists(correct_cache_folder):
                os.makedirs(correct_cache_folder)
            if not os.path.exists(correct_cache_img):
                cur_lfi.MakeThumbnail(correct_cache_img)
            
            with open(correct_cache_file,'wb') as fid:
                pickle.dump([correct_index,correct_cache_folder,cur_lfi.show_name],fid)
        
        with open(self.cache_desc_file,'wb') as fid:
            pickle.dump(all_mapping,fid)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        event.ignore()
        return super().mousePressEvent(event)



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

        self.is_editable=True

        self.is_editable=True

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
        self.MakeSubjectsWidget()

    def MakeSettingWidget(self):
        self.right_stack.addWidget(QtWidgets.QFrame())
        cur_widget=self.right_stack.widget(2) #currentWidget()

        display_label=QtWidgets.QLabel("Display Type: ",parent=cur_widget)
        display_label_box=QtWidgets.QComboBox(cur_widget)
        display_label_box.addItem("2D")
        display_label_box.addItem("3D | Left & Right")
        display_label_box.addItem("3D | Top & Bottom")
        display_label_box.addItem("3D | Full")

        layout=QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        cur_widget.setLayout(layout)

        display_label_layout=QtWidgets.QHBoxLayout()
        display_label_layout.addWidget(display_label)
        display_label_layout.addWidget(display_label_box)

        layout.addLayout(display_label_layout)


        display_label=QtWidgets.QLabel("Display Type: ",parent=cur_widget)
        display_label_box=QtWidgets.QComboBox(cur_widget)
        display_label_box.addItem("2D")
        display_label_box.addItem("3D | Left & Right")
        display_label_box.addItem("3D | Top & Bottom")
        display_label_box.addItem("3D | Full")

        layout=QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        cur_widget.setLayout(layout)

        display_label_layout=QtWidgets.QHBoxLayout()
        display_label_layout.addWidget(display_label)
        display_label_layout.addWidget(display_label_box)

        layout.addLayout(display_label_layout)

        
    def MakeSubjectsWidget(self):
        self.right_stack.addWidget(QtWidgets.QFrame())

        cur_widget=self.right_stack.widget(3) #currentWidget()

        layout=QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        cur_widget.setLayout(layout)

        subject_unit=ImageUnit(icon_title="Shengyang",icon_img=":/icons/res/subject.png")
        subject_unit.setParent(cur_widget)

        subject_unit.setGeometry(0,0,100,100)

    def contextMenuEvent(self, event):
        menu=QtWidgets.QMenu(self)

        action1 = menu.addAction("Show in folder")
        action2 = menu.addAction("Open File")
        action3 = menu.addAction("Delete")

        menu.exec(event.globalPos())
        cur_widget=self.right_stack.widget(3) #currentWidget()

        layout=QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        cur_widget.setLayout(layout)

        subject_unit=ImageUnit(icon_title="Shengyang",icon_img=":/icons/res/subject.png")
        subject_unit.setParent(cur_widget)

        subject_unit.setGeometry(0,0,100,100)

    def contextMenuEvent(self, event):
        menu=QtWidgets.QMenu(self)

        action1 = menu.addAction("Show in folder")
        action2 = menu.addAction("Open File")
        action3 = menu.addAction("Delete")

        menu.exec(event.globalPos())

    def MakeMaterialWidget(self):
        right_stack_width=self.right_stack.width()
        right_stack_height=self.right_stack.height()

        self.material_widget=QtWidgets.QTabWidget()
        self.right_stack.addWidget(self.material_widget)
        self.material_widget.setGeometry(0,0,right_stack_width,right_stack_height)

        exp_setting=self.cur_project.GetExpSetting()

        self.material_widget.addTab(MaterialFolderFrame(self.cur_project.training_scoring_lfi_info,exp_setting),u"Training")
        self.material_widget.addTab(MaterialFolderFrame(self.cur_project.test_scoring_lfi_info,exp_setting),u"Testing")

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

    project_display=ProjectDisplay(project_info)
    project_display.resize(800,600)
    project_display.resize(800,600)

    project_display.show()

    sys.exit(app.exec())