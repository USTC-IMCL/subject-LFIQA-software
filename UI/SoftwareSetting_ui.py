# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SoftwareSetting.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGroupBox, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QToolButton,
    QWidget)
import UI_res_rc

class Ui_SoftwareSetting(object):
    def setupUi(self, SoftwareSetting):
        if not SoftwareSetting.objectName():
            SoftwareSetting.setObjectName(u"SoftwareSetting")
        SoftwareSetting.resize(777, 587)
        SoftwareSetting.setContextMenuPolicy(Qt.NoContextMenu)
        icon = QIcon()
        icon.addFile(u":/logo/imcl_logo", QSize(), QIcon.Normal, QIcon.Off)
        SoftwareSetting.setWindowIcon(icon)
        SoftwareSetting.setWindowOpacity(0.900000000000000)
        SoftwareSetting.setStyleSheet(u"background: gray;\n"
"color: rgb(255, 255, 255);")
        self.groupBox = QGroupBox(SoftwareSetting)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 10, 741, 511))
        font = QFont()
        font.setPointSize(14)
        self.groupBox.setFont(font)
        self.line_editor_project_path = QLineEdit(self.groupBox)
        self.line_editor_project_path.setObjectName(u"line_editor_project_path")
        self.line_editor_project_path.setEnabled(True)
        self.line_editor_project_path.setGeometry(QRect(140, 70, 341, 31))
        self.line_editor_project_path.setMinimumSize(QSize(341, 31))
        self.line_editor_project_path.setFont(font)
        self.btn_project_path = QToolButton(self.groupBox)
        self.btn_project_path.setObjectName(u"btn_project_path")
        self.btn_project_path.setEnabled(True)
        self.btn_project_path.setGeometry(QRect(490, 70, 30, 30))
        self.label_project_path = QLabel(self.groupBox)
        self.label_project_path.setObjectName(u"label_project_path")
        self.label_project_path.setGeometry(QRect(17, 70, 121, 30))
        self.label_project_path.setFont(font)
        self.checkBox = QCheckBox(self.groupBox)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(20, 190, 331, 71))
        self.checkBox.setFont(font)
        self.btn_confirm = QPushButton(SoftwareSetting)
        self.btn_confirm.setObjectName(u"btn_confirm")
        self.btn_confirm.setGeometry(QRect(370, 530, 120, 40))
        self.btn_confirm.setFont(font)
        self.btn_apply = QPushButton(SoftwareSetting)
        self.btn_apply.setObjectName(u"btn_apply")
        self.btn_apply.setGeometry(QRect(500, 530, 120, 40))
        self.btn_apply.setFont(font)
        self.btn_cancel = QPushButton(SoftwareSetting)
        self.btn_cancel.setObjectName(u"btn_cancel")
        self.btn_cancel.setGeometry(QRect(630, 530, 120, 40))
        self.btn_cancel.setFont(font)

        self.retranslateUi(SoftwareSetting)

        QMetaObject.connectSlotsByName(SoftwareSetting)
    # setupUi

    def retranslateUi(self, SoftwareSetting):
        SoftwareSetting.setWindowTitle(QCoreApplication.translate("SoftwareSetting", u"Software Setting", None))
        self.groupBox.setTitle(QCoreApplication.translate("SoftwareSetting", u"Software Setting", None))
        self.btn_project_path.setText(QCoreApplication.translate("SoftwareSetting", u"...", None))
        self.label_project_path.setText(QCoreApplication.translate("SoftwareSetting", u"Saving Path: ", None))
        self.checkBox.setText(QCoreApplication.translate("SoftwareSetting", u"Skip the refocusing calculation", None))
        self.btn_confirm.setText(QCoreApplication.translate("SoftwareSetting", u"Confirm", None))
        self.btn_apply.setText(QCoreApplication.translate("SoftwareSetting", u"Apply", None))
        self.btn_cancel.setText(QCoreApplication.translate("SoftwareSetting", u"Cancel", None))
    # retranslateUi

