from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
    QInputDialog,
    QMessageBox,
    QTableWidgetItem,
    QTreeWidgetItem,
)

from gui.models import InstrumentTableModel
from gui.views import MainWindow
from src import (
    Constant,
    Experiment,
    InstrumentAbsolute,
    InstrumentRelative,
    VariableCalculated,
    VariableMeasured,
)
from src.serializers import ExperimentSerializer


class MainController:
    def __init__(self, window: MainWindow) -> None:
        self.window = window
        self.experiment = Experiment.get_experiment()

        self._setup_tree()
        self._setup_models()
        self._connect_signals()
        self._refresh_tree()

        self.window.ui.statusbar.showMessage("Готово")

    def _setup_tree(self) -> None:
        tree = self.window.ui.treeExperiment
        self._vars_item = QTreeWidgetItem(["Переменные"])
        self._consts_item = QTreeWidgetItem(["Константы"])
        self._insts_item = QTreeWidgetItem(["Приборы"])

        tree.addTopLevelItem(self._vars_item)
        tree.addTopLevelItem(self._consts_item)
        tree.addTopLevelItem(self._insts_item)
        tree.expandAll()

    def _setup_models(self) -> None:
        self.instrument_table_model = InstrumentTableModel(self.experiment)
        self.window.ui.tableInstruments.setModel(self.instrument_table_model)

    def _connect_signals(self) -> None:
        ui = self.window.ui

        ui.actionNew.triggered.connect(self._on_new)
        ui.actionOpen.triggered.connect(self._on_open)
        ui.actionSave.triggered.connect(self._on_save)
        ui.actionExit.triggered.connect(self.window.close)

        ui.actionAddVariable.triggered.connect(self._on_add_variable)
        ui.actionAddConstant.triggered.connect(self._on_add_constant)
        ui.actionAddInstrument.triggered.connect(self._on_add_instrument)

        ui.treeExperiment.itemClicked.connect(self._on_tree_item_clicked)

    def _on_new(self) -> None:
        reply = QMessageBox.question(
            self.window, "Новый эксперимент", "Очистить текущий эксперимент?"
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.experiment.clear()
            self._refresh_tree()
            self.window.ui.statusbar.showMessage("Создан новый эксперимент")

    def _on_open(self) -> None:
        filename, _ = QFileDialog.getOpenFileName(
            self.window, "Открыть эксперимент", "", "JSON (*.json)"
        )
        if not filename:
            return

        serializer = ExperimentSerializer(self.experiment)
        serializer.load(Path(filename))
        self._refresh_tree()
        self.window.ui.statusbar.showMessage(f"Загружен: {filename}")

    def _on_save(self) -> None:
        filename, _ = QFileDialog.getSaveFileName(
            self.window, "Сохранить эксперимент", "", "JSON (*.json)"
        )
        if not filename:
            return

        filepath = Path(filename)
        data_dir = filepath.parent / "data"
        serializer = ExperimentSerializer(self.experiment)
        serializer.save(filepath, data_dir)
        self.window.ui.statusbar.showMessage(f"Сохранён: {filename}")

    def _on_add_variable(self) -> None:
        name, ok = QInputDialog.getText(
            self.window, "Новая переменная", "Имя переменной:"
        )
        if not (ok and name):
            return

        types = ["Измеренная (с прибором)", "Вычисленная"]
        var_type, ok = QInputDialog.getItem(
            self.window, "Тип переменной", "Выберите тип:", types, 0, False
        )
        if not ok:
            return

        variable = VariableMeasured(name) if var_type == types[0] else VariableCalculated(name)
        self.experiment.add_variable(variable)
        self._refresh_tree()
        self.window.ui.statusbar.showMessage(f"Добавлена переменная: {name}")

    def _on_add_constant(self) -> None:
        name, ok = QInputDialog.getText(
            self.window, "Новая константа", "Имя константы:"
        )
        if not (ok and name):
            return

        value, ok = QInputDialog.getDouble(
            self.window, "Значение", "Введите значение:", 0.0, -1e308, 1e308, 6
        )
        if not ok:
            return

        error, ok = QInputDialog.getDouble(
            self.window,
            "Погрешность",
            "Введите погрешность:",
            0.0,
            0.0,
            1e308,
            6,
        )
        if not ok:
            return

        self.experiment.add_constant(Constant(name, value, error, readonly=False))
        self._refresh_tree()
        self.window.ui.statusbar.showMessage(f"Добавлена константа: {name}")

    def _on_add_instrument(self) -> None:
        name, ok = QInputDialog.getText(self.window, "Новый прибор", "Имя прибора:")
        if not (ok and name):
            return

        types = ["Абсолютная погрешность", "Относительная погрешность (%)"]
        inst_type, ok = QInputDialog.getItem(
            self.window, "Тип прибора", "Выберите тип:", types, 0, False
        )
        if not ok:
            return

        error, ok = QInputDialog.getDouble(
            self.window,
            "Погрешность",
            "Введите значение:",
            0.001,
            0.0,
            1e308,
            6,
        )
        if not ok:
            return

        instrument = (
            InstrumentAbsolute(name, error)
            if inst_type == types[0]
            else InstrumentRelative(name, error)
        )
        self.experiment.add_instrument(instrument)
        self._refresh_tree()
        self.window.ui.statusbar.showMessage(f"Добавлен прибор: {name}")

    def _on_tree_item_clicked(self, item, column) -> None:
        text = item.text(0)

        for var in self.experiment.get_variables():
            if var.name == text:
                self._show_variable(var)
                return

        for const in self.experiment.get_constants():
            if const.name == text:
                self._show_constant(const)
                return

        for inst in self.experiment.get_instruments():
            if inst.name == text:
                self._show_instrument(inst)
                return

    def _show_variable(self, var) -> None:
        ui = self.window.ui
        ui.valueName.setText(var.name)
        ui.valueType.setText("Измеренная" if isinstance(var, VariableMeasured) else "Вычисленная")
        ui.valueCount.setText(str(var.count()))

        table = ui.tableValues
        table.setRowCount(var.count())

        values = var.values
        errors = var.get_errors()
        for i, val in enumerate(values):
            err = errors[i] if i < len(errors) else 0.0
            table.setItem(i, 0, QTableWidgetItem(str(i)))
            table.setItem(i, 1, QTableWidgetItem(str(val)))
            table.setItem(i, 2, QTableWidgetItem(str(err)))

    def _show_constant(self, const: Constant) -> None:
        ui = self.window.ui
        ui.valueName.setText(const.name)
        ui.valueType.setText("Константа" + (" (readonly)" if const.readonly else ""))
        ui.valueCount.setText("1")

        ui.tableValues.setRowCount(1)
        ui.tableValues.setItem(0, 0, QTableWidgetItem("0"))
        ui.tableValues.setItem(0, 1, QTableWidgetItem(str(const.value)))
        ui.tableValues.setItem(0, 2, QTableWidgetItem(str(const.error)))

    def _show_instrument(self, inst) -> None:
        ui = self.window.ui
        ui.valueName.setText(inst.name)
        ui.valueType.setText(f"Прибор ({self._instrument_type_label(inst)})")
        ui.valueCount.setText("1")

        ui.tableValues.setRowCount(1)
        ui.tableValues.setItem(0, 0, QTableWidgetItem("0"))
        ui.tableValues.setItem(0, 1, QTableWidgetItem(self._instrument_type_label(inst)))
        ui.tableValues.setItem(0, 2, QTableWidgetItem(str(inst.error_value)))

    def _instrument_type_label(self, inst) -> str:
        return "абсолютная" if isinstance(inst, InstrumentAbsolute) else "относительная"

    def _refresh_tree(self) -> None:
        for item in (self._vars_item, self._consts_item, self._insts_item):
            item.takeChildren()

        for var in self.experiment.get_variables():
            self._vars_item.addChild(QTreeWidgetItem([var.name]))
        for const in self.experiment.get_constants():
            self._consts_item.addChild(QTreeWidgetItem([const.name]))
        for inst in self.experiment.get_instruments():
            self._insts_item.addChild(QTreeWidgetItem([inst.name]))

        self.window.ui.treeExperiment.expandAll()
        self.instrument_table_model.refresh()
