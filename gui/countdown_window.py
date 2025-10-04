from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QListWidget,
                               QVBoxLayout, QPushButton, QHBoxLayout, )
from PySide6.QtCore import QTimer, Qt


class CountdownWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("技能計時器控制台")
        self.setMinimumSize(600, 400)

        # 計時器列表（可選取）
        self.timer_list = QListWidget()

        # 操作按鈕
        self.add_btn = QPushButton("新增計時器")
        self.edit_btn = QPushButton("編輯選取")
        self.delete_btn = QPushButton("刪除選取")
        self.reset_btn = QPushButton("時間重置")
        self.save_btn = QPushButton("儲存設定")
        self.load_btn = QPushButton("匯入設定")

        # 總開關
        self.toggle_all_btn = QPushButton("🟢 計時器已啟用")  # 點擊後切換狀態

        # 排版
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.reset_btn)

        config_layout = QHBoxLayout()
        config_layout.addWidget(self.save_btn)
        config_layout.addWidget(self.load_btn)
        config_layout.addStretch()
        config_layout.addWidget(self.toggle_all_btn)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.timer_list)
        main_layout.addLayout(btn_layout)
        main_layout.addLayout(config_layout)

        self.setLayout(main_layout)

        # 事件綁定（可後續補上）
        self.add_btn.clicked.connect(self.add_timer)
        self.edit_btn.clicked.connect(self.edit_selected)
        self.delete_btn.clicked.connect(self.delete_selected)
        self.reset_btn.clicked.connect(self.reset_selected)
        self.save_btn.clicked.connect(self.save_config)
        self.load_btn.clicked.connect(self.load_config)
        self.toggle_all_btn.clicked.connect(self.toggle_all_timers)

    def update_countdown(self):
        self.remaining -= 1
        if self.remaining <= 0:
            self.close()
        else:
            self.label.setText(f"{self.name} 倒數 {self.remaining} 秒")

    def toggle_all_timers(self):
        self.all_enabled = not self.all_enabled
        self.toggle_all_btn.setText("🔴 計時器已停用" if not self.all_enabled else "🟢 計時器已啟用")
        self.timer_manager.set_all_enabled(self.all_enabled)

if __name__ == "__main__":
    app = QApplication([])
    window = CountdownWindow()
    window.show()
    app.exec()