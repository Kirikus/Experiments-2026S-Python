"""
Variable classes for storing measurement data.
"""

import csv
from pathlib import Path
from typing import List, Optional, TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from .instrument import Instrument


class Variable(ABC):
    """
    Абстрактный базовый класс для переменных.

    Хранит:
    - values: List[float] — измеренные значения (N неявно = len(values))
    - name: str — имя переменной
    """

    def __init__(self, name: str) -> None:
        """
        Инициализировать переменную с именем.

        :param name: Имя переменной.
        """
        self._name: str = name
        self._values: List[float] = []
        self._measurement_type: Optional[str] = None

    _MISSING_CELL = " "

    @property
    def name(self) -> str:
        """Получить имя переменной."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Установить имя переменной."""
        self._name = value

    @property
    def values(self) -> List[float]:
        """
        Получить копию списка значений.

        Возвращает копию, чтобы внешний код не мог мутировать внутреннее состояние.
        """
        return self._values.copy()

    def add_value(self, value: float) -> None:
        """Добавить значение к списку."""
        self._values.append(value)

    def set_values(self, values: List[float]) -> None:
        """Установить список значений целиком (копируется)."""
        self._values = values.copy()

    def count(self) -> int:
        """Получить N — количество измерений."""
        return len(self._values)

    @property
    def measurement_type(self) -> Optional[str]:
        """Получить тип измерения для фильтрации в объединённом CSV (если задан)."""
        return self._measurement_type

    @measurement_type.setter
    def measurement_type(self, value: Optional[str]) -> None:
        """Установить тип измерения для фильтрации в объединённом CSV."""
        self._measurement_type = value

    def __repr__(self) -> str:
        """Получить отладочное строковое представление переменной."""
        return (
            f"{self.__class__.__name__}(name={self._name!r}, "
            f"count={self.count()}, measurement_type={self._measurement_type!r})"
        )

    def __str__(self) -> str:
        """Получить краткое представление переменной для UI/логов."""
        return f"{self._name} (N={self.count()})"

    def write_csv(self, filepath: Path) -> None:
        """
        Сохранить значения и погрешности переменной в CSV.

        Формат:
        - index,value,error
        - при наличии measurement_type добавляется 4-й столбец measurement_type
        """
        values = self.values
        errors = self.get_errors()
        include_measurement_type = self._measurement_type is not None

        with open(filepath, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            headers = ["index", "value", "error"]
            if include_measurement_type:
                headers.append("measurement_type")
            writer.writerow(headers)

            for index, value in enumerate(values):
                error_cell = (
                    str(errors[index])
                    if index < len(errors)
                    else Variable._MISSING_CELL
                )
                row = [index, value, error_cell]
                if include_measurement_type:
                    row.append(self._measurement_type)
                writer.writerow(row)

    def read_csv(self, filepath: Path) -> None:
        """
        Загрузить значения переменной из CSV.

        Если у переменной задан measurement_type, загружаются только строки
        с соответствующим значением столбца measurement_type.
        """
        values: List[float] = []

        if hasattr(self, "errors"):
            self.errors = []

        with open(filepath, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                if self._measurement_type is not None:
                    row_type = (row.get("measurement_type") or "").strip()
                    if row_type != self._measurement_type:
                        continue

                value_cell = (row.get("value") or "").strip()
                if value_cell in {"", Variable._MISSING_CELL}:
                    continue

                values.append(float(value_cell))

                error_cell = (row.get("error") or "").strip()
                if (
                    hasattr(self, "add_error")
                    and error_cell not in {"", Variable._MISSING_CELL}
                ):
                    self.add_error(float(error_cell))

        self.set_values(values)

    @abstractmethod
    def serialize(self) -> dict:
        """Сериализовать метаданные переменной в dict."""
        ...

    @classmethod
    def deserialize(
        cls,
        data: dict,
        instruments: Optional[dict[str, "Instrument"]] = None,
    ) -> "Variable":
        """Создать Variable из сериализованных метаданных."""
        variable_type = data.get("type")
        name = data["name"]

        if variable_type == "measured":
            inst_name = data.get("instrument_name")
            instrument = instruments.get(inst_name) if (instruments and inst_name) else None
            variable = VariableMeasured(name, instrument)
        elif variable_type == "calculated":
            variable = VariableCalculated(name)
        else:
            raise ValueError(f"Unknown variable type: {variable_type}")

        variable.measurement_type = data.get("measurement_type")
        return variable

    @abstractmethod
    def get_errors(self) -> List[float]:
        """
        Получить список погрешностей для каждого значения.

        Реализуется в наследниках: VariableMeasured берёт ошибки от прибора,
        VariableCalculated хранит собственные ошибки.
        """
        ...


class VariableMeasured(Variable):
    """
    Переменная, значения которой измерены прибором.

    Погрешности вычисляются через связанный Instrument.get_error(value),
    что корректно работает как для абсолютной, так и для относительной погрешности.
    """

    def __init__(self, name: str, instrument: Optional["Instrument"] = None) -> None:
        """
        Инициализировать измеренную переменную.

        :param name: Имя переменной.
        :param instrument: Прибор для расчёта погрешностей (может быть None).
        """
        super().__init__(name)
        self._instrument: Optional["Instrument"] = instrument

    @property
    def instrument(self) -> Optional["Instrument"]:
        """Получить связанный прибор."""
        return self._instrument

    @instrument.setter
    def instrument(self, instrument: "Instrument") -> None:
        """Установить прибор для расчёта погрешностей."""
        self._instrument = instrument

    def get_errors(self) -> List[float]:
        """
        Получить список погрешностей от прибора для каждого измеренного значения.

        Для InstrumentAbsolute — константная ошибка.
        Для InstrumentRelative — ошибка зависит от конкретного значения.
        Если прибор не установлен — возвращает нулевые ошибки.
        """
        if self._instrument is None:
            return [0.0] * len(self._values)
        return [self._instrument.get_error(v) for v in self._values]

    def serialize(self) -> dict:
        """Сериализовать метаданные измеряемой переменной."""
        data = {
            "name": self.name,
            "type": "measured",
        }
        if self.instrument is not None:
            data["instrument_name"] = self.instrument.name
        if self.measurement_type is not None:
            data["measurement_type"] = self.measurement_type
        return data


class VariableCalculated(Variable):
    """
    Переменная, значения которой получены вычислением.

    Хранит собственный список погрешностей, не связанный с прибором.
    """

    def __init__(self, name: str) -> None:
        """
        Инициализировать вычисленную переменную.

        :param name: Имя переменной.
        """
        super().__init__(name)
        self._errors: List[float] = []

    @property
    def errors(self) -> List[float]:
        """
        Получить копию списка погрешностей.

        Возвращает копию, чтобы внешний код не мог мутировать внутреннее состояние.
        """
        return self._errors.copy()

    @errors.setter
    def errors(self, errors: List[float]) -> None:
        """Установить список погрешностей целиком (копируется)."""
        self._errors = errors.copy()

    def add_error(self, error: float) -> None:
        """Добавить погрешность для соответствующего значения."""
        self._errors.append(error)

    def get_errors(self) -> List[float]:
        """Получить копию списка погрешностей."""
        return self._errors.copy()

    def serialize(self) -> dict:
        """Сериализовать метаданные вычисляемой переменной."""
        data = {
            "name": self.name,
            "type": "calculated",
        }
        if self.measurement_type is not None:
            data["measurement_type"] = self.measurement_type
        return data
