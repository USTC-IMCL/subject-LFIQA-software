import os
import sys
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
sys.path.append('../Utils')
sys.path.append('../UI')


class InterchangeDataTable(QTableWidget):
    def __init__(self, parent=None):
        super(InterchangeDataTable, self).__init__(parent)

        self.setWindowTitle("Interchange Data Table")

        self.resize(800, 600)

        self.setColumnCount(8)

        self.setHorizontalHeaderLabels(['Image Index', 'Image Name', 'Codec_Left', 'Dlevel_Left', 'Codec_Right', 'Dlevel_Right', 'Bitrate_Left', 'Bitrate_Right'])

        self.setRowCount(10)

        for i in range(10):
            self.setItem(i,0, QTableWidgetItem(str(i)))


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = InterchangeDataTable()
    window.show()
    sys.exit(app.exec())
