# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Log_UI.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)
import UI_res_rc

class Ui_LogForm(object):
    def setupUi(self, LogForm):
        if not LogForm.objectName():
            LogForm.setObjectName(u"LogForm")
        LogForm.resize(810, 486)
        icon = QIcon()
        icon.addFile(u":/logo/imcl_logo", QSize(), QIcon.Normal, QIcon.Off)
        LogForm.setWindowIcon(icon)
        LogForm.setWindowOpacity(0.900000000000000)
        LogForm.setStyleSheet(u"background: gray;\n"
"color: rgb(255, 255, 255);")
        self.logo_label = QLabel(LogForm)
        self.logo_label.setObjectName(u"logo_label")
        self.logo_label.setGeometry(QRect(60, 90, 151, 151))
        self.logo_label.setPixmap(QPixmap(u":/logo/imcl_logo"))
        self.logo_label.setScaledContents(True)
        self.text_label = QLabel(LogForm)
        self.text_label.setObjectName(u"text_label")
        self.text_label.setGeometry(QRect(20, 250, 241, 141))
        font = QFont()
        font.setFamilies([u"Blackadder ITC"])
        font.setPointSize(20)
        self.text_label.setFont(font)
        self.verticalLayoutWidget = QWidget(LogForm)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(320, 50, 451, 374))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.button_new_experiment = QPushButton(self.verticalLayoutWidget)
        self.button_new_experiment.setObjectName(u"button_new_experiment")
        self.button_new_experiment.setMinimumSize(QSize(220, 70))
        font1 = QFont()
        font1.setPointSize(14)
        self.button_new_experiment.setFont(font1)

        self.verticalLayout.addWidget(self.button_new_experiment)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.button_start_training = QPushButton(self.verticalLayoutWidget)
        self.button_start_training.setObjectName(u"button_start_training")
        self.button_start_training.setMinimumSize(QSize(220, 70))
        self.button_start_training.setFont(font1)

        self.horizontalLayout.addWidget(self.button_start_training)

        self.button_start_test = QPushButton(self.verticalLayoutWidget)
        self.button_start_test.setObjectName(u"button_start_test")
        self.button_start_test.setMinimumSize(QSize(220, 70))
        self.button_start_test.setFont(font1)

        self.horizontalLayout.addWidget(self.button_start_test)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.button_post_processing = QPushButton(self.verticalLayoutWidget)
        self.button_post_processing.setObjectName(u"button_post_processing")
        self.button_post_processing.setMinimumSize(QSize(220, 70))
        self.button_post_processing.setFont(font1)

        self.verticalLayout.addWidget(self.button_post_processing)

        self.button_about = QPushButton(self.verticalLayoutWidget)
        self.button_about.setObjectName(u"button_about")
        self.button_about.setMinimumSize(QSize(220, 70))
        self.button_about.setFont(font1)

        self.verticalLayout.addWidget(self.button_about)

        self.button_exit = QPushButton(self.verticalLayoutWidget)
        self.button_exit.setObjectName(u"button_exit")
        self.button_exit.setMinimumSize(QSize(220, 70))
        self.button_exit.setFont(font1)

        self.verticalLayout.addWidget(self.button_exit)


        self.retranslateUi(LogForm)

        QMetaObject.connectSlotsByName(LogForm)
    # setupUi

    def retranslateUi(self, LogForm):
        LogForm.setWindowTitle(QCoreApplication.translate("LogForm", u"IMCL Light Field imag Quality Assessment Software", None))
        self.logo_label.setText("")
        self.text_label.setText(QCoreApplication.translate("LogForm", u"<html><head/><body><p align=\"center\">Light Field Image </p><p align=\"center\">Quality Assessment </p><p align=\"center\">Software</p></body></html>", None))
        self.button_new_experiment.setText(QCoreApplication.translate("LogForm", u"New Experiment Config", None))
        self.button_start_training.setText(QCoreApplication.translate("LogForm", u"Start Training", None))
        self.button_start_test.setText(QCoreApplication.translate("LogForm", u"Start Experiment", None))
        self.button_post_processing.setText(QCoreApplication.translate("LogForm", u"Post Processing", None))
        self.button_about.setText(QCoreApplication.translate("LogForm", u"About", None))
        self.button_exit.setText(QCoreApplication.translate("LogForm", u"Exit", None))
    # retranslateUi

