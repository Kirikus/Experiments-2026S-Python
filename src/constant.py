"""
Constant class for physical and calculated constants.
"""

from typing import Optional


class Constant:
    """
    Константа эксперимента — физическая или вычисленная.

    Хранит:
    - name: str — имя константы (пр.: "g", "π", "mean_X")
    - value: float — значение константы
    - error: float — погрешность константы
    - readonly: bool — True для вычисленных (mean_X), False для введённых вручную (g)
    """

    def __init__(
        self, name: str, value: float, error: float = 0.0, readonly: bool = False
    ) -> None:
        """
        Инициализировать константу.

        :param name: Имя константы.
        :param value: Значение константы.
        :param error: Погрешность (по умолчанию 0.0).
        :param readonly: Если True — константа защищена от изменений (вычисленная).
        """
        self._name: str = name
        self._value: float = value
        self._error: float = error
        self._readonly: bool = readonly

    @property
    def name(self) -> str:
        """Получить имя константы."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Установить имя константы."""
        self._name = value

    @property
    def value(self) -> float:
        """Получить значение константы."""
        return self._value

    @value.setter
    def value(self, value: float) -> None:
        """
        Установить значение константы.

        :raises ValueError: Если константа помечена как readonly.
        """
        if self._readonly:
            raise ValueError(f"Constant '{self._name}' is readonly")
        self._value = value

    @property
    def error(self) -> float:
        """Получить погрешность константы."""
        return self._error

    @error.setter
    def error(self, value: float) -> None:
        """
        Установить погрешность константы.

        :raises ValueError: Если константа помечена как readonly.
        """
        if self._readonly:
            raise ValueError(f"Constant '{self._name}' is readonly")
        self._error = value

    @property
    def readonly(self) -> bool:
        """Получить флаг readonly (True = вычисленная, False = введённая)."""
        return self._readonly

    def set_readonly(self, readonly: bool = True) -> None:
        """
        Установить флаг readonly.

        Используется после вычисления константы (например, mean_X).
        """
        self._readonly = readonly

    def __repr__(self) -> str:
        """Получить строковое представление константы."""
        return f"Constant({self._name}={self._value}±{self._error}, readonly={self._readonly})"

    def to_string(self) -> str:
        """Получить отформатированную строку для отображения."""
        if self._error > 0:
            return f"{self._name} = {self._value} ± {self._error}"
        return f"{self._name} = {self._value}"
