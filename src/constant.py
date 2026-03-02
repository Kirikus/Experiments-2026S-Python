"""
Constant class for physical and calculated constants.
"""

from typing import Optional


class Constant:
    """
    Класс для хранения констант эксперимента.
    
    Хранит:
    - double value - значение константы
    - double error - погрешность константы
    - QString name - имя константы (пр.: "g", "π", "mean_X")
    - bool readonly - True для вычисленных (mean_X), False для введённых (g)
    """
    
    def __init__(
        self,
        name: str,
        value: float,
        error: float = 0.0,
        readonly: bool = False
    ) -> None:
        self._name: str = name
        self._value: float = value
        self._error: float = error
        self._readonly: bool = readonly
    
    @property
    def name(self) -> str:
        # Получить имя константы
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        # Установить имя константы
        self._name = value
    
    @property
    def value(self) -> float:
        # Получить значение константы
        return self._value
    
    @value.setter
    def value(self, value: float) -> None:
        # Установить значение константы (если не readonly)
        if self._readonly:
            raise ValueError(f"Constant '{self._name}' is readonly")
        self._value = value
    
    @property
    def error(self) -> float:
        # Получить погрешность константы
        return self._error
    
    @error.setter
    def error(self, value: float) -> None:
        # Установить погрешность константы (если не readonly)
        if self._readonly:
            raise ValueError(f"Constant '{self._name}' is readonly")
        self._error = value
    
    @property
    def readonly(self) -> bool:
        # Получить флаг readonly (True = вычисленная, False = введённая)
        return self._readonly
    
    def set_readonly(self, readonly: bool = True) -> None:
        # Установить флаг readonly
        # Используется после вычисления константы (mean_X)
        self._readonly = readonly
    
    def __repr__(self) -> str:
        # Получить строковое представление константы
        return f"Constant({self._name}={self._value}±{self._error}, readonly={self._readonly})"
    
    def to_string(self) -> str:
        # Получить отформатированную строку для отображения
        if self._error > 0:
            return f"{self._name} = {self._value} ± {self._error}"
        return f"{self._name} = {self._value}"