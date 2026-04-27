# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'correlogram_plot.ui'
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

class Ui_CorrelogramPlot(object):
    def setupUi(self, CorrelogramPlot):
        if not CorrelogramPlot.objectName():
            CorrelogramPlot.setObjectName(u"CorrelogramPlot")
        CorrelogramPlot.resize(700, 600)
        self.verticalLayout = QVBoxLayout(CorrelogramPlot)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.parent_ui = QWidget(CorrelogramPlot)
        self.parent_ui.setObjectName(u"parent_ui")
        self.parentLayout = QVBoxLayout(self.parent_ui)
        self.parentLayout.setContentsMargins(0, 0, 0, 0)
        self.parentLayout.setObjectName(u"parentLayout")

        self.verticalLayout.addWidget(self.parent_ui)

        self.settingsLayout = QFormLayout()
        self.settingsLayout.setObjectName(u"settingsLayout")
        self.labelYVar = QLabel(CorrelogramPlot)
        self.labelYVar.setObjectName(u"labelYVar")

        self.settingsLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelYVar)

        self.yVariableCombo = QComboBox(CorrelogramPlot)
        self.yVariableCombo.setObjectName(u"yVariableCombo")

        self.settingsLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.yVariableCombo)

        self.labelMaxLag = QLabel(CorrelogramPlot)
        self.labelMaxLag.setObjectName(u"labelMaxLag")

        self.settingsLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelMaxLag)

        self.maxLagSpin = QSpinBox(CorrelogramPlot)
        self.maxLagSpin.setObjectName(u"maxLagSpin")
        self.maxLagSpin.setMinimum(1)
        self.maxLagSpin.setMaximum(500)
        self.maxLagSpin.setValue(20)

        self.settingsLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.maxLagSpin)


        self.verticalLayout.addLayout(self.settingsLayout)


        self.retranslateUi(CorrelogramPlot)

        QMetaObject.connectSlotsByName(CorrelogramPlot)
    # setupUi

    def retranslateUi(self, CorrelogramPlot):
        CorrelogramPlot.setWindowTitle(QCoreApplication.translate("CorrelogramPlot", u"Correlogram Plot", None))
        self.labelYVar.setText(QCoreApplication.translate("CorrelogramPlot", u"\u041f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u0430\u044f", None))
        self.labelMaxLag.setText(QCoreApplication.translate("CorrelogramPlot", u"\u041c\u0430\u043a\u0441\u0438\u043c\u0430\u043b\u044c\u043d\u044b\u0439 \u043b\u0430\u0433", None))
    # retranslateUi

