import ScoringWidget
import sys
sys.path.append("../Utils")

import ExpInfo
from ScoringWidget import PairWiseScoringWidget, ScoringWidget
from ExpInfo import ComparisonType
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication

class ExperimentSession(QObject):
    '''
     Handle one experiment session.
     Used to start the 
    '''
    exp_finished = Signal()
    def __init__(self, show_list: ExpInfo.AllScoringLFI, exp_setting: ExpInfo.ExpSetting=None,mode="training"):
        super().__init__()
        self.exp_setting = exp_setting
        self.exp_mode=mode
        self.all_scoring_lfi = show_list
        self.subject_info=None
        self.scoring_page=None
        self.screen_index = 0
        self.result=None
        self.show_index=None

    def SetSubjectInfo(self, subject_info:ExpInfo.PersonInfo):
        self.subject_info = subject_info
    
    def SetScreenIndex(self, screen_index:int):
        self.screen_index = screen_index

    def StartExperiment(self, scoring_mode:ComparisonType=ComparisonType.DoubleStimuli):
        show_lfi_num=self.all_scoring_lfi.GetLFINum()
        self.show_index=None
        if self.exp_mode.lower() == "training":
            all_show_index=list(range(show_lfi_num))
        else:
            all_show_index = self.all_scoring_lfi.GetRandomShowOrder()
        self.show_index=all_show_index
        
        if scoring_mode == ComparisonType.PairComparison:
            self.scoring_page = PairWiseScoringWidget(self.all_scoring_lfi,self.exp_setting,all_show_index)
        else:
            self.scoring_page = ScoringWidget(self.all_scoring_lfi,self.exp_setting,all_show_index)
        
        app=QApplication.instance()
        if app is None:
            app = QApplication([])
        self.scoring_page.setScreen(app.screens()[self.screen_index])
        cur_screen=self.scoring_page.screen()

        self.scoring_page.move(cur_screen.geometry().topLeft())
        self.scoring_page.SetScoringScreen(self.screen_index)
        self.scoring_page.showFullScreen()

        self.scoring_page.scoring_finished.connect(self.FinishExperiment)
    
    def FinishExperiment(self,all_results):
        self.result=all_results
        self.scoring_page.deleteLater()
        self.scoring_page=None
        self.exp_finished.emit()
    
    def GetResult(self):
        return self.result
    
    def GetShowIndex(self):
        return self.show_index
    
    def Release(self):
        self.scoring_page=None

    def getScore(self):
        pass


if __name__ == "__main__":
    app = QApplication([])
    exp_setting=ExpInfo.ExpSetting()
    exp_setting.two_folder_mode=True
    exp_setting.comparison_type=ExpInfo.ComparisonType.DoubleStimuli
    exp_setting.score_names=["Please Rate the Quality"]
    exp_setting.score_definition=[[
        "5. Imperceptible",
        "4. Perceptible but not annoying",
        "3. Slightly Annoying",
        "2. Annoying",
        "1. Very Annoying"
    ]]
    exp_setting.score_levels=[5]
    exp_setting.score_values=[[5,4,3,2,1]]
    exp_setting.lfi_features=[ExpInfo.LFIFeatures.Passive_ViewChanging]
    exp_setting.first_loop_skip=False

    all_scoring_lfi=ExpInfo.AllScoringLFI(in_mode="training")
    scoring_lfi=ExpInfo.ScoringExpLFIInfo()
    scoring_lfi.passive_view_video_path="/data_0/shengyang/Work/JPEG/LFIQA/examples/two_folder/foo_1/1.mp4"
    all_scoring_lfi.AddScoringLFI(scoring_lfi)

    exp_session = ExperimentSession(all_scoring_lfi,exp_setting=exp_setting,mode="training")
    exp_session.SetScreenIndex(0)

    from PySide6.QtWidgets import QWidget,QPushButton
    exp_window=QWidget()
    exp_window.resize(800,600)
    exp_btn=QPushButton("Start",parent=exp_window)
    exp_btn.setGeometry(100,100,40,20)

    exp_btn.clicked.connect(exp_session.StartExperiment)

    exp_window.show()

    app.exec()