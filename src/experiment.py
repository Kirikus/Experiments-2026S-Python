"""
Experiment - класс для хранения всех данных эксперимента.
Хранит Variable, Constant, Instrument.
"""

from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .variable import Variable
    from .constant import Constant
    from .instrument import Instrument


class Experiment:
    """
    Хранит:
    - QList<Variable> - переменные (X, Y, Z...)
    - QList<Constant> - константы (g, π, mean_X...)
    - QList<Instrument> - приборы (линейка, секундомер...)
    """
    
    _instance: Optional['Experiment'] = None
    _initialized: bool = False
    
    def __new__(cls) -> 'Experiment':
        """Реализация паттерна."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        """Инициализация хранилищ данных."""
        if self._initialized:
            return
        
        self._variables: List['Variable'] = []
        self._constants: List['Constant'] = []
        self._instruments: List['Instrument'] = []
        self._initialized = True
    
    @staticmethod
    def get_experiment() -> 'Experiment':
        return Experiment()
    
    #  Методы для работы с Variable 
    def add_variable(self, variable: 'Variable') -> None:
        # Добавить переменную
        self._variables.append(variable)
        
    
    def get_variables(self) -> List['Variable']:
        # Получить список всех переменных
        return self._variables.copy()
        
    
    # Методы для работы с Constant
    def add_constant(self, constant: 'Constant') -> None:
        # Добавить константу в эксперимент
        self._constants.append(constant)
        
    
    def get_constants(self) -> List['Constant']:
        # Получить список всех констант
        return self._constants.copy()
        
    
    # Методы для работы с Instrument 
    def add_instrument(self, instrument: 'Instrument') -> None:
        # Добавить прибор в эксперимент
        self._instruments.append(instrument)
        
    
    def get_instruments(self) -> List['Instrument']:
        # Получить список всех приборов
        return self._instruments.copy()
        