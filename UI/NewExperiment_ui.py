# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'NewExperiment.ui'
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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QRadioButton, QScrollArea, QSizePolicy, QSpacerItem,
    QStackedWidget, QToolButton, QVBoxLayout, QWidget)
import UI_res_rc

class Ui_NewExperimentForm(object):
    def setupUi(self, NewExperimentForm):
        if not NewExperimentForm.objectName():
            NewExperimentForm.setObjectName(u"NewExperimentForm")
        NewExperimentForm.resize(777, 587)
        icon = QIcon()
        icon.addFile(u":/logo/imcl_logo", QSize(), QIcon.Normal, QIcon.Off)
        NewExperimentForm.setWindowIcon(icon)
        NewExperimentForm.setWindowOpacity(0.900000000000000)
        NewExperimentForm.setStyleSheet(u"background: gray;\n"
"color: rgb(255, 255, 255);")
        self.ConfigStackWidget = QStackedWidget(NewExperimentForm)
        self.ConfigStackWidget.setObjectName(u"ConfigStackWidget")
        self.ConfigStackWidget.setGeometry(QRect(0, 0, 777, 587))
        self.page_0 = QWidget()
        self.page_0.setObjectName(u"page_0")
        self.HintLabel = QLabel(self.page_0)
        self.HintLabel.setObjectName(u"HintLabel")
        self.HintLabel.setGeometry(QRect(20, 10, 631, 251))
        font = QFont()
        font.setPointSize(14)
        self.HintLabel.setFont(font)
        self.groupBox = QGroupBox(self.page_0)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(20, 290, 731, 181))
        self.groupBox.setFont(font)
        self.radio_btn_json = QRadioButton(self.groupBox)
        self.radio_btn_json.setObjectName(u"radio_btn_json")
        self.radio_btn_json.setGeometry(QRect(50, 38, 211, 131))
        self.radio_btn_json.setFont(font)
        self.page_0_json_path = QLineEdit(self.groupBox)
        self.page_0_json_path.setObjectName(u"page_0_json_path")
        self.page_0_json_path.setGeometry(QRect(250, 90, 341, 31))
        self.page_0_json_path.setFont(font)
        self.btn_select_json = QToolButton(self.groupBox)
        self.btn_select_json.setObjectName(u"btn_select_json")
        self.btn_select_json.setGeometry(QRect(590, 90, 24, 31))
        self.horizontalLayoutWidget_7 = QWidget(self.page_0)
        self.horizontalLayoutWidget_7.setObjectName(u"horizontalLayoutWidget_7")
        self.horizontalLayoutWidget_7.setGeometry(QRect(480, 520, 270, 43))
        self.horizontalLayout_14 = QHBoxLayout(self.horizontalLayoutWidget_7)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.page_0_btn_next = QPushButton(self.horizontalLayoutWidget_7)
        self.page_0_btn_next.setObjectName(u"page_0_btn_next")
        self.page_0_btn_next.setMinimumSize(QSize(131, 41))
        self.page_0_btn_next.setFont(font)

        self.horizontalLayout_14.addWidget(self.page_0_btn_next)

        self.page_0_btn_cancel = QPushButton(self.horizontalLayoutWidget_7)
        self.page_0_btn_cancel.setObjectName(u"page_0_btn_cancel")
        self.page_0_btn_cancel.setMinimumSize(QSize(131, 41))
        self.page_0_btn_cancel.setFont(font)

        self.horizontalLayout_14.addWidget(self.page_0_btn_cancel)

        self.ConfigStackWidget.addWidget(self.page_0)
        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")
        self.groupBox_2 = QGroupBox(self.page_1)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 10, 751, 561))
        self.groupBox_2.setFont(font)
        self.ConfigScrollAreaTrain = QScrollArea(self.groupBox_2)
        self.ConfigScrollAreaTrain.setObjectName(u"ConfigScrollAreaTrain")
        self.ConfigScrollAreaTrain.setGeometry(QRect(10, 89, 731, 411))
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ConfigScrollAreaTrain.sizePolicy().hasHeightForWidth())
        self.ConfigScrollAreaTrain.setSizePolicy(sizePolicy)
        self.ConfigScrollAreaTrain.setMinimumSize(QSize(731, 411))
        self.ConfigScrollAreaTrain.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.ConfigScrollAreaTrain.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ConfigScrollAreaTrain.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.ConfigScrollAreaTrain.setWidgetResizable(True)
        self.scrollAreaWidgetContents_training = QWidget()
        self.scrollAreaWidgetContents_training.setObjectName(u"scrollAreaWidgetContents_training")
        self.scrollAreaWidgetContents_training.setGeometry(QRect(0, 0, 729, 409))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents_training)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.LFILayout_training = QVBoxLayout()
        self.LFILayout_training.setObjectName(u"LFILayout_training")

        self.verticalLayout_2.addLayout(self.LFILayout_training)

        self.ConfigScrollAreaTrain.setWidget(self.scrollAreaWidgetContents_training)
        self.page_1_btn_add_group = QPushButton(self.groupBox_2)
        self.page_1_btn_add_group.setObjectName(u"page_1_btn_add_group")
        self.page_1_btn_add_group.setGeometry(QRect(20, 40, 141, 41))
        self.page_1_btn_add_group.setFont(font)
        self.training_angularBox = QGroupBox(self.groupBox_2)
        self.training_angularBox.setObjectName(u"training_angularBox")
        self.training_angularBox.setGeometry(QRect(190, 20, 241, 61))
        self.training_radio_btn_xy = QRadioButton(self.training_angularBox)
        self.training_radio_btn_xy.setObjectName(u"training_radio_btn_xy")
        self.training_radio_btn_xy.setGeometry(QRect(30, 18, 95, 31))
        self.training_radio_btn_xy.setFont(font)
        self.training_radio_btn_xy.setChecked(True)
        self.training_radio_btn_hw = QRadioButton(self.training_angularBox)
        self.training_radio_btn_hw.setObjectName(u"training_radio_btn_hw")
        self.training_radio_btn_hw.setGeometry(QRect(130, 18, 95, 31))
        self.training_radio_btn_hw.setFont(font)
        self.horizontalLayoutWidget_6 = QWidget(self.groupBox_2)
        self.horizontalLayoutWidget_6.setObjectName(u"horizontalLayoutWidget_6")
        self.horizontalLayoutWidget_6.setGeometry(QRect(340, 510, 407, 43))
        self.horizontalLayout_13 = QHBoxLayout(self.horizontalLayoutWidget_6)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.page_1_btn_prev = QPushButton(self.horizontalLayoutWidget_6)
        self.page_1_btn_prev.setObjectName(u"page_1_btn_prev")
        self.page_1_btn_prev.setMinimumSize(QSize(131, 41))
        self.page_1_btn_prev.setFont(font)

        self.horizontalLayout_13.addWidget(self.page_1_btn_prev)

        self.page_1_btn_next = QPushButton(self.horizontalLayoutWidget_6)
        self.page_1_btn_next.setObjectName(u"page_1_btn_next")
        self.page_1_btn_next.setMinimumSize(QSize(131, 41))
        self.page_1_btn_next.setFont(font)

        self.horizontalLayout_13.addWidget(self.page_1_btn_next)

        self.page_1_btn_cancel = QPushButton(self.horizontalLayoutWidget_6)
        self.page_1_btn_cancel.setObjectName(u"page_1_btn_cancel")
        self.page_1_btn_cancel.setMinimumSize(QSize(131, 41))
        self.page_1_btn_cancel.setFont(font)

        self.horizontalLayout_13.addWidget(self.page_1_btn_cancel)

        self.page_1_btn_add_group.raise_()
        self.ConfigScrollAreaTrain.raise_()
        self.training_angularBox.raise_()
        self.horizontalLayoutWidget_6.raise_()
        self.ConfigStackWidget.addWidget(self.page_1)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.groupBox_4 = QGroupBox(self.page_2)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(10, 10, 751, 561))
        self.groupBox_4.setFont(font)
        self.ConfigScrollAreaTest = QScrollArea(self.groupBox_4)
        self.ConfigScrollAreaTest.setObjectName(u"ConfigScrollAreaTest")
        self.ConfigScrollAreaTest.setGeometry(QRect(10, 89, 731, 411))
        sizePolicy.setHeightForWidth(self.ConfigScrollAreaTest.sizePolicy().hasHeightForWidth())
        self.ConfigScrollAreaTest.setSizePolicy(sizePolicy)
        self.ConfigScrollAreaTest.setMinimumSize(QSize(731, 411))
        self.ConfigScrollAreaTest.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.ConfigScrollAreaTest.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ConfigScrollAreaTest.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.ConfigScrollAreaTest.setWidgetResizable(True)
        self.scrollAreaWidgetContents_test = QWidget()
        self.scrollAreaWidgetContents_test.setObjectName(u"scrollAreaWidgetContents_test")
        self.scrollAreaWidgetContents_test.setGeometry(QRect(0, 0, 729, 409))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents_test)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.LFILayout_test = QVBoxLayout()
        self.LFILayout_test.setObjectName(u"LFILayout_test")

        self.verticalLayout_3.addLayout(self.LFILayout_test)

        self.ConfigScrollAreaTest.setWidget(self.scrollAreaWidgetContents_test)
        self.page_2_btn_add_group = QPushButton(self.groupBox_4)
        self.page_2_btn_add_group.setObjectName(u"page_2_btn_add_group")
        self.page_2_btn_add_group.setGeometry(QRect(20, 40, 141, 41))
        self.page_2_btn_add_group.setFont(font)
        self.angularBox_2 = QGroupBox(self.groupBox_4)
        self.angularBox_2.setObjectName(u"angularBox_2")
        self.angularBox_2.setGeometry(QRect(190, 20, 241, 61))
        self.test_radio_btn_xy = QRadioButton(self.angularBox_2)
        self.test_radio_btn_xy.setObjectName(u"test_radio_btn_xy")
        self.test_radio_btn_xy.setGeometry(QRect(30, 18, 95, 31))
        self.test_radio_btn_xy.setFont(font)
        self.test_radio_btn_xy.setChecked(True)
        self.test_radio_btn_hw = QRadioButton(self.angularBox_2)
        self.test_radio_btn_hw.setObjectName(u"test_radio_btn_hw")
        self.test_radio_btn_hw.setGeometry(QRect(130, 18, 95, 31))
        self.test_radio_btn_hw.setFont(font)
        self.horizontalLayoutWidget_9 = QWidget(self.groupBox_4)
        self.horizontalLayoutWidget_9.setObjectName(u"horizontalLayoutWidget_9")
        self.horizontalLayoutWidget_9.setGeometry(QRect(340, 510, 407, 43))
        self.horizontalLayout_16 = QHBoxLayout(self.horizontalLayoutWidget_9)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.page_2_btn_prev = QPushButton(self.horizontalLayoutWidget_9)
        self.page_2_btn_prev.setObjectName(u"page_2_btn_prev")
        self.page_2_btn_prev.setMinimumSize(QSize(131, 41))
        self.page_2_btn_prev.setFont(font)

        self.horizontalLayout_16.addWidget(self.page_2_btn_prev)

        self.page_2_btn_next = QPushButton(self.horizontalLayoutWidget_9)
        self.page_2_btn_next.setObjectName(u"page_2_btn_next")
        self.page_2_btn_next.setMinimumSize(QSize(131, 41))
        self.page_2_btn_next.setFont(font)

        self.horizontalLayout_16.addWidget(self.page_2_btn_next)

        self.page_2_btn_cancel = QPushButton(self.horizontalLayoutWidget_9)
        self.page_2_btn_cancel.setObjectName(u"page_2_btn_cancel")
        self.page_2_btn_cancel.setMinimumSize(QSize(131, 41))
        self.page_2_btn_cancel.setFont(font)

        self.horizontalLayout_16.addWidget(self.page_2_btn_cancel)

        self.ConfigStackWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.groupBox_3 = QGroupBox(self.page_3)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(10, 10, 751, 561))
        self.groupBox_3.setFont(font)
        self.gridLayoutWidget = QWidget(self.groupBox_3)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(20, 40, 633, 394))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_9)

        self.page_3_display_label_4 = QLabel(self.gridLayoutWidget)
        self.page_3_display_label_4.setObjectName(u"page_3_display_label_4")
        self.page_3_display_label_4.setFont(font)

        self.horizontalLayout_9.addWidget(self.page_3_display_label_4)

        self.horizontalSpacer_20 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_20)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.radio_btn_refocusing_passive = QRadioButton(self.gridLayoutWidget)
        self.radio_btn_refocusing_passive.setObjectName(u"radio_btn_refocusing_passive")
        self.radio_btn_refocusing_passive.setFont(font)

        self.horizontalLayout_10.addWidget(self.radio_btn_refocusing_passive)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_12)

        self.radio_btn_refocusing_active = QRadioButton(self.gridLayoutWidget)
        self.radio_btn_refocusing_active.setObjectName(u"radio_btn_refocusing_active")
        self.radio_btn_refocusing_active.setFont(font)

        self.horizontalLayout_10.addWidget(self.radio_btn_refocusing_active)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_13)

        self.radio_btn_refocusing_none = QRadioButton(self.gridLayoutWidget)
        self.radio_btn_refocusing_none.setObjectName(u"radio_btn_refocusing_none")
        self.radio_btn_refocusing_none.setFont(font)

        self.horizontalLayout_10.addWidget(self.radio_btn_refocusing_none)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_15)


        self.horizontalLayout_9.addLayout(self.horizontalLayout_10)


        self.gridLayout.addLayout(self.horizontalLayout_9, 5, 0, 1, 1)

        self.page_2_display_label_2 = QLabel(self.gridLayoutWidget)
        self.page_2_display_label_2.setObjectName(u"page_2_display_label_2")
        self.page_2_display_label_2.setFont(font)

        self.gridLayout.addWidget(self.page_2_display_label_2, 3, 0, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_16)

        self.radio_btn_cmp_pair = QRadioButton(self.gridLayoutWidget)
        self.radio_btn_cmp_pair.setObjectName(u"radio_btn_cmp_pair")
        self.radio_btn_cmp_pair.setFont(font)

        self.horizontalLayout_5.addWidget(self.radio_btn_cmp_pair)

        self.pair_line_editor = QLineEdit(self.gridLayoutWidget)
        self.pair_line_editor.setObjectName(u"pair_line_editor")
        self.pair_line_editor.setMinimumSize(QSize(290, 0))
        self.pair_line_editor.setFont(font)

        self.horizontalLayout_5.addWidget(self.pair_line_editor)

        self.btn_pair_line_editor = QToolButton(self.gridLayoutWidget)
        self.btn_pair_line_editor.setObjectName(u"btn_pair_line_editor")

        self.horizontalLayout_5.addWidget(self.btn_pair_line_editor)

        self.horizontalSpacer_21 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_21)


        self.gridLayout.addLayout(self.horizontalLayout_5, 11, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_11)

        self.radio_btn_cmp_double = QRadioButton(self.gridLayoutWidget)
        self.radio_btn_cmp_double.setObjectName(u"radio_btn_cmp_double")
        self.radio_btn_cmp_double.setFont(font)

        self.horizontalLayout_4.addWidget(self.radio_btn_cmp_double)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_17)

        self.radio_btn_cmp_single = QRadioButton(self.gridLayoutWidget)
        self.radio_btn_cmp_single.setObjectName(u"radio_btn_cmp_single")
        self.radio_btn_cmp_single.setFont(font)

        self.horizontalLayout_4.addWidget(self.radio_btn_cmp_single)

        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_18)


        self.gridLayout.addLayout(self.horizontalLayout_4, 8, 0, 1, 1)

        self.page_2_display_label_4 = QLabel(self.gridLayoutWidget)
        self.page_2_display_label_4.setObjectName(u"page_2_display_label_4")
        self.page_2_display_label_4.setFont(font)

        self.gridLayout.addWidget(self.page_2_display_label_4, 12, 0, 1, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_8)

        self.page_3_display_label_3 = QLabel(self.gridLayoutWidget)
        self.page_3_display_label_3.setObjectName(u"page_3_display_label_3")
        self.page_3_display_label_3.setFont(font)

        self.horizontalLayout_7.addWidget(self.page_3_display_label_3)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_10)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.radio_btn_view_change_passive = QRadioButton(self.gridLayoutWidget)
        self.radio_btn_view_change_passive.setObjectName(u"radio_btn_view_change_passive")
        self.radio_btn_view_change_passive.setFont(font)

        self.horizontalLayout_8.addWidget(self.radio_btn_view_change_passive)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_6)

        self.radio_btn_view_change_active = QRadioButton(self.gridLayoutWidget)
        self.radio_btn_view_change_active.setObjectName(u"radio_btn_view_change_active")
        self.radio_btn_view_change_active.setFont(font)

        self.horizontalLayout_8.addWidget(self.radio_btn_view_change_active)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_7)

        self.radio_btn_view_change_none = QRadioButton(self.gridLayoutWidget)
        self.radio_btn_view_change_none.setObjectName(u"radio_btn_view_change_none")
        self.radio_btn_view_change_none.setFont(font)

        self.horizontalLayout_8.addWidget(self.radio_btn_view_change_none)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_14)


        self.horizontalLayout_7.addLayout(self.horizontalLayout_8)


        self.gridLayout.addLayout(self.horizontalLayout_7, 4, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 2, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 6, 0, 1, 1)

        self.page_2_display_label = QLabel(self.gridLayoutWidget)
        self.page_2_display_label.setObjectName(u"page_2_display_label")
        self.page_2_display_label.setFont(font)

        self.gridLayout.addWidget(self.page_2_display_label, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.radio_btn_disp_2D = QRadioButton(self.gridLayoutWidget)
        self.radio_btn_disp_2D.setObjectName(u"radio_btn_disp_2D")
        self.radio_btn_disp_2D.setFont(font)

        self.horizontalLayout.addWidget(self.radio_btn_disp_2D)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.radio_btn_disp_3D_LR = QRadioButton(self.gridLayoutWidget)
        self.radio_btn_disp_3D_LR.setObjectName(u"radio_btn_disp_3D_LR")
        self.radio_btn_disp_3D_LR.setFont(font)

        self.horizontalLayout.addWidget(self.radio_btn_disp_3D_LR)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.radio_btn_disp_3D_full = QRadioButton(self.gridLayoutWidget)
        self.radio_btn_disp_3D_full.setObjectName(u"radio_btn_disp_3D_full")
        self.radio_btn_disp_3D_full.setFont(font)
        self.radio_btn_disp_3D_full.setFocusPolicy(Qt.StrongFocus)
        self.radio_btn_disp_3D_full.setStyleSheet(u"color: rgb(148, 148, 148)")
        self.radio_btn_disp_3D_full.setCheckable(False)
        self.radio_btn_disp_3D_full.setAutoExclusive(False)

        self.horizontalLayout.addWidget(self.radio_btn_disp_3D_full)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.page_2_display_label_3 = QLabel(self.gridLayoutWidget)
        self.page_2_display_label_3.setObjectName(u"page_2_display_label_3")
        self.page_2_display_label_3.setFont(font)

        self.gridLayout.addWidget(self.page_2_display_label_3, 7, 0, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer_19 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_19)

        self.radio_btn_save_csv = QRadioButton(self.gridLayoutWidget)
        self.radio_btn_save_csv.setObjectName(u"radio_btn_save_csv")
        self.radio_btn_save_csv.setFont(font)

        self.horizontalLayout_6.addWidget(self.radio_btn_save_csv)

        self.horizontalSpacer_22 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_22)

        self.radio_btn_save_excel = QRadioButton(self.gridLayoutWidget)
        self.radio_btn_save_excel.setObjectName(u"radio_btn_save_excel")
        self.radio_btn_save_excel.setFont(font)

        self.horizontalLayout_6.addWidget(self.radio_btn_save_excel)

        self.horizontalSpacer_24 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_24)

        self.horizontalSpacer_25 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_25)

        self.horizontalSpacer_23 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_23)


        self.gridLayout.addLayout(self.horizontalLayout_6, 13, 0, 1, 1)

        self.horizontalLayoutWidget_8 = QWidget(self.groupBox_3)
        self.horizontalLayoutWidget_8.setObjectName(u"horizontalLayoutWidget_8")
        self.horizontalLayoutWidget_8.setGeometry(QRect(340, 510, 407, 43))
        self.horizontalLayout_15 = QHBoxLayout(self.horizontalLayoutWidget_8)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.page_3_btn_prev = QPushButton(self.horizontalLayoutWidget_8)
        self.page_3_btn_prev.setObjectName(u"page_3_btn_prev")
        self.page_3_btn_prev.setMinimumSize(QSize(131, 41))
        self.page_3_btn_prev.setFont(font)

        self.horizontalLayout_15.addWidget(self.page_3_btn_prev)

        self.page_3_btn_finish = QPushButton(self.horizontalLayoutWidget_8)
        self.page_3_btn_finish.setObjectName(u"page_3_btn_finish")
        self.page_3_btn_finish.setMinimumSize(QSize(131, 41))
        self.page_3_btn_finish.setFont(font)

        self.horizontalLayout_15.addWidget(self.page_3_btn_finish)

        self.page_3_btn_cancel = QPushButton(self.horizontalLayoutWidget_8)
        self.page_3_btn_cancel.setObjectName(u"page_3_btn_cancel")
        self.page_3_btn_cancel.setMinimumSize(QSize(131, 41))
        self.page_3_btn_cancel.setFont(font)

        self.horizontalLayout_15.addWidget(self.page_3_btn_cancel)

        self.label_3d_ns = QLabel(self.groupBox_3)
        self.label_3d_ns.setObjectName(u"label_3d_ns")
        self.label_3d_ns.setGeometry(QRect(480, 90, 191, 31))
        self.label_3d_ns.setStyleSheet(u"")
        self.ConfigStackWidget.addWidget(self.page_3)

        self.retranslateUi(NewExperimentForm)

        self.ConfigStackWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(NewExperimentForm)
    # setupUi

    def retranslateUi(self, NewExperimentForm):
        NewExperimentForm.setWindowTitle(QCoreApplication.translate("NewExperimentForm", u"Create New Experiment", None))
        self.HintLabel.setText(QCoreApplication.translate("NewExperimentForm", u"<html><head/><body><p>Only configuration from Json file is supported.</p><p><br/>Please select your json file first.</p><p><br/>Then click the next step.</p></body></html>", None))
        self.groupBox.setTitle(QCoreApplication.translate("NewExperimentForm", u"Configuration", None))
        self.radio_btn_json.setText(QCoreApplication.translate("NewExperimentForm", u"Config with Json", None))
        self.btn_select_json.setText(QCoreApplication.translate("NewExperimentForm", u"...", None))
        self.page_0_btn_next.setText(QCoreApplication.translate("NewExperimentForm", u"Next Step", None))
        self.page_0_btn_cancel.setText(QCoreApplication.translate("NewExperimentForm", u"Cancel", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("NewExperimentForm", u"Training Configuration", None))
        self.page_1_btn_add_group.setText(QCoreApplication.translate("NewExperimentForm", u"Add New LFI", None))
        self.training_angularBox.setTitle(QCoreApplication.translate("NewExperimentForm", u"Angular Format", None))
        self.training_radio_btn_xy.setText(QCoreApplication.translate("NewExperimentForm", u"X_Y", None))
        self.training_radio_btn_hw.setText(QCoreApplication.translate("NewExperimentForm", u"H_W", None))
        self.page_1_btn_prev.setText(QCoreApplication.translate("NewExperimentForm", u"Previous", None))
        self.page_1_btn_next.setText(QCoreApplication.translate("NewExperimentForm", u"Next", None))
        self.page_1_btn_cancel.setText(QCoreApplication.translate("NewExperimentForm", u"Cancel", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("NewExperimentForm", u"Test Configuration", None))
        self.page_2_btn_add_group.setText(QCoreApplication.translate("NewExperimentForm", u"Add New LFI", None))
        self.angularBox_2.setTitle(QCoreApplication.translate("NewExperimentForm", u"Angular Format", None))
        self.test_radio_btn_xy.setText(QCoreApplication.translate("NewExperimentForm", u"X_Y", None))
        self.test_radio_btn_hw.setText(QCoreApplication.translate("NewExperimentForm", u"H_W", None))
        self.page_2_btn_prev.setText(QCoreApplication.translate("NewExperimentForm", u"Previous", None))
        self.page_2_btn_next.setText(QCoreApplication.translate("NewExperimentForm", u"Next", None))
        self.page_2_btn_cancel.setText(QCoreApplication.translate("NewExperimentForm", u"Cancel", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("NewExperimentForm", u"Experiment Settings", None))
        self.page_3_display_label_4.setText(QCoreApplication.translate("NewExperimentForm", u"--Refocusing", None))
        self.radio_btn_refocusing_passive.setText(QCoreApplication.translate("NewExperimentForm", u"Passive", None))
        self.radio_btn_refocusing_active.setText(QCoreApplication.translate("NewExperimentForm", u"Active", None))
        self.radio_btn_refocusing_none.setText(QCoreApplication.translate("NewExperimentForm", u"None", None))
        self.page_2_display_label_2.setText(QCoreApplication.translate("NewExperimentForm", u"Features", None))
        self.radio_btn_cmp_pair.setText(QCoreApplication.translate("NewExperimentForm", u"Pair-wise", None))
        self.btn_pair_line_editor.setText(QCoreApplication.translate("NewExperimentForm", u"...", None))
        self.radio_btn_cmp_double.setText(QCoreApplication.translate("NewExperimentForm", u"Double Stimulus", None))
        self.radio_btn_cmp_single.setText(QCoreApplication.translate("NewExperimentForm", u"Single Stimuli", None))
        self.page_2_display_label_4.setText(QCoreApplication.translate("NewExperimentForm", u"Save Format", None))
        self.page_3_display_label_3.setText(QCoreApplication.translate("NewExperimentForm", u"--View Change", None))
        self.radio_btn_view_change_passive.setText(QCoreApplication.translate("NewExperimentForm", u"Passive", None))
        self.radio_btn_view_change_active.setText(QCoreApplication.translate("NewExperimentForm", u"Active", None))
        self.radio_btn_view_change_none.setText(QCoreApplication.translate("NewExperimentForm", u"None", None))
        self.page_2_display_label.setText(QCoreApplication.translate("NewExperimentForm", u"Display Type", None))
        self.radio_btn_disp_2D.setText(QCoreApplication.translate("NewExperimentForm", u"2D", None))
        self.radio_btn_disp_3D_LR.setText(QCoreApplication.translate("NewExperimentForm", u"3D (Left & Right)", None))
        self.radio_btn_disp_3D_full.setText(QCoreApplication.translate("NewExperimentForm", u"3D (Full)", None))
        self.page_2_display_label_3.setText(QCoreApplication.translate("NewExperimentForm", u"Methodology", None))
        self.radio_btn_save_csv.setText(QCoreApplication.translate("NewExperimentForm", u"CSV", None))
        self.radio_btn_save_excel.setText(QCoreApplication.translate("NewExperimentForm", u"Excel", None))
        self.page_3_btn_prev.setText(QCoreApplication.translate("NewExperimentForm", u"Previous", None))
        self.page_3_btn_finish.setText(QCoreApplication.translate("NewExperimentForm", u"Finish", None))
        self.page_3_btn_cancel.setText(QCoreApplication.translate("NewExperimentForm", u"Cancel", None))
        self.label_3d_ns.setText(QCoreApplication.translate("NewExperimentForm", u"Not supported yet.", None))
    # retranslateUi

