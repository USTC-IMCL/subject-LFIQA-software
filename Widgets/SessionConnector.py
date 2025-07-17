from PySide6.QtWidgets import QWidget, QVBoxLayout
import sys
sys.path.append("../Utils")
from PassiveTools import *
import logging
logger=logging.getLogger("LogWindow")
from SofwareConfig import LFIWindowSize, session_connector_size

class SessionConnector(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Session Connector")
        self.resize(session_connector_size.width,session_connector_size.height)

        self.already_done=0

        self.v_layout= QVBoxLayout(self)
        self.hint_label= QLabel()
        self.v_layout.addWidget(self.hint_label)


        

