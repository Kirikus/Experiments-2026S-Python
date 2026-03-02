"""
JSON serializer for Experiment metadata.
Соответствует ТЗ: JSON/TOML для метаданных + CSV для данных Variable
"""

import json
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..experiment import Experiment
    from ..variable import Variable, VariableMeasured, VariableCalculated
    from ..instrument import Instrument, InstrumentAbsolute, InstrumentRelative
    from ..constant import Constant


class ExperimentSerializer:
    """
    Класс для сериализации/десериализации Experiment в JSON.
    
    Формат:
    - JSON содержит метаданные (имена, типы, ссылки)
    - Данные Variable хранятся в отдельных CSV (через CSVHandler)
    """
    
    def __init__(self, experiment: 'Experiment') -> None:
        # Инициализировать сериализатор с экспериментом
        self._experiment = experiment
    
    def save(self, filepath: Path, data_dir: Path) -> None:
        # Сохранить эксперимент в JSON + CSV
        from .csv_handler import CSVHandler
        
        data = {
            'experiment': {
                'variables': [],
                'constants': [],
                'instruments': []
            }
        }
        
        # Сохранить переменные
        for var in self._experiment.get_variables():
            var_data = {
                'name': var.name,
                'type': self._get_variable_type(var),
                'csv_file': None
            }
            
            # Сохранить данные в CSV
            csv_path = CSVHandler.get_csv_path(var.name, data_dir)
            CSVHandler.save_variable(var, csv_path)
            var_data['csv_file'] = str(csv_path.relative_to(data_dir.parent))
            
            # Добавить ссылку на прибор для измеренных
            if isinstance(var, VariableMeasured) and var.instrument:
                var_data['instrument_name'] = var.instrument.name
            
            data['experiment']['variables'].append(var_data)
        
        # Сохранить константы
        for const in self._experiment.get_constants():
            data['experiment']['constants'].append({
                'name': const.name,
                'value': const.value,
                'error': const.error,
                'readonly': const.readonly
            })
        
        # Сохранить приборы
        for inst in self._experiment.get_instruments():
            inst_data = {
                'name': inst.name,
                'type': self._get_instrument_type(inst),
                'error_value': inst.error_value
            }
            data['experiment']['instruments'].append(inst_data)
        
        # Записать JSON
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def load(self, filepath: Path) -> None:
        # Загрузить эксперимент из JSON + CSV
        from ..variable import VariableMeasured, VariableCalculated
        from ..instrument import InstrumentAbsolute, InstrumentRelative
        from ..constant import Constant
        from .csv_handler import CSVHandler
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        exp_data = data['experiment']
        base_dir = filepath.parent
        
        # Загрузить приборы (сначала, т.к. переменные ссылаются на них)
        instruments = {}
        for inst_data in exp_data['instruments']:
            inst = self._create_instrument(inst_data)
            instruments[inst.name] = inst
            self._experiment.add_instrument(inst)
        
        # Загрузить константы
        for const_data in exp_data['constants']:
            const = Constant(
                name=const_data['name'],
                value=const_data['value'],
                error=const_data['error'],
                readonly=const_data['readonly']
            )
            self._experiment.add_constant(const)
        
        # Загрузить переменные
        for var_data in exp_data['variables']:
            var = self._create_variable(var_data, instruments)
            
            # Загрузить данные из CSV
            csv_path = base_dir / var_data['csv_file']
            CSVHandler.load_variable(var, csv_path)
            
            self._experiment.add_variable(var)
    
    def _get_variable_type(self, var: 'Variable') -> str:
        # Получить строковой тип переменной
        from ..variable import VariableMeasured, VariableCalculated
        
        if isinstance(var, VariableMeasured):
            return 'measured'
        elif isinstance(var, VariableCalculated):
            return 'calculated'
        return 'unknown'
    
    def _get_instrument_type(self, inst: 'Instrument') -> str:
        # Получить строковой тип прибора
        from ..instrument import InstrumentAbsolute, InstrumentRelative
        
        if isinstance(inst, InstrumentAbsolute):
            return 'absolute'
        elif isinstance(inst, InstrumentRelative):
            return 'relative'
        return 'unknown'
    
    def _create_instrument(self, data: dict) -> 'Instrument':
        # Создать прибор из данных JSON
        from ..instrument import InstrumentAbsolute, InstrumentRelative
        
        name = data['name']
        error_value = data['error_value']
        
        if data['type'] == 'absolute':
            return InstrumentAbsolute(name, error_value)
        elif data['type'] == 'relative':
            return InstrumentRelative(name, error_value)
        else:
            raise ValueError(f"Unknown instrument type: {data['type']}")
    
    def _create_variable(self, data: dict, instruments: dict) -> 'Variable':
        # Создать переменную из данных JSON
        from ..variable import VariableMeasured, VariableCalculated
        
        name = data['name']
        var_type = data['type']
        
        if var_type == 'measured':
            inst_name = data.get('instrument_name')
            instrument = instruments.get(inst_name) if inst_name else None
            return VariableMeasured(name, instrument)
        elif var_type == 'calculated':
            return VariableCalculated(name)
        else:
            raise ValueError(f"Unknown variable type: {var_type}")