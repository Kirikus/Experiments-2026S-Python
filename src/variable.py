"""
Variable classes for storing measurement data.
"""

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
