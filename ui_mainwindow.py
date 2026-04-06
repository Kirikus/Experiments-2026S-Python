# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCharts import QChartView
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFormLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QMainWindow, QMenu,
    QMenuBar, QSizePolicy, QStatusBar, QTableView,
    QTableWidget, QTableWidgetItem, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName(u"actionNew")
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionAddVariable = QAction(MainWindow)
        self.actionAddVariable.setObjectName(u"actionAddVariable")
        self.actionAddConstant = QAction(MainWindow)
        self.actionAddConstant.setObjectName(u"actionAddConstant")
        self.actionAddInstrument = QAction(MainWindow)
        self.actionAddInstrument.setObjectName(u"actionAddInstrument")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.treeExperiment = QTreeWidget(self.centralwidget)
        self.treeExperiment.setObjectName(u"treeExperiment")
        self.treeExperiment.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout.addWidget(self.treeExperiment)

        self.rightPanel = QWidget(self.centralwidget)
        self.rightPanel.setObjectName(u"rightPanel")
        self.verticalLayoutRight = QVBoxLayout(self.rightPanel)
        self.verticalLayoutRight.setObjectName(u"verticalLayoutRight")
        self.tableValues = QTableWidget(self.rightPanel)
        if (self.tableValues.columnCount() < 3):
            self.tableValues.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableValues.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableValues.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableValues.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tableValues.setObjectName(u"tableValues")
        self.tableValues.setAlternatingRowColors(True)

        self.verticalLayoutRight.addWidget(self.tableValues)

        self.plotGroup = QGroupBox(self.rightPanel)
        self.plotGroup.setObjectName(u"plotGroup")
        self.verticalLayoutPlot = QVBoxLayout(self.plotGroup)
        self.verticalLayoutPlot.setObjectName(u"verticalLayoutPlot")
        self.plotChartView = QChartView(self.plotGroup)
        self.plotChartView.setObjectName(u"plotChartView")
        self.plotChartView.setMinimumSize(QSize(200, 150))

        self.verticalLayoutPlot.addWidget(self.plotChartView)


        self.verticalLayoutRight.addWidget(self.plotGroup)

        self.instrumentsGroup = QGroupBox(self.rightPanel)
        self.instrumentsGroup.setObjectName(u"instrumentsGroup")
        self.verticalLayoutInstruments = QVBoxLayout(self.instrumentsGroup)
        self.verticalLayoutInstruments.setObjectName(u"verticalLayoutInstruments")
        self.tableInstruments = QTableView(self.instrumentsGroup)
        self.tableInstruments.setObjectName(u"tableInstruments")
        self.tableInstruments.setAlternatingRowColors(True)

        self.verticalLayoutInstruments.addWidget(self.tableInstruments)


        self.verticalLayoutRight.addWidget(self.instrumentsGroup)

        self.infoGroup = QGroupBox(self.rightPanel)
        self.infoGroup.setObjectName(u"infoGroup")
        self.formLayout = QFormLayout(self.infoGroup)
        self.formLayout.setObjectName(u"formLayout")
        self.labelName = QLabel(self.infoGroup)
        self.labelName.setObjectName(u"labelName")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelName)

        self.valueName = QLabel(self.infoGroup)
        self.valueName.setObjectName(u"valueName")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.valueName)

        self.labelType = QLabel(self.infoGroup)
        self.labelType.setObjectName(u"labelType")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelType)

        self.valueType = QLabel(self.infoGroup)
        self.valueType.setObjectName(u"valueType")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.valueType)

        self.labelCount = QLabel(self.infoGroup)
        self.labelCount.setObjectName(u"labelCount")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelCount)

        self.valueCount = QLabel(self.infoGroup)
        self.valueCount.setObjectName(u"valueCount")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.valueCount)


        self.verticalLayoutRight.addWidget(self.infoGroup)


        self.horizontalLayout.addWidget(self.rightPanel)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuExperiment = QMenu(self.menubar)
        self.menuExperiment.setObjectName(u"menuExperiment")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuExperiment.menuAction())
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuExperiment.addAction(self.actionAddVariable)
        self.menuExperiment.addAction(self.actionAddConstant)
        self.menuExperiment.addAction(self.actionAddInstrument)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430 \u044d\u043a\u0441\u043f\u0435\u0440\u0438\u043c\u0435\u043d\u0442\u0430\u043b\u044c\u043d\u044b\u0445 \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c...", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0445\u043e\u0434", None))
        self.actionAddVariable.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u0443\u044e", None))
        self.actionAddConstant.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043a\u043e\u043d\u0441\u0442\u0430\u043d\u0442\u0443", None))
        self.actionAddInstrument.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043f\u0440\u0438\u0431\u043e\u0440", None))
        ___qtreewidgetitem = self.treeExperiment.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"\u042d\u043a\u0441\u043f\u0435\u0440\u0438\u043c\u0435\u043d\u0442", None));
        ___qtablewidgetitem = self.tableValues.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"N", None));
        ___qtablewidgetitem1 = self.tableValues.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435", None));
        ___qtablewidgetitem2 = self.tableValues.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0433\u0440\u0435\u0448\u043d\u043e\u0441\u0442\u044c", None));
        self.plotGroup.setTitle(QCoreApplication.translate("MainWindow", u"\u0413\u0440\u0430\u0444\u0438\u043a", None))
        self.instrumentsGroup.setTitle(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u0438\u0431\u043e\u0440\u044b", None))
        self.infoGroup.setTitle(QCoreApplication.translate("MainWindow", u"\u0418\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f", None))
        self.labelName.setText(QCoreApplication.translate("MainWindow", u"\u0418\u043c\u044f:", None))
        self.valueName.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.labelType.setText(QCoreApplication.translate("MainWindow", u"\u0422\u0438\u043f:", None))
        self.valueType.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.labelCount.setText(QCoreApplication.translate("MainWindow", u"\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e:", None))
        self.valueCount.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"\u0424\u0430\u0439\u043b", None))
        self.menuExperiment.setTitle(QCoreApplication.translate("MainWindow", u"\u042d\u043a\u0441\u043f\u0435\u0440\u0438\u043c\u0435\u043d\u0442", None))
    # retranslateUi

