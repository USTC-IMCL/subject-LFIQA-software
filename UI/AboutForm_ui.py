# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AboutForm.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QWidget)
import UI_res_rc

class Ui_AboutForm(object):
    def setupUi(self, AboutForm):
        if not AboutForm.objectName():
            AboutForm.setObjectName(u"AboutForm")
        AboutForm.resize(600, 500)
        icon = QIcon()
        icon.addFile(u":/logo/imcl_logo", QSize(), QIcon.Normal, QIcon.Off)
        AboutForm.setWindowIcon(icon)
        AboutForm.setStyleSheet(u"background: gray;\n"
"color: rgb(255, 255, 255);")
        self.logo_label = QLabel(AboutForm)
        self.logo_label.setObjectName(u"logo_label")
        self.logo_label.setGeometry(QRect(224, 20, 151, 151))
        self.logo_label.setPixmap(QPixmap(u":/logo/imcl_logo"))
        self.logo_label.setScaledContents(True)
        self.label = QLabel(AboutForm)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 170, 331, 61))
        font = QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label_2 = QLabel(AboutForm)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(120, 180, 331, 91))
        self.label_2.setFont(font)
        self.label_2.setLineWidth(1)
        self.label_2.setMidLineWidth(0)
        self.label_3 = QLabel(AboutForm)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(30, 360, 541, 61))
        self.label_3.setFont(font)
        self.label_4 = QLabel(AboutForm)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(30, 290, 331, 61))
        self.label_4.setFont(font)
        self.label_5 = QLabel(AboutForm)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(120, 290, 331, 61))
        self.label_5.setFont(font)
        self.label_6 = QLabel(AboutForm)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(120, 360, 541, 61))
        self.label_6.setFont(font)

        self.retranslateUi(AboutForm)

        QMetaObject.connectSlotsByName(AboutForm)
    # setupUi

    def retranslateUi(self, AboutForm):
        AboutForm.setWindowTitle(QCoreApplication.translate("AboutForm", u"About", None))
        self.logo_label.setText("")
        self.label.setText(QCoreApplication.translate("AboutForm", u"Authors:   ", None))
        self.label_2.setText(QCoreApplication.translate("AboutForm", u"Dr. Shengyang Zhao\n"
"Mr. Likun Shi\n"
"Prof. Zhibo Chen", None))
        self.label_3.setText(QCoreApplication.translate("AboutForm", u"<html><head/><body><p>Lab:</p></body></html>", None))
        self.label_4.setText(QCoreApplication.translate("AboutForm", u"Email: ", None))
        self.label_5.setText(QCoreApplication.translate("AboutForm", u"chenzhibo@ustc.edu.cn", None))
        self.label_6.setText(QCoreApplication.translate("AboutForm", u"<html><head/><body><p><a href=\"https://faculty.ustc.edu.cn/chenzhibo\"><span style=\" text-decoration: underline; color:#0000ff;\">https://faculty.ustc.edu.cn/chenzhibo</span></a></p></body></html>", None))
    # retranslateUi

