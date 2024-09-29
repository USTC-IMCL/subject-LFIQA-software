import sys
import copy
from PySide6 import QtWidgets,QtCore, QtGui
from PySide6.QtWidgets import QSizePolicy
sys.path.append('../Utils')
sys.path.append('../UI')
import UI_res_rc
from ExpInfo import ProjectInfo, AllScoringLFI, ScoringExpLFIInfo, ExpSetting, FeatureType, LFIFeatures
import ExpInfo
from CollapsibleContainer import Container, EditableLabel, QToggle, EditableTexeEdit
import PathManager
import os
import shutil
import pickle
import logging
from LogWindow import QLogTextEditor
logger = logging.getLogger("LogWindow")

class ScrollUnitArea(QtWidgets.QScrollArea):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.content_widget=QtWidgets.QFrame()
        self.setWidget(self.content_widget)

        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBar(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.unit_col_num=0
        self.unit_num=0
        self.need_update=True
        self.force_update=False

        self.unit_size=[100,100] # height x width
        self.h_space=10
        self.v_space=10
        self.unit_list=None
        self.unit_list_labels=[] # QLabels to show the LFI info
        self.item_index=[None]*(1+self.unit_list.exp_lfi_info_num) #[[row, col]]
        self.item_pos=[None]*(1+self.unit_list.exp_lfi_info_num) #[height,width]

        self.margin_top=10
        self.margin_bottom=10
        self.margin_left=10
        self.margin_right=10

    def MakeColRowIndex(self):
        old_unit_col_num=self.unit_col_num
        self.unit_col_num=(self.width()-self.margin_left-self.margin_right+self.h_space)//(self.unit_size[1]+self.h_space)
        if self.unit_col_num < 1:
            self.unit_col_num=1
        if old_unit_col_num == self.unit_col_num and (not self.force_update):
            self.need_update=False
            return
        else:
            self.need_update=True

        start_x=self.margin_left
        start_y=self.margin_top 
        for list_index in range(self.unit_list.exp_lfi_info_num+1):
            row=list_index//self.unit_col_num
            col=list_index-row*self.unit_col_num
            self.item_index [list_index]=[row,col]
            self.item_pos[list_index]=[row*(self.unit_size[0]+self.h_space),col*(self.unit_size[1]+self.h_space)]

class SubjectsManagerWidget(QtWidgets.QScrollArea):
    def __init__(self, subject_list, *args, **kwargs):
        super().__init__(*args,*kwargs)
        self.content_widget=QtWidgets.QFrame()
        self.setWidget(self.main_widget)

        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBar(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

    def MakeRowCol(self):
        old_unit_col_num=self.unit_col_num
        self.unit_col_num=(self.width()+self.h_space)//(self.unit_size[1]+self.h_space)
        if self.unit_col_num < 1:
            self.unit_col_num=1
        if old_unit_col_num == self.unit_col_num and (not self.force_update):
            self.need_update=False
            return
        else:
            self.need_update=True 
        
        for list_index in range(self.unit_list.exp_lfi_info_num+1):
            row=list_index//self.unit_col_num
            col=list_index-row*self.unit_col_num
            self.item_index [list_index]=[row,col]
            self.item_pos[list_index]=[row*(self.unit_size[0]+self.h_space),col*(self.unit_size[1]+self.h_space)]

    def MakeSubjectLabels(self):
        pass



class ExpSettingWidget(QtWidgets.QScrollArea):
    def __init__(self, exp_setting: ExpSetting, has_subjects=False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.content_widget=QtWidgets.QWidget()
        self.setWidget(self.content_widget)
        self.exp_setting=exp_setting

        self.has_subjects=has_subjects
        if self.has_subjects:
            self.b_editable=False
        else:
            self.b_editable=True
        
        self.project_info=exp_setting.GetProjectInfo()
        self.temp_project_info=copy.deepcopy(self.project_info)

        self.widget_layout=QtWidgets.QVBoxLayout()
        self.widget_layout.setAlignment(QtCore.Qt.AlignTop)
        self.content_widget.setLayout(self.widget_layout)

        self.editable_text="Editable  "
        self.disabled_text="Not Editable  "
        self.locked_text="Locked  "

        self.set_method_set=[
            self.SetRefocusingType,
            self.SetViewChangeType,
            self.SetComparisonType,
            self.SetDisplayType,
            self.SetSaveFormat,
            self.SetAutoPlay,
            self.SetAutoTransition,
            self.SetLoppTimes,
            self.SetPauseAllowed,
            self.SetFirstLoopSkip,
            self.SetSkipHint,
            self.SetAllowUndistinguishable
        ]
        self.MakeEditToogle()
        self.MakeProjectInfoContainer()
        self.MakePlayerControlContainer()
        self.MakeScoringControlContainer()

    def GetAllInput(self):
        for set_method in self.set_method_set:
            set_method()

    def MakeEditToogle(self):
        edit_toogle_layout=QtWidgets.QHBoxLayout()
        self.edit_toogle=QToggle()
        self.edit_toogle.setMinimumHeight(26)
        self.edit_toogle.setText(self.editable_text)
        self.edit_toogle.setStyleSheet("QToggle{"
                            "qproperty-bg_color:#FAA;"
                            "font-size: 18px;}")
        self.edit_toogle.toggled.connect(self.ToogleEditable)
        if self.has_subjects:
            self.edit_toogle.setText(self.disabled_text)
            self.edit_toogle.setToolTip("The experiment has already begun, the settings are not editable now.")
            self.edit_toogle.setEnabled(False)

        self.edit_save_button=QtWidgets.QPushButton("Save")
        self.edit_save_button.clicked.connect(self.EditSave)
        self.edit_cancel_button=QtWidgets.QPushButton("Cancel")
        self.edit_cancel_button.clicked.connect(self.EditCancel)
        
        edit_toogle_layout.addWidget(self.edit_toogle,alignment=QtCore.Qt.AlignmentFlag.AlignLeft,stretch=8)
        button_layout=QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.edit_save_button)
        button_layout.addWidget(self.edit_cancel_button)
        edit_toogle_layout.addLayout(button_layout,stretch=2)

        self.widget_layout.addLayout(edit_toogle_layout)

        if not self.b_editable:
            self.edit_save_button.hide()
            self.edit_cancel_button.hide()
    
    def EditCancel(self):
        logger.info("Editing cancelled.")
        self.edit_toogle.ManualShutDown()
        self.RefreshAll()
    
    def EditSave(self):
        logger.info("Now try to update the project information.")

        self.GetAllInput()
        self.project_info=copy.deepcopy(self.temp_project_info)
        self.project_info.SaveToFile()
        self.edit_toogle.ManualShutDown()

    def MakeProjectInfoContainer(self):
        # projcet info container & settings
        self.project_list=[]
        self.project_container=Container('Project Information',color_background=False)
        project_layout=QtWidgets.QGridLayout(self.project_container.contentWidget)

        project_info=self.exp_setting.GetProjectInfo()
        self.project_name=project_info.project_name
        self.project_version=project_info.project_version

        project_version_label=QtWidgets.QLabel()
        project_version_label.setText(f"Project Version")
        project_version_value=QtWidgets.QLabel()
        project_version_value.setText(self.project_version)
        project_layout.addWidget(project_version_label,0,0)
        project_layout.addWidget(project_version_value,0,1)
        project_layout.setColumnStretch(0,3.5)
        project_layout.setColumnStretch(1,3)
        project_layout.setColumnStretch(2,4)

        self.project_name_label=QtWidgets.QLabel()
        self.project_name_value=QtWidgets.QLabel()
        #self.project_name_value=EditableLabel()
        #self.project_list.append(self.project_name_value)
        self.project_name_label.setText("Project Name")
        self.project_name_value.setText(self.project_name)
        project_layout.addWidget(self.project_name_label,1,0)
        project_layout.addWidget(self.project_name_value,1,1)

        feature_list=[FeatureType.Active, FeatureType.Passive, FeatureType.None_Type]
        self.refocusing_type=QtWidgets.QComboBox()
        self.project_list.append(self.refocusing_type)
        for feature in feature_list:
            if 'none' in feature.name.lower():
                self.refocusing_type.addItem("None")
            else:
                self.refocusing_type.addItem(feature.name)
        self.refocusing_type.setCurrentIndex(self.exp_setting.refocusing_type.value)
        refocusing_type_label=QtWidgets.QLabel()
        refocusing_type_label.setText("Refocusing Type")
        project_layout.addWidget(refocusing_type_label,2,0)
        project_layout.addWidget(self.refocusing_type,2,1)

        self.view_changing_type=QtWidgets.QComboBox()
        self.project_list.append(self.view_changing_type)
        for feature in feature_list:
            if 'none' in feature.name.lower():
                self.view_changing_type.addItem("None")
            else:
                self.view_changing_type.addItem(feature.name)
        self.view_changing_type.setCurrentIndex(self.exp_setting.view_changing_type.value)
        view_changing_type_label=QtWidgets.QLabel()
        view_changing_type_label.setText("View Changing Type")
        project_layout.addWidget(view_changing_type_label,3,0)
        project_layout.addWidget(self.view_changing_type,3,1)

        comparison_list=[ExpInfo.ComparisonType.SingleStimuli, ExpInfo.ComparisonType.DoubleStimuli, ExpInfo.ComparisonType.PairComparison]
        self.comparison_type=QtWidgets.QComboBox()
        self.project_list.append(self.comparison_type)
        for comparison in comparison_list:
            if 'single' in comparison.name.lower():
                cur_name='Single-Stimulus'
            if 'pair' in comparison.name.lower():
                cur_name='Pair-Comparison'
            if 'double' in comparison.name.lower():
                cur_name='Double-Stimuli'
            self.comparison_type.addItem(cur_name)
        self.comparison_type.setCurrentIndex(self.exp_setting.comparison_type.value)
        comparison_type_label=QtWidgets.QLabel()
        comparison_type_label.setText("Comparison Type")
        project_layout.addWidget(comparison_type_label,4,0)
        project_layout.addWidget(self.comparison_type,4,1)

        self.display_type=QtWidgets.QComboBox()
        display_type=self.display_type
        self.project_list.append(self.display_type)
        display_type.addItem("2D")
        display_type.addItem("3D | Left & Right")
        display_type.addItem("3D | Up & Down")
        display_type.addItem("3D | Full")
        display_type.setCurrentIndex(self.exp_setting.display_type.value)
        display_type_label=QtWidgets.QLabel()
        display_type_label.setText("Display Type")
        project_layout.addWidget(display_type_label,5,0)
        project_layout.addWidget(display_type,5,1)

        self.save_format=QtWidgets.QComboBox()
        self.project_list.append(self.save_format)
        self.save_format.addItem("Excel")
        self.save_format.addItem("CSV")
        self.save_format.setCurrentIndex(self.exp_setting.save_format.value)
        save_format_label=QtWidgets.QLabel()
        save_format_label.setText("Save Format")
        project_layout.addWidget(save_format_label,6,0)
        project_layout.addWidget(self.save_format,6,1)

        self.project_container.content_clicked.connect(self.ProjectReturn)
        self.widget_layout.addWidget(self.project_container)

    def SetViewChangeType(self, index=None):
        if index is None:
            index=self.view_changing_type.currentIndex()
        lfi_features=self.temp_project_info.exp_setting.lfi_features
        view_change_type=FeatureType(index)
        old_type=self.temp_project_info.exp_setting.view_changing_type
        if old_type==view_change_type:
            return
        if old_type == FeatureType.Active and LFIFeatures.Active_ViewChanging in lfi_features:
            lfi_features.remove(LFIFeatures.Active_ViewChanging)
        if old_type == FeatureType.Passive and LFIFeatures.Passive_ViewChanging in lfi_features:
            lfi_features.remove(LFIFeatures.Passive_ViewChanging)
        if old_type == FeatureType.None_Type and LFIFeatures.None_ViewChanging in lfi_features:
            lfi_features.remove(LFIFeatures.None_ViewChanging)

        self.temp_project_info.exp_setting.view_changing_type=view_change_type
        if view_change_type == FeatureType.Active:
            lfi_features.append(LFIFeatures.Active_ViewChanging)
        if view_change_type == FeatureType.Passive:
            lfi_features.append(LFIFeatures.Passive_ViewChanging)
        if view_change_type == FeatureType.None_Type:
            lfi_features.append(LFIFeatures.None_ViewChanging)

    def SetRefocusingType(self, index=None):
        if index is None:
            index=self.refocusing_type.currentIndex()
        lfi_features=self.temp_project_info.exp_setting.lfi_features
        refocusing_type=FeatureType(index)
        old_type=self.temp_project_info.exp_setting.refocusing_type
        if old_type==refocusing_type:
            return
        if old_type == FeatureType.Active and LFIFeatures.Active_Refocusing in lfi_features:
            lfi_features.remove(LFIFeatures.Active_Refocusing)
        if old_type == FeatureType.Passive and LFIFeatures.Passive_Refocusing in lfi_features:
            lfi_features.remove(LFIFeatures.Passive_Refocusing)
        if old_type == FeatureType.None_Type and LFIFeatures.None_Refocusing in lfi_features:
            lfi_features.remove(LFIFeatures.None_Refocusing)
        
        self.temp_project_info.exp_setting.refocusing_type=refocusing_type
        if refocusing_type == FeatureType.Active:
            lfi_features.append(LFIFeatures.Active_Refocusing)
        if refocusing_type == FeatureType.Passive:
            lfi_features.append(LFIFeatures.Passive_Refocusing)
        if refocusing_type == FeatureType.None_Type:
            lfi_features.append(LFIFeatures.None_Refocusing)

    def SetComparisonType(self, index=None):
        if index is None:
            index=self.comparison_type.currentIndex()
        old_type=self.temp_project_info.exp_setting.comparison_type
        comparison_type=ExpInfo.ComparisonType(index)
        if old_type==comparison_type:
            return
        self.temp_project_info.exp_setting.comparison_type=comparison_type

    def SetDisplayType(self, index=None):
        if index is None:
            index=self.display_type.currentIndex()
        lfi_features=self.temp_project_info.exp_setting.lfi_features
        old_type=self.temp_project_info.exp_setting.display_type
        display_type=ExpInfo.DisplayType(index)

        if old_type==display_type:
            return
        if old_type == ExpInfo.DisplayType.TwoD and ExpInfo.LFIFeatures.TwoD in lfi_features:
            lfi_features.remove(ExpInfo.LFIFeatures.TwoD)
        if old_type == ExpInfo.DisplayType.ThreeD_LR and ExpInfo.LFIFeatures.Stereo_horizontal in lfi_features:
            lfi_features.remove(ExpInfo.LFIFeatures.Stereo_horizontal)
        if old_type == ExpInfo.DisplayType.ThreeD_UD and ExpInfo.LFIFeatures.Stereo_vertical in lfi_features:
            lfi_features.remove(ExpInfo.LFIFeatures.Stereo_vertical)
        if old_type == ExpInfo.DisplayType.ThreeD_Full and ExpInfo.LFIFeatures.Stereo_full in lfi_features:
            lfi_features.remove(ExpInfo.LFIFeatures.Stereo_full)

        self.temp_project_info.exp_setting.display_type=display_type
        if display_type == ExpInfo.DisplayType.TwoD:
            lfi_features.append(ExpInfo.LFIFeatures.TwoD)
        if display_type == ExpInfo.DisplayType.ThreeD_LR:
            lfi_features.append(ExpInfo.LFIFeatures.Stereo_horizontal)
        if display_type == ExpInfo.DisplayType.ThreeD_UD:
            lfi_features.append(ExpInfo.LFIFeatures.Stereo_vertical)
        if display_type == ExpInfo.DisplayType.ThreeD_Full:
            lfi_features.append(ExpInfo.LFIFeatures.Stereo_full)

    def SetSaveFormat(self, index=None):
        if index is None:
            index=self.save_format.currentIndex()
        old_type=self.temp_project_info.exp_setting.save_format
        save_format=ExpInfo.SaveFormat(index)
        if old_type==save_format:
            return
        self.temp_project_info.exp_setting.save_format=save_format

    def MakePlayerControlContainer(self):
        self.player_control_container=Container("Player Control")
        self.player_control_list=[]
        player_control_layout=QtWidgets.QGridLayout(self.player_control_container._content_widget)

        player_control_layout.setColumnStretch(0,3.5)
        player_control_layout.setColumnStretch(1,3)
        player_control_layout.setColumnStretch(2,4)

        auto_play_label=QtWidgets.QLabel("Auto Play")
        auto_play=self.temp_project_info.exp_setting.auto_play
        self.auto_play_box=QtWidgets.QComboBox()
        self.player_control_list.append(self.auto_play_box)
        self.auto_play_box.addItems(["False","True"])
        self.auto_play_box.setCurrentIndex(1 if auto_play else 0)
        player_control_layout.addWidget(auto_play_label,0,0)
        player_control_layout.addWidget(self.auto_play_box,0,1)

        auto_transition_label=QtWidgets.QLabel("Auto Transition")
        auto_transition=self.temp_project_info.exp_setting.auto_transition
        self.auto_transition_box=QtWidgets.QComboBox()
        self.player_control_list.append(self.auto_transition_box)
        self.auto_transition_box.addItems(["False","True"])
        self.auto_transition_box.setCurrentIndex(1 if auto_transition else 0)
        player_control_layout.addWidget(auto_transition_label,1,0)
        player_control_layout.addWidget(self.auto_transition_box,1,1)

        loop_times_label=QtWidgets.QLabel("Loop Times")
        self.loop_times_box=QtWidgets.QSpinBox()
        self.player_control_list.append(self.loop_times_box)
        self.loop_times_box.setValue(self.temp_project_info.exp_setting.loop_times)
        self.loop_times_box.setRange(0,100)
        self.loop_times_box.setToolTip("Set the loop times of the video player. 0 means infinite loop.")
        player_control_layout.addWidget(loop_times_label,2,0)
        player_control_layout.addWidget(self.loop_times_box,2,1)

        self.player_control_container.content_clicked.connect(self.PlayerControlReturn)
        self.widget_layout.addWidget(self.player_control_container)

    def SetAutoPlay(self,index=None):
        if index is None:
            index=self.auto_play_box.currentIndex()
        if index==0:
            self.temp_project_info.exp_setting.auto_play=False
        else:
            self.temp_project_info.exp_setting.auto_play=True
    
    def SetAutoTransition(self,index=None):
        if index is None:
            index=self.auto_transition_box.currentIndex()
        if index==0:
            self.temp_project_info.exp_setting.auto_transition=False
        else:
            self.temp_project_info.exp_setting.auto_transition=True
    
    def SetLoppTimes(self,index=None):
        if index is None:
            index=self.loop_times_box.value()
        self.temp_project_info.exp_setting.loop_times=index

    def MakeScoringControlContainer(self):
        self.scoring_control_container=Container("Scoring Control")
        self.scoring_control_list=[]
        scoring_layout=QtWidgets.QGridLayout(self.scoring_control_container._content_widget)

        scoring_layout.setColumnStretch(0,3.5)
        scoring_layout.setColumnStretch(1,3)
        scoring_layout.setColumnStretch(2,4)

        pause_allowed_label=QtWidgets.QLabel("Pause Allowed")
        pause_allowed=self.temp_project_info.exp_setting.pause_allowed
        self.pause_allowed_box=QtWidgets.QComboBox()
        self.scoring_control_list.append(self.pause_allowed_box)
        self.pause_allowed_box.addItems(["False","True"])
        self.pause_allowed_box.setCurrentIndex(1 if pause_allowed else 0)
        scoring_layout.addWidget(pause_allowed_label,0,0)
        scoring_layout.addWidget(self.pause_allowed_box,0,1)

        first_loop_skip_label=QtWidgets.QLabel("First Loop Skip")
        first_loop_skip=self.temp_project_info.exp_setting.first_loop_skip
        self.first_loop_skip_box=QtWidgets.QComboBox()
        self.scoring_control_list.append(self.first_loop_skip_box)
        self.first_loop_skip_box.addItems(["False","True"])
        self.first_loop_skip_box.setCurrentIndex(1 if first_loop_skip else 0)
        scoring_layout.addWidget(first_loop_skip_label,1,0)
        scoring_layout.addWidget(self.first_loop_skip_box,1,1)

        skip_hint_label=QtWidgets.QLabel("Skip Hint")
        skip_hint=self.temp_project_info.exp_setting.skip_hint_text
        self.skip_hint_box=EditableLabel()
        self.scoring_control_list.append(self.skip_hint_box)
        self.skip_hint_box.setText(skip_hint)
        scoring_layout.addWidget(skip_hint_label,2,0)
        scoring_layout.addWidget(self.skip_hint_box,2,1)

        allow_undistinguishable_label=QtWidgets.QLabel("Allow Undistinguishable")
        allow_undistinguishable=self.temp_project_info.exp_setting.allow_undistinguishable
        self.allow_undistinguishable_box=QtWidgets.QComboBox()
        self.scoring_control_list.append(self.allow_undistinguishable_box)
        self.allow_undistinguishable_box.addItems(["False","True"])
        self.allow_undistinguishable_box.setCurrentIndex(1 if allow_undistinguishable else 0)
        scoring_layout.addWidget(allow_undistinguishable_label,3,0)
        scoring_layout.addWidget(self.allow_undistinguishable_box,3,1)

        table_num=len(self.exp_setting.score_names)
        table_num_label=QtWidgets.QLabel("Table Num")
        table_num_value=QtWidgets.QLabel(str(table_num))
        scoring_layout.addWidget(table_num_label,4,0)
        scoring_layout.addWidget(table_num_value,4,1)

        cur_layout_index=5
        for i in range(table_num):
            score_name=self.exp_setting.score_names[i]
            score_definition=self.exp_setting.score_definition[i]
            score_value=self.exp_setting.score_values[i]
            score_value=[str(x) for x in score_value]
            cur_layout_index=self.MakeTableDesc(scoring_layout,cur_layout_index,i+1,score_name,score_definition,score_value)


        self.scoring_control_container.content_clicked.connect(self.ScoringControlReturn)
        self.widget_layout.addWidget(self.scoring_control_container)
    
    def MakeTableDesc(self,in_layout:QtWidgets.QGridLayout,layout_index,table_index,score_name,score_definition,score_values):
        table_label=QtWidgets.QLabel("Scoring table "+str(table_index))
        in_layout.addWidget(table_label,layout_index,0)

        table_title_label=QtWidgets.QLabel("Title")
        #table_title_value=EditableLabel()
        table_title_value=QtWidgets.QLabel()
        table_title_value.setText(score_name)
        #self.scoring_control_list.append(table_title_value)
        in_layout.addWidget(table_title_label,layout_index,1)
        in_layout.addWidget(table_title_value,layout_index,2)

        layout_index+=1
        table_values_label=QtWidgets.QLabel("Scoring Values")
        #talbe_values_value=EditableLabel()
        table_values_value=QtWidgets.QLabel()
        table_values_value.setText(",".join(score_values))
        #self.scoring_control_list.append(table_values_value)
        in_layout.addWidget(table_values_label,layout_index,1)
        in_layout.addWidget(table_values_value,layout_index,2)

        layout_index+=1
        table_definition_label=QtWidgets.QLabel("Score Definition")        
        #table_definition_value=EditableLabel()
        table_definition_value=QtWidgets.QLabel()
        #self.scoring_control_list.append(table_definition_value)
        table_definition_value.setText("\n".join(score_definition))
        in_layout.addWidget(table_definition_label,layout_index,1)
        in_layout.addWidget(table_definition_value,layout_index,2)

        layout_index+=1
        return layout_index
        
    def SetPauseAllowed(self,index=None):
        if index is None:
            index=self.pause_allowed_box.currentIndex()
        if index==0:
            self.temp_project_info.exp_setting.pause_allowed=False
        else:
            self.temp_project_info.exp_setting.pause_allowed=True
    
    def SetFirstLoopSkip(self,index=None):
        if index is None:
            index=self.first_loop_skip_box.currentIndex()
        if index==0:
            self.temp_project_info.exp_setting.first_loop_skip=False
        else:
            self.temp_project_info.exp_setting.first_loop_skip=True
    
    def SetAllowUndistinguishable(self,index=None):
        if index is None:
            index=self.allow_undistinguishable_box.currentIndex()
        if index==0:
            self.temp_project_info.exp_setting.allow_undistinguishable=False
        else:
            self.temp_project_info.exp_setting.allow_undistinguishable=True
    
    def SetSkipHint(self,text=None):
        if text is None:
            text=self.skip_hint_box.text()
        self.temp_project_info.exp_setting.skip_hint_text=text
    
    def RefreshAll(self):
        self.refocusing_type.setCurrentIndex(self.project_info.exp_setting.refocusing_type.value)
        self.view_changing_type.setCurrentIndex(self.project_info.exp_setting.view_changing_type.value)
        self.comparison_type.setCurrentIndex(self.project_info.exp_setting.comparison_type.value)
        
        self.display_type.setCurrentIndex(self.project_info.exp_setting.display_type.value)
        self.save_format.setCurrentIndex(self.project_info.exp_setting.save_format.value)

        self.auto_play_box.setCurrentIndex(1 if self.project_info.exp_setting.auto_play else 0)
        self.auto_transition_box.setCurrentIndex(1 if self.project_info.exp_setting.auto_transition else 0)
        self.loop_times_box.setValue(self.project_info.exp_setting.loop_times)

        self.pause_allowed_box.setCurrentIndex(1 if self.project_info.exp_setting.pause_allowed else 0)
        self.first_loop_skip_box.setCurrentIndex(1 if self.project_info.exp_setting.first_loop_skip else 0)
        self.skip_hint_box.setText(self.project_info.exp_setting.skip_hint_text)


    def ProjectReturn(self):
        for item in self.project_list:
            if isinstance(item,EditableLabel):
                item.returnPressedAction()
    def PlayerControlReturn(self):
        for item in self.player_control_list:
            if isinstance(item,EditableLabel):
                item.returnPressedAction()
    def ScoringControlReturn(self):
        for item in self.scoring_control_list:
            if isinstance(item,EditableLabel):
                item.returnPressedAction()

    def SetEditable(self, b_editable):
        if self.has_subjects:
            self.b_editable=False
        else:
            self.b_editable=b_editable
    
        if not self.b_editable:
            for item in self.project_list:
                if isinstance(item,EditableLabel):
                    item.escapePressedAction()
                item.setDisabled(True)
            for item in self.scoring_control_list:
                if isinstance(item,QtWidgets.QComboBox):
                    item.setDisabled(True)
                elif isinstance(item,QtWidgets.QSpinBox):
                    item.setDisabled(True)
                else:
                    item.escapePressedAction()
                    item.setDisabled(True)
            for item in self.player_control_list:
                if isinstance(item, EditableLabel):
                    item.escapePressedAction()
                item.setDisabled(True)
        else:
            for item in self.project_list:
                item.setDisabled(False)
            for item in self.player_control_list:
                item.setDisabled(False)
            for item in self.scoring_control_list:
                item.setDisabled(False)
        
    def ToogleEditable(self):
        self.SetEditable(not self.b_editable)
        #self.edit_toogle.setChecked(self.b_editable)
        if self.b_editable:
            self.edit_toogle.setText(self.editable_text)
        else:
            self.edit_toogle.setText(self.locked_text)
        if self.has_subjects:
            self.b_editable=False
            self.edit_toogle.setText(self.disabled_text)
            self.edit_toogle.setToolTip("The experiment has already begun, the settings are not editable now.")
            self.edit_toogle.setEnabled(False)
        
        if not self.b_editable:
            self.edit_save_button.hide()
            self.edit_cancel_button.hide()
            self.RefreshAll()
        else:
            self.edit_save_button.show()
            self.edit_cancel_button.show()
        

        

class NewLFISelector(QtWidgets.QDialog):
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
        else:
            refocusing_type=exp_setting.refocusing_type

        if not hasattr(exp_setting, 'view_changing_type'):
            if ExpInfo.LFIFeatures.Active_ViewChanging in exp_setting.lfi_features:
                view_changing_type=FeatureType.Active
            elif ExpInfo.LFIFeatures.Passive_ViewChanging in exp_setting.lfi_features:
                view_changing_type=FeatureType.Passive
            else:
                view_changing_type=FeatureType.None_Type
        else:
            view_changing_type=exp_setting.view_changing_type


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
        
    def GetFilePath(self):
        passive_file_path=QtWidgets.QFileDialog.getOpenFileName(self,'Select video file','./',PathManager.)

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
        self.deleteLater()

    def CancelClicked(self):
        self.hide()
        logger.info('Add new LFI is cancelled.')
        self.on_cancel.emit()
        self.deleteLater()

class ImageUnit(QtWidgets.QFrame):
    clicked=QtCore.Signal()
    menu_clicked=QtCore.Signal(int,int)
    def __init__(self,unit_info:ScoringExpLFIInfo=None, logo_size=[80,80], icon_img=':/icons/res/icon_add.png', icon_title='New One',unit_index=0, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.logo_size=logo_size
        self.SetBasicParam(unit_info)
        self.InitIconUI(icon_img, icon_title)
        self.index=unit_index
        self.open_menu=False
        
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
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.clicked.emit()
            event.ignore()
        return super().mousePressEvent(event)
    
    def MakeMenu(self, menu_text):
        self.open_menu=True
        self.menu=QtWidgets.QMenu(self)
        self.menu_action_list=[]
        self.menu_dict={}
        for index,text in enumerate(menu_text):
            self.menu_action_list.append(self.menu.addAction(text))
            self.menu_dict[text]=index
            self.menu_action_list[-1].triggered.connect(lambda: self.menu_clicked.emit(self.index,self.menu_dict[text]))

    def contextMenuEvent(self, event):
        if not self.open_menu:
            return

        self.menu.exec(event.globalPos())

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
        self.force_update=False

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
        if old_unit_col_num == self.unit_col_num and (not self.force_update):
            self.need_update=False
            return
        else:
            self.need_update=True 
        
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
            self.unit_list_labels[-1].MakeMenu(['Open in folder','Delete'])

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
        self.add_form=NewLFISelector(self.exp_setting,parent=self)
        self.add_form.show()
        self.add_form.on_confirm.connect(self.ConfirmAddNewLFI)
        self.add_form.on_cancel.connect(self.CancleAddNewLFI)

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
        
        be_successful=new_scoring_lfi.CheckAllInput()


        if not be_successful:
            logger.error('Invalid input! Adding terminates.')
            return
        else:
            self.unit_list.AddScoringLFI(new_scoring_lfi)
            self.unit_list_labels.append(ImageUnit(unit_info=new_scoring_lfi,icon_img=':/icons/res/image.png',icon_title=f'LFI {self.unit_list.exp_lfi_info_num}',parent=self))
            self.item_index=[None]*(1+self.unit_list.exp_lfi_info_num) #[[row, col]]
            self.item_pos=[None]*(1+self.unit_list.exp_lfi_info_num) #[height,width]
            self.force_update=True
            self.UpdateLabelPos()
            self.force_update=False

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

        self.right_text_editor=QLogTextEditor()
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
        subject_num=len(self.cur_project.subject_list)
        if subject_num > 0:
            has_subjects=True
        else:
            has_subjects=False
        self.right_stack.addWidget(ExpSettingWidget(self.cur_project.exp_setting,has_subjects=has_subjects))
        
    def MakeSubjectsWidget(self):
        self.right_stack.addWidget(QtWidgets.QFrame())

        cur_widget=self.right_stack.widget(3) #currentWidget()

        layout=QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        cur_widget.setLayout(layout)

        icon_img=":/icons/res/subject.png"

        subject_num=len(self.cur_project.subject_list)
        self.all_subjects=[]
        for i in range(subject_num):
            subject_unit=ImageUnit(icon_title=f"Subject {i}",icon_img=icon_img)
            subject_unit.MakeMenu(['Open in folder','Open file','Delete'])
            subject_unit.setParent(cur_widget)
            self.all_subjects.append(subject_unit)
            subject_unit.setGeometry(0,0,100,100)


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
    #project_info=ProjectInfo('jpeg_1','../Projects/')

    #exp_setting=project_info.exp_setting

    #exp_setting.SetProjectInfo(project_info)

    project_display=ProjectDisplay(project_info)
    project_display.resize(800,600)

    project_display.show()


    #exp_setting_display=ExpSettingWidget(exp_setting)

    #exp_setting_display.resize(800,600)

    #exp_setting_display.show()


    sys.exit(app.exec())