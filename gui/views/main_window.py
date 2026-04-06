from ui_mainwindow import Ui_MainWindow

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
from .plot_manager import PlotManager


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Подменяем tableValues на QTableView для работы через внешнюю модель.
        old_values_table = self.ui.tableValues
        values_table = QTableView(self.ui.rightPanel)
        values_table.setObjectName("tableValues")
        values_table.setAlternatingRowColors(True)
        self.ui.verticalLayoutRight.replaceWidget(old_values_table, values_table)
        old_values_table.deleteLater()
        self.ui.tableValues = values_table

        self._build_workspace_pages()

        # Растягиваем столбцы таблиц значений и приборов на всю ширину
        self.ui.tableValues.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableInstruments.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Скрываем боковую нумерацию строк, чтобы не дублировать столбец N
        self.ui.tableValues.verticalHeader().setVisible(False)
        self.ui.tableInstruments.verticalHeader().setVisible(False)

        # Инициализируем менеджер графиков
        self.plot_manager = PlotManager(self.ui.plotChartView)
        self.show_variables_page()

    def _setup_page_nav_styles(self) -> None:
        self._page_buttons = {
            "variables": self.btnPageVariables,
            "constants": self.btnPageConstants,
            "instruments": self.btnPageInstruments,
            "graph": self.btnPageGraph,
            "formulas": self.btnPageFormulas,
        }

        for button in self._page_buttons.values():
            button.setCheckable(True)

        nav_stylesheet = """
        QPushButton {
            padding: 6px 10px;
            border: 1px solid #c7ccd2;
            border-radius: 6px;
            background-color: #f5f7fa;
            color: #1f2a36;
            font-weight: 500;
        }
        QPushButton:hover {
            background-color: #e9eef5;
        }
        QPushButton:checked {
            background-color: #0d6efd;
            border-color: #0b5ed7;
            color: #ffffff;
            font-weight: 600;
        }
        """
        for button in self._page_buttons.values():
            button.setStyleSheet(nav_stylesheet)

    def _set_active_page(self, page_key: str) -> None:
        self.workspacePages.setCurrentIndex(self._page_indices[page_key])
        for key, button in self._page_buttons.items():
            button.setChecked(key == page_key)

    def _build_workspace_pages(self) -> None:
        # Навигация по учебным страницам рабочей области.
        right_layout = self.ui.verticalLayoutRight
        right_layout.removeWidget(self.ui.tableValues)
        right_layout.removeWidget(self.ui.plotGroup)
        right_layout.removeWidget(self.ui.instrumentsGroup)

        nav_widget = QWidget(self.ui.rightPanel)
        nav_layout = QHBoxLayout(nav_widget)
        nav_layout.setContentsMargins(0, 0, 0, 0)

        self.btnPageVariables = QPushButton("Переменные", nav_widget)
        self.btnPageConstants = QPushButton("Константы", nav_widget)
        self.btnPageInstruments = QPushButton("Приборы", nav_widget)
        self.btnPageGraph = QPushButton("График", nav_widget)
        self.btnPageFormulas = QPushButton("Формулы", nav_widget)

        nav_layout.addWidget(self.btnPageVariables)
        nav_layout.addWidget(self.btnPageConstants)
        nav_layout.addWidget(self.btnPageInstruments)
        nav_layout.addWidget(self.btnPageGraph)
        nav_layout.addWidget(self.btnPageFormulas)

        self.workspacePages = QStackedWidget(self.ui.rightPanel)

        # Страница переменных.
        variables_page = QWidget(self.workspacePages)
        variables_layout = QVBoxLayout(variables_page)
        variables_layout.setContentsMargins(8, 8, 8, 8)
        variables_layout.addWidget(self.ui.tableValues)
        self.workspacePages.addWidget(variables_page)

        # Страница констант.
        self.constantsTable = QTableView(self.ui.rightPanel)
        self.constantsTable.setObjectName("constantsTable")
        self.constantsTable.setAlternatingRowColors(True)

        constants_page = QWidget(self.workspacePages)
        constants_layout = QVBoxLayout(constants_page)
        constants_layout.setContentsMargins(8, 8, 8, 8)
        constants_layout.addWidget(self.constantsTable)
        self.workspacePages.addWidget(constants_page)

        # Страница приборов.
        instruments_page = QWidget(self.workspacePages)
        instruments_layout = QVBoxLayout(instruments_page)
        instruments_layout.setContentsMargins(8, 8, 8, 8)
        instruments_layout.addWidget(self.ui.instrumentsGroup)
        self.workspacePages.addWidget(instruments_page)

        # Страница графиков.
        graph_page = QWidget(self.workspacePages)
        graph_layout = QVBoxLayout(graph_page)
        graph_layout.setContentsMargins(8, 8, 8, 8)
        graph_layout.addWidget(self.ui.plotGroup)
        self.workspacePages.addWidget(graph_page)

        # Страница формул (заглушка).
        formulas_page = QWidget(self.workspacePages)
        formulas_layout = QVBoxLayout(formulas_page)
        formulas_layout.setContentsMargins(8, 8, 8, 8)

        formulas_hint = QLabel("Заглушка: здесь будет редактор и список формул.", formulas_page)
        formulas_hint.setWordWrap(True)
        formulas_layout.addWidget(formulas_hint)
        self.workspacePages.addWidget(formulas_page)

        self._page_indices = {
            "variables": 0,
            "constants": 1,
            "instruments": 2,
            "graph": 3,
            "formulas": 4,
        }

        self.btnPageVariables.clicked.connect(self.show_variables_page)
        self.btnPageConstants.clicked.connect(self.show_constants_page)
        self.btnPageInstruments.clicked.connect(self.show_instruments_page)
        self.btnPageGraph.clicked.connect(self.show_graph_page)
        self.btnPageFormulas.clicked.connect(self.show_formulas_page)
        self._setup_page_nav_styles()

        info_index = right_layout.indexOf(self.ui.infoGroup)
        if info_index >= 0:
            right_layout.insertWidget(info_index, nav_widget)
            right_layout.insertWidget(info_index + 1, self.workspacePages)
        else:
            right_layout.addWidget(nav_widget)
            right_layout.addWidget(self.workspacePages)

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
