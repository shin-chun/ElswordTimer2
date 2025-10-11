import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
from listen_hotkey.hotkey_listener import HotkeyListener


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()