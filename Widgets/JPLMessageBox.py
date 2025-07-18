from PySide6.QtWidgets import QMessageBox, QWidget

def ShowErrorMessage(message_text):
    dlg=QMessageBox()
    dlg.setStandardButtons(QMessageBox.Ok)
    dlg.setWindowTitle("Error!")
    dlg.setIcon(QMessageBox.Critical)
    dlg.setText(message_text)
    dlg.exec()

def ShowWarningMessage(message_text):
    dlg=QMessageBox()
    dlg.setStandardButtons(QMessageBox.Ok)
    dlg.setWindowTitle("Warning!")
    dlg.setIcon(QMessageBox.Warning)
    dlg.setText(message_text)
    dlg.exec()

def ShowInformationMessage(message_text):
    dlg=QMessageBox()
    dlg.setStandardButtons(QMessageBox.Ok)
    dlg.setWindowTitle("Information")
    dlg.setIcon(QMessageBox.Information)
    dlg.setText(message_text)
    dlg.exec()

def ShowYesNoMessage(message_text):
    dlg=QMessageBox()
    dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    dlg.setWindowTitle("Notice")
    dlg.setIcon(QMessageBox.Question)
    dlg.setText(message_text)
    return dlg.exec()


if __name__ == "__main__":
    from PySide6 import QtWidgets
    app=QtWidgets.QApplication([])

    window=QWidget()
    vlayout= QtWidgets.QVBoxLayout(window)
    btn=QtWidgets.QPushButton("information")
    btn.clicked.connect(lambda:ShowInformationMessage("Information message"))
    vlayout.addWidget(btn)
    btn=QtWidgets.QPushButton("warning")
    btn.clicked.connect(lambda:ShowWarningMessage("Warning message"))
    vlayout.addWidget(btn)
    btn=QtWidgets.QPushButton("yes no")
    btn.clicked.connect(lambda:ShowYesNoMessage("Yes or No message"))
    vlayout.addWidget(btn)

    window.show()

    app.exec()