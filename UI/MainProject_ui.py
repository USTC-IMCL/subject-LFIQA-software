# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainProject.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QWidget)
import UI_res_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        font = QFont()
        font.setPointSize(14)
        MainWindow.setFont(font)
        icon = QIcon()
        icon.addFile(u":/logo/imcl_logo", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowOpacity(0.900000000000000)
        MainWindow.setStyleSheet(u"")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.action_Load_Project = QAction(MainWindow)
        self.action_Load_Project.setObjectName(u"action_Load_Project")
        self.actionNew_Project = QAction(MainWindow)
        self.actionNew_Project.setObjectName(u"actionNew_Project")
        self.action_show_log = QAction(MainWindow)
        self.action_show_log.setObjectName(u"action_show_log")
        self.action_show_log.setCheckable(True)
        self.actionLog = QAction(MainWindow)
        self.actionLog.setObjectName(u"actionLog")
        self.actionLog.setCheckable(True)
        self.action_log = QAction(MainWindow)
        self.action_log.setObjectName(u"action_log")
        self.action_log.setCheckable(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setFont(font)
        self.centralwidget.setStyleSheet(u"background: gray;\n"
"color: rgb(255, 255, 255);")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 23))
        font1 = QFont()
        font1.setPointSize(10)
        self.menubar.setFont(font1)
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuSetting = QMenu(self.menubar)
        self.menuSetting.setObjectName(u"menuSetting")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSetting.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.action_Load_Project)
        self.menuFile.addAction(self.actionNew_Project)
        self.menuSetting.addAction(self.action_show_log)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Light Field Quality of Experience", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save Project", None))
        self.action_Load_Project.setText(QCoreApplication.translate("MainWindow", u"Load Project", None))
        self.actionNew_Project.setText(QCoreApplication.translate("MainWindow", u"New Project", None))
        self.action_show_log.setText(QCoreApplication.translate("MainWindow", u"Skip Preprocessing", None))
        self.actionLog.setText(QCoreApplication.translate("MainWindow", u"Logs", None))
        self.action_log.setText(QCoreApplication.translate("MainWindow", u"Log", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"Project File", None))
        self.menuSetting.setTitle(QCoreApplication.translate("MainWindow", u"Setting", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
    # retranslateUi

