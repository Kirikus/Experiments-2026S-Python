"""
CSV handler for Variable values storage.
Данные Variable::values обязаны быть в .csv
"""

import csv
from pathlib import Path
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..variable import Variable


class CSVHandler:
    """
    Класс для сохранения и загрузки значений переменных в CSV.

    Формат CSV:
    - index,value,error

    Если значение ячейки отсутствует, в CSV записывается одиночный пробел.
    """

    _MISSING_CELL = " "

    @staticmethod
    def save_variable(variable: "Variable", filepath: Path) -> None:
        """Сохранить переменную в CSV-файл по табличному контракту ТЗ."""
        values = variable.values
        errors = variable.get_errors()

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            # Заголовок всегда фиксированный: графы таблицы шага расчёта
            writer.writerow(["index", "value", "error"])

            # Данные шага расчёта
            for i, val in enumerate(values):
                error_cell = (
                    str(errors[i])
                    if i < len(errors)
                    else CSVHandler._MISSING_CELL
                )
                writer.writerow([i, val, error_cell])

    @staticmethod
    def load_variable(variable: "Variable", filepath: Path) -> None:
        """Загрузить переменную из CSV-файла."""
        values: List[float] = []

        if hasattr(variable, "errors"):
            variable.errors = []

        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                value_cell = (row.get("value") or "").strip()
                if value_cell in {"", CSVHandler._MISSING_CELL}:
                    continue

                val = float(value_cell)
                values.append(val)

                error_cell = (row.get("error") or "").strip()
                if (
                    hasattr(variable, "add_error")
                    and error_cell not in {"", CSVHandler._MISSING_CELL}
                ):
                    err = float(error_cell)
                    variable.add_error(err)

        variable.set_values(values)

    @staticmethod
    def get_csv_path(variable_name: str, experiment_dir: Path) -> Path:
        """Получить путь к CSV-файлу для переменной в подпапке data/."""
        data_dir = experiment_dir / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir / f"{variable_name}.csv"
