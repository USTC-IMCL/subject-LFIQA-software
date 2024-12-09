from PySide6.QtWidgets import QMessageBox


def ShowWarningMessage(message_text):
    dlg=QMessageBox()
    dlg.setStandardButtons(QMessageBox.Ok)
    dlg.setWindowTitle("Warning!")
    dlg.setIcon(QMessageBox.Warning)
    dlg.setText(message_text)
    dlg.exec()


if __name__ == "__main__":
    from PySide6 import QtWidgets
    app=QtWidgets.QApplication()
    ShowWarningMessage('No file is selected!')

    app.exec()