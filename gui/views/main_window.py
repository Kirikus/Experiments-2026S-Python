from ui_mainwindow import Ui_MainWindow

from PySide6.QtWidgets import (
    QGroupBox,
    QHeaderView,
    QLabel,
    QMainWindow,
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

        self._build_variable_and_formula_groups()

        # Растягиваем столбцы таблиц значений и приборов на всю ширину
        self.ui.tableValues.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableInstruments.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Скрываем боковую нумерацию строк, чтобы не дублировать столбец N
        self.ui.tableValues.verticalHeader().setVisible(False)
        self.ui.tableInstruments.verticalHeader().setVisible(False)

        # Инициализируем менеджер графиков
        self.plot_manager = PlotManager(self.ui.plotChartView)

    def _build_variable_and_formula_groups(self) -> None:
        # Группа переменных: основная таблица значений только для переменных.
        variable_group = QGroupBox("Переменные", self.ui.rightPanel)
        variable_layout = QVBoxLayout(variable_group)
        variable_layout.setContentsMargins(8, 8, 8, 8)

        right_layout = self.ui.verticalLayoutRight
        right_layout.removeWidget(self.ui.tableValues)
        variable_layout.addWidget(self.ui.tableValues)
        right_layout.insertWidget(0, variable_group)

        # Группа формул: пока учебная заглушка.
        formulas_group = QGroupBox("Формулы", self.ui.rightPanel)
        formulas_layout = QVBoxLayout(formulas_group)
        formulas_layout.setContentsMargins(8, 8, 8, 8)

        formulas_hint = QLabel("Заглушка: здесь будет редактор и список формул.", formulas_group)
        formulas_hint.setWordWrap(True)
        formulas_layout.addWidget(formulas_hint)

        info_index = right_layout.indexOf(self.ui.infoGroup)
        if info_index >= 0:
            right_layout.insertWidget(info_index, formulas_group)
        else:
            right_layout.addWidget(formulas_group)
