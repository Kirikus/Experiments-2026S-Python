from PySide6.QtWidgets import QMainWindow, QWidget

from ui_mainwindow import Ui_MainWindow
from PySide6.QtCharts import QChart, QChartView, QLineSeries
from PySide6.QtGui import QPainter


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_plot()

    def init_plot(self):
        # Пример: создаём простой график (линейный график с тестовыми данными)
        series = QLineSeries()
        series.append(0, 0)
        series.append(1, 1)
        series.append(2, 0.5)
        series.append(3, 1.5)
        series.append(4, 1)

        chart = QChart()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setTitle("Пробный график (QtCharts)")

        self.ui.plotChartView.setChart(chart)
        self.ui.plotChartView.setRenderHint(QPainter.Antialiasing)
        # Для дальнейшей работы: замените данные на реальные экспериментальные значения
