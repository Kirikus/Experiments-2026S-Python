# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'histogram_plot.ui'
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

class Ui_HistogramPlot(object):
    def setupUi(self, HistogramPlot):
        if not HistogramPlot.objectName():
            HistogramPlot.setObjectName(u"HistogramPlot")
        HistogramPlot.resize(700, 600)
        self.verticalLayout = QVBoxLayout(HistogramPlot)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.parent_ui = QWidget(HistogramPlot)
        self.parent_ui.setObjectName(u"parent_ui")
        self.parentLayout = QVBoxLayout(self.parent_ui)
        self.parentLayout.setContentsMargins(0, 0, 0, 0)
        self.parentLayout.setObjectName(u"parentLayout")

        self.verticalLayout.addWidget(self.parent_ui)

        self.settingsLayout = QFormLayout()
        self.settingsLayout.setObjectName(u"settingsLayout")
        self.labelYVar = QLabel(HistogramPlot)
        self.labelYVar.setObjectName(u"labelYVar")

        self.settingsLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelYVar)

        self.yVariableCombo = QComboBox(HistogramPlot)
        self.yVariableCombo.setObjectName(u"yVariableCombo")

        self.settingsLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.yVariableCombo)

        self.labelBins = QLabel(HistogramPlot)
        self.labelBins.setObjectName(u"labelBins")

        self.settingsLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelBins)

        self.binsSpin = QSpinBox(HistogramPlot)
        self.binsSpin.setObjectName(u"binsSpin")
        self.binsSpin.setMinimum(1)
        self.binsSpin.setMaximum(100)
        self.binsSpin.setValue(10)

        self.settingsLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.binsSpin)


        self.verticalLayout.addLayout(self.settingsLayout)


        self.retranslateUi(HistogramPlot)

        QMetaObject.connectSlotsByName(HistogramPlot)
    # setupUi

    def retranslateUi(self, HistogramPlot):
        HistogramPlot.setWindowTitle(QCoreApplication.translate("HistogramPlot", u"Histogram Plot", None))
        self.labelYVar.setText(QCoreApplication.translate("HistogramPlot", u"\u041f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u0430\u044f", None))
        self.labelBins.setText(QCoreApplication.translate("HistogramPlot", u"\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0441\u0442\u043e\u043b\u0431\u0446\u043e\u0432", None))
    # retranslateUi

