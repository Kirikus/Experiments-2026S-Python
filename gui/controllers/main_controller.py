from __future__ import annotations

from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
)
from PySide6.QtCore import Qt

from gui.controllers.dialog_controller import DialogController
from gui.controllers.experiment_tree_controller import ExperimentTreeController
from gui.models import ConstantDetailTableModel, InstrumentTableModel, ValueTableModel
from gui.views import MainWindow
from gui.views.item_delegates import FloatValueDelegate
from src import (
    Constant,
    Experiment,
    InstrumentAbsolute,
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
        self._dialogs = DialogController(window, self.experiment)
        self._tree = ExperimentTreeController(self.window.ui.treeExperiment)

        self._setup_tree()
        self._setup_models()
        self._connect_signals()
        self._refresh_tree()

        self.window.ui.statusbar.showMessage("Готово")

    def _setup_tree(self) -> None:
        # Настройка дерева эксперимента (переменные, константы, приборы)
        self._tree.setup()

    def _setup_models(self) -> None:
        # Установка моделей таблиц
        self.instrument_table_model = InstrumentTableModel(self.experiment)
        self.window.ui.tableInstruments.setModel(self.instrument_table_model)

        self.value_table_model = ValueTableModel()
        self.window.ui.tableValues.setModel(self.value_table_model)
        self.value_table_model.validationFailed.connect(
            lambda message: self.window.ui.statusbar.showMessage(message, 4000)
        )

        self.constant_table_model = ConstantDetailTableModel()
        self.window.constantsTable.setModel(self.constant_table_model)
        self.window.constantsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.window.constantsTable.verticalHeader().setVisible(False)
        self.window.constantsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Делегаты для корректного редактирования данных в таблицах.
        self.window.ui.tableValues.setItemDelegateForColumn(1, FloatValueDelegate(self.window.ui.tableValues))
        self.window.ui.tableValues.setItemDelegateForColumn(2, FloatValueDelegate(self.window.ui.tableValues))

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

    def _on_new(self) -> None:
        # Обработчик создания нового эксперимента
        if self._dialogs.confirm_new_experiment():
            self.experiment.clear()
            self._refresh_tree()
            self.window.ui.statusbar.showMessage("Создан новый эксперимент")

    def _on_open(self) -> None:
        # Обработчик открытия эксперимента из файла
        filepath = self._dialogs.select_open_path()
        if filepath is None:
            return

        serializer = ExperimentSerializer(self.experiment)
        serializer.load(filepath)
        self._refresh_tree()
        self.window.ui.statusbar.showMessage(f"Загружен: {filepath}")

    def _on_save(self) -> None:
        # Обработчик сохранения эксперимента в файл
        filepath = self._dialogs.select_save_path()
        if filepath is None:
            return

        data_dir = filepath.parent / "data"
        serializer = ExperimentSerializer(self.experiment)
        serializer.save(filepath, data_dir)
        self.window.ui.statusbar.showMessage(f"Сохранён: {filepath}")

    def _on_add_variable(self) -> None:
        # Обработчик добавления новой переменной
        variable = self._dialogs.create_variable()
        if variable is None:
            return

        self.experiment.add_variable(variable)
        self._refresh_tree()
        self.window.ui.statusbar.showMessage(f"Добавлена переменная: {variable.name}")

    def _on_add_constant(self) -> None:
        # Обработчик добавления новой константы
        constant = self._dialogs.create_constant()
        if constant is None:
            return

        self.experiment.add_constant(constant)
        self._refresh_tree()
        self.window.ui.statusbar.showMessage(f"Добавлена константа: {constant.name}")

    def _on_add_instrument(self) -> None:
        # Обработчик добавления нового прибора
        instrument = self._dialogs.create_instrument()
        if instrument is None:
            return

        self.experiment.add_instrument(instrument)
        self._refresh_tree()
        self.window.ui.statusbar.showMessage(f"Добавлен прибор: {instrument.name}")

    def _on_tree_item_clicked(self, item, column) -> None:
        # Обработчик клика по элементу дерева эксперимента
        role_data = self._tree.resolve_entity(item)
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
        self.window.show_variables_page()
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
        self.constant_table_model.set_constant(None)

        # Сохраняем выбранную переменную как источник графика.
        self.window.plot_manager.set_source_variable(var)
        self.window.plot_manager.refresh_graph()

    def _show_constant(self, const: Constant) -> None:
        # Отображение информации о константе в интерфейсе
        self._selected_variable = None
        self.window.show_constants_page()
        ui = self.window.ui
        ui.valueName.setText(const.name)
        ui.valueType.setText("Константа" + (" (readonly)" if const.readonly else ""))
        ui.valueCount.setText("1")
        self.value_table_model.clear()
        self.constant_table_model.set_constant(const)

        self.window.plot_manager.set_source_variable(None)
        self.window.plot_manager.refresh_graph()

    def _show_instrument(self, inst) -> None:
        # Отображение информации о приборе в интерфейсе
        self._selected_variable = None
        self.window.show_instruments_page()
        ui = self.window.ui
        ui.valueName.setText(inst.name)
        ui.valueType.setText(f"Прибор ({self._instrument_type_label(inst)})")
        ui.valueCount.setText("1")
        self.value_table_model.clear()
        self.constant_table_model.set_constant(None)

        self.window.plot_manager.set_source_variable(None)
        self.window.plot_manager.refresh_graph()

    def _instrument_type_label(self, inst) -> str:
        # Получение текстовой метки типа прибора
        return "абсолютная" if isinstance(inst, InstrumentAbsolute) else "относительная"

    def _refresh_tree(self, refresh_instrument_model: bool = True) -> None:
        # Обновление дерева эксперимента и таблицы приборов
        self._tree.refresh(self.experiment)
        if refresh_instrument_model:
            self.instrument_table_model.refresh()
