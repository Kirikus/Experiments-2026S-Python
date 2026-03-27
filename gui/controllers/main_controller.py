from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
    QInputDialog,
    QMessageBox,
    QTableWidgetItem,
    QTreeWidgetItem,
)
from PySide6.QtCore import Qt

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
    # Главный контроллер приложения, связывает модель, представление и обработку событий
    def __init__(self, window: MainWindow) -> None:
        # Инициализация контроллера, установка модели, сигналов и начальное обновление дерева
        self.window = window
        self.experiment = Experiment.get_experiment()
        self._selected_variable = None

        self._setup_tree()
        self._setup_models()
        self._connect_signals()
        self._refresh_tree()

        self.window.ui.statusbar.showMessage("Готово")

    def _setup_tree(self) -> None:
        # Настройка дерева эксперимента (переменные, константы, приборы)
        tree = self.window.ui.treeExperiment
        self._vars_item = QTreeWidgetItem(["Переменные"])
        self._consts_item = QTreeWidgetItem(["Константы"])
        self._insts_item = QTreeWidgetItem(["Приборы"])

        tree.addTopLevelItem(self._vars_item)
        tree.addTopLevelItem(self._consts_item)
        tree.addTopLevelItem(self._insts_item)
        tree.expandAll()

    def _setup_models(self) -> None:
        # Установка модели таблицы приборов
        self.instrument_table_model = InstrumentTableModel(self.experiment)
        self.window.ui.tableInstruments.setModel(self.instrument_table_model)

    def _connect_signals(self) -> None:
        # Подключение сигналов интерфейса к обработчикам событий
        ui = self.window.ui

        ui.actionNew.triggered.connect(self._on_new)
        ui.actionOpen.triggered.connect(self._on_open)
        ui.actionSave.triggered.connect(self._on_save)
        ui.actionExit.triggered.connect(self.window.close)

        ui.actionAddVariable.triggered.connect(self._on_add_variable)
        ui.actionAddConstant.triggered.connect(self._on_add_constant)
        ui.actionAddInstrument.triggered.connect(self._on_add_instrument)

        ui.treeExperiment.itemClicked.connect(self._on_tree_item_clicked)
        ui.tableValues.itemChanged.connect(self._on_table_value_changed)
        self.instrument_table_model.instrument_changed.connect(self._on_instrument_changed)

    def _on_instrument_changed(self, instrument) -> None:
        # Синхронизация UI после редактирования прибора в таблице приборов.
        self._refresh_tree(refresh_instrument_model=False)

        if isinstance(self._selected_variable, VariableMeasured):
            if self._selected_variable.instrument is instrument:
                self._show_variable(self._selected_variable)

    def _on_new(self) -> None:
        # Обработчик создания нового эксперимента
        reply = QMessageBox.question(
            self.window, "Новый эксперимент", "Очистить текущий эксперимент?"
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.experiment.clear()
            self._refresh_tree()
            self.window.ui.statusbar.showMessage("Создан новый эксперимент")

    def _on_open(self) -> None:
        # Обработчик открытия эксперимента из файла
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
        # Обработчик сохранения эксперимента в файл
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
        # Обработчик добавления новой переменной
        name, ok = QInputDialog.getText(
            self.window, "Новая переменная", "Имя переменной:"
        )
        if not (ok and name):
            return

        if any(existing_var.name == name for existing_var in self.experiment.get_variables()):
            QMessageBox.warning(self.window, "Ошибка", f"Переменная '{name}' уже существует")
            return

        types = ["Измеренная (с прибором)", "Вычисленная"]
        var_type, ok = QInputDialog.getItem(
            self.window, "Тип переменной", "Выберите тип:", types, 0, False
        )
        if not ok:
            return

        if var_type == types[0]:
            instruments = self.experiment.get_instruments()
            if not instruments:
                QMessageBox.information(
                    self.window,
                    "Нет приборов",
                    "Сначала добавьте прибор, затем создайте измеряемую переменную.",
                )
                return

            instrument_names = [instrument.name for instrument in instruments]
            instrument_name, ok = QInputDialog.getItem(
                self.window,
                "Прибор переменной",
                "Выберите прибор:",
                instrument_names,
                0,
                False,
            )
            if not ok:
                return

            selected_instrument = next(
                instrument for instrument in instruments if instrument.name == instrument_name
            )
            variable = VariableMeasured(name, selected_instrument)
        else:
            variable = VariableCalculated(name)

        self.experiment.add_variable(variable)
        self._refresh_tree()
        self.window.ui.statusbar.showMessage(f"Добавлена переменная: {name}")

    def _on_add_constant(self) -> None:
        # Обработчик добавления новой константы
        name, ok = QInputDialog.getText(
            self.window, "Новая константа", "Имя константы:"
        )
        if not (ok and name):
            return

        if any(existing_const.name == name for existing_const in self.experiment.get_constants()):
            QMessageBox.warning(self.window, "Ошибка", f"Константа '{name}' уже существует")
            return

        value, ok = QInputDialog.getDouble(
            self.window, "Значение", "Введите значение:", 0.0, -1e308, 1e308, 6
        )
        if not ok:
            return

        self.experiment.add_constant(Constant(name, value, 0.0, readonly=False))
        self._refresh_tree()
        self.window.ui.statusbar.showMessage(f"Добавлена константа: {name}")

    def _on_add_instrument(self) -> None:
        # Обработчик добавления нового прибора
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
        # Обработчик клика по элементу дерева эксперимента
        role_data = item.data(0, Qt.UserRole)
        if role_data is None:
            return

        entity_type, entity = role_data
        match entity_type:
            case "variable":
                self._show_variable(entity)
            case "constant":
                self._show_constant(entity)
            case "instrument":
                self._show_instrument(entity)
            case _:
                return

    def _show_variable(self, var) -> None:
        # Отображение информации о переменной в интерфейсе
        self._selected_variable = var
        ui = self.window.ui
        ui.valueName.setText(var.name)
        ui.valueType.setText("Измеренная" if isinstance(var, VariableMeasured) else "Вычисленная")
        ui.valueCount.setText(str(var.count()))

        table = ui.tableValues
        table.blockSignals(True)
        table.setRowCount(var.count() + 1)

        values = var.values
        errors = var.get_errors()

        for i, val in enumerate(values):
            err = errors[i] if i < len(errors) else 0.0
            decimal_places = self._decimal_places_from_number(err)
            value_text = self._format_number_with_places(val, decimal_places)
            error_text = self._format_number_with_places(err, decimal_places)

            table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            table.setItem(i, 1, QTableWidgetItem(value_text))
            table.setItem(i, 2, QTableWidgetItem(error_text))

        # Пустая строка для добавления нового значения
        add_row = var.count()
        table.setItem(add_row, 0, QTableWidgetItem(str(add_row + 1)))
        table.setItem(add_row, 1, QTableWidgetItem(""))
        table.setItem(add_row, 2, QTableWidgetItem(""))

        # Колонка N и погрешность read-only для измеряемой переменной
        for row in range(table.rowCount()):
            index_item = table.item(row, 0)
            if index_item is not None:
                index_item.setFlags(index_item.flags() & ~Qt.ItemIsEditable)

            error_item = table.item(row, 2)
            if error_item is not None and isinstance(var, VariableMeasured):
                error_item.setFlags(error_item.flags() & ~Qt.ItemIsEditable)

        table.blockSignals(False)

    def _on_table_value_changed(self, item: QTableWidgetItem) -> None:
        # Обработчик изменения таблицы значений для выбранной переменной
        if self._selected_variable is None:
            return

        row = item.row()
        column = item.column()
        variable = self._selected_variable

        # Разрешаем ввод значений в колонке 1 и (для вычисляемых) ошибок в колонке 2
        if column not in (1, 2):
            return
        if isinstance(variable, VariableMeasured) and column == 2:
            return

        text = (item.text() or "").strip()
        values = variable.values
        errors = variable.get_errors()

        try:
            if column == 1:
                if text == "":
                    if row < len(values):
                        values.pop(row)
                        if row < len(errors):
                            errors.pop(row)
                    else:
                        return
                else:
                    number = float(text.replace(",", "."))
                    if row < len(values):
                        values[row] = number
                    elif row == len(values):
                        values.append(number)
                    else:
                        return

                variable.set_values(values)
                if isinstance(variable, VariableCalculated):
                    # В вычисляемой переменной поддерживаем длину errors = длине values
                    if len(errors) < len(values):
                        errors.extend([0.0] * (len(values) - len(errors)))
                    elif len(errors) > len(values):
                        errors = errors[: len(values)]
                    variable.errors = errors

            elif column == 2 and isinstance(variable, VariableCalculated):
                if text == "":
                    number = 0.0
                else:
                    number = float(text.replace(",", "."))

                if row >= len(values):
                    return

                if len(errors) < len(values):
                    errors.extend([0.0] * (len(values) - len(errors)))
                errors[row] = number
                variable.errors = errors

            self._show_variable(variable)
            self.window.ui.valueCount.setText(str(variable.count()))

        except ValueError:
            QMessageBox.warning(self.window, "Ошибка", "Введите корректное число")
            self._show_variable(variable)

    def _show_constant(self, const: Constant) -> None:
        # Отображение информации о константе в интерфейсе
        self._selected_variable = None
        ui = self.window.ui
        ui.valueName.setText(const.name)
        ui.valueType.setText("Константа" + (" (readonly)" if const.readonly else ""))
        ui.valueCount.setText("1")

        ui.tableValues.setRowCount(1)
        decimal_places = self._decimal_places_from_number(const.error)
        value_text = self._format_number_with_places(const.value, decimal_places)
        error_text = self._format_number_with_places(const.error, decimal_places)

        ui.tableValues.setItem(0, 0, QTableWidgetItem("1"))
        ui.tableValues.setItem(0, 1, QTableWidgetItem(value_text))
        ui.tableValues.setItem(0, 2, QTableWidgetItem(error_text))

    def _show_instrument(self, inst) -> None:
        # Отображение информации о приборе в интерфейсе
        self._selected_variable = None
        ui = self.window.ui
        ui.valueName.setText(inst.name)
        ui.valueType.setText(f"Прибор ({self._instrument_type_label(inst)})")
        ui.valueCount.setText("1")

        ui.tableValues.setRowCount(1)
        ui.tableValues.setItem(0, 0, QTableWidgetItem("1"))
        ui.tableValues.setItem(0, 1, QTableWidgetItem(self._instrument_type_label(inst)))
        ui.tableValues.setItem(0, 2, QTableWidgetItem(str(inst.error_value)))

    def _decimal_places_from_number(self, number: float) -> int:
        # Определяет количество знаков после запятой для согласованного отображения
        normalized = f"{number:.12f}".rstrip("0").rstrip(".")
        if "." not in normalized:
            return 0
        return len(normalized.split(".")[1])

    def _format_number_with_places(self, number: float, places: int) -> str:
        # Форматирует число с фиксированным количеством знаков после запятой
        if places <= 0:
            return str(int(number)) if float(number).is_integer() else str(number)
        return f"{number:.{places}f}"

    def _instrument_type_label(self, inst) -> str:
        # Получение текстовой метки типа прибора
        return "абсолютная" if isinstance(inst, InstrumentAbsolute) else "относительная"

    def _refresh_tree(self, refresh_instrument_model: bool = True) -> None:
        # Обновление дерева эксперимента и таблицы приборов
        for item in (self._vars_item, self._consts_item, self._insts_item):
            item.takeChildren()

        for var in self.experiment.get_variables():
            variable_item = QTreeWidgetItem([var.name])
            variable_item.setData(0, Qt.UserRole, ("variable", var))
            self._vars_item.addChild(variable_item)

        for const in self.experiment.get_constants():
            constant_item = QTreeWidgetItem([const.name])
            constant_item.setData(0, Qt.UserRole, ("constant", const))
            self._consts_item.addChild(constant_item)

        for inst in self.experiment.get_instruments():
            instrument_item = QTreeWidgetItem([inst.name])
            instrument_item.setData(0, Qt.UserRole, ("instrument", inst))
            self._insts_item.addChild(instrument_item)

        self.window.ui.treeExperiment.expandAll()
        if refresh_instrument_model:
            self.instrument_table_model.refresh()
