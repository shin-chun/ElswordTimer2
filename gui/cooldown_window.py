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
        super().__init__()  # 確保是獨立視窗
        self.name = name
        self.cooldown_seconds = cooldown_seconds
        self.remaining = cooldown_seconds
        self.state = CooldownState.IDLE
        self.drag_position = None  # 拖曳起始點

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        font = QFont("Arial", 14)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet("color: black;")
        self.setFixedHeight(80)  # 或你想要的高度

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.timer = QTimer(self)
        print(f"🔗 嘗試連接 QTimer：{self.name}")
        try:
            self.timer.timeout.connect(self.update_countdown)
            print(f"✅ QTimer timeout 成功連接：{self.name}")
        except Exception as e:
            print(f"❌ QTimer 連接失敗：{e}")

        self.update_label()
        self.resize(150, 80)  # 或者根據 label 大小自動調整

    def set_state(self, state: CooldownState):
        self.state = state
        self.update_label()

    def start(self, state: CooldownState):
        self.state = state
        self.remaining = self.cooldown_seconds
        self.update_label()

        if not self.timer.isActive():
            self.timer.timeout.connect(self.update_countdown)
            print(f"🔗 已連接 timeout → update_countdown：{self.name}")

        self.timer.start(1000)
        QTimer.singleShot(0, lambda: print(f"✅ QTimer 啟動狀態：{self.name} → {self.timer.isActive()}"))

    def update_countdown(self):
        print(f"📉 倒數觸發：{self.name} → {self.remaining}s")
        if self.remaining <= 1:
            self.remaining = 0
            self.timer.stop()
            self.state = CooldownState.IDLE
        else:
            self.remaining -= 1

        self.update_label()

    def reset_display(self, duration: int = None):
        if duration is not None:
            self.cooldown_seconds = duration
        self.remaining = self.cooldown_seconds
        self.state = CooldownState.IDLE
        self.timer.stop()
        self.update_label()

    def update_duration(self, new_duration: int):
        self.cooldown_seconds = new_duration
        self.remaining = new_duration
        self.update_label()

    def update_label(self):
        print(f"🎨 更新 label：{self.name} → {self.remaining}s，顏色：{STATE_COLOR_MAP.get(self.state)}")
        color = STATE_COLOR_MAP.get(self.state, "white")
        self.label.setStyleSheet(f"background-color: {color}; border: 1px solid black; color: black;")
        text = f"{self.name}：{self.remaining}s"
        self.label.setText(text)

        self.adjust_width(text)

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

        # ✅ 即時更新位置
        if hasattr(self, "on_position_changed"):
            self.on_position_changed(self.name, self.get_position())

    def adjust_width(self, text: str):
        font = self.label.font()
        metrics = QFontMetrics(font)
        text_width = metrics.horizontalAdvance(text)

        padding = 40  # 額外空間
        total_width = text_width + padding

        self.setFixedWidth(total_width)
        self.label.setFixedWidth(total_width - 20)

    def get_position(self) -> tuple[int, int]:
        pos = self.pos()
        return (pos.x(), pos.y())