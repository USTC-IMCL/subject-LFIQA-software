import LogWindow
import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QInputDialog
import logging

logger=logging.getLogger("LogWindow")

def test(inlog_widget: LogWindow.QLogWidget):
    if inlog_widget.isVisible():
        inlog_widget.hide()
    else:
        inlog_widget.show()

def test2():
    print(1/0)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget=QWidget()
    name,ok=input_d=QInputDialog.getText(widget,"Test","Please enter your project name")
    if ok :
        print(name)
    widget.show()

    sys.exit(app.exec())