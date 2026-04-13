from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem


class ExperimentTreeController:
    """Отдельный контроллер дерева сущностей эксперимента."""

    def __init__(self, tree_widget: QTreeWidget) -> None:
        self.tree_widget = tree_widget
        self._vars_item: QTreeWidgetItem | None = None
        self._consts_item: QTreeWidgetItem | None = None
        self._insts_item: QTreeWidgetItem | None = None

    def setup(self) -> None:
        self._vars_item = QTreeWidgetItem(["Переменные"])
        self._consts_item = QTreeWidgetItem(["Константы"])
        self._insts_item = QTreeWidgetItem(["Приборы"])

        self.tree_widget.addTopLevelItem(self._vars_item)
        self.tree_widget.addTopLevelItem(self._consts_item)
        self.tree_widget.addTopLevelItem(self._insts_item)
        self.tree_widget.expandAll()

    def refresh(self, experiment) -> None:
        for item in (self._vars_item, self._consts_item, self._insts_item):
            item.takeChildren()

        for var in experiment.get_variables():
            variable_item = QTreeWidgetItem([var.name])
            variable_item.setData(0, Qt.UserRole, ("variable", var))
            self._vars_item.addChild(variable_item)

        for const in experiment.get_constants():
            constant_item = QTreeWidgetItem([const.name])
            constant_item.setData(0, Qt.UserRole, ("constant", const))
            self._consts_item.addChild(constant_item)

        for inst in experiment.get_instruments():
            instrument_item = QTreeWidgetItem([inst.name])
            instrument_item.setData(0, Qt.UserRole, ("instrument", inst))
            self._insts_item.addChild(instrument_item)

        self.tree_widget.expandAll()

    @staticmethod
    def resolve_entity(item: QTreeWidgetItem):
        return item.data(0, Qt.UserRole)
