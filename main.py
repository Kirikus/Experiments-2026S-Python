"""
Точка входа в приложение.
"""

import sys

from PySide6.QtWidgets import QApplication

import subprocess
from pathlib import Path

def compile_ui_files(root_dir: str = ".") -> None:
    """
    Recursively find all *.ui files in the given directory (and subdirectories),
    excluding directories starting with '.', and compile them to ui_*.py using pyside6-uic.

    Args:
        root_dir: Root directory to start searching from (default: current directory)
    """
    root_path = Path(root_dir).resolve()

    print(f"Scanning for .ui files in: {root_path}")
    compiled_count = 0

    for ui_file in root_path.rglob("*.ui"):
        # Skip if any parent directory starts with '.'
        if any(part.startswith('.') for part in ui_file.relative_to(root_path).parts):
            continue

        # Generate output filename: ui_filename.py
        ui_name = ui_file.stem
        output_file = ui_file.with_name(f"ui_{ui_name}.py")

        # Skip if the .py file already exists and is newer than the .ui file
        if output_file.exists() and output_file.stat().st_mtime > ui_file.stat().st_mtime:
            print(f"✓ Skipped (up to date): {ui_file.name}")
            continue

        try:
            print(f"Compiling: {ui_file.name} → {output_file.name}")

            # Run pyside6-uic
            subprocess.run(
                ["pyside6-uic", str(ui_file), "-o", str(output_file)],
                check=True,
                capture_output=True,
                text=True
            )
            compiled_count += 1

        except subprocess.CalledProcessError as e:
            print(f"✗ Error compiling {ui_file.name}: {e.stderr.strip()}")
        except FileNotFoundError:
            print("✗ Error: pyside6-uic command not found. Make sure PySide6 is installed.")
            return
        except Exception as e:
            print(f"✗ Unexpected error with {ui_file.name}: {e}")

    print(f"\nDone! Compiled {compiled_count} .ui file(s).")

if __name__ == "__main__":
    compile_ui_files()

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
