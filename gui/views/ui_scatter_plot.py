# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'scatter_plot.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QLabel,
    QSizePolicy, QSpinBox, QVBoxLayout, QWidget)

class Ui_ScatterPlot(object):
    def setupUi(self, ScatterPlot):
        if not ScatterPlot.objectName():
            ScatterPlot.setObjectName(u"ScatterPlot")
        ScatterPlot.resize(700, 600)
        self.verticalLayout = QVBoxLayout(ScatterPlot)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.parent_ui = QWidget(ScatterPlot)
        self.parent_ui.setObjectName(u"parent_ui")
        self.parentLayout = QVBoxLayout(self.parent_ui)
        self.parentLayout.setContentsMargins(0, 0, 0, 0)
        self.parentLayout.setObjectName(u"parentLayout")

        self.verticalLayout.addWidget(self.parent_ui)

        self.settingsLayout = QFormLayout()
        self.settingsLayout.setObjectName(u"settingsLayout")
        self.labelXVar = QLabel(ScatterPlot)
        self.labelXVar.setObjectName(u"labelXVar")

        self.settingsLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelXVar)

        self.xVariableCombo = QComboBox(ScatterPlot)
        self.xVariableCombo.setObjectName(u"xVariableCombo")

        self.settingsLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.xVariableCombo)

        self.labelYVar = QLabel(ScatterPlot)
        self.labelYVar.setObjectName(u"labelYVar")

        self.settingsLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelYVar)

        self.yVariableCombo = QComboBox(ScatterPlot)
        self.yVariableCombo.setObjectName(u"yVariableCombo")

        self.settingsLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.yVariableCombo)

        self.labelSymbol = QLabel(ScatterPlot)
        self.labelSymbol.setObjectName(u"labelSymbol")

        self.settingsLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelSymbol)

        self.symbolCombo = QComboBox(ScatterPlot)
        self.symbolCombo.setObjectName(u"symbolCombo")

        self.settingsLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.symbolCombo)

        self.labelSize = QLabel(ScatterPlot)
        self.labelSize.setObjectName(u"labelSize")

        self.settingsLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.labelSize)

        self.sizeSpin = QSpinBox(ScatterPlot)
        self.sizeSpin.setObjectName(u"sizeSpin")
        self.sizeSpin.setMinimum(2)
        self.sizeSpin.setMaximum(50)
        self.sizeSpin.setValue(8)

        self.settingsLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.sizeSpin)


        self.verticalLayout.addLayout(self.settingsLayout)


        self.retranslateUi(ScatterPlot)

        QMetaObject.connectSlotsByName(ScatterPlot)
    # setupUi

    def retranslateUi(self, ScatterPlot):
        ScatterPlot.setWindowTitle(QCoreApplication.translate("ScatterPlot", u"Scatter Plot", None))
        self.labelXVar.setText(QCoreApplication.translate("ScatterPlot", u"\u041f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u0430\u044f X", None))
        self.labelYVar.setText(QCoreApplication.translate("ScatterPlot", u"\u041f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u0430\u044f Y", None))
        self.labelSymbol.setText(QCoreApplication.translate("ScatterPlot", u"\u0421\u0438\u043c\u0432\u043e\u043b", None))
        self.labelSize.setText(QCoreApplication.translate("ScatterPlot", u"\u0420\u0430\u0437\u043c\u0435\u0440", None))
    # retranslateUi

