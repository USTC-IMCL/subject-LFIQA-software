import sys
 
from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer, QMediaFormat
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import QMainWindow, QApplication,QWidget
 
def get_supported_mime_types():
    result = []
    for f in QMediaFormat().supportedFileFormats(QMediaFormat.Decode):
        mime_type = QMediaFormat(f).mimeType()
        result.append(mime_type.name())
    return result
 
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self._audio_output = QAudioOutput()
        self._player = QMediaPlayer()
        self._player.setAudioOutput(self._audio_output)
        self._video_widget = QVideoWidget(self)
        self._video_widget.resize(640, 480)
        self._player.setVideoOutput(self._video_widget)
 
    def play(self):
        fp="C:/Users/admin/Documents/Captura/a.mp4"
        self._player.setSource(QUrl.fromLocalFile(fp))
        self._player.play()
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    available_geometry = main_win.screen().availableGeometry()
    main_win.resize(available_geometry.width() / 3,
                    available_geometry.height() / 2)
    main_win.show()
    main_win.play()
    sys.exit(app.exec())