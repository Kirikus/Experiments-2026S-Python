from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QAbstractItemView,
    QFileDialog,
    QInputDialog,
    QMessageBox,
    QTreeWidgetItem,
)
from PySide6.QtCore import Qt

from gui.models import InstrumentTableModel, ValueTableModel
from gui.views import MainWindow
from gui.views.item_delegates import FloatValueDelegate, InstrumentTypeDelegate
from gui.views.plot_manager import PlotManager
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
        # Установка моделей таблиц
        self.instrument_table_model = InstrumentTableModel(
            self.experiment,
            on_changed=self._on_instruments_model_changed,
        )
        self.window.ui.tableInstruments.setModel(self.instrument_table_model)

        self.value_table_model = ValueTableModel(on_variable_changed=self._on_values_model_changed)
        self.window.ui.tableValues.setModel(self.value_table_model)

        # Делегаты для корректного редактирования данных в таблицах.
        self.window.ui.tableValues.setItemDelegateForColumn(1, FloatValueDelegate(self.window.ui.tableValues))
        self.window.ui.tableValues.setItemDelegateForColumn(2, FloatValueDelegate(self.window.ui.tableValues))
        self.window.ui.tableInstruments.setItemDelegateForColumn(
            1,
            InstrumentTypeDelegate(self.window.ui.tableInstruments),
        )
        self.window.ui.tableInstruments.setItemDelegateForColumn(
            2,
            FloatValueDelegate(self.window.ui.tableInstruments),
        )

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

    def _on_values_model_changed(self, variable) -> None:
        if isinstance(variable, VariableMeasured | VariableCalculated):
            self.window.ui.valueCount.setText(str(variable.count()))
            self._plot_variable(variable)

    def _on_instruments_model_changed(self, *_args) -> None:
        self._refresh_tree(refresh_instrument_model=False)
        self.value_table_model.refresh()

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
        ui.tableValues.setEditTriggers(
            QAbstractItemView.DoubleClicked
            | QAbstractItemView.EditKeyPressed
            | QAbstractItemView.AnyKeyPressed
        )
        self.value_table_model.set_entity("variable", var)

        # Построить график переменной
        self._plot_variable(var)

    def _plot_variable(self, var) -> None:
        # Построить график точечного графика для переменной
        values = var.values
        if not values:
            self.window.plot_manager.clear()
            return

        title = f"График: {var.name}"
        self.window.plot_manager.plot_scatter(values, title)

    def _show_constant(self, const: Constant) -> None:
        # Отображение информации о константе в интерфейсе
        self._selected_variable = None
        ui = self.window.ui
        ui.valueName.setText(const.name)
        ui.valueType.setText("Константа" + (" (readonly)" if const.readonly else ""))
        ui.valueCount.setText("1")
        ui.tableValues.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.value_table_model.set_entity("constant", const)

        self.window.plot_manager.clear()

    def _show_instrument(self, inst) -> None:
        # Отображение информации о приборе в интерфейсе
        self._selected_variable = None
        ui = self.window.ui
        ui.valueName.setText(inst.name)
        ui.valueType.setText(f"Прибор ({self._instrument_type_label(inst)})")
        ui.valueCount.setText("1")
        ui.tableValues.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.value_table_model.set_entity("instrument", inst)

        self.window.plot_manager.clear()

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
