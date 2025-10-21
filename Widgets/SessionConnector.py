from PySide6.QtWidgets import QWidget, QVBoxLayout,QHBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Signal
from PySide6.QtGui import QMovie
import sys
sys.path.append("../Utils")
from PassiveTools import *
import logging
logger=logging.getLogger("LogWindow")
from SofwareConfig import LFIWindowSize, session_connector_size
from JPLMessageBox import ShowWarningMessage
from PySide6.QtCore import QTimer

class SessionConnector(QWidget):
    '''
        Only used for showing the progress of the session connector
    '''
    task_finished=Signal()
    def __init__(self, task_num,parent=None):
        super().__init__(parent)

        self.setWindowTitle("Session Connector")
        self.resize(session_connector_size.width,session_connector_size.height)

        self.already_done=0
        self.task_num=task_num
        self.has_error=False

        self.v_layout= QVBoxLayout(self)
        self.hint_widget= QWidget()
        self.hint_widget.setLayout(QHBoxLayout())

        self.hint_label= QLabel()
        self.hint_label.setText(f"Already done {self.already_done}/{self.task_num}")

        self.animation_label= QLabel()
        self.dot_count=0
        self.dot_timer= QTimer()
        self.dot_timer.timeout.connect(self.TickDot)
        self.dot_timer.start(500)

        self.hint_widget.layout().addWidget(self.hint_label)
        self.hint_widget.layout().addWidget(self.animation_label)

        self.v_layout.addWidget(self.hint_widget)

        self.progress_bar= QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setRange(0,100)
        self.v_layout.addWidget(self.progress_bar)

    def TickDot(self):
        if self.dot_count>=6:
            self.dot_count=0
        else:
            self.dot_count+=1
        self.animation_label.setText(f" Processing{'.'*self.dot_count}")
    
    def SetTaskNum(self,num):
        self.task_num=num

    def UpdateProgress(self,num):
        self.already_done=num
        self.progress_bar.setValue(int(self.already_done/self.task_num*100))
        self.hint_label.setText(f"Already done {self.already_done}/{self.task_num}")
        if self.already_done>=self.task_num:
            self.hint_label.setText(f"All tasks done! {self.already_done}/{self.task_num}")
            self.task_finished.emit()
