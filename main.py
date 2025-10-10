import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
from gui.cooldown_window import CooldownWindow, CooldownState
from timer.manager import TimerManager


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    manager = TimerManager()
    manager.add_timer("Fireball", 10, position=(100, 100))
    manager.start_timer("Fireball", CooldownState.SELECTED)

    manager.add_timer("Ice Shield", 15, position=(250, 100))
    manager.start_timer("Ice Shield", CooldownState.LOCKED)
    window.show()
    sys.exit(app.exec())
    # app = QApplication(sys.argv)
    # manager = TimerManager()
    # manager.add_timer("Fireball", 10, position=(500, 300))
    # manager.start_timer("Fireball", CooldownState.SELECTED)
    # sys.exit(app.exec())



if __name__ == "__main__":
    main()