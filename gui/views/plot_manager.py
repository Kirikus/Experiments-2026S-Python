"""Управление набором графиков во вкладках внутри существующего блока графика."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from PySide6.QtCharts import QChart, QChartView, QLineSeries, QScatterSeries
from PySide6.QtCore import QPointF
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


@dataclass
class _PlotTab:
    chart_view: QChartView
    combo_type: QComboBox
    chart: QChart


class PlotManager:
    """Менеджер вкладок графиков с выбором типа построения для каждой вкладки."""

    _PLOT_TYPES = [
        ("Точки", "scatter"),
        ("Линия", "line"),
        ("Гистограмма", "histogram"),
        ("Аппроксимация", "approximation"),
    ]

    def __init__(self, placeholder_chart_view: QChartView) -> None:
        self._plot_group = placeholder_chart_view.parentWidget()
        self._plot_layout = self._plot_group.layout()
        self._current_values: List[float] = []
        self._current_title: str = "График"
        self._tabs: List[_PlotTab] = []

        self._toolbar_widget = QWidget(self._plot_group)
        self._toolbar_layout = QHBoxLayout(self._toolbar_widget)
        self._toolbar_layout.setContentsMargins(0, 0, 0, 0)

        self._btn_add_tab = QPushButton("Создать график", self._toolbar_widget)
        self._btn_add_tab.clicked.connect(self.add_plot_tab)
        self._toolbar_layout.addWidget(self._btn_add_tab)
        self._toolbar_layout.addStretch()

        self._tab_widget = QTabWidget(self._plot_group)
        self._tab_widget.setTabsClosable(True)
        self._tab_widget.tabCloseRequested.connect(self._on_tab_close_requested)

        self._plot_layout.removeWidget(placeholder_chart_view)
        placeholder_chart_view.deleteLater()
        self._plot_layout.addWidget(self._toolbar_widget)
        self._plot_layout.addWidget(self._tab_widget)

        self.add_plot_tab()

    def add_plot_tab(self) -> None:
        tab_content = QWidget(self._tab_widget)
        tab_layout = QVBoxLayout(tab_content)
        tab_layout.setContentsMargins(0, 0, 0, 0)

        combo = QComboBox(tab_content)
        for label, key in self._PLOT_TYPES:
            combo.addItem(label, key)
        tab_layout.addWidget(combo)

        chart_view = QChartView(tab_content)
        chart_view.setRenderHint(QPainter.Antialiasing)
        tab_layout.addWidget(chart_view)

        chart = QChart()
        chart.setTitle("График (ожидание выбора переменной)")
        chart_view.setChart(chart)

        tab_index = self._tab_widget.addTab(tab_content, f"График {self._tab_widget.count() + 1}")
        self._tab_widget.setCurrentIndex(tab_index)

        plot_tab = _PlotTab(chart_view=chart_view, combo_type=combo, chart=chart)
        self._tabs.append(plot_tab)

        combo.currentIndexChanged.connect(lambda _i, t=plot_tab: self._render_tab(t))
        self._render_tab(plot_tab)

    def _on_tab_close_requested(self, tab_index: int) -> None:
        if self._tab_widget.count() <= 1:
            return

        widget = self._tab_widget.widget(tab_index)
        self._tab_widget.removeTab(tab_index)
        if widget is not None:
            widget.deleteLater()

        self._tabs.pop(tab_index)

    def clear(self) -> None:
        self._current_values = []
        self._current_title = "График"
        for plot_tab in self._tabs:
            self._render_tab(plot_tab)

    def plot_scatter(self, values: List[float], title: str = "График") -> None:
        # Сохраняем данные, а каждый таб сам рисует выбранный им тип графика.
        self._current_values = values.copy()
        self._current_title = title
        for plot_tab in self._tabs:
            self._render_tab(plot_tab)

    def _render_tab(self, plot_tab: _PlotTab) -> None:
        plot_type = plot_tab.combo_type.currentData()
        chart = plot_tab.chart
        chart.removeAllSeries()
        self._clear_axes(chart)

        values = self._current_values
        if not values:
            chart.setTitle("График пуст (нет данных)")
            return

        if plot_type == "scatter":
            self._draw_scatter(chart, values)
        elif plot_type == "line":
            self._draw_line(chart, values)
        elif plot_type == "histogram":
            self._draw_histogram(chart, values, bins=10)
        elif plot_type == "approximation":
            if len(values) < 2:
                chart.setTitle("Для аппроксимации нужно минимум 2 точки")
                return
            self._draw_approximation(chart, values)

        chart.createDefaultAxes()
        chart.setTitle(f"{self._current_title} ({plot_tab.combo_type.currentText()})")

    def _clear_axes(self, chart: QChart) -> None:
        for axis in chart.axes():
            chart.removeAxis(axis)

    def _draw_scatter(self, chart: QChart, values: List[float]) -> None:
        series = QScatterSeries()
        series.setName("Значения")
        series.setMarkerSize(8)
        series.setColor(QColor(0, 122, 204))
        for i, value in enumerate(values):
            series.append(QPointF(i, value))
        chart.addSeries(series)

    def _draw_line(self, chart: QChart, values: List[float]) -> None:
        series = QLineSeries()
        series.setName("Значения")
        series.setPen(QPen(QColor(0, 122, 204), 2))
        for i, value in enumerate(values):
            series.append(QPointF(i, value))
        chart.addSeries(series)

    def _draw_histogram(self, chart: QChart, values: List[float], bins: int) -> None:
        min_val = min(values)
        max_val = max(values)
        bin_width = (max_val - min_val) / bins if max_val > min_val else 1.0

        hist = [0] * bins
        for value in values:
            bin_index = int((value - min_val) / bin_width)
            bin_index = min(bin_index, bins - 1)
            hist[bin_index] += 1

        series = QLineSeries()
        series.setName("Частота")
        series.setPen(QPen(QColor(204, 122, 0), 2))
        for i, count in enumerate(hist):
            x = min_val + (i + 0.5) * bin_width
            series.append(QPointF(x, count))
        chart.addSeries(series)

    def _draw_approximation(self, chart: QChart, values: List[float]) -> None:
        n = len(values)
        x_values = list(range(n))

        sum_x = sum(x_values)
        sum_y = sum(values)
        sum_xy = sum(x * y for x, y in zip(x_values, values))
        sum_x2 = sum(x * x for x in x_values)

        denominator = n * sum_x2 - sum_x * sum_x
        if denominator == 0:
            a, b = 0.0, sum_y / n
        else:
            a = (n * sum_xy - sum_x * sum_y) / denominator
            b = (sum_y - a * sum_x) / n

        scatter_series = QScatterSeries()
        scatter_series.setName("Исходные данные")
        scatter_series.setMarkerSize(6)
        scatter_series.setColor(QColor(0, 122, 204))
        for i, value in enumerate(values):
            scatter_series.append(QPointF(i, value))

        line_series = QLineSeries()
        line_series.setName(f"Линия тренда (y = {a:.3f}*x + {b:.3f})")
        line_series.setPen(QPen(QColor(204, 0, 0), 2))
        for i in range(n):
            line_series.append(QPointF(i, a * i + b))

        chart.addSeries(scatter_series)
        chart.addSeries(line_series)
