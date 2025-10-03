from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QPushButton, QLabel
from timer.manager import TimerManager

class SkillEditor(QWidget):
    def __init__(self, timer_manager: TimerManager):
        super().__init__()
        self.timer_manager = timer_manager
        self.setWindowTitle("技能設定")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("技能名稱")

        self.event_input = QLineEdit()
        self.event_input.setPlaceholderText("第一鍵（事件鍵）")

        self.lock_input = QLineEdit()
        self.lock_input.setPlaceholderText("第二鍵（鎖定鍵）")

        self.trigger_input = QLineEdit()
        self.trigger_input.setPlaceholderText("第三鍵（觸發鍵）")

        self.duration_input = QSpinBox()
        self.duration_input.setRange(1, 300)
        self.duration_input.setValue(30)
        self.duration_input.setPrefix("倒數秒數：")

        self.window_input = QDoubleSpinBox()
        self.window_input.setRange(0.1, 10.0)
        self.window_input.setValue(2.0)
        self.window_input.setPrefix("時間窗：")

        self.add_button = QPushButton("新增技能")
        self.add_button.clicked.connect(self.add_skill)

        layout.addWidget(QLabel("技能設定"))
        layout.addWidget(self.name_input)
        layout.addWidget(self.event_input)
        layout.addWidget(self.lock_input)
        layout.addWidget(self.trigger_input)
        layout.addWidget(self.duration_input)
        layout.addWidget(self.window_input)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def add_skill(self):
        name = self.name_input.text().strip()
        event = self.event_input.text().strip() or None
        lock = self.lock_input.text().strip() or None
        trigger = self.trigger_input.text().strip()

        duration = self.duration_input.value()
        window = self.window_input.value()

        if not name or not trigger:
            print("❌ 技能名稱與觸發鍵必填")
            return

        keys = (event, lock, trigger)
        self.timer_manager.add_timer(name=name, keys=keys, duration=duration, window=window)
        print(f"✅ 技能 [{name}] 已新增：{keys}，倒數 {duration}s，時間窗 {window}s")