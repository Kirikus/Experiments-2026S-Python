"""
Experiment — класс для хранения всех данных эксперимента.
Хранит Variable, Constant, Instrument.
"""

from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .variable import Variable
    from .constant import Constant
    from .instrument import Instrument


class Experiment:
    """
    Синглтон-хранилище данных эксперимента.

    Хранит:
    - variables: List[Variable] — переменные (X, Y, Z...)
    - constants: List[Constant] — константы (g, π, mean_X...)
    - instruments: List[Instrument] — приборы (линейка, секундомер...)
    """

    _instance: Optional["Experiment"] = None
    _initialized: bool = False

    def __new__(cls) -> "Experiment":
        """Реализация паттерна Singleton."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Инициализировать хранилища данных (выполняется только один раз)."""
        if self._initialized:
            return

        self._variables: List["Variable"] = []
        self._constants: List["Constant"] = []
        self._instruments: List["Instrument"] = []
        self._initialized = True

    @staticmethod
    def get_experiment() -> "Experiment":
        """Получить единственный экземпляр эксперимента."""
        return Experiment()

    def add_variable(self, variable: "Variable") -> None:
        """Добавить переменную в эксперимент."""
        self._variables.append(variable)

    def get_variables(self) -> List["Variable"]:
        """
        Получить копию списка всех переменных.

        Возвращает копию, чтобы внешний код не мог мутировать внутреннее состояние.
        """
        return self._variables.copy()

    def add_constant(self, constant: "Constant") -> None:
        """Добавить константу в эксперимент."""
        self._constants.append(constant)

    def get_constants(self) -> List["Constant"]:
        """
        Получить копию списка всех констант.

        Возвращает копию, чтобы внешний код не мог мутировать внутреннее состояние.
        """
        return self._constants.copy()

    def add_instrument(self, instrument: "Instrument") -> None:
        """Добавить прибор в эксперимент."""
        self._instruments.append(instrument)

    def get_instruments(self) -> List["Instrument"]:
        """
        Получить копию списка всех приборов.

        Возвращает копию, чтобы внешний код не мог мутировать внутреннее состояние.
        """
        return self._instruments.copy()
