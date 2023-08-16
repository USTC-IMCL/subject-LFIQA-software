# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'NewExperiment.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QLabel, QLineEdit,
    QPushButton, QRadioButton, QSizePolicy, QToolButton,
    QWidget)

class Ui_NewExperimentForm(object):
    def setupUi(self, NewExperimentForm):
        if not NewExperimentForm.objectName():
            NewExperimentForm.setObjectName(u"NewExperimentForm")
        NewExperimentForm.resize(777, 587)
        icon = QIcon()
        icon.addFile(u"LOGO_imcl_transparent.png", QSize(), QIcon.Normal, QIcon.Off)
        NewExperimentForm.setWindowIcon(icon)
        NewExperimentForm.setWindowOpacity(0.900000000000000)
        NewExperimentForm.setStyleSheet(u"background: gray;\n"
"color: rgb(255, 255, 255);")
        self.HintLabel = QLabel(NewExperimentForm)
        self.HintLabel.setObjectName(u"HintLabel")
        self.HintLabel.setGeometry(QRect(30, 20, 631, 131))
        font = QFont()
        font.setPointSize(14)
        self.HintLabel.setFont(font)
        self.groupBox = QGroupBox(NewExperimentForm)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(20, 150, 721, 321))
        self.groupBox.setFont(font)
        self.radioButton = QRadioButton(self.groupBox)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setGeometry(QRect(50, 160, 211, 131))
        self.radioButton.setFont(font)
        self.radioButton_2 = QRadioButton(self.groupBox)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setGeometry(QRect(50, 30, 211, 131))
        self.radioButton_2.setFont(font)
        self.lineEdit = QLineEdit(self.groupBox)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(250, 212, 341, 31))
        self.lineEdit.setFont(font)
        self.button_select_json = QToolButton(self.groupBox)
        self.button_select_json.setObjectName(u"button_select_json")
        self.button_select_json.setGeometry(QRect(590, 212, 24, 31))
        self.pushButton = QPushButton(NewExperimentForm)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(480, 530, 131, 41))
        self.pushButton.setFont(font)
        self.pushButton_2 = QPushButton(NewExperimentForm)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(620, 530, 131, 41))
        self.pushButton_2.setFont(font)
        self.groupBox.raise_()
        self.HintLabel.raise_()
        self.pushButton.raise_()
        self.pushButton_2.raise_()

        self.retranslateUi(NewExperimentForm)

        QMetaObject.connectSlotsByName(NewExperimentForm)
    # setupUi

    def retranslateUi(self, NewExperimentForm):
        NewExperimentForm.setWindowTitle(QCoreApplication.translate("NewExperimentForm", u"Create New Experiment", None))
        self.HintLabel.setText(QCoreApplication.translate("NewExperimentForm", u"<html><head/><body><p>Please Choose the way you want to config your new experiment. <br/></p><p>Then click the next step.</p></body></html>", None))
        self.groupBox.setTitle(QCoreApplication.translate("NewExperimentForm", u"Configuration", None))
        self.radioButton.setText(QCoreApplication.translate("NewExperimentForm", u"Config with Json", None))
        self.radioButton_2.setText(QCoreApplication.translate("NewExperimentForm", u"Config manually", None))
        self.button_select_json.setText(QCoreApplication.translate("NewExperimentForm", u"...", None))
        self.pushButton.setText(QCoreApplication.translate("NewExperimentForm", u"Next Step", None))
        self.pushButton_2.setText(QCoreApplication.translate("NewExperimentForm", u"Cancel", None))
    # retranslateUi

