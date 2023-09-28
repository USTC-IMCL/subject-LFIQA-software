# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Post_processing_config.ui'
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
    QRadioButton, QSizePolicy, QWidget)

class Ui_post_form(object):
    def setupUi(self, post_form):
        if not post_form.objectName():
            post_form.setObjectName(u"post_form")
        post_form.resize(779, 588)
        post_form.setWindowOpacity(0.900000000000000)
        post_form.setStyleSheet(u"background: gray;\n"
"color: rgb(255, 255, 255);")
        self.groupBox = QGroupBox(post_form)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 10, 751, 561))
        font = QFont()
        font.setPointSize(14)
        self.groupBox.setFont(font)
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(40, 50, 261, 31))
        self.label.setFont(font)
        self.checkBox = QCheckBox(self.groupBox)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(40, 100, 91, 41))
        self.checkBox.setFont(font)
        self.checkBox_2 = QCheckBox(self.groupBox)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setGeometry(QRect(150, 100, 91, 41))
        self.checkBox_2.setFont(font)
        self.checkBox_3 = QCheckBox(self.groupBox)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setGeometry(QRect(260, 100, 91, 41))
        self.checkBox_3.setFont(font)
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(40, 170, 261, 31))
        self.label_2.setFont(font)
        self.radioButton_4 = QRadioButton(self.groupBox)
        self.radioButton_4.setObjectName(u"radioButton_4")
        self.radioButton_4.setGeometry(QRect(320, 230, 111, 41))
        self.radioButton_4.setFont(font)
        self.radioButton_5 = QRadioButton(self.groupBox)
        self.radioButton_5.setObjectName(u"radioButton_5")
        self.radioButton_5.setGeometry(QRect(130, 230, 161, 41))
        self.radioButton_5.setFont(font)
        self.radioButton_6 = QRadioButton(self.groupBox)
        self.radioButton_6.setObjectName(u"radioButton_6")
        self.radioButton_6.setGeometry(QRect(40, 230, 91, 41))
        self.radioButton_6.setFont(font)
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(40, 300, 261, 31))
        self.label_3.setFont(font)
        self.radioButton_7 = QRadioButton(self.groupBox)
        self.radioButton_7.setObjectName(u"radioButton_7")
        self.radioButton_7.setGeometry(QRect(210, 345, 181, 41))
        self.radioButton_7.setFont(font)
        self.checkBox_8 = QCheckBox(self.groupBox)
        self.checkBox_8.setObjectName(u"checkBox_8")
        self.checkBox_8.setGeometry(QRect(40, 400, 181, 41))
        self.checkBox_8.setFont(font)
        self.radioButton_9 = QRadioButton(self.groupBox)
        self.radioButton_9.setObjectName(u"radioButton_9")
        self.radioButton_9.setGeometry(QRect(320, 345, 181, 41))
        self.radioButton_9.setFont(font)
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(40, 345, 161, 41))
        self.label_4.setFont(font)

        self.retranslateUi(post_form)

        QMetaObject.connectSlotsByName(post_form)
    # setupUi

    def retranslateUi(self, post_form):
        post_form.setWindowTitle(QCoreApplication.translate("post_form", u"Post Processing Configuration", None))
        self.groupBox.setTitle(QCoreApplication.translate("post_form", u"Post Precessing Config", None))
        self.label.setText(QCoreApplication.translate("post_form", u"Light field image type", None))
        self.checkBox.setText(QCoreApplication.translate("post_form", u"Dense", None))
        self.checkBox_2.setText(QCoreApplication.translate("post_form", u"Sparse", None))
        self.checkBox_3.setText(QCoreApplication.translate("post_form", u"Hybrid", None))
        self.label_2.setText(QCoreApplication.translate("post_form", u"Display type", None))
        self.radioButton_4.setText(QCoreApplication.translate("post_form", u"3D (Full)", None))
        self.radioButton_5.setText(QCoreApplication.translate("post_form", u"3D (Left & Right)", None))
        self.radioButton_6.setText(QCoreApplication.translate("post_form", u"2D", None))
        self.label_3.setText(QCoreApplication.translate("post_form", u"Features", None))
        self.radioButton_7.setText(QCoreApplication.translate("post_form", u"Passive", None))
        self.checkBox_8.setText(QCoreApplication.translate("post_form", u"Refocusing", None))
        self.radioButton_9.setText(QCoreApplication.translate("post_form", u"Active", None))
        self.label_4.setText(QCoreApplication.translate("post_form", u"---View Change: ", None))
    # retranslateUi

