# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'line_plot.ui'
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

class Ui_LinePlot(object):
    def setupUi(self, LinePlot):
        if not LinePlot.objectName():
            LinePlot.setObjectName(u"LinePlot")
        LinePlot.resize(700, 600)
        self.verticalLayout = QVBoxLayout(LinePlot)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.parent_ui = QWidget(LinePlot)
        self.parent_ui.setObjectName(u"parent_ui")
        self.parentLayout = QVBoxLayout(self.parent_ui)
        self.parentLayout.setContentsMargins(0, 0, 0, 0)
        self.parentLayout.setObjectName(u"parentLayout")

        self.verticalLayout.addWidget(self.parent_ui)

        self.settingsLayout = QFormLayout()
        self.settingsLayout.setObjectName(u"settingsLayout")
        self.labelXVar = QLabel(LinePlot)
        self.labelXVar.setObjectName(u"labelXVar")

        self.settingsLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelXVar)

        self.xVariableCombo = QComboBox(LinePlot)
        self.xVariableCombo.setObjectName(u"xVariableCombo")

        self.settingsLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.xVariableCombo)

        self.labelYVar = QLabel(LinePlot)
        self.labelYVar.setObjectName(u"labelYVar")

        self.settingsLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelYVar)

        self.yVariableCombo = QComboBox(LinePlot)
        self.yVariableCombo.setObjectName(u"yVariableCombo")

        self.settingsLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.yVariableCombo)

        self.labelColor = QLabel(LinePlot)
        self.labelColor.setObjectName(u"labelColor")

        self.settingsLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelColor)

        self.colorCombo = QComboBox(LinePlot)
        self.colorCombo.setObjectName(u"colorCombo")

        self.settingsLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.colorCombo)

        self.labelWidth = QLabel(LinePlot)
        self.labelWidth.setObjectName(u"labelWidth")

        self.settingsLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.labelWidth)

        self.widthSpin = QSpinBox(LinePlot)
        self.widthSpin.setObjectName(u"widthSpin")
        self.widthSpin.setMinimum(1)
        self.widthSpin.setMaximum(10)
        self.widthSpin.setValue(2)

        self.settingsLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.widthSpin)


        self.verticalLayout.addLayout(self.settingsLayout)


        self.retranslateUi(LinePlot)

        QMetaObject.connectSlotsByName(LinePlot)
    # setupUi

    def retranslateUi(self, LinePlot):
        LinePlot.setWindowTitle(QCoreApplication.translate("LinePlot", u"Line Plot", None))
        self.labelXVar.setText(QCoreApplication.translate("LinePlot", u"\u041f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u0430\u044f X", None))
        self.labelYVar.setText(QCoreApplication.translate("LinePlot", u"\u041f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u0430\u044f Y", None))
        self.labelColor.setText(QCoreApplication.translate("LinePlot", u"\u0426\u0432\u0435\u0442", None))
        self.labelWidth.setText(QCoreApplication.translate("LinePlot", u"\u0422\u043e\u043b\u0449\u0438\u043d\u0430", None))
    # retranslateUi

