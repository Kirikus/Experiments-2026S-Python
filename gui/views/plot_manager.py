"""
PlotManager для управления различными типами графиков (pyqtgraph-style визуализация).

Поддерживаемые типы:
- scatter: точечный график (значение vs индекс)
- line: линейный график через точки
- histogram: гистограмма распределения значений
- approximation: линейная аппроксимация (линия тренда)
"""

from typing import List, Optional
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QScatterSeries
from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QPainter, QColor, QPen


class PlotManager:
    """Менеджер для создания и обновления графиков в QChartView."""

    def __init__(self, chart_view: QChartView) -> None:
        """
        Инициализировать менеджер графиков.

        :param chart_view: Виджет QChartView для отображения графиков.
        """
        self._chart_view = chart_view
        self._chart: Optional[QChart] = None
        self._setup_chart()

    def _setup_chart(self) -> None:
        """Инициализировать пустой график."""
        self._chart = QChart()
        self._chart.setTitle("График (ожидание выбора переменной)")
        self._chart_view.setChart(self._chart)
        self._chart_view.setRenderHint(QPainter.Antialiasing)

    def clear(self) -> None:
        """Очистить все серии с графика."""
        if self._chart:
            self._chart.removeAllSeries()
            self._chart.removeAxis(self._chart.axisX())
            self._chart.removeAxis(self._chart.axisY())

    def plot_scatter(self, values: List[float], title: str = "Scatter Plot") -> None:
        """
        Построить точечный график.

        :param values: Список значений для визуализации.
        :param title: Заголовок графика.
        """
        self.clear()

        if not values:
            self._chart.setTitle("График пуст (нет данных)")
            return

        # Создаём серию точек
        series = QScatterSeries()
        series.setName("Значения")

        # Добавляем точки (индекс, значение)
        for i, value in enumerate(values):
            series.append(QPointF(i, value))

        # Стиль точек
        series.setMarkerSize(8)
        series.setColor(QColor(0, 122, 204))

        self._chart.addSeries(series)
        self._chart.createDefaultAxes()
        self._chart.setTitle(title)

    def plot_line(self, values: List[float], title: str = "Line Chart") -> None:
        """
        Построить линейный график через точки.

        :param values: Список значений для визуализации.
        :param title: Заголовок графика.
        """
        self.clear()

        if not values:
            self._chart.setTitle("График пуст (нет данных)")
            return

        # Создаём линейную серию
        series = QLineSeries()
        series.setName("Значения")

        # Добавляем точки
        for i, value in enumerate(values):
            series.append(QPointF(i, value))

        # Стиль линии
        pen = QPen(QColor(0, 122, 204), 2)
        series.setPen(pen)

        self._chart.addSeries(series)
        self._chart.createDefaultAxes()
        self._chart.setTitle(title)

    def plot_histogram(self, values: List[float], bins: int = 10, title: str = "Histogram") -> None:
        """
        Построить гистограмму распределения.

        :param values: Список значений.
        :param bins: Количество интервалов (бинов).
        :param title: Заголовок графика.
        """
        self.clear()

        if not values:
            self._chart.setTitle("График пуст (нет данных)")
            return

        # Вычисляем границы и интервалы
        min_val = min(values)
        max_val = max(values)
        bin_width = (max_val - min_val) / bins if max_val > min_val else 1

        # Инициализируем счетчики для каждого бина
        hist = [0] * bins

        # Распределяем значения по бинам
        for value in values:
            bin_index = int((value - min_val) / bin_width)
            bin_index = min(bin_index, bins - 1)  # Граничный случай для max_val
            hist[bin_index] += 1

        # Создаём столбцы (как серия линий)
        series = QLineSeries()
        series.setName("Частота")

        for i, count in enumerate(hist):
            bin_center = min_val + (i + 0.5) * bin_width
            series.append(QPointF(bin_center, count))

        pen = QPen(QColor(204, 122, 0), 2)
        series.setPen(pen)

        self._chart.addSeries(series)
        self._chart.createDefaultAxes()
        self._chart.setTitle(title)

    def plot_approximation(self, values: List[float], title: str = "Approximation") -> None:
        """
        Построить линейную аппроксимацию (линия тренда).

        :param values: Список значений.
        :param title: Заголовок графика.
        """
        self.clear()

        if len(values) < 2:
            self._chart.setTitle("Для аппроксимации нужно минимум 2 точки")
            return

        # Вычисляем линейную регрессию
        n = len(values)
        x_indices = list(range(n))
        
        # Формулы для коэффициентов линейной регрессии y = a*x + b
        sum_x = sum(x_indices)
        sum_y = sum(values)
        sum_xy = sum(x * y for x, y in zip(x_indices, values))
        sum_x2 = sum(x * x for x in x_indices)

        denominator = n * sum_x2 - sum_x * sum_x
        if denominator == 0:
            a, b = 0, sum_y / n
        else:
            a = (n * sum_xy - sum_x * sum_y) / denominator
            b = (sum_y - a * sum_x) / n

        # Строим исходные точки
        scatter_series = QScatterSeries()
        scatter_series.setName("Исходные данные")
        for i, value in enumerate(values):
            scatter_series.append(QPointF(i, value))
        scatter_series.setMarkerSize(6)
        scatter_series.setColor(QColor(0, 122, 204))

        # Строим линию аппроксимации
        line_series = QLineSeries()
        line_series.setName(f"Линия тренда (y = {a:.3f}*x + {b:.3f})")
        for i in range(n):
            y_approx = a * i + b
            line_series.append(QPointF(i, y_approx))

        pen = QPen(QColor(204, 0, 0), 2)
        line_series.setPen(pen)

        self._chart.addSeries(scatter_series)
        self._chart.addSeries(line_series)
        self._chart.createDefaultAxes()
        self._chart.setTitle(title)
