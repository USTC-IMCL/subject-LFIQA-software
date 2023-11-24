import PySide6.QtGui
from PySide6.QtWidgets import QApplication,QWidget,QTextEdit
from PySide6.QtGui import QMouseEvent,QKeyEvent
from PySide6.QtCore import Qt
import logging
import sys
sys.path.append('../UI')
from LogWidget_ui import Ui_LogWidget as LogWidget

class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, level):
       self.logger = logger
       self.level = level
       self.linebuf = ''

    def write(self, buf):
       for line in buf.rstrip().splitlines():
          self.logger.log(self.level, line.rstrip())

    def flush(self):
        pass

class QtLogTextEditorHandler(logging.Handler):
    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.log_text_editor=None

    def SetLogTextEditor(self,log_text_editor):
        self.log_text_editor=log_text_editor

    def emit(self, record):
        if self.log_text_editor is None:
            return
        else:
            self.log_text_editor.append(self.format(record))

class QLogWidget(QWidget, LogWidget):
    def __init__(self, *args, **kwargs):
        '''
        At least, the logs should be recorded in the text editor.
        But it can also record the 
        '''
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.text_editor.setReadOnly(True)
        self.logger=logging.getLogger(__name__)

        self.widget_handler=QtLogTextEditorHandler()
        self.widget_handler.SetLogTextEditor(self.text_editor)
        #format_str='%(asctime)s, From '+ __name__+' [%(levelname)s]: %(message)s'
        format_str='%(asctime)s [%(levelname)s]: %(message)s'
        self.log_format=logging.Formatter(fmt=format_str,datefmt='%Y-%m-%d-%H:%M')
        self.widget_handler.setFormatter(self.log_format)

        self.logger.addHandler(self.widget_handler)
        self.logger.setLevel(logging.DEBUG)

        sys.stdout=StreamToLogger(self.logger, logging.INFO)
        sys.stderr=StreamToLogger(self.logger, logging.ERROR)

        self.log_dict={
            'debug':self.logger.debug,
            'info':self.logger.info,
            'warning':self.logger.warning,
            'error':self.logger.error,
            'critical':self.logger.critical
        }

        self.log_level_dict={}
    
    def RecordMeassage(self,message,level='info'):
        if level in self.log_dict.keys():
            self.log_dict[level](message)
        else:
            self.log_dict['info'](message)
    
    def keyPressEvent(self, event: QKeyEvent) -> None:
        self.RecordMeassage('key pressed',level='aainfo')
        if event.text() == 'q':
            if self.isVisible():
                self.hide()
            else:
                self.show()

        print(1/0)
        return super().keyPressEvent(event)

if __name__ == "__main__":
    app=QApplication()
    window=QLogWidget()
    window.show()
    sys.exit(app.exec())