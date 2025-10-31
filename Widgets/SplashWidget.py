from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PySide6.QtGui import QMovie

class SplashGif(QWidget):
    def __init__(self, gif_path: str, timeout_ms: int = 3000):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        movie = QMovie(gif_path)
        label = QLabel()
        label.setMovie(movie)
        movie.start()

        QVBoxLayout(self).addWidget(label)
        self.adjustSize()
        self.center()

        # 3 秒后自动关闭并显示主窗口
        #QTimer.singleShot(timeout_ms, self.close)

    def center(self):
        from PySide6.QtGui import QGuiApplication
        fg = self.frameGeometry()
        fg.moveCenter(QGuiApplication.primaryScreen().geometry().center())
        self.move(fg.topLeft())
    
    def EndSplash(self):
        self.close()
        self.deleteLater()