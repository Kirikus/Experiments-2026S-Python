from PySide6.QtWidgets import QMainWindow, QWidget

from ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    """
    Это GUI в целом, который отображается при запуске.

    Спроектировано с использованием .ui файла:
    1. Создать файл class.ui
    2. Конвертировать файл class.ui в файл ui_class.py с помощью командной строки:
       > pyside6-uic class.ui -o ui_class.py
    3. Определить Класс в python
    4. Создать Ui_Class в Class.__init__()
    5. После этого, вызвать setupUi

    Если сомневаешься — создай C++ Designer Form Class и посмотри на его структуру!
    """

    def __init__(self, parent: QWidget = None) -> None:
        """
        parent: когда parent закрывается, этот виджет тоже закрывается
        """
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)