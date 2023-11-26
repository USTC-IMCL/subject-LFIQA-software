# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'LogWidget.ui'
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
from PySide6.QtWidgets import (QApplication, QSizePolicy, QTextEdit, QWidget)
import UI_res_rc

class Ui_LogWidget(object):
    def setupUi(self, LogWidget):
        if not LogWidget.objectName():
            LogWidget.setObjectName(u"LogWidget")
        LogWidget.resize(600, 300)
        icon = QIcon()
        icon.addFile(u":/logo/imcl_logo", QSize(), QIcon.Normal, QIcon.Off)
        LogWidget.setWindowIcon(icon)
        self.text_editor = QTextEdit(LogWidget)
        self.text_editor.setObjectName(u"text_editor")
        self.text_editor.setGeometry(QRect(0, 0, 600, 300))
        font = QFont()
        font.setPointSize(12)
        self.text_editor.setFont(font)

        self.retranslateUi(LogWidget)

        QMetaObject.connectSlotsByName(LogWidget)
    # setupUi

    def retranslateUi(self, LogWidget):
        LogWidget.setWindowTitle(QCoreApplication.translate("LogWidget", u"System Logs", None))
    # retranslateUi

