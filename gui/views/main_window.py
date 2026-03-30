from ui_mainwindow import Ui_MainWindow

from PySide6.QtWidgets import QMainWindow, QWidget, QHeaderView, QTableView
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

        # Растягиваем столбцы таблиц значений и приборов на всю ширину
        self.ui.tableValues.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableInstruments.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Скрываем боковую нумерацию строк, чтобы не дублировать столбец N
        self.ui.tableValues.verticalHeader().setVisible(False)
        self.ui.tableInstruments.verticalHeader().setVisible(False)

        # Инициализируем менеджер графиков
        self.plot_manager = PlotManager(self.ui.plotChartView)
