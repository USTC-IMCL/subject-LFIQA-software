import LogWindow
import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton

def test(inlog_widget: LogWindow.QLogWidget):
    if inlog_widget.isVisible():
        inlog_widget.hide()
    else:
        inlog_widget.show()

def test2():
    print(1/0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    big_window = QPushButton("Big Window")
    big_window.show()

    little_window=QPushButton("Little Window")
    little_window.show()

    LogWidget = QWidget()
    window=LogWindow.QLogWidget()
    window.show()

    big_window.clicked.connect(lambda: test(window))
    little_window.clicked.connect(lambda: test2())

    sys.exit(app.exec())