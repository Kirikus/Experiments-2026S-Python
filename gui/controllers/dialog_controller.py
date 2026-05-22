from __future__ import annotations

from enum import Enum
from pathlib import Path

from PySide6.QtWidgets import QFileDialog, QInputDialog, QMessageBox

from src import Constant, Experiment, InstrumentAbsolute, InstrumentRelative, VariableCalculated, VariableMeasured


class VariableKind(Enum):
    MEASURED = "Измеренная (с прибором)"
    CALCULATED = "Вычисленная"


class InstrumentKind(Enum):
    ABSOLUTE = "Абсолютная погрешность"
    RELATIVE = "Относительная погрешность (%)"


class DialogController:
    """Отдельный контроллер диалогов ввода/выбора для главного окна."""

    def __init__(self, window, experiment: Experiment) -> None:
        self.window = window
        self.experiment = experiment

    def confirm_new_experiment(self) -> bool:
        reply = QMessageBox.question(
            self.window, "Новый эксперимент", "Очистить текущий эксперимент?"
        )
        return reply == QMessageBox.StandardButton.Yes

    def select_open_path(self) -> Path | None:
        filename, _ = QFileDialog.getOpenFileName(
            self.window, "Открыть эксперимент", "", "JSON (*.json)"
        )
        return Path(filename) if filename else None

    def select_save_path(self) -> Path | None:
        filename, _ = QFileDialog.getSaveFileName(
            self.window, "Сохранить эксперимент", "", "JSON (*.json)"
        )
        return Path(filename) if filename else None

    def create_variable(self):
        name, ok = QInputDialog.getText(self.window, "Новая переменная", "Имя переменной:")
        if not (ok and name):
            return None

        if any(existing_var.name == name for existing_var in self.experiment.get_variables()):
            QMessageBox.warning(self.window, "Ошибка", f"Переменная '{name}' уже существует")
            return None

        var_type, ok = QInputDialog.getItem(
            self.window,
            "Тип переменной",
            "Выберите тип:",
            [kind.value for kind in VariableKind],
            0,
            False,
        )
        if not ok:
            return None

        if var_type == VariableKind.CALCULATED.value:
            return VariableCalculated(name)

        instruments = self.experiment.get_instruments()
        if not instruments:
            QMessageBox.information(
                self.window,
                "Нет приборов",
                "Сначала добавьте прибор, затем создайте измеряемую переменную.",
            )
            return None

        instrument_name, ok = QInputDialog.getItem(
            self.window,
            "Прибор переменной",
            "Выберите прибор:",
            [instrument.name for instrument in instruments],
            0,
            False,
        )
        if not ok:
            return None

        selected_instrument = next(
            instrument for instrument in instruments if instrument.name == instrument_name
        )
        return VariableMeasured(name, selected_instrument)

    def create_constant(self) -> Constant | None:
        name, ok = QInputDialog.getText(self.window, "Новая константа", "Имя константы:")
        if not (ok and name):
            return None

        if any(existing_const.name == name for existing_const in self.experiment.get_constants()):
            QMessageBox.warning(self.window, "Ошибка", f"Константа '{name}' уже существует")
            return None

        value, ok = QInputDialog.getDouble(
            self.window, "Значение", "Введите значение:", 0.0, -1e308, 1e308, 6
        )
        if not ok:
            return None

        return Constant(name, value, 0.0, readonly=False)

    def create_instrument(self):
        name, ok = QInputDialog.getText(self.window, "Новый прибор", "Имя прибора:")
        if not (ok and name):
            return None

        inst_type, ok = QInputDialog.getItem(
            self.window,
            "Тип прибора",
            "Выберите тип:",
            [kind.value for kind in InstrumentKind],
            0,
            False,
        )
        if not ok:
            return None

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
            return None

        if inst_type == InstrumentKind.ABSOLUTE.value:
            return InstrumentAbsolute(name, error)
        return InstrumentRelative(name, error)
