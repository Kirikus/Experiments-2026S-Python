"""Widget-классы графиков для UI вкладок."""

from __future__ import annotations

from typing import Any

import numpy as np
import pyqtgraph as pg
from PySide6.QtCore import QEvent, QRectF, Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QTableWidgetItem, QVBoxLayout, QWidget

from gui.views.ui_approximation_plot import Ui_ApproximationPlot
from gui.views.ui_correlogram_plot import Ui_CorrelogramPlot
from gui.views.ui_histogram_plot import Ui_HistogramPlot
from gui.views.ui_line_plot import Ui_LinePlot
from gui.views.ui_plot_base import Ui_PlotBase
from gui.views.ui_scatter_plot import Ui_ScatterPlot
from src import Experiment


def moveUiContents(source_widget: QWidget, target_widget: QWidget) -> None:
    """Переносит содержимое layout из source_widget в target_widget."""
    source_layout = source_widget.layout()
    if source_layout is None:
        return

    target_layout = target_widget.layout()
    if target_layout is None:
        target_layout = QVBoxLayout(target_widget)
        target_layout.setContentsMargins(0, 0, 0, 0)

    while source_layout.count():
        item = source_layout.takeAt(0)
        child_widget = item.widget()
        child_layout = item.layout()
        spacer = item.spacerItem()

        if child_widget is not None:
            target_layout.addWidget(child_widget)
        elif child_layout is not None:
            target_layout.addLayout(child_layout)
        elif spacer is not None:
            target_layout.addItem(spacer)


class Plot(QWidget):
    """Базовый класс для графиков, работающих с данными Experiment."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.experiment = Experiment.get_experiment()
        self._source_data: Any | None = None
        self._base: Ui_PlotBase | None = None

    @property
    def plot_widget(self) -> pg.PlotWidget:
        if self._base is None:
            raise RuntimeError("Ui_PlotBase не инициализирован")
        return self._base.plotWidget

    def setup_base_ui(self, parent_ui: QWidget) -> None:
        """Создает Ui_PlotBase и переносит его содержимое в parent_ui."""
        temp_container = QWidget()
        self._base = Ui_PlotBase()
        self._base.setupUi(temp_container)
        moveUiContents(temp_container, parent_ui)
        self.plot_widget.setBackground("w")
        self.plot_widget.showGrid(x=True, y=True, alpha=0.2)

    def set_source_data(self, data: Any | None) -> None:
        self._source_data = data

    def set_source_variable(self, variable: Any | None) -> None:
        """Совместимость с PlotManager: источник данных = выбранная переменная."""
        self.set_source_data(variable)

    def get_variable_by_name(self, name: str):
        for variable in self.experiment.get_variables():
            if variable.name == name:
                return variable
        return None

    def _fill_xy_combos(self, x_combo, y_combo, include_index: bool = True) -> None:
        variable_names = [v.name for v in self.experiment.get_variables()]

        x_combo.blockSignals(True)
        x_combo.clear()
        if include_index:
            x_combo.addItem("Индекс")
        x_combo.addItems(variable_names)
        x_combo.blockSignals(False)

        y_combo.blockSignals(True)
        y_combo.clear()
        y_combo.addItems(variable_names)
        y_combo.blockSignals(False)

    def _fill_y_combo(self, y_combo) -> None:
        variable_names = [v.name for v in self.experiment.get_variables()]
        y_combo.blockSignals(True)
        y_combo.clear()
        y_combo.addItems(variable_names)
        y_combo.blockSignals(False)

    def _apply_base_labels(self) -> None:
        if self._base is None:
            return
        self.plot_widget.setTitle(self._base.titleEdit.text())
        self.plot_widget.setLabel("bottom", self._base.xLabelEdit.text())
        self.plot_widget.setLabel("left", self._base.yLabelEdit.text())

class ScatterPlot(Plot):
    _SYMBOLS = {
        "Круг": "o",
        "Квадрат": "s",
        "Треугольник": "t",
        "Ромб": "d",
        "Плюс": "+",
        "Крест": "x",
    }

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.ui = Ui_ScatterPlot()
        self.ui.setupUi(self)
        self.setup_base_ui(self.ui.parent_ui)

        if self.ui.symbolCombo.count() == 0:
            for label, symbol in self._SYMBOLS.items():
                self.ui.symbolCombo.addItem(f"{label} ({symbol})", symbol)
        self.ui.symbolCombo.setCurrentIndex(0)

        self._fill_variable_combos()

        self.ui.yVariableCombo.currentIndexChanged.connect(self.plot)
        self.ui.xVariableCombo.currentIndexChanged.connect(self.plot)
        self.ui.symbolCombo.currentIndexChanged.connect(self.plot)
        self.ui.sizeSpin.valueChanged.connect(self.plot)

    def set_source_data(self, data: Any | None) -> None:
        super().set_source_data(data)
        self._fill_variable_combos()
        if data is not None and hasattr(data, "name"):
            idx = self.ui.yVariableCombo.findText(data.name)
            if idx >= 0:
                self.ui.yVariableCombo.setCurrentIndex(idx)

    def _fill_variable_combos(self) -> None:
        self._fill_xy_combos(self.ui.xVariableCombo, self.ui.yVariableCombo, include_index=True)

    def plot(self) -> None:
        self.plot_widget.clear()
        self._apply_base_labels()

        y_var = self.get_variable_by_name(self.ui.yVariableCombo.currentText())
        if y_var is None or y_var.count() == 0:
            return
        y_vals = list(y_var.values)

        x_name = self.ui.xVariableCombo.currentText()
        if x_name == "Индекс":
            x_vals = list(range(len(y_vals)))
        else:
            x_var = self.get_variable_by_name(x_name)
            if x_var is None or x_var.count() != len(y_vals):
                return
            x_vals = list(x_var.values)

        symbol = self.ui.symbolCombo.currentData() or "o"
        self.plot_widget.plot(
            x_vals,
            y_vals,
            pen=None,
            symbol=symbol,
            symbolSize=self.ui.sizeSpin.value(),
            symbolBrush=(0, 122, 204),
            symbolPen=(0, 122, 204),
            name=y_var.name,
        )


class LinePlot(Plot):
    _COL_LINE = 0
    _COL_WIDTH = 1
    _COL_SYMBOL = 2
    _COL_SIZE = 3
    _COL_COLOR = 4
    _COL_VISIBLE = 5

    _LINE_STYLES = {
        "Solid": Qt.PenStyle.SolidLine,
        "Dashed": Qt.PenStyle.DashLine,
        "Dotted": Qt.PenStyle.DotLine,
    }
    _DEFAULT_PALETTE = ["#1F77B4", "#D62728", "#2CA02C", "#9467BD", "#FF7F0E", "#000000"]
    _DEFAULTS = ("Solid", "2", "None", "5", "#1F77B4", "True")
    _X_INDEX = "Индекс"

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.ui = Ui_LinePlot()
        self.ui.setupUi(self)
        # Новая архитектура: PlotBase встроен как кастомный виджет в .ui,
        # переиспользуем его внутренний Ui_PlotBase под Plot.plot_widget / _apply_base_labels.
        self._base = self.ui._base.ui
        self.plot_widget.setBackground("w")
        self.plot_widget.showGrid(x=True, y=True, alpha=0.2)

        self.ui.xVariableCombo.currentIndexChanged.connect(self.plot)
        self.ui.settingsTable.itemChanged.connect(self.plot)

        self._main_window_signal_bound = False
        self._sync_with_experiment()
        self._bind_main_window_signal()

    def set_source_data(self, data: Any | None) -> None:
        # Перерисовываемся на любое изменение списка переменных:
        # PlotManager.refresh_variable_lists (его триггерит MainWindow.variableListChanged
        # после add/remove переменной) дёргает set_source_variable → set_source_data.
        super().set_source_data(data)
        self._sync_with_experiment()
        self._bind_main_window_signal()

    def event(self, event) -> bool:
        if event.type() == QEvent.Type.ParentChange:
            self._bind_main_window_signal()
        return super().event(event)

    def _bind_main_window_signal(self) -> None:
        if self._main_window_signal_bound:
            return

        widget = self.parentWidget()
        while widget is not None:
            signal = getattr(widget, "variableListChanged", None)
            if signal is not None and hasattr(signal, "connect"):
                signal.connect(self._sync_with_experiment)
                self._main_window_signal_bound = True
                return
            widget = widget.parentWidget()

    def _sync_with_experiment(self) -> None:
        variable_names = [v.name for v in self.experiment.get_variables()]
        self._rebuild_x_combo(variable_names)
        self._rebuild_settings_table(variable_names)

    def _rebuild_x_combo(self, variable_names: list[str]) -> None:
        combo = self.ui.xVariableCombo
        previous = combo.currentText()
        combo.blockSignals(True)
        combo.clear()
        combo.addItem(self._X_INDEX)
        combo.addItems(variable_names)
        restore = combo.findText(previous)
        combo.setCurrentIndex(restore if restore >= 0 else 0)
        combo.blockSignals(False)

    def _rebuild_settings_table(self, variable_names: list[str]) -> None:
        table = self.ui.settingsTable
        # Сохраняем текущие настройки по имени переменной, чтобы не сбрасывать их
        # при добавлении/удалении других переменных.
        saved: dict[str, list[str]] = {}
        for row in range(table.rowCount()):
            header = table.verticalHeaderItem(row)
            if header is None:
                continue
            saved[header.text()] = [
                (table.item(row, col).text() if table.item(row, col) is not None else "")
                for col in range(table.columnCount())
            ]

        table.blockSignals(True)
        table.clearContents()
        table.setRowCount(len(variable_names))
        table.setVerticalHeaderLabels(variable_names)

        for row, name in enumerate(variable_names):
            existing = saved.get(name)
            defaults = list(self._DEFAULTS)
            if existing is None:
                defaults[self._COL_COLOR] = self._DEFAULT_PALETTE[row % len(self._DEFAULT_PALETTE)]
            values = existing if existing is not None else defaults
            for col, value in enumerate(values):
                table.setItem(row, col, QTableWidgetItem(value))

        table.resizeColumnsToContents()
        table.blockSignals(False)

    def plot(self) -> None:
        self.plot_widget.clear()
        self._apply_base_labels()

        table = self.ui.settingsTable
        x_name = self.ui.xVariableCombo.currentText()

        for row in range(table.rowCount()):
            header = table.verticalHeaderItem(row)
            if header is None:
                continue

            visible_item = table.item(row, self._COL_VISIBLE)
            if visible_item is None or visible_item.text().strip().lower() != "true":
                continue

            y_var = self.get_variable_by_name(header.text())
            if y_var is None or y_var.count() == 0:
                continue
            y_vals = list(y_var.values)

            if x_name == self._X_INDEX:
                x_vals = list(range(len(y_vals)))
            else:
                x_var = self.get_variable_by_name(x_name)
                if x_var is None or x_var.count() != len(y_vals):
                    continue
                x_vals = list(x_var.values)

            color = self._cell_color(table, row, self._COL_COLOR)
            width = self._cell_int(table, row, self._COL_WIDTH, default=2)
            line_style = self._LINE_STYLES.get(
                self._cell_text(table, row, self._COL_LINE), Qt.PenStyle.SolidLine
            )
            symbol_text = self._cell_text(table, row, self._COL_SYMBOL)
            symbol = None if symbol_text.lower() in ("", "none") else symbol_text
            size = self._cell_int(table, row, self._COL_SIZE, default=5)

            self.plot_widget.plot(
                x_vals,
                y_vals,
                pen=pg.mkPen(color=color, width=width, style=line_style),
                name=header.text(),
                symbol=symbol,
                symbolSize=size,
                symbolBrush=color,
                symbolPen=color,
            )

    @staticmethod
    def _cell_text(table, row: int, col: int) -> str:
        item = table.item(row, col)
        return item.text() if item is not None else ""

    @classmethod
    def _cell_int(cls, table, row: int, col: int, default: int) -> int:
        try:
            return int(cls._cell_text(table, row, col))
        except ValueError:
            return default

    @classmethod
    def _cell_color(cls, table, row: int, col: int):
        text = cls._cell_text(table, row, col).strip()
        color = QColor(text)
        if not color.isValid():
            color = QColor(cls._DEFAULT_PALETTE[row % len(cls._DEFAULT_PALETTE)])
        return color


class HistogramPlot(Plot):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.ui = Ui_HistogramPlot()
        self.ui.setupUi(self)
        self.setup_base_ui(self.ui.parent_ui)

        self.ui.yVariableCombo.currentIndexChanged.connect(self.plot)
        self.ui.binsSpin.valueChanged.connect(self.plot)
        self._fill_variable_combos()

    def set_source_data(self, data: Any | None) -> None:
        super().set_source_data(data)
        self._fill_variable_combos()
        if data is not None and hasattr(data, "name"):
            idx = self.ui.yVariableCombo.findText(data.name)
            if idx >= 0:
                self.ui.yVariableCombo.setCurrentIndex(idx)

    def _fill_variable_combos(self) -> None:
        self._fill_y_combo(self.ui.yVariableCombo)

    def plot(self) -> None:
        self.plot_widget.clear()
        self._apply_base_labels()

        y_var = self.get_variable_by_name(self.ui.yVariableCombo.currentText())
        if y_var is None or y_var.count() == 0:
            return
        values = np.asarray(list(y_var.values), dtype=float)

        bins = max(1, self.ui.binsSpin.value())
        hist, edges = np.histogram(values, bins=bins)
        centers = (edges[:-1] + edges[1:]) / 2.0
        widths = np.diff(edges)

        bars = pg.BarGraphItem(x=centers, height=hist, width=widths * 0.9, brush=(204, 122, 0))
        self.plot_widget.addItem(bars)


class ApproximationPlot(Plot):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.ui = Ui_ApproximationPlot()
        self.ui.setupUi(self)
        self.setup_base_ui(self.ui.parent_ui)

        self.ui.yVariableCombo.currentIndexChanged.connect(self.plot)
        self.ui.xVariableCombo.currentIndexChanged.connect(self.plot)
        self.ui.showPointsCheckBox.toggled.connect(self.plot)
        self._fill_variable_combos()

    def set_source_data(self, data: Any | None) -> None:
        super().set_source_data(data)
        self._fill_variable_combos()
        if data is not None and hasattr(data, "name"):
            idx = self.ui.yVariableCombo.findText(data.name)
            if idx >= 0:
                self.ui.yVariableCombo.setCurrentIndex(idx)

    def _fill_variable_combos(self) -> None:
        self._fill_xy_combos(self.ui.xVariableCombo, self.ui.yVariableCombo, include_index=True)

    def plot(self) -> None:
        self.plot_widget.clear()
        self._apply_base_labels()

        y_var = self.get_variable_by_name(self.ui.yVariableCombo.currentText())
        if y_var is None or y_var.count() < 2:
            return
        y_vals = np.asarray(list(y_var.values), dtype=float)

        x_name = self.ui.xVariableCombo.currentText()
        if x_name == "Индекс":
            x_vals = np.arange(len(y_vals), dtype=float)
        else:
            x_var = self.get_variable_by_name(x_name)
            if x_var is None or x_var.count() != len(y_vals):
                return
            x_vals = np.asarray(list(x_var.values), dtype=float)

        a, b = np.polyfit(x_vals, y_vals, 1)
        y_fit = a * x_vals + b

        if self.ui.showPointsCheckBox.isChecked():
            self.plot_widget.plot(
                x_vals,
                y_vals,
                pen=None,
                symbol="o",
                symbolSize=6,
                symbolBrush=(0, 122, 204),
                symbolPen=(0, 122, 204),
                name="Исходные данные",
            )

        self.plot_widget.plot(
            x_vals,
            y_fit,
            pen=pg.mkPen(color=(204, 0, 0), width=2),
            name=f"Линия тренда (y = {a:.3f}*x + {b:.3f})",
        )


class CorrelogramPlot(Plot):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.ui = Ui_CorrelogramPlot()
        self.ui.setupUi(self)
        self.setup_base_ui(self.ui.parent_ui)

        self.ui.yVariableCombo.currentIndexChanged.connect(self.plot)
        self.ui.maxLagSpin.valueChanged.connect(self.plot)
        self._fill_variable_combos()

    def set_source_data(self, data: Any | None) -> None:
        super().set_source_data(data)
        self._fill_variable_combos()
        if data is not None and hasattr(data, "name"):
            idx = self.ui.yVariableCombo.findText(data.name)
            if idx >= 0:
                self.ui.yVariableCombo.setCurrentIndex(idx)

    def _fill_variable_combos(self) -> None:
        self._fill_y_combo(self.ui.yVariableCombo)

    def plot(self) -> None:
        self.plot_widget.clear()
        self._apply_base_labels()

        y_var = self.get_variable_by_name(self.ui.yVariableCombo.currentText())
        if y_var is None or y_var.count() < 2:
            return
        series = np.asarray(list(y_var.values), dtype=float)

        max_lag = min(max(1, int(self.ui.maxLagSpin.value())), series.size - 1)

        centered = series - float(np.mean(series))
        variance = float(np.dot(centered, centered))
        if variance == 0.0:
            autocorr = np.ones(max_lag + 1, dtype=float)
        else:
            autocorr = np.empty(max_lag + 1, dtype=float)
            autocorr[0] = 1.0
            for lag in range(1, max_lag + 1):
                numerator = float(np.dot(centered[:-lag], centered[lag:]))
                autocorr[lag] = numerator / variance

        corr_matrix = np.empty((max_lag + 1, max_lag + 1), dtype=float)
        for i in range(max_lag + 1):
            for j in range(max_lag + 1):
                corr_matrix[i, j] = autocorr[abs(i - j)]

        image = pg.ImageItem(corr_matrix)
        image.setRect(QRectF(0, 0, max_lag + 1, max_lag + 1))
        image.setColorMap(pg.colormap.get("CET-D1"))

        plot_item = self.plot_widget.getPlotItem()
        plot_item.addItem(image)
        plot_item.getViewBox().setLimits(xMin=0, xMax=max_lag + 1, yMin=0, yMax=max_lag + 1)
