"""Набор классов графиков с единым интерфейсом Plot."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

import numpy as np
import pyqtgraph as pg
from PySide6.QtCore import QRectF


class Plot(ABC):
    """Интерфейс для конкретного типа графика."""

    key: str
    label: str
    x_label: str = "Индекс"
    y_label: str = "Значение"
    min_points: int = 1
    min_points_message: str = "Недостаточно данных для построения"

    def validate(self, values: Sequence[float]) -> None:
        if len(values) < self.min_points:
            raise ValueError(self.min_points_message)

    @abstractmethod
    def plot(self, plot_widget: pg.PlotWidget, values: Sequence[float]) -> None:
        """Отрисовать график в переданном PlotWidget."""


class ScatterPlot(Plot):
    key = "scatter"
    label = "Точки"

    def plot(self, plot_widget: pg.PlotWidget, values: Sequence[float]) -> None:
        self.validate(values)
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


class LinePlot(Plot):
    key = "line"
    label = "Линия"

    def plot(self, plot_widget: pg.PlotWidget, values: Sequence[float]) -> None:
        self.validate(values)
        x_values = list(range(len(values)))
        plot_widget.plot(
            x_values,
            values,
            pen=pg.mkPen(color=(0, 122, 204), width=2),
            name="Значения",
        )


class HistogramPlot(Plot):
    key = "histogram"
    label = "Гистограмма"

    def __init__(self, bins: int = 10) -> None:
        self._bins = max(1, bins)

    def plot(self, plot_widget: pg.PlotWidget, values: Sequence[float]) -> None:
        self.validate(values)
        bins = self._bins
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


class ApproximationPlot(Plot):
    key = "approximation"
    label = "Аппроксимация"
    min_points = 2
    min_points_message = "Для аппроксимации нужно минимум 2 точки"

    def plot(self, plot_widget: pg.PlotWidget, values: Sequence[float]) -> None:
        self.validate(values)
        n = len(values)
        if n == 0:
            raise ValueError(self.min_points_message)
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


class CorrelogramPlot(Plot):
    key = "correlogram"
    label = "Коррелограмма"
    x_label = "Лаг j"
    y_label = "Лаг i"
    min_points = 2
    min_points_message = "Для коррелограммы нужно минимум 2 точки"

    def __init__(self, max_lag: int = 20) -> None:
        self._max_lag = max_lag

    def plot(self, plot_widget: pg.PlotWidget, values: Sequence[float]) -> None:
        """Рисует тепловую карту автокорреляции по лагам."""
        self.validate(values)
        series = np.asarray(values, dtype=float)
        n = int(series.size)
        lag_limit = min(self._max_lag, n - 1)
        if lag_limit < 1:
            raise ValueError("Для коррелограммы нужно минимум 2 точки")

        centered = series - float(np.mean(series))
        variance = float(np.dot(centered, centered))
        if variance == 0.0:
            autocorr = np.ones(lag_limit + 1, dtype=float)
        else:
            autocorr = np.empty(lag_limit + 1, dtype=float)
            autocorr[0] = 1.0
            for lag in range(1, lag_limit + 1):
                numerator = float(np.dot(centered[:-lag], centered[lag:]))
                autocorr[lag] = numerator / variance

        corr_matrix = np.empty((lag_limit + 1, lag_limit + 1), dtype=float)
        for i in range(lag_limit + 1):
            for j in range(lag_limit + 1):
                corr_matrix[i, j] = autocorr[abs(i - j)]

        image = pg.ImageItem(corr_matrix)
        image.setRect(QRectF(0, 0, lag_limit + 1, lag_limit + 1))
        image.setColorMap(pg.colormap.get("CET-D1"))

        plot_item = plot_widget.getPlotItem()
        plot_item.addItem(image)
        plot_item.getViewBox().setLimits(xMin=0, xMax=lag_limit + 1, yMin=0, yMax=lag_limit + 1)


def get_default_plots() -> dict[str, Plot]:
    """Возвращает реестр доступных графиков по ключу."""
    plot_objects: list[Plot] = [
        ScatterPlot(),
        LinePlot(),
        HistogramPlot(),
        ApproximationPlot(),
        CorrelogramPlot(),
    ]
    return {plot.key: plot for plot in plot_objects}
