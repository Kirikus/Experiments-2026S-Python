from __future__ import annotations

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt

from src import Experiment, InstrumentAbsolute, InstrumentRelative


class InstrumentTableModel(QAbstractTableModel):
    # Модель таблицы для отображения и редактирования приборов в эксперименте
    def __init__(self, experiment: Experiment) -> None:
        # Инициализация модели, установка эксперимента и заголовков столбцов
        super().__init__()
        self._experiment = experiment
        self._headers = ["Имя", "Тип погрешности", "Величина"]

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        # Возвращает количество строк (приборов) в таблице
        if parent.isValid():
            return 0
        return len(self._experiment.get_instruments())

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        # Возвращает количество столбцов в таблице
        if parent.isValid():
            return 0
        return 3

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        # Возвращает данные для отображения или редактирования в ячейке таблицы
        if not index.isValid() or role not in (Qt.DisplayRole, Qt.EditRole):
            return None

        inst = self._experiment.get_instruments()[index.row()]
        if index.column() == 0:
            return inst.name
        if index.column() == 1:
            return "absolute" if isinstance(inst, InstrumentAbsolute) else "relative"
        if index.column() == 2:
            return str(inst.error_value)
        return None

    def setData(self, index: QModelIndex, value, role: int = Qt.EditRole) -> bool:
        # Устанавливает новые данные в ячейку таблицы (редактирование)
        if not index.isValid() or role != Qt.EditRole:
            return False

        instruments = self._experiment.get_instruments()
        inst = instruments[index.row()]

        if index.column() == 0:
            inst.name = str(value)
        elif index.column() == 1:
            value_str = str(value).strip().lower()
            if value_str in {"absolute", "абсолютная", "abs"}:
                if not isinstance(inst, InstrumentAbsolute):
                    self._experiment._instruments[index.row()] = InstrumentAbsolute(
                        inst.name, inst.error_value
                    )
            elif value_str in {"relative", "относительная", "rel"}:
                if not isinstance(inst, InstrumentRelative):
                    self._experiment._instruments[index.row()] = InstrumentRelative(
                        inst.name, inst.error_value
                    )
            else:
                return False
        elif index.column() == 2:
            try:
                inst.error_value = float(value)
            except (TypeError, ValueError):
                return False
        else:
            return False

        self.dataChanged.emit(index, index, [Qt.DisplayRole, Qt.EditRole])
        return True

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        # Возвращает флаги для ячейки (разрешает редактирование)
        return Qt.ItemIsEditable | super().flags(index)

    def headerData(
        # Возвращает заголовки столбцов или строк
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.DisplayRole,
    ):
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal and 0 <= section < len(self._headers):
            return self._headers[section]
        return str(section + 1)

    def setHeaderData(
        # Позволяет редактировать заголовки столбцов
        self,
        section: int,
        orientation: Qt.Orientation,
        value,
        role: int = Qt.EditRole,
    ) -> bool:
        if orientation != Qt.Horizontal or role != Qt.EditRole:
            return False
        if not 0 <= section < len(self._headers):
            return False

        self._headers[section] = str(value)
        self.headerDataChanged.emit(orientation, section, section)
        return True

    def refresh(self) -> None:
        # Обновляет данные модели (перерисовывает таблицу)
        self.beginResetModel()
        self.endResetModel()
