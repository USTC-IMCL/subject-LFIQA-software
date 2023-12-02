# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'About_JPEG.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QWidget)
import UI_res_rc

class Ui_About_JPEG_Form(object):
    def setupUi(self, About_JPEG_Form):
        if not About_JPEG_Form.objectName():
            About_JPEG_Form.setObjectName(u"About_JPEG_Form")
        About_JPEG_Form.resize(600, 500)
        About_JPEG_Form.setStyleSheet(u"background: gray;\n"
"color: rgb(255, 255, 255);")
        self.logo_label = QLabel(About_JPEG_Form)
        self.logo_label.setObjectName(u"logo_label")
        self.logo_label.setGeometry(QRect(224, 60, 141, 171))
        self.logo_label.setPixmap(QPixmap(u":/logo/res/jpegpleno-logo.png"))
        self.logo_label.setScaledContents(True)
        self.label = QLabel(About_JPEG_Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(40, 270, 331, 61))
        font = QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label_6 = QLabel(About_JPEG_Form)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(100, 270, 541, 61))
        self.label_6.setFont(font)

        self.retranslateUi(About_JPEG_Form)

        QMetaObject.connectSlotsByName(About_JPEG_Form)
    # setupUi

    def retranslateUi(self, About_JPEG_Form):
        About_JPEG_Form.setWindowTitle(QCoreApplication.translate("About_JPEG_Form", u"Form", None))
        self.logo_label.setText("")
        self.label.setText(QCoreApplication.translate("About_JPEG_Form", u"Link:", None))
        self.label_6.setText(QCoreApplication.translate("About_JPEG_Form", u"<html><head/><body><p><a href=\"https://jpeg.org/jpegpleno/index.html\"><span style=\" text-decoration: underline; color:#0078d7;\">https://jpeg.org/jpegpleno/index.html</span></a></p></body></html>", None))
    # retranslateUi

