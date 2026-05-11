"""Widget-классы графиков для UI вкладок."""

from __future__ import annotations

from typing import Any

import numpy as np
import pyqtgraph as pg
from PySide6.QtCore import QEvent, QRectF, Qt, QAbstractTableModel
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QTableWidgetItem, QVBoxLayout, QWidget, QStyledItemDelegate, QSpinBox


from gui.views.item_delegates import *
from gui.views.ui_approximation_plot import Ui_ApproximationPlot
from gui.views.ui_correlogram_plot import Ui_CorrelogramPlot
from gui.views.ui_histogram_plot import Ui_HistogramPlot
from gui.views.ui_line_plot import Ui_LinePlot
from gui.views.ui_plot_base import Ui_PlotBase
from gui.views.ui_scatter_plot import Ui_ScatterPlot
from src import Experiment


class Plot(QWidget):
    """Базовый класс для графиков, работающих с данными Experiment."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.experiment = Experiment.get_experiment()
        self._base: Ui_PlotBase | None = None

    @property
    def plot_widget(self) -> pg.PlotWidget:
        if self._base is None:
            raise RuntimeError("Ui_PlotBase не инициализирован")
        return self._base.plotWidget

    def get_variable_by_name(self, name: str):
        for variable in self.experiment.get_variables():
            if variable.name == name:
                return variable
        return None

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
class LineSettingTableModle(QAbstractTableModel):
    def rowCount(self, parent: QTabelIndex = ...) -> int:
        return 5
    def columnCount(self, parent: QModelIndex = ...) -> int:
        print("LineSettingTableModel: ", len(Experiment.get_experiment().get_variables()))
        return len(Experiment.get_experiment().get_variables()) + 1
    def data(self, index, /, role = ...):
        if role == Qt.ItemDataRole.DisplayRole:
            return Experiment.get_experiment().get_variables()[index.count()].name
        return ""
    def headerData(self, section, orientation, role = ...):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return "H"
            else:
                return "V"
        return ""
    
    def flags(self, index, /):
        if index.row() == 4:
            return super().flags(index) | Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsUserCheckable
        return super().flags(index) | Qt.ItemFlag.ItemIsEditable
        self.plot_widget.setTitle(self._base.titleEdit.text())
        self.plot_widget.setLabel("bottom", self._base.xLabelEdit.text())
        self.plot_widget.setLabel("left", self._base.yLabelEdit.text())


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
        
        self.ui.settingsTable.setItemDelegateForRow(0, ComboBoxDelegate(options=list(self._LINE_TYPES.keys())))
        self.ui.settingsTable.setItemDelegateForRow(5, ComboBoxDelegate(options=list(self._VISIBILITY_TYPES.keys())))
        self.ui.settingsTable.setItemDelegateForRow(1, SpinBoxDelegate(min = 0, max = 100))
        self.ui.settingsTable.setItemDelegateForRow(3, SpinBoxDelegate(min = 0, max = 100))
        self.ui.settingsTable.setItemDelegateForRow(2, ComboBoxDelegate(options=list(self._POINT_TYPES.keys())))
        self.ui.settingsTable.setItemDelegateForRow(4, ColorDelegate())


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
        super().plot()

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

            color = self._cell_color(row, self._COL_COLOR)
            width = self._cell_int(row, self._COL_WIDTH, default=2)
            line_style = self._LINE_STYLES.get(
                self._cell_text(row, self._COL_LINE), Qt.PenStyle.SolidLine
            )
            symbol_text = self._cell_text(row, self._COL_SYMBOL)
            symbol = None if symbol_text.lower() in ("", "none") else symbol_text
            size = self._cell_int(row, self._COL_SIZE, default=5)

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

    def _cell_text(self, row: int, col: int) -> str:
        item = self.ui.settingsTable.item(row, col)
        return item.text() if item is not None else ""

    def _cell_int(self, row: int, col: int, default: int) -> int:
        try:
            return int(self._cell_text(row, col))
        except ValueError:
            return default

    def _cell_color(self, row: int, col: int):
        text = self._cell_text(row, col).strip()
        color = QColor(text)
        if not color.isValid():
            color = QColor(self._DEFAULT_PALETTE[row % len(self._DEFAULT_PALETTE)])
        return color
