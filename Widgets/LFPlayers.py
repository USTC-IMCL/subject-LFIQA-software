import os
os.environ['PATH']+=';./'
import mpv
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import Signal


class BasicPlayer(QOpenGLWidget):
    '''
    subjects actions: 1. watching 2. controlling
    two aspects: 1. time sequence 2. viewport changing 
    '''
    on_player_finished=Signal()
    on_enable_early_skip=Signal()


    def __init__(self) -> None:
        super(BasicPlayer,self).__init__()
        self.lfi_info=None
        self.pos_x=0
        self.pos_y=0
        self.content_height=0
        self.content_width=0

    def initializeGL(self) -> None:
        return super().initializeGL()

    def paintGL(self) -> None:
        return super().paintGL()
    
    def ResizeGL(self) -> None:
        return super().resizeGL()

    def Render(self):
        pass

    def StartPlaying(self):
        pass
        
    def StopPlaying(self):
        pass

    