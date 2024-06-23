# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FontSetting.ui'
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
    QLabel, QSizePolicy, QSpinBox, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(380, 187)
        Dialog.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.btns = QDialogButtonBox(Dialog)
        self.btns.setObjectName(u"btns")
        self.btns.setGeometry(QRect(20, 130, 341, 51))
        self.btns.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.btns.setOrientation(Qt.Horizontal)
        self.btns.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.font_spinbox = QSpinBox(Dialog)
        self.font_spinbox.setObjectName(u"font_spinbox")
        self.font_spinbox.setGeometry(QRect(20, 80, 341, 31))
        font = QFont()
        font.setPointSize(14)
        self.font_spinbox.setFont(font)
        self.font_spinbox.setMinimum(0)
        self.font_spinbox.setMaximum(100)
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 30, 281, 41))
        font1 = QFont()
        font1.setPointSize(16)
        self.label.setFont(font1)

        self.retranslateUi(Dialog)
        self.btns.accepted.connect(Dialog.accept)
        self.btns.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Font Size Setting", None))
#if QT_CONFIG(accessibility)
        self.btns.setAccessibleName("")
#endif // QT_CONFIG(accessibility)
        self.label.setText(QCoreApplication.translate("Dialog", u"Set the font size", None))
    # retranslateUi

