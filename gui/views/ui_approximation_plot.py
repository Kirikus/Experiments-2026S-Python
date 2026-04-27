# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'approximation_plot.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFormLayout,
    QLabel, QSizePolicy, QVBoxLayout, QWidget)

class Ui_ApproximationPlot(object):
    def setupUi(self, ApproximationPlot):
        if not ApproximationPlot.objectName():
            ApproximationPlot.setObjectName(u"ApproximationPlot")
        ApproximationPlot.resize(700, 600)
        self.verticalLayout = QVBoxLayout(ApproximationPlot)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.parent_ui = QWidget(ApproximationPlot)
        self.parent_ui.setObjectName(u"parent_ui")
        self.parentLayout = QVBoxLayout(self.parent_ui)
        self.parentLayout.setContentsMargins(0, 0, 0, 0)
        self.parentLayout.setObjectName(u"parentLayout")

        self.verticalLayout.addWidget(self.parent_ui)

        self.settingsLayout = QFormLayout()
        self.settingsLayout.setObjectName(u"settingsLayout")
        self.labelXVar = QLabel(ApproximationPlot)
        self.labelXVar.setObjectName(u"labelXVar")

        self.settingsLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelXVar)

        self.xVariableCombo = QComboBox(ApproximationPlot)
        self.xVariableCombo.setObjectName(u"xVariableCombo")

        self.settingsLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.xVariableCombo)

        self.labelYVar = QLabel(ApproximationPlot)
        self.labelYVar.setObjectName(u"labelYVar")

        self.settingsLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelYVar)

        self.yVariableCombo = QComboBox(ApproximationPlot)
        self.yVariableCombo.setObjectName(u"yVariableCombo")

        self.settingsLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.yVariableCombo)

        self.labelShowPoints = QLabel(ApproximationPlot)
        self.labelShowPoints.setObjectName(u"labelShowPoints")

        self.settingsLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelShowPoints)

        self.showPointsCheckBox = QCheckBox(ApproximationPlot)
        self.showPointsCheckBox.setObjectName(u"showPointsCheckBox")
        self.showPointsCheckBox.setChecked(True)

        self.settingsLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.showPointsCheckBox)


        self.verticalLayout.addLayout(self.settingsLayout)


        self.retranslateUi(ApproximationPlot)

        QMetaObject.connectSlotsByName(ApproximationPlot)
    # setupUi

    def retranslateUi(self, ApproximationPlot):
        ApproximationPlot.setWindowTitle(QCoreApplication.translate("ApproximationPlot", u"Approximation Plot", None))
        self.labelXVar.setText(QCoreApplication.translate("ApproximationPlot", u"\u041f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u0430\u044f X", None))
        self.labelYVar.setText(QCoreApplication.translate("ApproximationPlot", u"\u041f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u0430\u044f Y", None))
        self.labelShowPoints.setText(QCoreApplication.translate("ApproximationPlot", u"\u041f\u043e\u043a\u0430\u0437\u044b\u0432\u0430\u0442\u044c \u0442\u043e\u0447\u043a\u0438", None))
        self.showPointsCheckBox.setText("")
    # retranslateUi

