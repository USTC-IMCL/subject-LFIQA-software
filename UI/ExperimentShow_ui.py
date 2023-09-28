# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ExperimentShow.ui'
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
from PySide6.QtWidgets import (QApplication, QSizePolicy, QStackedWidget, QWidget)

class Ui_ScoringWidget(object):
    def setupUi(self, ScoringWidget):
        if not ScoringWidget.objectName():
            ScoringWidget.setObjectName(u"ScoringWidget")
        ScoringWidget.resize(757, 553)
        self.page_scoring = QWidget()
        self.page_scoring.setObjectName(u"page_scoring")
        ScoringWidget.addWidget(self.page_scoring)
        self.page_showing = QWidget()
        self.page_showing.setObjectName(u"page_showing")
        ScoringWidget.addWidget(self.page_showing)

        self.retranslateUi(ScoringWidget)

        QMetaObject.connectSlotsByName(ScoringWidget)
    # setupUi

    def retranslateUi(self, ScoringWidget):
        ScoringWidget.setWindowTitle(QCoreApplication.translate("ScoringWidget", u"StackedWidget", None))
    # retranslateUi

