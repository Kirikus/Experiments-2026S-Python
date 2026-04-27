# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plot_base.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QLabel, QLineEdit,
    QSizePolicy, QVBoxLayout, QWidget)

from pyqtgraph import PlotWidget

class Ui_PlotBase(object):
    def setupUi(self, PlotBase):
        if not PlotBase.objectName():
            PlotBase.setObjectName(u"PlotBase")
        PlotBase.resize(600, 500)
        self.verticalLayout = QVBoxLayout(PlotBase)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.plotWidget = PlotWidget(PlotBase)
        self.plotWidget.setObjectName(u"plotWidget")

        self.verticalLayout.addWidget(self.plotWidget)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.labelTitle = QLabel(PlotBase)
        self.labelTitle.setObjectName(u"labelTitle")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelTitle)

        self.titleEdit = QLineEdit(PlotBase)
        self.titleEdit.setObjectName(u"titleEdit")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.titleEdit)

        self.labelX = QLabel(PlotBase)
        self.labelX.setObjectName(u"labelX")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelX)

        self.xLabelEdit = QLineEdit(PlotBase)
        self.xLabelEdit.setObjectName(u"xLabelEdit")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.xLabelEdit)

        self.labelY = QLabel(PlotBase)
        self.labelY.setObjectName(u"labelY")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelY)

        self.yLabelEdit = QLineEdit(PlotBase)
        self.yLabelEdit.setObjectName(u"yLabelEdit")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.yLabelEdit)


        self.verticalLayout.addLayout(self.formLayout)


        self.retranslateUi(PlotBase)

        QMetaObject.connectSlotsByName(PlotBase)
    # setupUi

    def retranslateUi(self, PlotBase):
        PlotBase.setWindowTitle(QCoreApplication.translate("PlotBase", u"Plot Base", None))
        self.labelTitle.setText(QCoreApplication.translate("PlotBase", u"\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a", None))
        self.labelX.setText(QCoreApplication.translate("PlotBase", u"\u041e\u0441\u044c X", None))
        self.labelY.setText(QCoreApplication.translate("PlotBase", u"\u041e\u0441\u044c Y", None))
    # retranslateUi

