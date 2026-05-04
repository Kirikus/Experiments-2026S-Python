from ui_mainwindow import Ui_MainWindow

<<<<<<< HEAD
from PySide6.QtWidgets import QHeaderView, QMainWindow, QWidget

=======
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QTableView,
    QVBoxLayout,
    QWidget,
)
>>>>>>> afdc0f2 (Refactor plot tabs and line plot settings (ui files removed from tracking))
from .plot_manager import PlotManager


class MainWindow(QMainWindow):
    variableListChanged = Signal()

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.constantsTable = self.ui.constantsTable
        self.workspacePages = self.ui.workspacePages

<<<<<<< HEAD
=======
        self._build_workspace_pages()

        # Растягиваем столбцы таблиц значений и приборов на всю ширину
        self.ui.tableValues.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableInstruments.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Скрываем боковую нумерацию строк, чтобы не дублировать столбец N
        self.ui.tableValues.verticalHeader().setVisible(False)
        self.ui.tableInstruments.verticalHeader().setVisible(False)

        # Инициализируем менеджер графиков
        self.plot_manager = PlotManager(self.ui)
        self.variableListChanged.connect(self.plot_manager.refresh_variable_lists)
        self.show_variables_page()

    def _setup_page_nav_styles(self) -> None:
>>>>>>> afdc0f2 (Refactor plot tabs and line plot settings (ui files removed from tracking))
        self._page_buttons = {
            "variables": self.ui.btnPageValues,
            "constants": self.ui.btnPageConstants,
            "instruments": self.ui.btnPageInstruments,
            "graph": self.ui.btnPageGraph,
            "formulas": self.ui.btnPageFormulas,
        }
        self._page_indices = {
            "variables": 0,
            "constants": 1,
            "instruments": 2,
            "graph": 3,
            "formulas": 4,
        }

        self.ui.btnPageValues.clicked.connect(self.show_variables_page)
        self.ui.btnPageConstants.clicked.connect(self.show_constants_page)
        self.ui.btnPageInstruments.clicked.connect(self.show_instruments_page)
        self.ui.btnPageGraph.clicked.connect(self.show_graph_page)
        self.ui.btnPageFormulas.clicked.connect(self.show_formulas_page)

        self.ui.tableValues.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.constantsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableInstruments.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.ui.tableValues.verticalHeader().setVisible(False)
        self.constantsTable.verticalHeader().setVisible(False)
        self.ui.tableInstruments.verticalHeader().setVisible(False)

        self.plot_manager = PlotManager(self.ui)
        self.show_variables_page()

    def _set_active_page(self, page_key: str) -> None:
        self.workspacePages.setCurrentIndex(self._page_indices[page_key])
        for key, button in self._page_buttons.items():
            button.setChecked(key == page_key)

    def show_variables_page(self) -> None:
        self._set_active_page("variables")

    def show_constants_page(self) -> None:
        self._set_active_page("constants")

    def show_instruments_page(self) -> None:
        self._set_active_page("instruments")

    def show_graph_page(self) -> None:
        self._set_active_page("graph")

    def show_formulas_page(self) -> None:
        self._set_active_page("formulas")
