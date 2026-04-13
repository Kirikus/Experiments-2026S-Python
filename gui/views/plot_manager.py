"""Управление набором графических вкладок внутри блока графика."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import pyqtgraph as pg
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QComboBox,
    QLabel,
    QStackedWidget,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from gui.views.plots import ApproximationPlot, CorrelogramPlot, HistogramPlot, LinePlot, ScatterPlot


class PlotTab(ABC):
    """Абстрактная вкладка с общим UI и методом отрисовки графика."""

    graph_label: str = "График"

    def __init__(self, tab_title: str) -> None:
        self.tab_title = tab_title

        self.widget = QWidget()
        self._layout = QVBoxLayout(self.widget)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self.combo_type = QComboBox(self.widget)
        self.combo_type.addItems(["График", "Сообщение"])
        self.combo_type.currentIndexChanged.connect(self._sync_stack)

        self.stacked_widget = QStackedWidget(self.widget)

        self._plot_page = QWidget(self.stacked_widget)
        self._plot_layout = QVBoxLayout(self._plot_page)
        self._plot_layout.setContentsMargins(0, 0, 0, 0)
        self.plot_widget = pg.PlotWidget(self._plot_page)
        self.plot_widget.setBackground("w")
        self.plot_widget.showGrid(x=True, y=True, alpha=0.2)
        self._plot_layout.addWidget(self.plot_widget)

        self._message_page = QWidget(self.stacked_widget)
        self._message_layout = QVBoxLayout(self._message_page)
        self._message_layout.setContentsMargins(0, 0, 0, 0)
        self._message_label = QLabel("", self._message_page)
        self._message_label.setWordWrap(True)
        self._message_layout.addWidget(self._message_label)

        self.stacked_widget.addWidget(self._plot_page)
        self.stacked_widget.addWidget(self._message_page)

        self._layout.addWidget(self.combo_type)
        self._layout.addWidget(self.stacked_widget)

        self._source_variable: Any | None = None
        self._sync_stack()

    def set_source_variable(self, variable: Any | None) -> None:
        self._source_variable = variable

    def _sync_stack(self, *_args: object) -> None:
        self.stacked_widget.setCurrentIndex(0 if self.combo_type.currentIndex() == 0 else 1)

    @abstractmethod
    def plot(self) -> None:
        """Отрисовать содержимое вкладки для текущего источника данных."""


class _SinglePlotTab(PlotTab):
    """Базовая реализация вкладки для конкретного типа графика."""

    plot_class: Any

    def __init__(self, tab_title: str) -> None:
        super().__init__(tab_title)
        self._plot_impl = self.plot_class()

    def plot(self) -> None:
        if self._source_variable is None:
            self._message_label.setText("Выберите переменную и нажмите «Получить график»")
            self.combo_type.setCurrentIndex(1)
            return

        values = list(self._source_variable.values)
        if not values:
            self._message_label.setText(f"{self.tab_title}: нет данных")
            self.combo_type.setCurrentIndex(1)
            return

        self.plot_widget.clear()
        self.plot_widget.setTitle("")
        self.plot_widget.getPlotItem().legend = None
        try:
            self._plot_impl.plot(self.plot_widget, values)
        except ValueError as exc:
            self._message_label.setText(str(exc))
            self.combo_type.setCurrentIndex(1)
            return

        self.combo_type.setCurrentIndex(0)
        self.plot_widget.setTitle(f"{self.tab_title} ({self.graph_label})")
        self.plot_widget.setLabel("bottom", self._plot_impl.x_label)
        self.plot_widget.setLabel("left", self._plot_impl.y_label)


class ScatterPlotTab(_SinglePlotTab):
    graph_label = "Точки"
    plot_class = ScatterPlot


class LinePlotTab(_SinglePlotTab):
    graph_label = "Линия"
    plot_class = LinePlot


class HistogramPlotTab(_SinglePlotTab):
    graph_label = "Гистограмма"
    plot_class = HistogramPlot


class ApproximationPlotTab(_SinglePlotTab):
    graph_label = "Аппроксимация"
    plot_class = ApproximationPlot


class CorrelogramPlotTab(_SinglePlotTab):
    graph_label = "Коррелограмма"
    plot_class = CorrelogramPlot


class PlotManager:
    """Менеджер вкладок графиков."""

    _TAB_CLASSES = [
        ScatterPlotTab,
        LinePlotTab,
        HistogramPlotTab,
        ApproximationPlotTab,
        CorrelogramPlotTab,
    ]

    def __init__(self, ui) -> None:
        self.ui = ui
        self._source_variable: Any | None = None
        self._tabs: list[PlotTab] = []
        self._refresh_timer = QTimer(self.ui.plotGroup)
        self._refresh_timer.setSingleShot(True)
        self._refresh_timer.setInterval(120)
        self._refresh_timer.timeout.connect(self._refresh_graph_now)

        self.ui.btnGetGraph.clicked.connect(self.refresh_graph)
        self.ui._btn_add_tab.clicked.connect(self.add_plot_tab)

        self._tab_widget: QTabWidget = self.ui.plotTabs
        self._tab_widget.setTabsClosable(True)
        self._tab_widget.tabCloseRequested.connect(self._on_tab_close_requested)
        self.add_plot_tab()

    def set_source_variable(self, variable: Any | None) -> None:
        self._source_variable = variable
        for plot_tab in self._tabs:
            plot_tab.set_source_variable(variable)

    def refresh_graph(self) -> None:
        self._refresh_timer.start()

    def _refresh_graph_now(self) -> None:
        for plot_tab in self._tabs:
            plot_tab.plot()

    def add_plot_tab(self) -> None:
        tab_index = self._tab_widget.count()
        tab_cls = self._TAB_CLASSES[tab_index % len(self._TAB_CLASSES)]
        plot_tab = tab_cls(f"График {tab_index + 1}")
        plot_tab.set_source_variable(self._source_variable)
        self._tabs.append(plot_tab)

        self._tab_widget.addTab(plot_tab.widget, f"{plot_tab.graph_label} {tab_index + 1}")
        self._tab_widget.setCurrentIndex(tab_index)
        plot_tab.plot()

    def _on_tab_close_requested(self, tab_index: int) -> None:
        if self._tab_widget.count() <= 1:
            return

        widget = self._tab_widget.widget(tab_index)
        self._tab_widget.removeTab(tab_index)
        if widget is not None:
            widget.deleteLater()

        self._tabs.pop(tab_index)

    def clear(self) -> None:
        self.refresh_graph()
