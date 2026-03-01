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
    - QList<double> value - значения (N хранится неявно по размеру списка)
    - QString name - имя переменной
    """
    
    def __init__(self, name: str) -> None:
        self._name: str = name
        self._values: List[float] = []
    
    @property
    def name(self) -> str:
        # Получить имя переменной
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        # Установить имя переменной
        self._name = value
    
    @property
    def values(self) -> List[float]:
        # Получить список значений
        return self._values.copy()
    
    def add_value(self, value: float) -> None:
        # Добавить значение к списку
        self._values.append(value)
    
    def set_values(self, values: List[float]) -> None:
        # Установить список значений целиком
        self._values = values.copy()
    
    def count(self) -> int:
        # Получить N - количество измерений (неявно)
        return len(self._values)
    
    @abstractmethod
    def get_errors(self) -> List[float]:
        # Получить список ошибок для каждого значения
        # Реализуется в наследниках по-разному
        pass


class VariableMeasured(Variable):
    """
    Класс для измеренных переменных.
    
    Связан с Instrument для получения ошибок.
    Отличается от VariableCalculated тем, что ошибки берутся от прибора.
    """
    
    def __init__(self, name: str, instrument: Optional['Instrument'] = None) -> None:
        super().__init__(name)
        self._instrument: Optional['Instrument'] = instrument
    
    @property
    def instrument(self) -> Optional['Instrument']:
        # Получить связанный прибор
        return self._instrument
    
    @instrument.setter
    def instrument(self, instrument: 'Instrument') -> None:
        # Установить прибор для расчёта ошибок
        self._instrument = instrument
    
    def get_errors(self) -> List[float]:
        # Получить ошибки измерения от прибора
        # Если прибор не установлен - возвращает нулевые ошибки
        if self._instrument is None:
            return [0.0] * len(self._values)
        
        # Ошибка одинаковая для всех измерений (от прибора)
        error = self._instrument.get_error()
        return [error] * len(self._values)


class VariableCalculated(Variable):
    """
    Класс для вычисленных переменных.
    
    Хранит свои собственные ошибки (не связаны с прибором).
    Отличается от VariableMeasured наличием собственного списка errors.
    """
    
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._errors: List[float] = []
    
    @property
    def errors(self) -> List[float]:
        # Получить список ошибок
        return self._errors.copy()
    
    @errors.setter
    def errors(self, errors: List[float]) -> None:
        # Установить список ошибок
        self._errors = errors.copy()
    
    def add_error(self, error: float) -> None:
        # Добавить ошибку для соответствующего значения
        self._errors.append(error)
    
    def get_errors(self) -> List[float]:
        # Получить список ошибок (переопределение абстрактного метода)
        return self._errors.copy()