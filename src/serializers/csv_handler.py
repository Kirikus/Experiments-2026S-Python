"""
CSV handler for Variable values storage.
Данные Variable::values обязаны быть в .csv
"""

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..variable import Variable


class CSVHandler:
    """
    Класс для сохранения и загрузки значений переменных в CSV.

    Формат CSV:
    - index,value,error

    Если значение ячейки отсутствует, в CSV записывается одиночный пробел.
    """

    @staticmethod
    def save_variable(variable: "Variable", filepath: Path) -> None:
        """Сохранить переменную в CSV-файл через собственный метод Variable."""
        variable.write_csv(filepath)

    @staticmethod
    def load_variable(variable: "Variable", filepath: Path, measurement_type: str = None) -> None:
        """
        Загрузить переменную из CSV-файла.
        Если measurement_type указан, фильтрует строки по этому типу.
        """
        variable.measurement_type = measurement_type
        variable.read_csv(filepath)

    @staticmethod
    def get_csv_path(variable_name: str, experiment_dir: Path) -> Path:
        """Получить путь к CSV-файлу для переменной в подпапке data/."""
        data_dir = experiment_dir / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir / f"{variable_name}.csv"
