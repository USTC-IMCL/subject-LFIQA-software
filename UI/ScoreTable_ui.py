# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ScoreTable.ui'
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QLabel, QRadioButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_ScoreTable(object):
    def setupUi(self, ScoreTable):
        if not ScoreTable.objectName():
            ScoreTable.setObjectName(u"ScoreTable")
        ScoreTable.resize(290, 440)
        self.scoring_name = QGroupBox(ScoreTable)
        self.scoring_name.setObjectName(u"scoring_name")
        self.scoring_name.setGeometry(QRect(20, 10, 250, 420))
        font = QFont()
        font.setPointSize(20)
        self.scoring_name.setFont(font)
        self.scoring_name.setFocusPolicy(Qt.StrongFocus)
        self.verticalLayoutWidget = QWidget(self.scoring_name)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 40, 231, 371))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSpacing(30)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 10)
        self.radioButton = QRadioButton(self.verticalLayoutWidget)
        self.radioButton.setObjectName(u"radioButton")

        self.verticalLayout.addWidget(self.radioButton)

        self.radioButton_2 = QRadioButton(self.verticalLayoutWidget)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.verticalLayout.addWidget(self.radioButton_2)

        self.radioButton_3 = QRadioButton(self.verticalLayoutWidget)
        self.radioButton_3.setObjectName(u"radioButton_3")

        self.verticalLayout.addWidget(self.radioButton_3)

        self.radioButton_4 = QRadioButton(self.verticalLayoutWidget)
        self.radioButton_4.setObjectName(u"radioButton_4")

        self.verticalLayout.addWidget(self.radioButton_4)

        self.radioButton_5 = QRadioButton(self.verticalLayoutWidget)
        self.radioButton_5.setObjectName(u"radioButton_5")

        self.verticalLayout.addWidget(self.radioButton_5)

        self.border_label = QLabel(ScoreTable)
        self.border_label.setObjectName(u"border_label")
        self.border_label.setGeometry(QRect(0, 0, 290, 440))
        self.border_label.setFocusPolicy(Qt.StrongFocus)
        self.border_label.setStyleSheet(u"")
        self.border_label.setLineWidth(1)
        self.border_label.raise_()
        self.scoring_name.raise_()

        self.retranslateUi(ScoreTable)

        QMetaObject.connectSlotsByName(ScoreTable)
    # setupUi

    def retranslateUi(self, ScoreTable):
        ScoreTable.setWindowTitle(QCoreApplication.translate("ScoreTable", u"Form", None))
        self.scoring_name.setTitle(QCoreApplication.translate("ScoreTable", u"GroupBox", None))
        self.radioButton.setText(QCoreApplication.translate("ScoreTable", u"5, Excellent", None))
        self.radioButton_2.setText(QCoreApplication.translate("ScoreTable", u"4, Good", None))
        self.radioButton_3.setText(QCoreApplication.translate("ScoreTable", u"3, Fair", None))
        self.radioButton_4.setText(QCoreApplication.translate("ScoreTable", u"2, Poor", None))
        self.radioButton_5.setText(QCoreApplication.translate("ScoreTable", u"1, Bad", None))
        self.border_label.setText("")
    # retranslateUi

