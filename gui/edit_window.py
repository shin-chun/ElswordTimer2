from settings.common import *
from timer.edit_window_manager import EditWindowManager
from functools import partial
from settings.scan_code_resolver import ScanCodeStore


class EditWindow(QDialog):
    def __init__(self, title='編輯計時器', parent=None):
        super().__init__(parent)
        self.installEventFilter(self)
        self.event_name_inputs = []
        self.key_labels = []
        self.setWindowTitle(title)
        self.setMinimumSize(700, 350)  # 調整視窗大小以容納 6x4 格線

        self.recording_index = None
        grid = QGridLayout()

        scan_code_store = ScanCodeStore()  # 或指定路徑 ScanCodeStore("your/path/scan_code_map.json")

        self.manager = EditWindowManager(
            key_labels=self.key_labels,
            label_updater=self.update_label,
            scan_code_store=scan_code_store
        )

        # 事件名稱填寫區塊（最左側第 0 欄，佔 4 行）
        event_font = QFont()
        event_font.setBold(True)
        event_font.setPointSize(14)

        # 一個輸入欄位

        input_field = QLineEdit()
        input_field.setFont(event_font)
        input_field.setAlignment(Qt.AlignmentFlag.AlignCenter)
        input_field.setPlaceholderText("請輸入事件名稱")
        input_field.setStyleSheet("border: 1px solid gray;")
        input_field.installEventFilter(self)
        input_field.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        # grid.addWidget(input_field, 0, 5, 1, 6)  # 第 0 列，從第 0 欄開始，橫跨 6 欄
        self.event_name_inputs.append(input_field)

        group_box = QGroupBox("觸發主鍵")  # ✅ 你可以改成你想要的標題
        group_box.setStyleSheet("""
            QGroupBox { 
                font-weight: bold;
                border: 2px solid gray;
                border-radius: 6px;
                margin-top: 10px;
                padding: 6px;
            }
        """)
        group_layout = QGridLayout()
        group_box.setLayout(group_layout)

        record_btn_label = ['選擇鍵', '鎖定鍵', '觸發鍵', '選擇鍵2', '鎖定鍵2', '觸發鍵2']
        for i in range(3):  # 只放前 3 組
            col = i  # 在 group_layout 中從第 0 欄開始
            record_btn = QPushButton(record_btn_label[i])
            record_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            group_layout.addWidget(record_btn, 0, col)

            label = QLabel("None")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            group_layout.addWidget(label, 1, col)

            clear_btn = QPushButton("清除")
            clear_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            group_layout.addWidget(clear_btn, 2, col)

            record_btn.clicked.connect(partial(self.manager.start_recording, i))
            clear_btn.clicked.connect(partial(self.manager.clear_key, i))
            self.key_labels.append(label)
            grid.addWidget(group_box, 0, 1, 3, 3)  # 佔 3 列 × 3 欄

        sub_group_box = QGroupBox("副鍵位區")
        sub_group_box.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid gray;
                border-radius: 6px;
                margin-top: 10px;
                padding: 6px;
            }
        """)
        sub_layout = QGridLayout()
        sub_group_box.setLayout(sub_layout)
        for i in range(3, 6):
            col = i - 3  # 在 sub_layout 中從第 0 欄開始

            record_btn = QPushButton(record_btn_label[i])
            record_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            sub_layout.addWidget(record_btn, 0, col)

            label = QLabel("None")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            sub_layout.addWidget(label, 1, col)

            clear_btn = QPushButton("清除")
            clear_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            sub_layout.addWidget(clear_btn, 2, col)

            record_btn.clicked.connect(partial(self.manager.start_recording, i))
            clear_btn.clicked.connect(partial(self.manager.clear_key, i))
            self.key_labels.append(label)

        # 秒數標籤與輸入欄位
        duration_label = QLabel("持續秒數")
        duration_input = QSpinBox()
        duration_label.setFixedHeight(50)
        duration_input.setRange(1, 3600)  # 1秒～1小時
        duration_input.setValue(10)  # 預設 10 秒

        # 確認及取消按鈕區塊
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        confirm_btn = QPushButton("確認")
        confirm_btn.setFixedSize(100, 50)
        confirm_btn.setStyleSheet("""
            QPushButton {
                background-color: #D0D0D0;  /* 綠色 */
                color: black;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2196F3;  /* 滑鼠懸停時的顏色 */
            }
        """)

        cancel_btn = QPushButton("取消")
        cancel_btn.setFixedSize(100, 50)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #D0D0D0;  /* 綠色 */
                color: black;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2196F3;  /* 滑鼠懸停時的顏色 */
            }
        """)

        confirm_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(confirm_btn)
        btn_layout.addWidget(cancel_btn)
        btn_layout.addStretch()

        main_layout = QVBoxLayout()

        # 事件名稱區塊（左側）
        event_layout = QVBoxLayout()
        event_layout.addWidget(input_field)

        event_frame = QFrame()
        event_frame.setLayout(event_layout)
        event_frame.setFrameShape(QFrame.Shape.Box)
        event_frame.setFixedWidth(200)  # 你可以調整成你想要的寬度
        event_frame.setStyleSheet("QFrame { border: 2px solid #aaa; border-radius: 6px; padding: 6px; }")

        # 鍵位區塊（右側）
        key_layout = QHBoxLayout()
        key_layout.addWidget(group_box)  # 主要鍵位區
        key_layout.addWidget(sub_group_box)  # 副鍵位區

        # 合併事件名稱與鍵位區塊
        top_layout = QHBoxLayout()
        top_layout.addWidget(event_frame)
        top_layout.addLayout(key_layout)

        main_layout.addLayout(top_layout)
        main_layout.addLayout(btn_layout)  # 確認/取消按鈕區塊

        # 加入事件名稱區塊
        event_layout.addWidget(duration_label)
        event_layout.addWidget(duration_input)

        self.setLayout(main_layout)
        self.duration_input = duration_input
        self.duration_input.setFixedHeight(40)  # 你可以試試 60、70、100 等數值
        confirm_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        cancel_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def get_event_data(self):
        return {
            "name": self.event_name_inputs[0].text(),
            "main_keys": [label.text() for label in self.key_labels[:3]],
            "sub_keys": [label.text() for label in self.key_labels[3:]],
            "duration": self.duration_input.value()  # ✅ 關鍵回傳
        }

    def key_label(self, key_labels):
        self.key_labels = self.key_labels = key_labels

    def update_label(self, index, key_name):
        self.key_labels[index].setText(key_name)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress:
            if self.manager.recording_index is None:
                return False  # ✅ 未錄製狀態，不處理鍵盤事件

            if self.manager.handle_special_key(event):
                return True

            self.manager.keyPressEvent(event)
            return True

        return super().eventFilter(obj, event)

