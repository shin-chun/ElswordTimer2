import unittest

from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import QTimer, Qt

class CountdownWindow(QWidget):
    def __init__(self, name, duration):
        super().__init__()
        self.name = name
        self.remaining = duration

        self.setWindowTitle(name)
        self.setFixedSize(200, 100)

        self.label = QLabel(f"{name} 倒數 {self.remaining} 秒")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_countdown)
        self.timer.start(1000)

        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.raise_()
        self.activateWindow()

    def update_countdown(self):
        self.remaining -= 1
        if self.remaining <= 0:
            self.close()
        else:
            self.label.setText(f"{self.name} 倒數 {self.remaining} 秒")

app = QApplication([])
window = CountdownWindow("測試技能", 5)
window.show()
app.exec()