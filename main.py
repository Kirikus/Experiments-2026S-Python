"""
Точка входа в приложение.
"""

import sys

from PySide6.QtWidgets import QApplication

from gui import MainWindow, MainController


def main() -> None:
    # Создать приложение Qt
    app = QApplication(sys.argv)

    # Создать окно
    mainwindow = MainWindow()

    # Создать контроллер (связывает UI с данными)
    controller = MainController(mainwindow)

    # Показать окно
    mainwindow.show()

    # Запустить цикл событий
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
