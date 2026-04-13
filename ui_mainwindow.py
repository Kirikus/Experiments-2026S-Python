# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QStatusBar, QTabWidget, QTableView,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(820, 900)
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
        self.rightPanel.setStyleSheet(u"QPushButton {\n"
"    padding: 6px 10px;\n"
"    border: 1px solid #c7ccd2;\n"
"    border-radius: 6px;\n"
"    background-color: #f5f7fa;\n"
"    color: #1f2a36;\n"
"    font-weight: 500;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #e9eef5;\n"
"}\n"
"QPushButton:checked {\n"
"    background-color: #0d6efd;\n"
"    border-color: #0b5ed7;\n"
"    color: #ffffff;\n"
"    font-weight: 600;\n"
"}")
        self.verticalLayoutRight = QVBoxLayout(self.rightPanel)
        self.verticalLayoutRight.setObjectName(u"verticalLayoutRight")
        self.nav_layout = QHBoxLayout()
        self.nav_layout.setObjectName(u"nav_layout")
        self.btnPageValues = QPushButton(self.rightPanel)
        self.btnPageValues.setObjectName(u"btnPageValues")
        self.btnPageValues.setCheckable(True)

        self.nav_layout.addWidget(self.btnPageValues)

        self.btnPageConstants = QPushButton(self.rightPanel)
        self.btnPageConstants.setObjectName(u"btnPageConstants")
        self.btnPageConstants.setCheckable(True)

        self.nav_layout.addWidget(self.btnPageConstants)

        self.btnPageInstruments = QPushButton(self.rightPanel)
        self.btnPageInstruments.setObjectName(u"btnPageInstruments")
        self.btnPageInstruments.setCheckable(True)

        self.nav_layout.addWidget(self.btnPageInstruments)

        self.btnPageGraph = QPushButton(self.rightPanel)
        self.btnPageGraph.setObjectName(u"btnPageGraph")
        self.btnPageGraph.setCheckable(True)

        self.nav_layout.addWidget(self.btnPageGraph)

        self.btnPageFormulas = QPushButton(self.rightPanel)
        self.btnPageFormulas.setObjectName(u"btnPageFormulas")
        self.btnPageFormulas.setCheckable(True)

        self.nav_layout.addWidget(self.btnPageFormulas)


        self.verticalLayoutRight.addLayout(self.nav_layout)

        self.workspacePages = QStackedWidget(self.rightPanel)
        self.workspacePages.setObjectName(u"workspacePages")
        self.variables_page = QWidget()
        self.variables_page.setObjectName(u"variables_page")
        self.variablesLayout = QVBoxLayout(self.variables_page)
        self.variablesLayout.setObjectName(u"variablesLayout")
        self.variablesLayout.setContentsMargins(8, 8, 8, 8)
        self.tableValues = QTableView(self.variables_page)
        self.tableValues.setObjectName(u"tableValues")
        self.tableValues.setAlternatingRowColors(True)

        self.variablesLayout.addWidget(self.tableValues)

        self.workspacePages.addWidget(self.variables_page)
        self.constants_page = QWidget()
        self.constants_page.setObjectName(u"constants_page")
        self.constantsLayout = QVBoxLayout(self.constants_page)
        self.constantsLayout.setObjectName(u"constantsLayout")
        self.constantsLayout.setContentsMargins(8, 8, 8, 8)
        self.constantsTable = QTableView(self.constants_page)
        self.constantsTable.setObjectName(u"constantsTable")
        self.constantsTable.setAlternatingRowColors(True)

        self.constantsLayout.addWidget(self.constantsTable)

        self.workspacePages.addWidget(self.constants_page)
        self.instruments_page = QWidget()
        self.instruments_page.setObjectName(u"instruments_page")
        self.instrumentsLayout = QVBoxLayout(self.instruments_page)
        self.instrumentsLayout.setObjectName(u"instrumentsLayout")
        self.instrumentsLayout.setContentsMargins(8, 8, 8, 8)
        self.instrumentsGroup = QGroupBox(self.instruments_page)
        self.instrumentsGroup.setObjectName(u"instrumentsGroup")
        self.verticalLayoutInstruments = QVBoxLayout(self.instrumentsGroup)
        self.verticalLayoutInstruments.setObjectName(u"verticalLayoutInstruments")
        self.tableInstruments = QTableView(self.instrumentsGroup)
        self.tableInstruments.setObjectName(u"tableInstruments")
        self.tableInstruments.setAlternatingRowColors(True)

        self.verticalLayoutInstruments.addWidget(self.tableInstruments)


        self.instrumentsLayout.addWidget(self.instrumentsGroup)

        self.workspacePages.addWidget(self.instruments_page)
        self.graph_page = QWidget()
        self.graph_page.setObjectName(u"graph_page")
        self.graphLayout = QVBoxLayout(self.graph_page)
        self.graphLayout.setObjectName(u"graphLayout")
        self.graphLayout.setContentsMargins(8, 8, 8, 8)
        self.plotGroup = QGroupBox(self.graph_page)
        self.plotGroup.setObjectName(u"plotGroup")
        self.verticalLayoutPlot = QVBoxLayout(self.plotGroup)
        self.verticalLayoutPlot.setObjectName(u"verticalLayoutPlot")
        self.plotToolbarLayout = QHBoxLayout()
        self.plotToolbarLayout.setObjectName(u"plotToolbarLayout")
        self.btnGetGraph = QPushButton(self.plotGroup)
        self.btnGetGraph.setObjectName(u"btnGetGraph")

        self.plotToolbarLayout.addWidget(self.btnGetGraph)

        self._btn_add_tab = QPushButton(self.plotGroup)
        self._btn_add_tab.setObjectName(u"_btn_add_tab")

        self.plotToolbarLayout.addWidget(self._btn_add_tab)

        self.plotToolbarSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.plotToolbarLayout.addItem(self.plotToolbarSpacer)


        self.verticalLayoutPlot.addLayout(self.plotToolbarLayout)

        self.plotTabs = QTabWidget(self.plotGroup)
        self.plotTabs.setObjectName(u"plotTabs")
        self.plotTabs.setMinimumSize(QSize(200, 150))

        self.verticalLayoutPlot.addWidget(self.plotTabs)


        self.graphLayout.addWidget(self.plotGroup)

        self.workspacePages.addWidget(self.graph_page)
        self.formulas_page = QWidget()
        self.formulas_page.setObjectName(u"formulas_page")
        self.formulasLayout = QVBoxLayout(self.formulas_page)
        self.formulasLayout.setObjectName(u"formulasLayout")
        self.formulasLayout.setContentsMargins(8, 8, 8, 8)
        self.formulas_hint = QLabel(self.formulas_page)
        self.formulas_hint.setObjectName(u"formulas_hint")
        self.formulas_hint.setWordWrap(True)

        self.formulasLayout.addWidget(self.formulas_hint)

        self.workspacePages.addWidget(self.formulas_page)

        self.verticalLayoutRight.addWidget(self.workspacePages)

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
        self.menubar.setGeometry(QRect(0, 0, 820, 25))
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
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"\u042d\u043a\u0441\u043f\u0435\u0440\u0438\u043c\u0435\u043d\u0442", None))
        self.btnPageValues.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0435", None))
        self.btnPageConstants.setText(QCoreApplication.translate("MainWindow", u"\u041a\u043e\u043d\u0441\u0442\u0430\u043d\u0442\u044b", None))
        self.btnPageInstruments.setText(QCoreApplication.translate("MainWindow", u"\u0418\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442\u044b", None))
        self.btnPageGraph.setText(QCoreApplication.translate("MainWindow", u"\u0413\u0440\u0430\u0444\u0438\u043a\u0438", None))
        self.btnPageFormulas.setText(QCoreApplication.translate("MainWindow", u"\u0424\u043e\u0440\u043c\u0443\u043b\u044b", None))
        self.instrumentsGroup.setTitle(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u0438\u0431\u043e\u0440\u044b", None))
        self.plotGroup.setTitle(QCoreApplication.translate("MainWindow", u"\u0413\u0440\u0430\u0444\u0438\u043a", None))
        self.btnGetGraph.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043b\u0443\u0447\u0438\u0442\u044c \u0433\u0440\u0430\u0444\u0438\u043a", None))
        self._btn_add_tab.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0432\u043a\u043b\u0430\u0434\u043a\u0443", None))
        self.formulas_hint.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u043b\u0443\u0448\u043a\u0430: \u0437\u0434\u0435\u0441\u044c \u0431\u0443\u0434\u0435\u0442 \u0440\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u0438 \u0441\u043f\u0438\u0441\u043e\u043a \u0444\u043e\u0440\u043c\u0443\u043b.", None))
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

