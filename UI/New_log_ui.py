# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'New_log.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
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

class Ui_ProjectOpen(object):
    def setupUi(self, ProjectOpen):
        if not ProjectOpen.objectName():
            ProjectOpen.setObjectName(u"ProjectOpen")
        ProjectOpen.resize(810, 486)
        ProjectOpen.setWindowOpacity(0.900000000000000)
        ProjectOpen.setStyleSheet(u"background: gray;\n"
"color: rgb(255, 255, 255);")
        ProjectOpen.setLocale(QLocale(QLocale.Chinese, QLocale.China))
        self.logo_label = QLabel(ProjectOpen)
        self.logo_label.setObjectName(u"logo_label")
        self.logo_label.setGeometry(QRect(60, 90, 151, 151))
        self.logo_label.setPixmap(QPixmap(u":/logo/imcl_logo"))
        self.logo_label.setScaledContents(True)
        self.text_label = QLabel(ProjectOpen)
        self.text_label.setObjectName(u"text_label")
        self.text_label.setGeometry(QRect(20, 250, 241, 141))
        font = QFont()
        font.setFamilies([u"Z003"])
        font.setPointSize(20)
        font.setItalic(True)
        self.text_label.setFont(font)
        self.verticalLayoutWidget = QWidget(ProjectOpen)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(340, 90, 450, 299))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.button_load_project = QPushButton(self.verticalLayoutWidget)
        self.button_load_project.setObjectName(u"button_load_project")
        self.button_load_project.setMinimumSize(QSize(220, 70))
        font1 = QFont()
        font1.setPointSize(14)
        self.button_load_project.setFont(font1)

        self.horizontalLayout.addWidget(self.button_load_project)

        self.button_new_project = QPushButton(self.verticalLayoutWidget)
        self.button_new_project.setObjectName(u"button_new_project")
        self.button_new_project.setMinimumSize(QSize(220, 70))
        self.button_new_project.setFont(font1)

        self.horizontalLayout.addWidget(self.button_new_project)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.button_setting = QPushButton(self.verticalLayoutWidget)
        self.button_setting.setObjectName(u"button_setting")
        self.button_setting.setMinimumSize(QSize(220, 70))
        self.button_setting.setFont(font1)

        self.verticalLayout.addWidget(self.button_setting)

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


        self.retranslateUi(ProjectOpen)

        QMetaObject.connectSlotsByName(ProjectOpen)
    # setupUi

    def retranslateUi(self, ProjectOpen):
        ProjectOpen.setWindowTitle(QCoreApplication.translate("ProjectOpen", u"IMCL Light Field imag Quality Assessment Software", None))
        self.logo_label.setText("")
        self.text_label.setText(QCoreApplication.translate("ProjectOpen", u"<html><head/><body><p align=\"center\">Light Field Image </p><p align=\"center\">Quality Assessment </p><p align=\"center\">Software</p></body></html>", None))
        self.button_load_project.setText(QCoreApplication.translate("ProjectOpen", u"Load Project", None))
        self.button_new_project.setText(QCoreApplication.translate("ProjectOpen", u"New Project", None))
        self.button_setting.setText(QCoreApplication.translate("ProjectOpen", u"Setting", None))
        self.button_about.setText(QCoreApplication.translate("ProjectOpen", u"About", None))
        self.button_exit.setText(QCoreApplication.translate("ProjectOpen", u"Exit", None))
    # retranslateUi

