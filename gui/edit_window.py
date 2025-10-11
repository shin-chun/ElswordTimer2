from settings.common import *
from manager.edit_window_manager import EditWindowManager
from functools import partial
from settings.scan_code_resolver import ScanCodeStore


class EditWindow(QDialog):
    def __init__(self, title='編輯計時器', parent=None):
        super().__init__(parent)
        self.installEventFilter(self)
        self.setWindowTitle(title)
        self.setMinimumSize(700, 350)

        self.event_name_input = QLineEdit()
        self.key_labels = []
        self.recording_index = None

        scan_code_store = ScanCodeStore()
        self.manager = EditWindowManager(
            key_labels=self.key_labels,
            label_updater=self.update_label,
            scan_code_store=scan_code_store
        )

        self._setup_ui()
        self.load_existing_data()

    def _setup_ui(self):
        main_layout = QVBoxLayout()

        # 事件名稱區塊
        event_font = QFont()
        event_font.setBold(True)
        event_font.setPointSize(14)

        self.event_name_input.setFont(event_font)
        self.event_name_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.event_name_input.setPlaceholderText("請輸入事件名稱")
        self.event_name_input.setStyleSheet("border: 1px solid gray;")
        self.event_name_input.installEventFilter(self)
        self.event_name_input.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        self.duration_input = QSpinBox()
        self.duration_input.setRange(1, 3600)
        self.duration_input.setValue(10)
        self.duration_input.setFixedHeight(40)

        event_layout = QVBoxLayout()
        event_layout.addWidget(self.event_name_input)
        event_layout.addWidget(QLabel("持續秒數"))
        event_layout.addWidget(self.duration_input)

        event_frame = QFrame()
        event_frame.setLayout(event_layout)
        event_frame.setFrameShape(QFrame.Shape.Box)
        event_frame.setFixedWidth(200)
        event_frame.setStyleSheet("QFrame { border: 2px solid #aaa; border-radius: 6px; padding: 6px; }")

        # 主鍵位區
        group_box = self._create_key_group("觸發主鍵", range(3))
        # 副鍵位區
        sub_group_box = self._create_key_group("副鍵位區", range(3, 6))

        key_layout = QHBoxLayout()
        key_layout.addWidget(group_box)
        key_layout.addWidget(sub_group_box)

        top_layout = QHBoxLayout()
        top_layout.addWidget(event_frame)
        top_layout.addLayout(key_layout)

        # 確認/取消按鈕
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        confirm_btn = QPushButton("確認")
        confirm_btn.setFixedSize(100, 50)
        confirm_btn.setStyleSheet(self._button_style())
        confirm_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        confirm_btn.clicked.connect(self.on_confirm)

        cancel_btn = QPushButton("取消")
        cancel_btn.setFixedSize(100, 50)
        cancel_btn.setStyleSheet(self._button_style())
        cancel_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(confirm_btn)
        btn_layout.addWidget(cancel_btn)
        btn_layout.addStretch()

        main_layout.addLayout(top_layout)
        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)

    def _create_key_group(self, title, indices):
        record_btn_label = ['選擇鍵', '鎖定鍵', '觸發鍵', '選擇鍵2', '鎖定鍵2', '觸發鍵2']
        group_box = QGroupBox(title)
        group_box.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid gray;
                border-radius: 6px;
                margin-top: 10px;
                padding: 6px;
            }
        """)
        layout = QGridLayout()
        group_box.setLayout(layout)

        for i in indices:
            col = i % 3
            record_btn = QPushButton(record_btn_label[i])
            record_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            layout.addWidget(record_btn, 0, col)

            label = QLabel("None")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            layout.addWidget(label, 1, col)

            clear_btn = QPushButton("清除")
            clear_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            layout.addWidget(clear_btn, 2, col)

            record_btn.clicked.connect(partial(self.manager.start_recording, i))
            clear_btn.clicked.connect(partial(self.manager.clear_key, i))
            self.key_labels.append(label)

        return group_box

    def _button_style(self):
        return """
            QPushButton {
                background-color: #D0D0D0;
                color: black;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2196F3;
            }
        """

    def get_event_data(self):
        return {
            "name": self.event_name_input.text(),
            "main_keys": [label.text() for label in self.key_labels[:3]],
            "sub_keys": [label.text() for label in self.key_labels[3:]],
            "duration": self.duration_input.value()
        }

    def save_event_data(self):
        event_data = self.get_event_data()
        self.manager.store_event_data(event_data)

    def load_existing_data(self):
        event_data = self.manager.load_event_data()
        if event_data:
            self.event_name_input.setText(event_data.get("name", ""))
            self.duration_input.setValue(event_data.get("duration", 10))
            for i, key in enumerate(event_data.get("main_keys", []) + event_data.get("sub_keys", [])):
                if i < len(self.key_labels):
                    self.key_labels[i].setText(key)

    def on_confirm(self):
        self.save_event_data()
        self.accept()

    def update_label(self, index, key_name):
        self.key_labels[index].setText(key_name)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress:
            if self.manager.recording_index is None:
                return False
            if self.manager.handle_special_key(event):
                return True
            self.manager.keyPressEvent(event)
            return True
        return super().eventFilter(obj, event)