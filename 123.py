from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import QTimer

class TimerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.elapsed = 0

        self.label = QLabel("Elapsed: 0s")
        self.button = QPushButton("Start Timer")
        self.button.clicked.connect(self.start_timer)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_time)

    def start_timer(self):
        if not self.timer.isActive():
            self.timer.start()
            self.button.setText("Timer Running...")

    def update_time(self):
        self.elapsed += 1
        self.label.setText(f"Elapsed: {self.elapsed}s")

if __name__ == "__main__":
    app = QApplication([])
    widget = TimerWidget()
    widget.resize(300, 120)
    widget.show()
    app.exec()