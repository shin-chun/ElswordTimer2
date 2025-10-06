from settings.common import *
from timer.manager import EditWindowManager
from functools import partial


# from settings.scan_code_resolver import *


# SCAN_CODE_MAP = load_scan_code_map()


class EditWindow(QDialog):
    def __init__(self, title='編輯計時器', parent=None):
        super().__init__(parent)
        self.installEventFilter(self)
        self.setWindowTitle(title)
        self.setMinimumSize(600, 300)  # 調整視窗大小以容納 6x4 格線

        self.recording_index = None
        self.key_labels = []
        layout = QVBoxLayout()
        grid = QGridLayout()
        self.manager = EditWindowManager(
            key_labels=self.key_labels,
            label_updater=self.update_label
        )

        # 事件名稱填寫區塊（最左側第 0 欄，佔 4 行）
        event_font = QFont()
        event_font.setBold(True)
        event_font.setPointSize(14)

        # 標籤：事件名稱
        event_title = QLabel("事件名稱")
        event_title.setFont(event_font)
        event_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        event_title.setFrameShape(QFrame.Shape.Box)
        grid.addWidget(event_title, 0, 0)

        # 三個輸入欄位
        self.event_name_inputs = []

        input_field = QLineEdit()
        input_field.setFont(event_font)
        input_field.setAlignment(Qt.AlignmentFlag.AlignCenter)
        input_field.setPlaceholderText(f"請輸入事件名稱")
        input_field.setStyleSheet("border: 1px solid gray;")
        grid.addWidget(input_field, 1, 0)  # 第 1 列，第 0 欄
        self.event_name_inputs.append(input_field)

        # 按鈕UI區塊
        record_btn_label = ['選擇鍵', '鎖定鍵', '觸發鍵', '選擇鍵2', '鎖定鍵2', '觸發鍵2']

        for i in range(6):
            col = i % 3 * 2 + 2 # 每組佔 2 欄（按鈕 + label/清除）
            row_base = i // 3 * 2  # 每組佔 2 行

            # 錄製按鈕：佔 2 行 × 1 欄
            record_btn = QPushButton(record_btn_label[i])
            record_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            grid.addWidget(record_btn, row_base, col, 2, 1)

            # 顯示 Label：佔 1 行 × 1 欄
            label = QLabel("None")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            grid.addWidget(label, row_base, col + 1)

            # 清除按鈕：佔 1 行 × 1 欄（在 label 下方）
            clear_btn = QPushButton("清除")
            clear_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            grid.addWidget(clear_btn, row_base + 1, col + 1)

            record_btn.clicked.connect(partial(self.manager.keyPressEvent, i))
            clear_btn.clicked.connect(partial(self.manager.clear_key, i))

            self.key_labels.append(label)

        layout.addLayout(grid)
        self.setLayout(layout)

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

        layout.addLayout(btn_layout)

    def key_label(self, key_labels):
        self.key_labels =

    def update_label(self, index, key_name):
        self.key_labels[index].setText(key_name)



# def keyPressEvent(self, event: QKeyEvent):
#     if self.recording_index is None:
#         return
#
#     scan_code = event.nativeScanCode()
#     qt_key = event.key()
#     text = event.text()
#
#     # 優先使用 SCAN_CODE_MAP
#     key_name = SCAN_CODE_MAP.get(scan_code)
#
#     # 特殊鍵處理（例如 TAB）
#     if not key_name:
#         if qt_key == Qt.Key_Tab:
#             key_name = "Tab"
#         elif qt_key == Qt.Key_Return:
#             key_name = "Enter"
#         elif qt_key == Qt.Key_Escape:
#             key_name = "Esc"
#         elif qt_key == Qt.Key_Space:
#             key_name = "Space"
#         else:
#             # fallback：使用 Qt 的 key name 或 QKeySequence
#             key_name = QKeySequence(qt_key).toString() or f"Key({qt_key})"
#
#         # 自動補充映射表（可選）
#         SCAN_CODE_MAP[scan_code] = key_name
#         print(f"📝 已記錄新掃描碼：{scan_code} → {key_name}")
#
#     # 更新 UI
#     self.key_labels[self.recording_index].setText(key_name)
#     print(f"✅ 錄製完成：index={self.recording_index}, key={key_name}")
#     self.recording_index = None

