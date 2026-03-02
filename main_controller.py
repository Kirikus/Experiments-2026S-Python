"""
Контроллер главного окна.
Связывает UI (MainWindow) с моделью данных (Experiment).
"""

from mainwindow import MainWindow
from src import Experiment, VariableMeasured, VariableCalculated
from src import InstrumentAbsolute, InstrumentRelative, Constant
from PySide6.QtWidgets import QInputDialog, QMessageBox, QFileDialog


class MainController:
    """
    Контроллер для управления MainWindow и Experiment.
    
    Реализует:
    - Обработчики меню (Файл, Эксперимент)
    - Работу с деревом переменных/констант/приборов
    - Отображение данных в таблице
    - Сериализацию/десериализацию
    """

    def __init__(self, window: MainWindow) -> None:
        # Инициализировать контроллер с окном
        self.window = window
        self.experiment = Experiment.get_experiment()
        
        # Настроить UI
        self._setup_tree()
        self._connect_signals()
        
        # Обновить статус
        self.window.ui.statusbar.showMessage("Готово")
    
    def _setup_tree(self) -> None:
        # Настроить дерево элементов эксперимента
        tree = self.window.ui.treeWidget
        
        # Создать корневые элементы
        self._vars_item = tree.invisibleRootItem().addChild(
            ["Переменные"]
        )
        self._consts_item = tree.invisibleRootItem().addChild(
            ["Константы"]
        )
        self._insts_item = tree.invisibleRootItem().addChild(
            ["Приборы"]
        )
        
        # Развернуть все
        tree.expandAll()
    
    def _connect_signals(self) -> None:
        # Подключить сигналы к слотам
        ui = self.window.ui
        
        # Меню Файл
        ui.actionNew.triggered.connect(self._on_new)
        ui.actionOpen.triggered.connect(self._on_open)
        ui.actionSave.triggered.connect(self._on_save)
        ui.actionExit.triggered.connect(self.window.close)
        
        # Меню Эксперимент
        ui.actionAddVariable.triggered.connect(self._on_add_variable)
        ui.actionAddConstant.triggered.connect(self._on_add_constant)
        ui.actionAddInstrument.triggered.connect(self._on_add_instrument)
        
        # Дерево
        ui.treeWidget.itemClicked.connect(self._on_tree_item_clicked)
    
    def _on_new(self) -> None:
        # Создать новый эксперимент
        reply = QMessageBox.question(
            self.window, "Новый эксперимент",
            "Очистить текущий эксперимент?"
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.experiment = Experiment()
            self._refresh_tree()
            self.window.ui.statusbar.showMessage("Создан новый эксперимент")
    
    def _on_open(self) -> None:
        # Открыть эксперимент из файла
        filename, _ = QFileDialog.getOpenFileName(
            self.window, "Открыть эксперимент", "",
            "JSON (*.json)"
        )
        if filename:
            from src.serializers import ExperimentSerializer
            
            serializer = ExperimentSerializer(self.experiment)
            serializer.load(filename)
            self._refresh_tree()
            self.window.ui.statusbar.showMessage(f"Загружен: {filename}")
    
    def _on_save(self) -> None:
        # Сохранить эксперимент в файл
        filename, _ = QFileDialog.getSaveFileName(
            self.window, "Сохранить эксперимент", "",
            "JSON (*.json)"
        )
        if filename:
            from pathlib import Path
            from src.serializers import ExperimentSerializer
            
            filepath = Path(filename)
            data_dir = filepath.parent / "data"
            serializer = ExperimentSerializer(self.experiment)
            serializer.save(filepath, data_dir)
            self.window.ui.statusbar.showMessage(f"Сохранён: {filename}")
    
    def _on_add_variable(self) -> None:
        # Добавить новую переменную
        name, ok = QInputDialog.getText(
            self.window, "Новая переменная", "Имя переменной:"
        )
        if ok and name:
            types = ["Измеренная (с прибором)", "Вычисленная"]
            var_type, ok = QInputDialog.getItem(
                self.window, "Тип переменной", "Выберите тип:", types, 0, False
            )
            if ok:
                if var_type == "Измеренная (с прибором)":
                    var = VariableMeasured(name)
                else:
                    var = VariableCalculated(name)
                
                self.experiment.add_variable(var)
                self._refresh_tree()
                self.window.ui.statusbar.showMessage(f"Добавлена переменная: {name}")
    
    def _on_add_constant(self) -> None:
        # Добавить новую константу
        name, ok = QInputDialog.getText(
            self.window, "Новая константа", "Имя константы:"
        )
        if ok and name:
            value, ok = QInputDialog.getDouble(
                self.window, "Значение", "Введите значение:",
                0.0, -1e308, 1e308, 6
            )
            if ok:
                error, ok = QInputDialog.getDouble(
                    self.window, "Погрешность", "Введите погрешность:",
                    0.0, 0.0, 1e308, 6
                )
                if ok:
                    const = Constant(name, value, error, readonly=False)
                    self.experiment.add_constant(const)
                    self._refresh_tree()
                    self.window.ui.statusbar.showMessage(f"Добавлена константа: {name}")
    
    def _on_add_instrument(self) -> None:
        # Добавить новый прибор
        name, ok = QInputDialog.getText(
            self.window, "Новый прибор", "Имя прибора:"
        )
        if ok and name:
            types = ["Абсолютная погрешность", "Относительная погрешность (%)"]
            inst_type, ok = QInputDialog.getItem(
                self.window, "Тип прибора", "Выберите тип:", types, 0, False
            )
            if ok:
                error, ok = QInputDialog.getDouble(
                    self.window, "Погрешность", "Введите значение:",
                    0.001, 0.0, 1e308, 6
                )
                if ok:
                    if inst_type == "Абсолютная погрешность":
                        inst = InstrumentAbsolute(name, error)
                    else:
                        inst = InstrumentRelative(name, error)
                    
                    self.experiment.add_instrument(inst)
                    self._refresh_tree()
                    self.window.ui.statusbar.showMessage(f"Добавлен прибор: {name}")
    
    def _on_tree_item_clicked(self, item, column) -> None:
        # Обработка клика по дереву
        text = item.text(0)
        
        # Найти объект по имени
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
        # Отобразить переменную
        ui = self.window.ui
        ui.valueName.setText(var.name)
        
        from src import VariableMeasured
        if isinstance(var, VariableMeasured):
            ui.valueType.setText("Измеренная")
        else:
            ui.valueType.setText("Вычисленная")
        
        ui.valueCount.setText(str(var.count()))
        
        # Заполнить таблицу
        table = ui.tableWidget
        table.setRowCount(var.count())
        
        values = var.values
        errors = var.get_errors()
        
        for i, (val, err) in enumerate(zip(values, errors)):
            table.setItem(i, 0, str(i))
            table.setItem(i, 1, str(val))
            table.setItem(i, 2, str(err))
    
    def _show_constant(self, const: Constant) -> None:
        # Отобразить константу
        ui = self.window.ui
        ui.valueName.setText(const.name)
        ui.valueType.setText("Константа" + (" (readonly)" if const.readonly else ""))
        ui.valueCount.setText("1")
        
        # Одна строка в таблице
        ui.tableWidget.setRowCount(1)
        ui.tableWidget.setItem(0, 0, "0")
        ui.tableWidget.setItem(0, 1, str(const.value))
        ui.tableWidget.setItem(0, 2, str(const.error))
    
    def _show_instrument(self, inst) -> None:
        # Отобразить прибор
        ui = self.window.ui
        ui.valueName.setText(inst.name)
        
        from src import InstrumentAbsolute
        if isinstance(inst, InstrumentAbsolute):
            ui.valueType.setText("Прибор (абсолютная)")
        else:
            ui.valueType.setText("Прибор (относительная)")
        
        ui.valueCount.setText("-")
        ui.tableWidget.setRowCount(0)
    
    def _refresh_tree(self) -> None:
        # Обновить дерево
        for item in [self._vars_item, self._consts_item, self._insts_item]:
            item.takeChildren()
        
        for var in self.experiment.get_variables():
            self._vars_item.addChild([var.name])
        
        for const in self.experiment.get_constants():
            self._consts_item.addChild([const.name])
        
        for inst in self.experiment.get_instruments():
            self._insts_item.addChild([inst.name])
        
        self.window.ui.treeWidget.expandAll()