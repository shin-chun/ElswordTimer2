import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    # manager = TimerManager()
    # manager.add_timer("Fireball", 10, position=(100, 100))
    # manager.start_timer("Fireball", CooldownState.SELECTED)
    #
    # manager.add_timer("Ice Shield", 15, position=(250, 100))
    # manager.start_timer("Ice Shield", CooldownState.LOCKED)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()