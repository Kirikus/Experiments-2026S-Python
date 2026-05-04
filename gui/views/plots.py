"""Widget-классы графиков для UI вкладок."""

from __future__ import annotations

from typing import Any

import numpy as np
import pyqtgraph as pg
<<<<<<< HEAD
from PySide6.QtCore import QRectF
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget
=======
from PySide6.QtCore import QRectF, Qt
from PySide6.QtWidgets import QTableWidgetItem, QVBoxLayout, QWidget
>>>>>>> afdc0f2 (Refactor plot tabs and line plot settings (ui files removed from tracking))

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
<<<<<<< HEAD

    @property
    def plot_widget(self) -> pg.PlotWidget:
        return self.ui._base.ui.plotWidget
=======
        self._source_data: Any | None = None
        self._base: Ui_PlotBase | None = None

    @property
    def plot_widget(self) -> pg.PlotWidget:
        if self._base is None:
            raise RuntimeError("Ui_PlotBase не инициализирован")
        return self._base.plotWidget
>>>>>>> afdc0f2 (Refactor plot tabs and line plot settings (ui files removed from tracking))

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

<<<<<<< HEAD
    def plot(self) -> None:
        self.plot_widget.clear()
        self.plot_widget.setTitle(self.ui._base.ui.titleEdit.text())
        self.plot_widget.setLabel("bottom", self.ui._base.ui.xLabelEdit.text())
        self.plot_widget.setLabel("left", self.ui._base.ui.yLabelEdit.text())
=======
    def _apply_base_labels(self) -> None:
        if self._base is None:
            return
        self.plot_widget.setTitle(self._base.titleEdit.text())
        self.plot_widget.setLabel("bottom", self._base.xLabelEdit.text())
        self.plot_widget.setLabel("left", self._base.yLabelEdit.text())

>>>>>>> afdc0f2 (Refactor plot tabs and line plot settings (ui files removed from tracking))

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
<<<<<<< HEAD
    _COLOR_MAP = {
        "Синий": (0, 122, 204),
        "Красный": (204, 0, 0),
        "Зеленый": (0, 153, 76),
        "Черный": (0, 0, 0),
    }

    def variable_added(self):
        #TODO: use this slot to update settings table then Variable is added.
        ...

    def variable_removed(self, index: int) -> None:
        #TODO: use this slot to update settings table then Variable is removed.
        ...

=======
>>>>>>> afdc0f2 (Refactor plot tabs and line plot settings (ui files removed from tracking))
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.ui = Ui_LinePlot()
        self.ui.setupUi(self)
<<<<<<< HEAD

        #TODO: populate ui.settingsTable and connect it to MainWindow signals
        #FIXME: remove all references to self.ui.yVariableCombo and similar fields
        #FIXME: remove all references to self.set_source_data and similar methods
        #TODO: add combobox "X Variable" to lineplot.ui, which chooses which variable is used for X axis (None for simple range)
        #TODO: connect variable_added and variable_removed to signals from MainWindow

        return

        if self.ui.colorCombo.count() == 0:
            self.ui.colorCombo.addItems(list(self._COLOR_MAP.keys()))

        self._fill_variable_combos()

        self.ui.yVariableCombo.currentIndexChanged.connect(self.plot)
        self.ui.xVariableCombo.currentIndexChanged.connect(self.plot)
        self.ui.colorCombo.currentIndexChanged.connect(self.plot)
        self.ui.widthSpin.valueChanged.connect(self.plot)

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
        super().plot()

        for i, variable in enumerate(Experiment.get_experiment().get_variables()):
            # Skip invisible lines
            if self.ui.settingsTable.item(5, i).text() == "False":
                continue

            # TODO: allow choice of X variable via QComboBox
            y_vals = variable.values
            x_vals = list(range(len(y_vals)))

            name = self.ui.settingsTable.horizontalHeaderItem(0)
            linetype = {
                "Solid": Qt.PenStyle.SolidLine,
                "Dashed": Qt.PenStyle.DashLine,
            }[self.ui.settingsTable.item(0, i).text()]
            width = int(self.ui.settingsTable.item(1, i).text())
            symbol = self.ui.settingsTable.item(2, i).text()
            size = int(self.ui.settingsTable.item(3, i).text())
            color = self.ui.settingsTable.item(4, i).text()
            self.plot_widget.plot(
                x_vals,
                y_vals,
                pen=pg.mkPen(color=color, width=width, style=linetype),
                name=name,
                symbol=symbol,
                symbolSize=size,
                symbolBrush=color,
            )
=======
        self.setup_base_ui(self.ui.parent_ui)

        self.ui.xVariableCombo.currentIndexChanged.connect(self.plot)
        self.ui.settingsTable.itemChanged.connect(self.plot)
        self._fill_variable_controls()

    def set_source_data(self, data: Any | None) -> None:
        super().set_source_data(data)
        self._fill_variable_controls()

    def _fill_variable_controls(self) -> None:
        variable_names = [v.name for v in self.experiment.get_variables()]

        selected_x = self.ui.xVariableCombo.currentText()
        self.ui.xVariableCombo.blockSignals(True)
        self.ui.xVariableCombo.clear()
        self.ui.xVariableCombo.addItem("Индекс")
        self.ui.xVariableCombo.addItems(variable_names)
        restore_x_index = self.ui.xVariableCombo.findText(selected_x)
        self.ui.xVariableCombo.setCurrentIndex(restore_x_index if restore_x_index >= 0 else 0)
        self.ui.xVariableCombo.blockSignals(False)

        checked_by_name: dict[str, bool] = {}
        table = self.ui.settingsTable
        for col in range(table.columnCount()):
            header_item = table.horizontalHeaderItem(col)
            flag_item = table.item(1, col)
            if header_item is None or flag_item is None:
                continue
            checked_by_name[header_item.text()] = flag_item.checkState() == Qt.CheckState.Checked

        table.blockSignals(True)
        table.clearContents()
        table.setRowCount(2)
        table.setColumnCount(len(variable_names))
        table.setVerticalHeaderLabels(["Переменная Y", "Показать"])
        table.setHorizontalHeaderLabels(variable_names)

        for col, var_name in enumerate(variable_names):
            name_item = QTableWidgetItem(var_name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            table.setItem(0, col, name_item)

            enabled_item = QTableWidgetItem()
            enabled_item.setFlags(
                (enabled_item.flags() | Qt.ItemFlag.ItemIsUserCheckable) & ~Qt.ItemFlag.ItemIsEditable
            )
            enabled_item.setCheckState(
                Qt.CheckState.Checked
                if checked_by_name.get(var_name, True)
                else Qt.CheckState.Unchecked
            )
            table.setItem(1, col, enabled_item)

        table.resizeColumnsToContents()
        table.blockSignals(False)

    def plot(self) -> None:
        self.plot_widget.clear()
        self._apply_base_labels()

        table = self.ui.settingsTable
        if table.columnCount() == 0:
            return

        palette = [
            (0, 122, 204),
            (204, 0, 0),
            (0, 153, 76),
            (122, 0, 153),
            (255, 140, 0),
            (0, 0, 0),
        ]
        x_name = self.ui.xVariableCombo.currentText()

        plotted_count = 0
        for col in range(table.columnCount()):
            header_item = table.horizontalHeaderItem(col)
            enabled_item = table.item(1, col)
            if header_item is None or enabled_item is None:
                continue
            if enabled_item.checkState() != Qt.CheckState.Checked:
                continue

            y_var = self.get_variable_by_name(header_item.text())
            if y_var is None or y_var.count() == 0:
                continue
            y_vals = list(y_var.values)

            if x_name == "Индекс":
                x_vals = list(range(len(y_vals)))
            else:
                x_var = self.get_variable_by_name(x_name)
                if x_var is None or x_var.count() != len(y_vals):
                    continue
                x_vals = list(x_var.values)

            color = palette[plotted_count % len(palette)]
            self.plot_widget.plot(
                x_vals,
                y_vals,
                pen=pg.mkPen(color=color, width=2),
                name=y_var.name,
            )
            plotted_count += 1
>>>>>>> afdc0f2 (Refactor plot tabs and line plot settings (ui files removed from tracking))


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
