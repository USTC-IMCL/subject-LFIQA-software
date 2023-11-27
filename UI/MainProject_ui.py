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
        self.action_save_project = QAction(MainWindow)
        self.action_save_project.setObjectName(u"action_save_project")
        self.action_load_project = QAction(MainWindow)
        self.action_load_project.setObjectName(u"action_load_project")
        self.action_new_project = QAction(MainWindow)
        self.action_new_project.setObjectName(u"action_new_project")
        self.action_show_log = QAction(MainWindow)
        self.action_show_log.setObjectName(u"action_show_log")
        self.action_show_log.setCheckable(True)
        self.actionLog = QAction(MainWindow)
        self.actionLog.setObjectName(u"actionLog")
        self.actionLog.setCheckable(True)
        self.action_log = QAction(MainWindow)
        self.action_log.setObjectName(u"action_log")
        self.action_log.setCheckable(True)
        self.action_preprocessing = QAction(MainWindow)
        self.action_preprocessing.setObjectName(u"action_preprocessing")
        icon1 = QIcon(QIcon.fromTheme(u"accessories-dictionary"))
        self.action_preprocessing.setIcon(icon1)
        self.actionExperiment = QAction(MainWindow)
        self.actionExperiment.setObjectName(u"actionExperiment")
        self.actionStart_Testing = QAction(MainWindow)
        self.actionStart_Testing.setObjectName(u"actionStart_Testing")
        self.actionSave_As = QAction(MainWindow)
        self.actionSave_As.setObjectName(u"actionSave_As")
        self.actionJPEG_Pleno = QAction(MainWindow)
        self.actionJPEG_Pleno.setObjectName(u"actionJPEG_Pleno")
        self.actionAuthors = QAction(MainWindow)
        self.actionAuthors.setObjectName(u"actionAuthors")
        self.actionLFIQoE = QAction(MainWindow)
        self.actionLFIQoE.setObjectName(u"actionLFIQoE")
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
        self.menuRun = QMenu(self.menubar)
        self.menuRun.setObjectName(u"menuRun")
        self.menuAbout = QMenu(self.menubar)
        self.menuAbout.setObjectName(u"menuAbout")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSetting.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuRun.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        self.menuFile.addAction(self.action_new_project)
        self.menuFile.addAction(self.action_load_project)
        self.menuFile.addAction(self.action_save_project)
        self.menuFile.addAction(self.actionSave_As)
        self.menuSetting.addAction(self.action_show_log)
        self.menuRun.addAction(self.action_preprocessing)
        self.menuRun.addAction(self.actionExperiment)
        self.menuRun.addAction(self.actionStart_Testing)
        self.menuAbout.addAction(self.actionJPEG_Pleno)
        self.menuAbout.addAction(self.actionAuthors)
        self.menuAbout.addAction(self.actionLFIQoE)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Light Field Quality of Experience", None))
        self.action_save_project.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.action_load_project.setText(QCoreApplication.translate("MainWindow", u"Load...", None))
        self.action_new_project.setText(QCoreApplication.translate("MainWindow", u"New Project", None))
        self.action_show_log.setText(QCoreApplication.translate("MainWindow", u"Skip Preprocessing", None))
        self.actionLog.setText(QCoreApplication.translate("MainWindow", u"Logs", None))
        self.action_log.setText(QCoreApplication.translate("MainWindow", u"Log", None))
        self.action_preprocessing.setText(QCoreApplication.translate("MainWindow", u"Pre Processing", None))
        self.actionExperiment.setText(QCoreApplication.translate("MainWindow", u"Start Training", None))
        self.actionStart_Testing.setText(QCoreApplication.translate("MainWindow", u"Start Test", None))
        self.actionSave_As.setText(QCoreApplication.translate("MainWindow", u"Save As", None))
        self.actionJPEG_Pleno.setText(QCoreApplication.translate("MainWindow", u"JPEG Pleno", None))
        self.actionAuthors.setText(QCoreApplication.translate("MainWindow", u"Authors", None))
        self.actionLFIQoE.setText(QCoreApplication.translate("MainWindow", u"LFIQoE", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"Project File", None))
        self.menuSetting.setTitle(QCoreApplication.translate("MainWindow", u"Setting", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuRun.setTitle(QCoreApplication.translate("MainWindow", u"Run", None))
        self.menuAbout.setTitle(QCoreApplication.translate("MainWindow", u"About", None))
    # retranslateUi

