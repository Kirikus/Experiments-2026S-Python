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
        # Прямой доступ к данным, без копирования
        return len(self._experiment._instruments)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        # Возвращает количество столбцов в таблице
        if parent.isValid():
            return 0
        return 3

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        # Возвращает данные для отображения или редактирования в ячейке таблицы
        if not index.isValid():
            return None

        instrument = self._experiment._instruments[index.row()]

        if role == Qt.UserRole:
            return instrument
        if role == Qt.UserRole + 1:
            return "Абсолютная" if isinstance(instrument, InstrumentAbsolute) else "относительная"
        if role not in (Qt.DisplayRole, Qt.EditRole):
            return None

        match index.column():
            case 0:
                return instrument.name
            case 1:
                # Определяем тип погрешности через match-case
                match instrument:
                    case InstrumentAbsolute():
                        return "Абсолютная"
                    case InstrumentRelative():
                        return "Относительная"
                    case _:
                        return "..."
            case 2:
                return str(instrument.error_value)
            case _:
                return None

    def setData(self, index: QModelIndex, value, role: int = Qt.EditRole) -> bool:
        return False

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        # Приборы отображаются только для просмотра.
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

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

    def refresh(self) -> None:
        # Обновляет данные модели (перерисовывает таблицу)
        self.beginResetModel()
        self.endResetModel()
