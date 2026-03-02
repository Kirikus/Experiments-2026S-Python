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
    - index,value,error (для VariableCalculated)
    - index,value (для VariableMeasured - ошибки берутся от прибора)
    """
    
    @staticmethod
    def save_variable(variable: 'Variable', filepath: Path) -> None:
        # Сохранить переменную в CSV файл
        values = variable.values
        errors = variable.get_errors()
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Заголовок
            if errors:
                writer.writerow(['index', 'value', 'error'])
            else:
                writer.writerow(['index', 'value'])
            
            # Данные
            for i, val in enumerate(values):
                if errors:
                    writer.writerow([i, val, errors[i]])
                else:
                    writer.writerow([i, val])
    
    @staticmethod
    def load_variable(variable: 'Variable', filepath: Path) -> None:
        # Загрузить переменную из CSV файла
        values: List[float] = []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # Получить значение
                val = float(row['value'])
                values.append(val)
                
                # Если есть колонка error и переменная вычисленная
                if 'error' in row and hasattr(variable, 'add_error'):
                    err = float(row['error'])
                    variable.add_error(err)
        
        # Установить значения
        variable.set_values(values)
    
    @staticmethod
    def get_csv_path(variable_name: str, experiment_dir: Path) -> Path:
        # Получить путь к CSV файлу для переменной
        # Сохраняем в подпапку data/
        data_dir = experiment_dir / 'data'
        data_dir.mkdir(exist_ok=True)
        return data_dir / f"{variable_name}.csv"