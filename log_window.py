import logging
from PySide6.QtWidgets import QApplication
import logging
logger = logging.getLogger(__name__)

from PySide6.QtWidgets import QWidget, QTextEdit, QPushButton, QVBoxLayout

class QtWindowHandler(logging.Handler):

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.window = Window()
        self.window.show()

    def emit(self, record):
        self.window.textEdit.append(self.format(record))


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        # set the title
        self.setWindowTitle("Debugger")
 
        # setting  the geometry of window
        self.setGeometry(0, 0, 500, 500)

        # Layout
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.btn_debbugger = QPushButton('Start Debugger')
        self.btn_clean_debbugger = QPushButton('Clean Debugger')
        self.lbl_debugger = QTextEdit('Debbuger')
            
        self.vertLayout = QVBoxLayout()
        self.vertLayout .addWidget(self.textEdit)
        self.vertLayout .addWidget(self.btn_debbugger)
        self.vertLayout .addWidget(self.btn_clean_debbugger)
        self.setLayout(self.vertLayout )

        # Connect button
        self.btn_debbugger.clicked.connect(self.initialize_thread_1)
        self.btn_clean_debbugger.clicked.connect(self.CleanUi)
        


    def initialize_thread_1(self):
        logger.info("Starting Debugger ...")
        logger.error("No such file!")


    def CleanUi(self):
        self.textEdit.clear()

def main():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    f = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    window_handler = QtWindowHandler()
    window_handler.setFormatter(f)
    logger.addHandler(window_handler)

    file_handler=logging.FileHandler('./test.log')
    file_handler.setFormatter(f)
    logger.addHandler(logging.FileHandler('./test.log'))

    logger = logging.getLogger(__name__)
    logger.debug("test debug")
    logger.info("test info")
    logger.warning("test warn")
    app.exec()

if __name__ == "__main__":
    app = QApplication()
    main()