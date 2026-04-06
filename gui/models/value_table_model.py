from __future__ import annotations

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt

from src import VariableCalculated, VariableMeasured


class ValueTableModel(QAbstractTableModel):
    """Модель правой таблицы значений/погрешностей для выбранной сущности."""

    def __init__(self) -> None:
        super().__init__()
        self._entity_type: str | None = None
        self._entity = None
        self._headers = ["N", "Значение", "Погрешность"]

    def clear(self) -> None:
        self.set_entity(None, None)

    def set_entity(self, entity_type: str | None, entity) -> None:
        self.beginResetModel()
        self._entity_type = entity_type
        self._entity = entity
        self.endResetModel()

    def refresh(self) -> None:
        self.beginResetModel()
        self.endResetModel()

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid() or self._entity is None:
            return 0

        if self._entity_type == "variable":
            return self._entity.count() + 1
        return 1

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return 3

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid() or self._entity is None:
            return None

        if role not in (Qt.DisplayRole, Qt.EditRole):
            return None

        row = index.row()
        column = index.column()

        if column == 0:
            return str(row + 1)

        if self._entity_type == "variable":
            return self._variable_data(row, column)

        return None

    def _variable_data(self, row: int, column: int):
        variable = self._entity
        values = variable.values

        if row == len(values):
            return ""
        if row > len(values):
            return None

        if column == 1:
            return str(values[row])

        if column == 2:
            errors = variable.get_errors()
            return str(errors[row] if row < len(errors) else 0.0)

        return None

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid() or self._entity is None:
            return Qt.NoItemFlags

        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        row = index.row()
        column = index.column()

        if self._entity_type != "variable":
            return flags

        variable = self._entity
        values_len = len(variable.values)

        if column == 0:
            return flags

        if isinstance(variable, VariableMeasured):
            if column == 1 and row <= values_len:
                return flags | Qt.ItemIsEditable
            return flags

        if isinstance(variable, VariableCalculated):
            if column == 1 and row <= values_len:
                return flags | Qt.ItemIsEditable
            if column == 2 and row < values_len:
                return flags | Qt.ItemIsEditable

        return flags

    def setData(self, index: QModelIndex, value, role: int = Qt.EditRole) -> bool:
        if role != Qt.EditRole or not index.isValid() or self._entity_type != "variable":
            return False

        variable = self._entity
        row = index.row()
        column = index.column()
        text = str(value).strip()

        if column not in (1, 2):
            return False
        if isinstance(variable, VariableMeasured) and column == 2:
            return False

        values = variable.values
        errors = variable.get_errors()

        try:
            if column == 1:
                if text == "":
                    if row < len(values):
                        values.pop(row)
                        if row < len(errors):
                            errors.pop(row)
                    else:
                        return False
                else:
                    number = float(text.replace(",", "."))
                    if row < len(values):
                        values[row] = number
                    elif row == len(values):
                        values.append(number)
                    else:
                        return False

                variable.set_values(values)
                if isinstance(variable, VariableCalculated):
                    if len(errors) < len(values):
                        errors.extend([0.0] * (len(values) - len(errors)))
                    elif len(errors) > len(values):
                        errors = errors[: len(values)]
                    variable.errors = errors

            elif column == 2 and isinstance(variable, VariableCalculated):
                number = 0.0 if text == "" else float(text.replace(",", "."))

                if row >= len(values):
                    return False

                if len(errors) < len(values):
                    errors.extend([0.0] * (len(values) - len(errors)))
                errors[row] = number
                variable.errors = errors

            self.refresh()
            return True

        except ValueError:
            return False

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
