# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SubjectInfo.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QHBoxLayout, QLabel, QLineEdit, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_SubjectIfo(object):
    def setupUi(self, SubjectIfo):
        if not SubjectIfo.objectName():
            SubjectIfo.setObjectName(u"SubjectIfo")
        SubjectIfo.resize(392, 284)
        font = QFont()
        font.setPointSize(16)
        SubjectIfo.setFont(font)
        self.btns = QDialogButtonBox(SubjectIfo)
        self.btns.setObjectName(u"btns")
        self.btns.setGeometry(QRect(-10, 240, 281, 32))
        self.btns.setOrientation(Qt.Horizontal)
        self.btns.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.verticalLayoutWidget = QWidget(SubjectIfo)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(50, 20, 282, 148))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_name = QLabel(self.verticalLayoutWidget)
        self.label_name.setObjectName(u"label_name")
        self.label_name.setMinimumSize(QSize(80, 0))
        self.label_name.setFont(font)

        self.horizontalLayout.addWidget(self.label_name)

        self.lineEdit_name = QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_name.setObjectName(u"lineEdit_name")
        font1 = QFont()
        font1.setPointSize(14)
        self.lineEdit_name.setFont(font1)

        self.horizontalLayout.addWidget(self.lineEdit_name)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_gender = QLabel(self.verticalLayoutWidget)
        self.label_gender.setObjectName(u"label_gender")
        self.label_gender.setFont(font)

        self.horizontalLayout_3.addWidget(self.label_gender)

        self.lineEdit_gender = QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_gender.setObjectName(u"lineEdit_gender")
        self.lineEdit_gender.setFont(font1)

        self.horizontalLayout_3.addWidget(self.lineEdit_gender)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_age = QLabel(self.verticalLayoutWidget)
        self.label_age.setObjectName(u"label_age")
        self.label_age.setMinimumSize(QSize(80, 0))
        self.label_age.setFont(font)

        self.horizontalLayout_5.addWidget(self.label_age)

        self.lineEdit_age = QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_age.setObjectName(u"lineEdit_age")
        self.lineEdit_age.setFont(font1)

        self.horizontalLayout_5.addWidget(self.lineEdit_age)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_job = QLabel(self.verticalLayoutWidget)
        self.label_job.setObjectName(u"label_job")
        self.label_job.setMinimumSize(QSize(80, 0))
        self.label_job.setFont(font)

        self.horizontalLayout_4.addWidget(self.label_job)

        self.lineEdit_job = QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_job.setObjectName(u"lineEdit_job")
        self.lineEdit_job.setFont(font1)

        self.horizontalLayout_4.addWidget(self.lineEdit_job)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.label = QLabel(SubjectIfo)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(50, 180, 271, 41))
        self.label.setFont(font1)

        self.retranslateUi(SubjectIfo)
        self.btns.accepted.connect(SubjectIfo.accept)
        self.btns.rejected.connect(SubjectIfo.reject)

        QMetaObject.connectSlotsByName(SubjectIfo)
    # setupUi

    def retranslateUi(self, SubjectIfo):
        SubjectIfo.setWindowTitle(QCoreApplication.translate("SubjectIfo", u"Please Enter Your Information", None))
        self.label_name.setText(QCoreApplication.translate("SubjectIfo", u"Name:  ", None))
        self.label_gender.setText(QCoreApplication.translate("SubjectIfo", u"Gender:", None))
        self.label_age.setText(QCoreApplication.translate("SubjectIfo", u"Age:", None))
        self.label_job.setText(QCoreApplication.translate("SubjectIfo", u"Job:", None))
        self.label.setText(QCoreApplication.translate("SubjectIfo", u"* Only for Scientific usage.", None))
    # retranslateUi

