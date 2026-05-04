from __future__ import annotations
from ui_mainwindow import Ui_MainWindow
from PySide6.QtCore import QLocale, Qt
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import QComboBox, QLineEdit, QStyledItemDelegate, QWidget, QSpinBox


class FloatValueDelegate(QStyledItemDelegate):
    """Делегат редактирования вещественных чисел с валидацией."""

    def __init__(
        self,
        parent: QWidget | None = None,
        *,
        bottom: float = -1e308,
        top: float = 1e308,
        decimals: int = 12,
    ) -> None:
        super().__init__(parent)
        self._bottom = bottom
        self._top = top
        self._decimals = decimals

    def createEditor(self, parent: QWidget, option, index) -> QWidget:
        editor = QLineEdit(parent)
        validator = QDoubleValidator(self._bottom, self._top, self._decimals, editor)
        validator.setNotation(QDoubleValidator.StandardNotation)
        validator.setLocale(QLocale.system())
        editor.setValidator(validator)
        return editor

    def setEditorData(self, editor: QWidget, index) -> None:
        if not isinstance(editor, QLineEdit):
            return
        value = index.model().data(index, Qt.EditRole)
        editor.setText("" if value is None else str(value))

    def setModelData(self, editor: QWidget, model, index) -> None:
        if not isinstance(editor, QLineEdit):
            return
        text = editor.text().strip()
        # Сохраняем единый формат десятичного разделителя перед записью в модель.
        model.setData(index, text.replace(",", "."), Qt.EditRole)


class InstrumentTypeDelegate(QStyledItemDelegate):
    """Делегат выбора типа погрешности прибора через выпадающий список."""

    _OPTIONS = ["Абсолютная", "Относительная"]

    def createEditor(self, parent: QWidget, option, index) -> QWidget:
        editor = QComboBox(parent)
        editor.addItems(self._OPTIONS)
        return editor

    def setEditorData(self, editor: QWidget, index) -> None:
        if not isinstance(editor, QComboBox):
            return
        current = str(index.model().data(index, Qt.EditRole) or "").strip().lower()
        for row, option in enumerate(self._OPTIONS):
            if option.lower() == current:
                editor.setCurrentIndex(row)
                return

    def setModelData(self, editor: QWidget, model, index) -> None:
        if not isinstance(editor, QComboBox):
            return
        model.setData(index, editor.currentText(), Qt.EditRole)



class SpinBoxDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent: QWidget, option, index) -> QWidget:
        """Создаёт редактор — QSpinBox для редактирования целых чисел."""
        editor = QSpinBox(parent)
        editor.setFrame(False)
        editor.setMinimum(0)
        editor.setMaximum(100)
        return editor

    def setEditorData(self, editor: QWidget, index) -> None:
        """Устанавливает данные из модели в редактор."""
        value = index.model().data(index, Qt.EditRole)
        try:
            editor.setValue(int(value))
        except (ValueError, TypeError):
            editor.setValue(0)  # значение по умолчанию при ошибке

    def setModelData(self, editor: QWidget, model, index) -> None:
        """Сохраняет данные из редактора в модель."""
        spin_box = editor
        spin_box.interpretText()
        value = spin_box.value()
        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, editor: QWidget, option, index) -> None:
        """Обновляет геометрию редактора согласно параметрам представления."""
        editor.setGeometry(option.rect)
