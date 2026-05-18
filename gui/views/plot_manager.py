"""Управление набором графических вкладок внутри блока графика."""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QInputDialog, QTabWidget, QVBoxLayout, QWidget

from gui.views.plots import Plot, LinePlot, HistogramPlot


class PlotTab:
    """Вкладка, которая содержит готовый plot-widget и страницу сообщения."""

    def __init__(self, plot_widget: Plot, title: str) -> None:
        self.plot_impl = plot_widget
        self.tab_title = title

        self.widget = QWidget()
        layout = QVBoxLayout(self.widget)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.plot_impl)

    def plot(self) -> None:
        y_combo = getattr(self.plot_impl.ui, "yVariableCombo", None)
        settings_table = getattr(self.plot_impl.ui, "settingsTable", None)

        if y_combo is not None and y_combo.currentText().strip() == "":
            return

        if settings_table is not None and settings_table.columnCount() == 0:
            return

        try:
            self.plot_impl.plot()
        except ValueError as exc:
            print(f"Plot error: {exc}")


class PlotManager:
    """Менеджер вкладок графиков."""

    _PLOT_CLASSES = [
        ("Линия", LinePlot),
        ('Гистограмма', HistogramPlot),
    ]

    def __init__(self, ui) -> None:
        self.ui = ui
        self._tabs: list[PlotTab] = []
        self._plot_class_by_label = {label: cls for label, cls in self._PLOT_CLASSES}
        self._plot_label_by_class = {cls: label for label, cls in self._PLOT_CLASSES}
        self._refresh_timer = QTimer(self.ui.plotGroup)
        self._refresh_timer.setSingleShot(True)
        self._refresh_timer.setInterval(120)
        self._refresh_timer.timeout.connect(self._refresh_graph_now)

        self.ui.btnGetGraph.clicked.connect(self.refresh_graph)
        self.ui._btn_add_tab.clicked.connect(lambda *_: self.add_plot_tab())
        self.ui.btnGetGraph.setToolTip("Перерисовать текущую вкладку графика по выбранным переменным и настройкам")
        self.ui._btn_add_tab.setToolTip("Добавить новую вкладку и выбрать тип графика")

        self._tab_widget: QTabWidget = self.ui.plotTabs
        self._tab_widget.setTabsClosable(True)
        self._tab_widget.tabCloseRequested.connect(self._on_tab_close_requested)
        self.add_plot_tab(LinePlot)

    def refresh_graph(self) -> None:
        self._refresh_timer.start()

    def _refresh_graph_now(self) -> None:
        for plot_tab in self._tabs:
            plot_tab.plot()

    def _pick_plot_class(self) -> type[Plot] | None:
        labels = [label for label, _cls in self._PLOT_CLASSES]
        selected_label, accepted = QInputDialog.getItem(
            self.ui.plotGroup,
            "Добавить вкладку",
            "Выберите тип графика:",
            labels,
            0,
            False,
        )
        if not accepted:
            return None

        return self._plot_class_by_label.get(selected_label)

    def add_plot_tab(self, tab_cls: type[Plot] | None = None, *_args: object) -> None:
        if not isinstance(tab_cls, type):
            tab_cls = None

        if tab_cls is None:
            tab_cls = self._pick_plot_class()
            if tab_cls is None:
                return

        plot_widget = tab_cls(self._tab_widget)

        plot_label = self._plot_label_by_class.get(tab_cls, "График")
        tab_index = len(self._tabs) + 1

        tab = PlotTab(plot_widget, f"{plot_label} {tab_index}")
        self._tabs.append(tab)

        self._tab_widget.addTab(tab.widget, tab.tab_title)
        self._tab_widget.setCurrentWidget(tab.widget)
        tab.plot()

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
