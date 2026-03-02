"""
Instrument classes for measurement error calculation.
"""

from abc import ABC, abstractmethod
from typing import List


class Instrument(ABC):
    """
    Абстрактный базовый класс для приборов измерения.
    
    Хранит:
    - QString name - имя прибора 
    - double error_value - величина ошибки
    """
    
    def __init__(self, name: str, error_value: float) -> None:
        self._name: str = name
        self._error_value: float = error_value
    
    @property
    def name(self) -> str:
        # Получить имя прибора
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        # Установить имя прибора
        self._name = value
    
    @property
    def error_value(self) -> float:
        # Получить величину ошибки
        return self._error_value
    
    @error_value.setter
    def error_value(self, value: float) -> None:
        # Установить величину ошибки
        self._error_value = value
    
    @abstractmethod
    def get_error(self) -> float:
        # Получить ошибку для расчётов (реализуется в наследниках)
        pass
    
    @abstractmethod
    def get_error_for_value(self, value: float) -> float:
        # Получить ошибку для конкретного значения измерения
        pass


class InstrumentAbsolute(Instrument):
    """
    Класс для приборов с абсолютной погрешностью.
    
    Линейка (±0.5 мм), секундомер (±0.01 с) и т.д.
    Ошибка постоянна и не зависит от измеряемого значения.
    """
    
    def __init__(self, name: str, absolute_error: float) -> None:
        # Инициализировать с абсолютной ошибкой
        super().__init__(name, absolute_error)
    
    def get_error(self) -> float:
        # Получить абсолютную ошибку (постоянная)
        return self._error_value
    
    def get_error_for_value(self, value: float) -> float:
        # Получить ошибку для значения (абсолютная = постоянная)
        # Параметр value игнорируется для абсолютной погрешности
        return self._error_value


class InstrumentRelative(Instrument):
    """
    Класс для приборов с относительной погрешностью.
    
    Мультиметр (±2%), весы (±0.1%) и т.д.
    Ошибка зависит от измеряемого значения: Δ = value * (error% / 100)
    """
    
    def __init__(self, name: str, relative_error_percent: float) -> None:
        # Инициализировать с относительной ошибкой в процентах
        super().__init__(name, relative_error_percent)
        self._relative_error_percent: float = relative_error_percent
    
    @property
    def relative_error_percent(self) -> float:
        # Получить относительную ошибку в процентах
        return self._relative_error_percent
    
    @relative_error_percent.setter
    def relative_error_percent(self, value: float) -> None:
        # Установить относительную ошибку в процентах
        self._relative_error_percent = value
        self._error_value = value
    
    def get_error(self) -> float:
        # Получить относительную ошибку в процентах (без value)
        # Для совместимости с базовым классом
        return self._relative_error_percent
    
    def get_error_for_value(self, value: float) -> float:
        # Получить абсолютную ошибку для конкретного значения
        # Δ = value * (error% / 100)
        return abs(value) * (self._relative_error_percent / 100.0)