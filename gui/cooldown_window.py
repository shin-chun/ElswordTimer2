from settings.common import *
from enum import Enum

class CooldownState(Enum):
    EMPTY = 0
    SELECTED = 1
    LOCKED = 2
    TRIGGERED = 3

STATE_COLOR_MAP = {
    CooldownState.EMPTY: "white",
    CooldownState.SELECTED: "yellow",
    CooldownState.LOCKED: "red",
    CooldownState.TRIGGERED: "gray"
}

class CooldownWindow(QWidget):
    def __init__(self, name: str, cooldown_seconds: int):
        super().__init__(None)  # 確保是獨立視窗
        self.name = name
        self.cooldown_seconds = cooldown_seconds
        self.remaining = cooldown_seconds
        self.state = CooldownState.EMPTY
        self.drag_position = None  # 拖曳起始點

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFixedSize(120, 60)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_countdown)

        self.update_label()


    def start(self, state: CooldownState):
        self.state = state
        self.remaining = self.cooldown_seconds
        self.update_label()
        self.timer.start(1000)

    def update_countdown(self):
        self.remaining -= 1
        if self.remaining <= 0:
            self.timer.stop()
            self.state = CooldownState.TRIGGERED
        self.update_label()

    def update_label(self):
        color = STATE_COLOR_MAP.get(self.state, "white")
        self.label.setStyleSheet(f"background-color: {color}; border: 1px solid black;")
        self.label.setText(f"{self.name}：{self.remaining}s")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton and self.drag_position:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.drag_position = None
        event.accept()
