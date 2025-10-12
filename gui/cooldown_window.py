from PySide6.QtGui import QFontMetrics

from settings.common import *
from enum import Enum

class CooldownState(Enum):
    IDLE = 0
    SELECTED = 1
    LOCKED = 2
    TRIGGERED = 3

STATE_COLOR_MAP = {
    CooldownState.IDLE: "white",
    CooldownState.SELECTED: "yellow",
    CooldownState.LOCKED: "red",
    CooldownState.TRIGGERED: "gray"
}


class CooldownWindow(QWidget):
    def __init__(self, name: str, cooldown_seconds: int):
        super().__init__()
        self.name = name
        self.cooldown_seconds = cooldown_seconds
        self.remaining = cooldown_seconds
        self.state = CooldownState.IDLE

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        font = QFont("Arial", 14)
        font.setBold(True)
        self.label.setFont(font)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setFixedHeight(50)

    def set_state(self, state: CooldownState):
        self.state = state
        self.update_label()

    def set_remaining(self, seconds: int):
        self.remaining = seconds
        self.update_label()

    def decrement(self):
        self.remaining -= 1
        self.update_label()

    def is_expired(self) -> bool:
        return self.remaining <= 0

    def update_label(self):
        color = STATE_COLOR_MAP.get(self.state, "white")
        text = f"{self.name}：{self.remaining}s"
        self.label.setText(text)
        self.label.setStyleSheet(f"background-color: {color}; border: 1px solid black; color: black;")
        self.adjust_width(text)

    def adjust_width(self, text: str):
        font = self.label.font()
        metrics = QFontMetrics(font)
        text_width = metrics.horizontalAdvance(text)
        padding = 40
        total_width = text_width + padding
        self.setFixedWidth(total_width)
        self.label.setFixedWidth(total_width - 20)

    def get_position(self) -> tuple[int, int]:
        pos = self.pos()
        return (pos.x(), pos.y())
