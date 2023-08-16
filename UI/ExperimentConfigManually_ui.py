# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ExperimentConfigManually.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGroupBox, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QToolButton,
    QWidget)

class Ui_ExperimentConfigManually(object):
    def setupUi(self, ExperimentConfigManually):
        if not ExperimentConfigManually.objectName():
            ExperimentConfigManually.setObjectName(u"ExperimentConfigManually")
        ExperimentConfigManually.resize(779, 587)
        ExperimentConfigManually.setWindowOpacity(0.900000000000000)
        ExperimentConfigManually.setStyleSheet(u"background: gray;\n"
"color: rgb(255, 255, 255);")
        self.groupBox = QGroupBox(ExperimentConfigManually)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 10, 751, 561))
        font = QFont()
        font.setPointSize(14)
        self.groupBox.setFont(font)
        self.pushButton = QPushButton(self.groupBox)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(20, 40, 141, 41))
        self.pushButton.setFont(font)
        self.lineEdit = QLineEdit(self.groupBox)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(120, 120, 341, 31))
        self.lineEdit.setFont(font)
        self.button_select_json = QToolButton(self.groupBox)
        self.button_select_json.setObjectName(u"button_select_json")
        self.button_select_json.setGeometry(QRect(460, 120, 24, 31))
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(50, 120, 71, 31))
        self.label.setFont(font)
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 170, 91, 31))
        self.label_2.setFont(font)
        self.button_select_json_2 = QToolButton(self.groupBox)
        self.button_select_json_2.setObjectName(u"button_select_json_2")
        self.button_select_json_2.setGeometry(QRect(460, 170, 24, 31))
        self.lineEdit_2 = QLineEdit(self.groupBox)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(120, 170, 341, 31))
        self.lineEdit_2.setFont(font)
        self.checkBox = QCheckBox(self.groupBox)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(190, 40, 331, 41))
        self.checkBox.setFont(font)
        self.pushButton_2 = QPushButton(self.groupBox)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(590, 510, 141, 41))
        self.pushButton_2.setFont(font)

        self.retranslateUi(ExperimentConfigManually)

        QMetaObject.connectSlotsByName(ExperimentConfigManually)
    # setupUi

    def retranslateUi(self, ExperimentConfigManually):
        ExperimentConfigManually.setWindowTitle(QCoreApplication.translate("ExperimentConfigManually", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("ExperimentConfigManually", u"Configuration", None))
        self.pushButton.setText(QCoreApplication.translate("ExperimentConfigManually", u"Add New LFI", None))
        self.button_select_json.setText(QCoreApplication.translate("ExperimentConfigManually", u"...", None))
        self.label.setText(QCoreApplication.translate("ExperimentConfigManually", u"Origin:", None))
        self.label_2.setText(QCoreApplication.translate("ExperimentConfigManually", u"Distorted:", None))
        self.button_select_json_2.setText(QCoreApplication.translate("ExperimentConfigManually", u"...", None))
        self.checkBox.setText(QCoreApplication.translate("ExperimentConfigManually", u"Detect angular size automatically", None))
        self.pushButton_2.setText(QCoreApplication.translate("ExperimentConfigManually", u"Next", None))
    # retranslateUi

