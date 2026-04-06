from __future__ import annotations

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt

from src import Constant


class ConstantDetailTableModel(QAbstractTableModel):
    """Read-only model for a single selected constant."""

    def __init__(self) -> None:
        super().__init__()
        self._constant: Constant | None = None
        self._headers = ["Имя", "Значение", "Погрешность", "Readonly"]

    def set_constant(self, constant: Constant | None) -> None:
        self.beginResetModel()
        self._constant = constant
        self.endResetModel()

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid() or self._constant is None:
            return 0
        return 1

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return 4

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid() or self._constant is None:
            return None

        if role != Qt.DisplayRole:
            return None

        match index.column():
            case 0:
                return self._constant.name
            case 1:
                return str(self._constant.value)
            case 2:
                return str(self._constant.error)
            case 3:
                return "Да" if self._constant.readonly else "Нет"
            case _:
                return None

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(
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
