"""
Instrument classes for measurement error calculation.
"""

from abc import ABC, abstractmethod
from typing import Optional


class Instrument(ABC):
    """
    Абстрактный базовый класс для приборов измерения.

    Хранит:
    - name: str — имя прибора
    - error_value: float — величина ошибки
    """

    def __init__(self, name: str, error_value: float) -> None:
        """
        Инициализировать прибор с именем и величиной ошибки.

        :param name: Имя прибора.
        :param error_value: Величина ошибки.
        """
        self._name: str = name
        self._error_value: float = error_value

    @property
    def name(self) -> str:
        """Получить имя прибора."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Установить имя прибора."""
        self._name = value

    @property
    def error_value(self) -> float:
        """Получить базовую величину ошибки."""
        return self._error_value

    @error_value.setter
    def error_value(self, value: float) -> None:
        """Установить базовую величину ошибки."""
        self._error_value = value

    @abstractmethod
    def get_error(self, value: Optional[float] = None) -> float:
        """
        Получить погрешность прибора.

        :param value: Измеренное значение. Если передано — ошибка считается
                      относительно него (актуально для относительной погрешности).
                      Если None — возвращается базовая ошибка прибора.
        :return: Значение погрешности.
        """
        ...


class InstrumentAbsolute(Instrument):
    """
    Прибор с абсолютной погрешностью.

    Линейка (±0.5 мм), секундомер (±0.01 с) и т.д.
    Ошибка постоянна и не зависит от измеряемого значения.
    """

    def __init__(self, name: str, absolute_error: float) -> None:
        """
        Инициализировать прибор с абсолютной погрешностью.

        :param name: Имя прибора.
        :param absolute_error: Абсолютная погрешность (одинаковая для всех значений).
        """
        super().__init__(name, absolute_error)

    def get_error(self, value: Optional[float] = None) -> float:
        """
        Получить абсолютную погрешность.

        Параметр value игнорируется — ошибка постоянна для всех измерений.

        :param value: Не используется.
        :return: Абсолютная погрешность.
        """
        return self._error_value


class InstrumentRelative(Instrument):
    """
    Прибор с относительной погрешностью.

    Мультиметр (±2%), весы (±0.1%) и т.д.
    Ошибка зависит от измеряемого значения: Δ = |value| × (error% / 100).
    """

    def __init__(self, name: str, relative_error_percent: float) -> None:
        """
        Инициализировать прибор с относительной погрешностью.

        :param name: Имя прибора.
        :param relative_error_percent: Относительная погрешность в процентах.
        """
        super().__init__(name, relative_error_percent)

    @property
    def relative_error_percent(self) -> float:
        """Получить относительную погрешность в процентах."""
        return self._error_value

    @relative_error_percent.setter
    def relative_error_percent(self, value: float) -> None:
        """Установить относительную погрешность в процентах."""
        self._error_value = value

    def get_error(self, value: Optional[float] = None) -> float:
        """
        Получить погрешность.

        Если value не передан — возвращает процент погрешности (базовое значение).
        Если value передан — возвращает абсолютную погрешность: Δ = |value| × (error% / 100).

        :param value: Измеренное значение. Если None — возвращается процент.
        :return: Погрешность.
        """
        if value is None:
            return self._error_value
        return abs(value) * (self._error_value / 100.0)
