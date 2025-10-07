from settings.common import *

class CooldownAnimator:
    def __init__(self, label: QLabel, duration: int, on_finish=None):
        self.label = label
        self.duration = duration
        self.remaining = duration
        self.timer = QTimer()
        self.timer.setInterval(1000)  # 每秒更新
        self.timer.timeout.connect(self.update)
        self.on_finish = on_finish

    def start(self):
        self.remaining = self.duration
        self.label.setText(f"⏳ 倒數中：{self.remaining} 秒")
        self.timer.start()

    def update(self):
        self.remaining -= 1
        if self.remaining <= 0:
            self.timer.stop()
            self.label.setText("✅ 冷卻結束")
            if self.on_finish:
                self.on_finish()
        else:
            self.label.setText(f"⏳ 倒數中：{self.remaining} 秒")


# class CountdownWindow(QWidget):
#     def __init__(self, duration_sec=10):
#         super().__init__()
#         self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
#         self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
#         self.setFixedSize(200, 100)
#
#         # 設定字型
#         font = QFont()
#         font.setPointSize(12)
#         font.setBold(True)
#
#         # 建立 label
#         self.label = QLabel("倒數開始", self)
#         self.label.setFont(font)
#         self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.label.setGeometry(0, 0, 200, 100)
#         self.label.setStyleSheet("color: black; background-color: rgba(255, 255, 255, 180); border-radius: 10px;")
#
#         # 初始狀態
#         # self.remaining = duration_sec
#         # self.timer = QTimer(self)
#         # self.timer.timeout.connect(CooldownManager.update_countdown)
#         # self.timer.start(1000)
#         #
#         # CooldownManager.update_label()
