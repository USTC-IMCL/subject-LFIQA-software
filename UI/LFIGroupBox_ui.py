# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'LFIGroupBox.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QToolButton, QWidget)

class Ui_LFIGroupWidget(object):
    def setupUi(self, LFIGroupWidget):
        if not LFIGroupWidget.objectName():
            LFIGroupWidget.setObjectName(u"LFIGroupWidget")
        LFIGroupWidget.resize(511, 203)
        LFIGroupWidget.setMinimumSize(QSize(511, 187))
        self.line = QFrame(LFIGroupWidget)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(70, 20, 421, 16))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.btn_del = QPushButton(LFIGroupWidget)
        self.btn_del.setObjectName(u"btn_del")
        self.btn_del.setGeometry(QRect(10, 10, 51, 31))
        font = QFont()
        font.setPointSize(14)
        self.btn_del.setFont(font)
        self.gridLayoutWidget = QWidget(LFIGroupWidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 50, 472, 143))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.button_select_ori = QToolButton(self.gridLayoutWidget)
        self.button_select_ori.setObjectName(u"button_select_ori")
        self.button_select_ori.setEnabled(True)

        self.gridLayout.addWidget(self.button_select_ori, 1, 3, 1, 1)

        self.label_11 = QLabel(self.gridLayoutWidget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font)

        self.gridLayout.addWidget(self.label_11, 3, 0, 1, 1)

        self.line_editor_dist = QLineEdit(self.gridLayoutWidget)
        self.line_editor_dist.setObjectName(u"line_editor_dist")
        self.line_editor_dist.setEnabled(True)
        self.line_editor_dist.setMinimumSize(QSize(341, 31))
        self.line_editor_dist.setFont(font)

        self.gridLayout.addWidget(self.line_editor_dist, 2, 2, 1, 1)

        self.line_editor_name = QLineEdit(self.gridLayoutWidget)
        self.line_editor_name.setObjectName(u"line_editor_name")
        self.line_editor_name.setEnabled(True)
        self.line_editor_name.setMinimumSize(QSize(341, 31))
        self.line_editor_name.setFont(font)
        self.line_editor_name.setCursorPosition(0)

        self.gridLayout.addWidget(self.line_editor_name, 0, 2, 1, 1)

        self.label_10 = QLabel(self.gridLayoutWidget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(71, 31))
        self.label_10.setFont(font)

        self.gridLayout.addWidget(self.label_10, 0, 0, 1, 1)

        self.label_8 = QLabel(self.gridLayoutWidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font)

        self.gridLayout.addWidget(self.label_8, 1, 0, 1, 1)

        self.label_9 = QLabel(self.gridLayoutWidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font)

        self.gridLayout.addWidget(self.label_9, 2, 0, 1, 1)

        self.button_select_dist = QToolButton(self.gridLayoutWidget)
        self.button_select_dist.setObjectName(u"button_select_dist")
        self.button_select_dist.setEnabled(True)

        self.gridLayout.addWidget(self.button_select_dist, 2, 3, 1, 1)

        self.line_editor_ori = QLineEdit(self.gridLayoutWidget)
        self.line_editor_ori.setObjectName(u"line_editor_ori")
        self.line_editor_ori.setEnabled(True)
        self.line_editor_ori.setMinimumSize(QSize(341, 31))
        self.line_editor_ori.setFont(font)

        self.gridLayout.addWidget(self.line_editor_ori, 1, 2, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(10, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.radio_btn_dense = QRadioButton(self.gridLayoutWidget)
        self.radio_btn_dense.setObjectName(u"radio_btn_dense")
        self.radio_btn_dense.setFont(font)
        self.radio_btn_dense.setChecked(True)
        self.radio_btn_dense.setAutoExclusive(True)

        self.horizontalLayout_2.addWidget(self.radio_btn_dense)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.radio_btn_sparse = QRadioButton(self.gridLayoutWidget)
        self.radio_btn_sparse.setObjectName(u"radio_btn_sparse")
        self.radio_btn_sparse.setFont(font)

        self.horizontalLayout_2.addWidget(self.radio_btn_sparse)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 2, 1, 1)


        self.retranslateUi(LFIGroupWidget)

        QMetaObject.connectSlotsByName(LFIGroupWidget)
    # setupUi

    def retranslateUi(self, LFIGroupWidget):
        LFIGroupWidget.setWindowTitle(QCoreApplication.translate("LFIGroupWidget", u"Form", None))
        self.btn_del.setText(QCoreApplication.translate("LFIGroupWidget", u"Del", None))
        self.button_select_ori.setText(QCoreApplication.translate("LFIGroupWidget", u"...", None))
        self.label_11.setText(QCoreApplication.translate("LFIGroupWidget", u"LFI Type\uff1a", None))
        self.label_10.setText(QCoreApplication.translate("LFIGroupWidget", u"Name:", None))
        self.label_8.setText(QCoreApplication.translate("LFIGroupWidget", u"Origin:", None))
        self.label_9.setText(QCoreApplication.translate("LFIGroupWidget", u"Distorted:", None))
        self.button_select_dist.setText(QCoreApplication.translate("LFIGroupWidget", u"...", None))
        self.radio_btn_dense.setText(QCoreApplication.translate("LFIGroupWidget", u"Dense", None))
        self.radio_btn_sparse.setText(QCoreApplication.translate("LFIGroupWidget", u"Sparse", None))
    # retranslateUi

