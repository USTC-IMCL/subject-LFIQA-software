import ScoringWidget
import sys
sys.path.append("../Utils")

import ExpInfo
from PySide6.QtCore import QObject

class ExperimentSession(QObject):
    '''
     Handle one experiment session.
     Used to start the 
    '''
    def __init__(self, exp_setting: ExpInfo.ExperimentInfo):
        super().__init__()
        self.exp_setting = exp_setting

    def start(self):
        self.scoringWidget.start()

    def stop(self):
        self.scoringWidget.stop()

    def getScore(self):