"""Управление набором plot-графиков во вкладках внутри существующего блока графика."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

import pyqtgraph as pg
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
    plot_widget: pg.PlotWidget
    combo_type: QComboBox
    tab_title: str


class PlotManager:
    """Менеджер вкладок графиков с выбором типа построения для каждой вкладки."""

    _PLOT_TYPES = [
        ("Точки", "scatter"),
        ("Линия", "line"),
        ("Гистограмма", "histogram"),
        ("Аппроксимация", "approximation"),
    ]

    def __init__(self, placeholder_widget: QWidget) -> None:
        self._plot_group = placeholder_widget.parentWidget()
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

        self._plot_layout.removeWidget(placeholder_widget)
        placeholder_widget.deleteLater()
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

        plot_widget = pg.PlotWidget(tab_content)
        plot_widget.setBackground("w")
        plot_widget.showGrid(x=True, y=True, alpha=0.2)
        tab_layout.addWidget(plot_widget)

        tab_index = self._tab_widget.addTab(tab_content, f"График {self._tab_widget.count() + 1}")
        self._tab_widget.setCurrentIndex(tab_index)

        plot_tab = _PlotTab(
            plot_widget=plot_widget,
            combo_type=combo,
            tab_title=f"График {tab_index + 1}",
        )
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
        pw = plot_tab.plot_widget
        pw.clear()
        pw.setTitle("")
        pw.getPlotItem().legend = None

        values = self._current_values
        if not values:
            pw.setTitle("График пуст (нет данных)")
            return

        if plot_type == "scatter":
            self._draw_scatter(pw, values)
        elif plot_type == "line":
            self._draw_line(pw, values)
        elif plot_type == "histogram":
            self._draw_histogram(pw, values, bins=10)
        elif plot_type == "approximation":
            if len(values) < 2:
                pw.setTitle("Для аппроксимации нужно минимум 2 точки")
                return
            self._draw_approximation(pw, values)

        pw.setTitle(f"{self._current_title} ({plot_tab.combo_type.currentText()})")
        pw.setLabel("bottom", "Индекс")
        pw.setLabel("left", "Значение")

    def _draw_scatter(self, plot_widget: pg.PlotWidget, values: List[float]) -> None:
        x_values = list(range(len(values)))
        plot_widget.plot(
            x_values,
            values,
            pen=None,
            symbol="o",
            symbolSize=8,
            symbolBrush=(0, 122, 204),
            symbolPen=(0, 122, 204),
            name="Значения",
        )

    def _draw_line(self, plot_widget: pg.PlotWidget, values: List[float]) -> None:
        x_values = list(range(len(values)))
        plot_widget.plot(
            x_values,
            values,
            pen=pg.mkPen(color=(0, 122, 204), width=2),
            name="Значения",
        )

    def _draw_histogram(self, plot_widget: pg.PlotWidget, values: List[float], bins: int) -> None:
        min_val = min(values)
        max_val = max(values)
        bin_width = (max_val - min_val) / bins if max_val > min_val else 1.0

        hist = [0] * bins
        for value in values:
            bin_index = int((value - min_val) / bin_width)
            bin_index = min(bin_index, bins - 1)
            hist[bin_index] += 1

        x_points = []
        y_points = []
        for i, count in enumerate(hist):
            x = min_val + (i + 0.5) * bin_width
            x_points.append(x)
            y_points.append(count)

        bars = pg.BarGraphItem(x=x_points, height=y_points, width=bin_width * 0.9, brush=(204, 122, 0))
        plot_widget.addItem(bars)

    def _draw_approximation(self, plot_widget: pg.PlotWidget, values: List[float]) -> None:
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

        y_approx = [a * i + b for i in x_values]

        plot_widget.plot(
            x_values,
            values,
            pen=None,
            symbol="o",
            symbolSize=6,
            symbolBrush=(0, 122, 204),
            symbolPen=(0, 122, 204),
            name="Исходные данные",
        )
        plot_widget.plot(
            x_values,
            y_approx,
            pen=pg.mkPen(color=(204, 0, 0), width=2),
            name=f"Линия тренда (y = {a:.3f}*x + {b:.3f})",
        )
