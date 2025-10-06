from settings.common import *
from settings.scan_code_resolver import *


SCAN_CODE_MAP = load_scan_code_map()


class EditWindow(QDialog):
    def __init__(self, title='編輯計時器', parent=None):
        super().__init__(parent)
        self.installEventFilter(self)
        self.setWindowTitle(title)
        self.setMinimumSize(600, 200)  # 調整視窗大小以容納 6x4 格線

        self.recording_index = None
        self.key_labels = []

        layout = QVBoxLayout()
        grid = QGridLayout()
        record_btn_label = ['選擇鍵', '鎖定鍵', '觸發鍵', '選擇鍵2', '鎖定鍵2', '觸發鍵2']

        for i in range(6):
            col = i % 3 * 2  # 每組佔 2 欄（按鈕 + label/清除）
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

            record_btn.clicked.connect(lambda _, idx=i: self.start_recording(idx))
            clear_btn.clicked.connect(lambda _, idx=i: self.clear_key(idx))

            self.key_labels.append(label)

        layout.addLayout(grid)
        self.setLayout(layout)

    def start_recording(self, index):
        self.recording_index = index
        self.key_labels[index].setText("等待按鍵...")
        self.setFocus()  # 確保 keyPressEvent 可觸發

    def clear_key(self, index):
        self.key_labels[index].setText("None")
        if self.recording_index == index:
            self.recording_index = None

    SCAN_CODE_MAP = load_scan_code_map()

    def keyPressEvent(self, event):
        if self.recording_index is None:
            return
        scan_code = event.nativeScanCode()
        qt_key = event.key()

        if scan_code not in SCAN_CODE_MAP:
            key_name = QKeySequence(qt_key).toString() or f"Key({qt_key})"
            SCAN_CODE_MAP[scan_code] = key_name
            save_scan_code_map(SCAN_CODE_MAP)
            print(f"📝 新增掃描碼：{scan_code} → {key_name}")
        else:
            key_name = SCAN_CODE_MAP[scan_code]
            print(f"🔁 已存在掃描碼：{scan_code} → {key_name}")

        if not key_name:
            key_name = QKeySequence(qt_key).toString() or f"Key({qt_key})"
            SCAN_CODE_MAP[scan_code] = key_name
            save_scan_code_map(SCAN_CODE_MAP)
            print(f"📝 自動記錄：{scan_code} → {key_name}")

        self.key_labels[self.recording_index].setText(key_name)
        self.recording_index = None

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

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Tab and self.recording_index is not None:
                scan_code = event.nativeScanCode()
                key_name = SCAN_CODE_MAP.get(scan_code, "Tab")
                self.key_labels[self.recording_index].setText(key_name)
                self.recording_index = None
                return True  # 阻止 Qt 處理 TAB
        return super().eventFilter(obj, event)