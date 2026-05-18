from PySide6.QtCore import QLocale, Qt, QModelIndex
from PySide6.QtGui import QDoubleValidator, QPainter, QColor
from PySide6.QtWidgets import QComboBox, QLineEdit, QStyledItemDelegate, QWidget, QSpinBox, QColorDialog, QStyleOptionViewItem


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
class ColorDelegate(QStyledItemDelegate):
    def paint(
        self,
        painter: QPainter,
        option: "QStyleOptionViewItem",
        index: QModelIndex,
    ) -> None:
        self.draw_background(painter, option, index)
        super().paint(painter, option, index)

    def createEditor(
        self,
        parent: QWidget,
        option: "QStyleOptionViewItem",
        index: QModelIndex,
    ) -> QWidget:
        dialog = QColorDialog(parent)
        return dialog

    def setModelData(self, editor: QWidget, model, index: QModelIndex) -> None:
        color_dialog = editor
        color = color_dialog.selectedColor()
        model.setData(index, color.name().upper(), Qt.EditRole)

    def draw_background(
        self,
        painter: QPainter,
        option: "QStyleOptionViewItem",
        index: QModelIndex,
    ) -> None:
        value = index.model().data(index, Qt.EditRole)
        color = value if isinstance(value, QColor) else QColor(str(value))

        if color.isValid():
            painter.fillRect(option.rect, color)
        else:
            super().paint(painter, option, index)


class ComboBoxDelegate(QStyledItemDelegate):
    def __init__(self, options, parent = None):
        super().__init__(parent)
        self.options = options

    def createEditor(self, parent: QWidget, option, index) -> QWidget:
        """Создаёт редактор — QSpinBox для редактирования целых чисел."""
        editor = QComboBox(parent)
        editor.addItems(self.options)
        editor.setCurrentIndex(0)
        editor.setFrame(False)
        return editor

    def setEditorData(self, editor: QWidget, index) -> None:
        """Устанавливает данные из модели в редактор."""
        value = index.model().data(index, Qt.EditRole)
        index = editor.findText(value)

        if index != -1:
            editor.setCurrentIndex(index)
        else:
            editor.setCurrentIndex(0)  # значение по умолч

    def setModelData(self, editor: QWidget, model, index) -> None:
        """Сохраняет данные из редактора в модель."""
        combo_box = editor
        combo_box.currentText()
        value = combo_box.currentText()
        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, editor: QWidget, option, index) -> None:
        """Обновляет геометрию редактора согласно параметрам представления."""
        editor.setGeometry(option.rect)


class SpinBoxDelegate(QStyledItemDelegate):
    def __init__(self, min, max, parent=None):
        super().__init__(parent)
        self.min = min
        self.max = max

    def createEditor(self, parent: QWidget, option, index) -> QWidget:
        """Создаёт редактор — QSpinBox для редактирования целых чисел."""
        editor = QSpinBox(parent)
        editor.setFrame(False)
        editor.setMinimum(self.min)
        editor.setMaximum(self.max)
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