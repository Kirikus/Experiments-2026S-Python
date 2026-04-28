"""Базовый класс для Widget-графиков для UI вкладок."""

from __future__ import annotations

from PySide6.QtWidgets import QWidget
from gui.views.ui_plot_base import Ui_PlotBase


class PlotBase(QWidget):
    """Базовый класс для ui графиков, работающих с данными Experiment."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_PlotBase()
        self.ui.setupUi(self)
