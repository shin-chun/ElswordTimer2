from settings.common import QWidget, Qt, QLabel, QFont

class CountdownWindow(QWidget):
    def __init__(self, duration_sec=10):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(200, 100)

        # 設定字型
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)

        # 建立 label
        self.label = QLabel("倒數開始", self)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setGeometry(0, 0, 200, 100)
        self.label.setStyleSheet("color: black; background-color: rgba(255, 255, 255, 180); border-radius: 10px;")

        # 初始狀態
        # self.remaining = duration_sec
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(CooldownManager.update_countdown)
        # self.timer.start(1000)
        #
        # CooldownManager.update_label()
